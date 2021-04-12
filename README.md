# Proceso de trabajo

  1. Crear una rama apartir de develop
  2. Hacemos un PULL de la rama que hemos creado a nuestro local (aplicar todos los cambios solo a esa rama)
  3. Anter de hacer la PR (pull-request) hacemos un PULL de develop para asegurarnos que no hay nuevos cambios mientras estabamos trabajando
  4. Al terminar hacer un PUSH de nuestra rama a la rama develop
  5. Añadir reviewers (personas) para comprobar que nuestro código esté bien
  6. Una vez aprobadas las reviews se podrá mergear sobre develop 

NOTA: cada vez que instalemos una librería actualizamos los requirements (en este caso están los de Django)
```
pip3 freeze > requirements.txt
```

# Cómo actualizar una rama

  1. git fetch
  2. git checkout develop
  3. git pull
  4. git checkout "nombre_de_tu_rama"
  5. git add "nombre_del_archivo"
  6. git commit -m "mensaje de la modificacion"
  7. git push -u origin "nombre_de_tu_rama"
  
  https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

# Cómo seguir una estructura de trabajo

### **NUNCA** trabajar sobre la rama **develop**

Se debería crear una rama por cada ticket a realizar.

**Nomenclatura**

- style/ : si es algo de diseño
- bugfix/ : resolucion de errores
- feature/ : nuevo desarrollo

Ejemplo: feature/CMS-X(numero de ticket del Kanban)-nombre(funcionalidad del ticket) -> feature/CMS-41-estructura-github

# Arquitectura 

Incluimos en arquitectura Docker/Kubernetes/SwiftStack/ElasticSearch, trabajar siempre dentro de la carpeta /architecture.

ElasticSearch se despliega con Docker a la vez que Django y PostgreSQL, hay que tener cuidado únicamente con que cada vez que se indexe algo llamar al siguiente comando si queremos reindexar:

```
docker exec -it <container_id> python manage.py search_index --rebuild
```

# Django

Trabajar siempre dentro de la carpeta /djangocms.

### **Configuración** de logs:

Para mandar los logs de django a elasticsearch, se utiliza "filebeat". El container de filebeat corre junto al de django y manda los logs directamente a elasticsearch (hasta que no tengamos logstash).

Para configurar los logs de django y que se manden a Elasticsearch, primero hay que tener el cluster montado siguiendo las instrucciones [aqui](architecture/README.md). Luego:

  1. Cambiar el valor de `output.elasticsearch.hosts` en [la configuracion de filebeat](djangocms/config/filebeat.yml) para apuntar a un nodo del cluster. 
  
  2. En el mismo archivo, cambiar el valor de `output.elasticsearch.password` por la password que tenga el usuario de elastic en el cluster creado.
  
  3. Cuando tengamos logstash, los logs se podran ver en kibana. De momento se puede ver que estan elasticsearch haciendo GET requests al indice creado por filebeat.
  
   
 
### **Instalación** de Django:

Estos pasos solo se tendrán que realizar una vez, a no ser que borremos el container o las imágenes.

  1. Ir al directorio /djangocms 
      ``` 
      cd djandocms 
      ```
  2. Dar permisos a docker-entrypoint.sh para que pueda ejecutarse al lanzar Docker
      ```
      chmod +x /docker-entrypoint.sh
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

Estructura para entender Django

    CMS-COOL-MEN-SOFTWARE
    ├── architecture              | everything that is NOT Django
    ├── djangocms                 | django project
    │   ├── djangoadmin           | manages everything in Django
    │   ├── homepage              | main front site
    │   ├── search                | manages elascticsearch
    │   ├── static                | all images, css, etc
    │   ├── users                 | django user management
    │   ├── credentials.json      | it should be downloaded from slack
    │   ├── debug.log             | django logs
    │   ├── docker-compose.yml    | docker-compose to build docker
    │   ├── docker-entrypoint.sh  | entrypoint to run Django as desired
    │   ├── Dockerfile            | create docker
    │   ├── manage.py             | script to execute django commands
    │   ├── requirements.txt      | all requirements
    └── README.md
