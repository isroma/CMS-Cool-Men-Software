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