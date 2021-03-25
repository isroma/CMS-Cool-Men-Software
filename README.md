# Proceso de trabajo
  1. Crear una rama apartir de develop
  2. Hacemos un PULL de la rama que hemos creado a nuestro local (aplicar todos los cambios solo a esa rama)
  3. Anter de hacer la PR (pull-request) hacemos un PULL de develop para asegurarnos que no hay nuevos cambios mientras estabamos trabajando
  4. Al terminar hacer un PUSH de nuestra rama a la rama develop
  5. Añadir reviewers (personas) para comprobar que nuestro código esté bien
  6. Una vez aprobadas las reviews se podrá mergear sobre develop 

NOTA: cada vez que instalemos una librería actualizamos los requirements
```pip3 freeze > requirements.txt```

# Cómo actualizar una rama
  1. git fetch
  2. git checkout develop
  3. git pull
  4. git checkout "nombre_de_tu_rama"
  5. git add "nombre_del_archivo"
  6. git commit -m "mensaje de la modificacion"
  7. git push -u origin "nombre_de_tu_rama"
  
  https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

# NUNCA trabajar directamente sobre *develop*

Se debería crear una rama por cada ticket a realizar.

**Nomenclatura**

- style/ : si es algo de diseño
- bugfix/ : resolucion de errores
- feature/ : nuevo desarrollo

Ejemplo: feature/CMS-X(numero de ticket del Kanban)-nombre(funcionalidad del ticket) -> feature/CMS-41-estructura-github

# Arquitectura (Docker/Kubernetes/SwiftStack/ElasticSearch)

Trabajar siempre dentro de la carpeta /architecture.

# Virtual env

Para trabajar con django siempre utilizaremos un venv, pasos a seguir para crearlo:

  1. python3 -m venv venv
  2. source venv/bin/activate
  3. pip3 install -r requirements.txt

Solo hay que realizar el paso 1 cuando creemos el venv, desde esa vez basta con seguir a partir del 2.

# Django

Pasos para lanzar Django:

  1. pip3 install -r requirements.txt (tras haber activado el venv y en caso de no tenerlos instalados)
  2. cd djandocms (hay que estar en la carpeta de Django)
  3. docker-compose up (construye las dos imagenes de docker, postgresql y django)
  4. docker exec -it <container_id> python manage.py createsuperuser (ejemplo para lanzar comandos de django dockerizado)

Estructura para entender Django

    CMS-COOL-MEN-SOFTWARE
    ├── architecture          | everything that is NOT Django
    ├── djangocms             | django project
    │   ├── data              | manages postgresql database
    │   ├── djangoadmin       | manages everything in Django
    │   ├── homepage          | main front site
    │   ├── search            | manages elascticsearch
    │   ├── static            | all images, css, etc
    │   ├── users             | django user management
    │   ├── docker-compose    | docker-compose to build docker
    │   ├── Dockerfile        | create docker
    │   ├── manage.py         | script to execute django commands
    │   ├── requirements.txt  | all requirements
    └── README.md
