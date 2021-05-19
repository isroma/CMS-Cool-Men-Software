# Django
## Regenerar un despliegue de Django

  1. Primero debemos conectar nuestro repositorio local de imagenes de Docker con el repositorio de imagenes de Minikube con el siguiente comando:

   `eval $(minikube docker-env)`

  IMPORTANTE: Este comando ejecuta un cambio en la TERMINAL. Debemos trabajar con la misma terminal en la que se ha ejecutado este comando.

  2. Tras esto, podemos cargarnos el despliegue actual de django con:

   `kubectl delete -f architecture/templates/django/django-deployment.yml`

  3. Nos contruimos la nueva imagen:

   `docker build djangocms/ -t cms/django`

  4. Volvernos a crear el despliegue con:

   `kubectl apply -f architecture/templates/django/django-deployment.yml`

## Estructura de Django

Trabajar siempre dentro de la carpeta /djangocms.

Estructura del proyecto de Django

    CMS-COOL-MEN-SOFTWARE
    ├── architecture              | kubernetes
    ├── djangocms                 | django project
    │   ├── data                  | PostgreSQL database
    │   ├── djangoadmin           | manages everything in Django
    │   ├── homepage              | main front site
    │   ├── search                | manages file searchs
    │   ├── static                | all images, css, etc
    │   ├── upload                | manages file uploads
    │   ├── users                 | django user management
    │   ├── credentials.json      | it should be downloaded from slack
    │   ├── docker-compose.yml    | docker-compose to build docker
    │   ├── docker-entrypoint.sh  | entrypoint to run Django as desired
    │   ├── Dockerfile            | create docker
    │   ├── manage.py             | script to execute django commands
    │   ├── requirements.txt      | all requirements
    ├── doc                       | extra documentation
    └── README.md