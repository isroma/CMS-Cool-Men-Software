# Django legacy (con Docker)

## Primera instalación de Django:

Estos pasos solo se tendrán que realizar una vez, a no ser que borremos el container o las imágenes.

  1. Ir al directorio /djangocms 
      ``` 
      cd djandocms 
      ```
  2. Dar permisos a docker-entrypoint.sh para que pueda ejecutarse al lanzar Docker
      ```
      chmod +x docker-entrypoint.sh
      ```
  4. Hacer la build del container y las imágenes
      ``` 
      docker-compose build
      ```
  5. Levantar el contenedor una primera vez, creando Django y PostgresSQL
      ``` 
      docker-compose up
      ```
      Tarda un poco y parece que se queda pillado en:
      ```
      web_1  |        Is the server running on host "db" (172.27.0.2) and accepting
      web_1  |        TCP/IP connections on port 5432?
      ```
      Pero hay que esperar hasta que salga el siguiente mensaje:
      ```
      LOG:  database system is ready to accept connections
      ```
  6. Apagamos el servicio con ctrl + c y hacemos otro docker-compose up, aquí ya funcionará la web
      ``` 
      docker-compose up
      ```
  7. Volvemos a apagar con ctrl + c y hacemos un último docker-compose up (en total son 3), este último creará el superuser 'admin admin'
      ``` 
      docker-compose up
      ```
  9.  Para habilitar la subida de archivos a Swiftstack también es necesario ejecutar este comando en la máquina de django:
      ```
      docker exec -it <container_id> swift -A ST_AUTH -U ST_USER -K ST_KEY post container -H "X-Container-Meta-Access-Control-Allow-Origin:*"
      ```
      Donde ST_AUTH es algo como “http://swiftstack:8080/auth/v1.0“ y ST_USER y ST_KEY son usuario y contraseña de Swiftstack. 
 10. Para habilitar la subida de archivos a ElasticSearch tambien es necesario ejecutar estos comando en la maquina de ElasticSearch:
      ```
      cd /opt/bitnami/elasticsearch/config/
      echo 'http.cors.enabled: true' >> elasticsearch.yml
      echo 'http.cors.allow-origin: "*"' >> elasticsearch.yml
      ```
 11. Creamos los indices para ElasticSearch ejecutando este comando en nuestra terminal:
      ```
      curl --request PUT 'http://localhost:9200/nombre_contenedor' \
           --header 'Content-Type: application/json' \
           -d '{
                "mappings": {
                    "properties": {
                        "date": {
                            "type": "search_as_you_type"
                        },
                        "user": {
                            "type": "search_as_you_type"
                        },
                        "title": {
                            "type": "search_as_you_type"
                        },
                        "text": {
                            "type": "search_as_you_type"
                        },
                        "metadata": {
                            "type": "text"
                        },
                        "url": {
                            "type": "text"
                        }
                    }
                }
            }'
      ```
      Donde nombre_contenedor sera el nombre del contenedor que queremos crear.
      Esto deberia cambiar si añadimos mas campos a lo que se sube a ElasticSearch.

## Lanzar Django una vez instalado:

  1. Ahora cada vez que queramos lanzar Django solo es necesario ejecutar un comando
      ```
      docker-compose up
      ```
  2. Si quisiéramos lanzar un comando de Django deberíamos hacer en Docker, un ejemplo para crear un superuser sería
      ```
      docker exec -it <container_id> python manage.py createsuperuser
      ```
  3. Otro ejemplo de utilidad, para instalar un nuevo requirement (previo pip freeze > requirements dentro de la carpeta djangocms):
      ```
      docker exec -it <container_id> pip install -r requirements.txt   
      ```

# Anexo

## Por qué no movemos los archivos de Docker a /architecture

Desafortunadamente, por razones prácticas y de seguridad, si se quiere añadir o copiar contenido local (como requirements.txt), debe estar alojado en el mismo path que el Dockerfile.

Fuentes: 
- https://stackoverflow.com/questions/24537340/docker-adding-a-file-from-a-parent-directory
- https://docs.docker.com/engine/reference/builder/
