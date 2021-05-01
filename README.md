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

A continuación se encuentran las instrucciones para la configuración de nuestros recursos de Kubernetes. En el vamos a desplegar:
    - ElasticCloud (ECK) para habilitar la API de objetos de Elastic que será usada para los siguientes despliegues
    - Un cluster de Elastic, haciendo uso de los objetos de ECK, que tenga incorporado todas las funcionalidades de Elastic y se abstraiga de nuestro trabajo

NOTA: Todos el desarrollo en Kubernetes se va a realizar dentro de un namespace llamado "elastic". Para crear este namespace, es necesario ejecutar la siguiente linea:

`kubectl create namespace elastic`

  # Instalacion de ECK

Utilizaremos el endpoint de la API para usar sus objetos o CRD (CustomResourceDefinitions) para desplegar el resto de herramientas

1. Primero, instalaremos los CRD el operador con sus reglas RBAC:

    `kubectl apply -f https://download.elastic.co/downloads/eck/1.1.1/all-in-one.yaml`

2. Para monitorizar los logs del operador de ECK:

    `kubectl -n elastic-system logs -f statefulset.apps/elastic-operator`

  # Instalación del cluster de Elastic

Una vez tenemos acceso a los objetos de la API de ECK, podemos proceder a instalar el resto de componentes. Primero, el cluster de Elastic. Esto nos instalará un cluster de 1 nodo de Elastic dentro de nuestro cluster de k8s. Si queremos cambiar el numero de nodos que se levantan, solo tenemos que cambiar la configuracion dentro del archivo yml. 

NOTA: Con el cluster de Elastic se instala un servicio de Kubernetes. Estos servicios se utilizan para exponer servicios (quien lo hubiera dicho) a otros clientes. El tipo de servicio que instala Elastic es un ClusterIP. Este ClusterIP es visible al resto de recursos de dentro del cluster de k8s, PERO NO FUERA DE EL. Veremos mas adelante como podemos reconducir su trafico para poder hacer pruebas desde fuera.

NOTA: Si nos sale un error dentro de los pods de elastic relacionado con vm.max_map_count es un error de nuestra maquina host. Hay que cambiar la configuración del sistema y reiniciar la máquina.

1. Primero, aplicar la configuracion dentro del archivo elastic.yml:

    `kubectl apply -f elastic.yml`

2. Si queremos ver el estado general del cluster de Elastic:

    `kubectl get elasticsearch -n elastic`

3. Si queremos ver los pods del cluster de Elastic:

    `kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-name=quickstart' -n elastic`

4. Si queremos ver los logs de un nodo en concreto:

    `kubectl logs -f quickstart-es-default-XXXXXXX -n elastic`

5. IMPORTANTE: Para acceder al cluster de Elastic y poder enviar peticiones desde FUERA del cluster de Kubernetes

    `kubectl get service quickstart-es-http -n elastic`

Aqui vemos el servicio predeterminado que ECK nos ha configurado para poder acceder al cluster de Elastic. Un ClusterIP. De acuerdo a la documentacion oficial de Kubernetes:

"ClusterIP: Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default ServiceType."

Lo que quiere decir que si queremos acceder a este servicio, tenemos que:

    a) Entrar al cluster de Kubernetes y realizar las peticiones desde DENTRO del cluster
    b) Redirigir el trafico de este servicio a nuestra maquina host

En un principio, antes de incorporar el resto de componentes al cluster de Kubernetes, nos vamos a deantar por la opcion b. Una vez que el resto de componentes tambien se encuentren dentro del cluster, no sera necesario.

6. Conseguir las credenciales del usuario de Elastic

Elastic de forma predeterminada crea un usuario con el cual podemos hacer uso del cluster de Elastic. Su nombre es elastic. Para conseguir su contraseña:

   `kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'`

7. Acceder al endpoint de Elastic

Para acceder desde fuera del cluster, primero tenemos que correr este comando en una terminal independiente:

   `kubectl port-forward service/quickstart-es-http 9200 -n elastic`

Ahora, con el usuario y la contraseña que hemos obtenido anteriormente, podemos hacerle peticiones a Elastic:

   `curl -u "elastic:$PASSWORD" -k "https://localhost:9200"`

NOTA: La contraseña que hemos obtenido para elastic la hemos guardado en la variable de entorno $PASSWORD

Elastic nos deberia de responder algo parecido a esto:

{
  "name" : "quickstart-es-default-0",
  "cluster_name" : "quickstart",
  "cluster_uuid" : "R8aRxZImShC7IU0uZRgACw",
  "version" : {
    "number" : "7.11.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "3e5a16cfec50876d20ea77b075070932c6464c7d",
    "build_date" : "2021-03-06T05:54:38.141101Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

  # POSTGRESQL en K8S

Para desplegar postgresql en nuestro cluster de k8s utilizaremos los archivos que se encuentran en k8s/postgresql

1. Primero instalamos el PersistentVolume con:

   `kubectl apply -f architecture/postgresql/postgresql-pv.yml`

2. Creamos el PersistentVolumeClaim para el PersistentVolume con:

   `kubectl apply -f architecture/postgresql/postgresql-pvc.yml`

3. Creamos el Deployment de postgresql con:

   `kubectl apply -f architecture/postgresql/postgresql-deployment.yml`

4. Creamos el Service para exponer el despliegue con:

   `kubectl apply -f architecture/postgresql/postgresql-service.yml`

 # DJANGO en K8S

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