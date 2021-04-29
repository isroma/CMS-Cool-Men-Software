# Arquitectura legacy (con Docker)

ElasticSearch se despliega con Docker a la vez que Django y PostgreSQL, hay que tener cuidado únicamente con que cada vez que se indexe algo llamar al siguiente comando si queremos reindexar:

```
docker exec -it <container_id> python manage.py search_index --rebuild
```

# Django legacy (con Docker)

### **Instalación** de Django:

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
  8. Volvemos a apagar con ctrl + c y hacemos un último docker-compose up (en total son 3), este último creará el superuser 'admin admin'
      ``` 
      docker-compose up
      ```

### Lanzar Django una vez instalado:

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

### Por qué no movemos los archivos de Docker a /architecture

Desafortunadamente, por razones prácticas y de seguridad, si se quiere añadir o copiar contenido local (como requirements.txt), debe estar alojado en el mismo path que el Dockerfile.

Fuentes: 
- https://stackoverflow.com/questions/24537340/docker-adding-a-file-from-a-parent-directory
- https://docs.docker.com/engine/reference/builder/