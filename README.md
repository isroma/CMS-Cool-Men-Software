**Proceso de trabajo**
  1. Crear una rama apartir de develop
  2. Hacemos un PULL de la rama que hemos creado a nuestro local (aplicar todos los cambios solo a esa rama)
  3. Anter de hacer la PR (pull-request) hacemos un PULL de develop para asegurarnos que no hay nuevos cambios mientras estabamos trabajando
  4. Al terminar hacer un PUSH de nuestra rama a la rama develop
  5. Añadir reviewers (personas) para comprobar que nuestro código esté bien
  6. Una vez aprovadas las reviews se podrá mergear sobre develop

**Cómo actualizar una rama**
  1. git fetch
  2. git checkout develop
  3. git pull
  4. git checkout "nombre_de_tu_rama"
  5. git add "nombre_del_archivo"
  6. git commit -m "mensaje de la modificacion"
  7. git push -u origin "nombre_de_tu_rama"
  
  https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

**NUNCA trabajar directamente sobre *develop***

Se debería crear una rama por cada ticket a realizar.

**Nomenclatura**

- style/ : si es algo de diseño
- bugfix/ : resolucion de errores
- feature/ : nuevo desarrollo

Ejemplo: feature/CMS-X(numero de ticket del Kanban)-nombre(funcionalidad del ticket) -> feature/CMS-41-estructura-github

**Arquitectura (Docker/Kubernetes/SwiftStack/ElasticSearch)**

Trabajar siempre dentro de la carpeta /architecture.

**Virtual env**

Para trabajar con django siempre utilizaremos un venv, pasos a seguir para crearlo:

  1. python3 -m venv venv
  2. source venv/bin/activate
  3. pip3 install -r requirements.txt

Solo hay que realizar el paso 1 cuando creemos el venv, desde esa vez basta con seguir a partir del 2.

**Django**

Pasos para lanzar django:

  1. pip install -r requirements.txt (en caso de no tenerlos instalado)
  2. cd djandocms (hay que estar en la carpeta de django)
  3. python3 manage.py runserver
