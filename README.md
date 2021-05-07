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

  # Configuracion de Kubernetes

  Todos los componentes de arquitectura se desplegarán dentro de un namespace que no es el (default) por problemas de compatibilidad con otros proyectos de los integrantes. Por defecto, se ha decidido el namespace "cms", y todos los comandos que utilizen el CLI de K8s (kubectl) deberán de ir acompañados de -n cms

  Para crear el namespace "cms" dentro de nuestro cluster de minikube se debe ejecutar:

   `kubectl create namespace cms`

   TL;DR: Ejecutar:

   `kubectl apply -f cms.yml`

   Para acceder a django:

  `minikube service django-service -n cms`

  # POSTGRESQL

  Para desplegar postgresql en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/postgresql/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de PostGreSQL. Estos componentes son:

  - Un PV (PersistentVolume): Que reservará un espacio de almacenamiento persistente dentro del cluster que podrá usado por otros deployments para almacenar datos que existan más allá de la vida del contenedor.
  - Un PVC (PersistentVolumeClaim): Que vinculará un Deployment con un PV para montar un directorio dentro de un Pod en el almacenamiento reservado
  - Un Service: Que le permitirá a Django acceder al servicio de PostGreSQL gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
  - Un Deployment: Que es el principal componente de despliegue PostGreSQL

  # ELASTIC

  Para desplegar la imagen de bitnami/elasticsearch en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/elastic/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de la imagen bitnami/elasticsearch. Estos componentes son:

  - Un Service: Que le permitirá a Django acceder al servicio de elastic gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
  - Un Deployment: Que es el principal componente de despliegue de la imagen bitnami/elasticsearch
  
  # KIBANA

  Para desplegar Kibana en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/kibana/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Kibana. Estos componentes son:

  - Un Service: Que nos permitira a nosotros acceder a la UI de Kibana.
  - Un Deployment: Que es el principal componente de despliegue de Kibana
  
  # LOGSTASH

  Para desplegar Logstash en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/logstash/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Logstash. Estos componentes son:

  - Un ConfigMap: Que indica a Logstash como tiene que parsear los logs que vienen de los distintos pods.
  - Un Service: Que permitira a Filebeat comunicarse con Logstash para mandar logs a ser procesados.
  - Un Deployment: Que es el principal componente de despliegue de Logstash
  
  # FILEBEAT

  Para desplegar Filebeat en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/filebeat/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Logstash. Estos componentes son:

  # TIKA

  Para desplegar tika en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/tika/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de Tika. Estos componentes son:

  - Un Service: Que le permitirá a Django acceder al servicio de tika gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
  - Un Deployment: Que es el principal componente de despliegue de Tika

  # SWIFT

  Para desplegar swift en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/swift/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de SwiftStack. Estos componentes son:

  - Un Service: Que le permitirá a Django acceder al servicio de swift gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
  - Un Deployment: Que es el principal componente de despliegue de SwiftStack

 # DJANGO en K8S

  Para desplegar Django en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/swift/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de Django. Estos componentes son:

  - Un Service: Que les permitirá a los usuarios acceder al cliente web del framework. Para acceder a este servicio, en vez de averiguar la IP del nodo en el que está desplegado y el puerto que Kubernetes le ha asignado automáticamente, se puede ejecutar el siguiente comando y se abrirá en nuestro navegador predeterminado el servicio:

   `minikube service django-service -n cms`

  - Un Deployment: Que es el principal componente de despliegue de Django

  # REGENERAR UN DESPLIEGUE DE DJANGO

  1. Primero debemos conectar nuestro repositorio local de imagenes de Docker con el repositorio de imagenes de Minikube con el siguiente comando:

   `eval $(minikube docker-env)`

  IMPORTANTE: Este comando ejecuta un cambio en la TERMINAL. Debemos trabajar con la misma terminal en la que se ha ejecutado este comando.

  2. Tras esto, podemos cargarnos el despliegue actual de django con:

   `kubectl delete -f architecture/templates/django/django-deployment.yml`

  3. Nos contruimos la nueva imagen:

   `docker build djangocms/ -t cms/django`

  4. Volvernos a crear el despliegue con:

   `kubectl apply -f architecture/templates/django/django-deployment.yml`

# Django

Trabajar siempre dentro de la carpeta /djangocms.

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

# Versiones legacy

- [Docker legacy](/doc/legacy.md)