**Proceso de trabajo**
  1. Crear una rama apartir de la main
  2. Hacemos un PULL de la rama que hemos creado a nuestro local (aplicar todos los cambios solo a esa rama)
  3. Anter de hacer la PR hacemos un Pull de la main para asegurarnos que no hay nuevos cambios mientras estabamos trabajando.
  4. Al terminar hacer un PUSH de nuestra rama a la rama main.
  5. Comprobar los cambios y mergear la rama desde el Git

**Cómo actualizar una rama**
  1. git fetch
  2. git checkout develop
  3. git pull
  4. git checkout "tu rama"
  5. git merge develop
  
  https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

**Todas las ramas se tienen que crear de *develop***

Se deberia crear una rama por cada ticket a realizar.

**Nomenclatura de ramas**

- style/ : si es algo de diseño
- bugfix/ : resolucion de errores
- feature/ : nuevo desarrollo

Ejemplo: feature/CMS-X(Numero de ticket del Kanban)-nombre(funcionalidad del ticket)

Los espacios se separan por -

**Tecnologias**
- Acceder y Leer contenidos: SwiftStack
- Busqueda de archivos: SwiftStack
- Balanceo de carga: Nginx
- Gestion de usuarios: SwiftStack + Django 
- Web: Django

**URLS utiles**
- https://meet.google.com/linkredirect?authuser=0&dest=https%3A%2F%2Fwww.nginx.com%2Fblog%2Fmaximizing-python-performance-with-nginx-parti-web-serving-and-caching%2F
