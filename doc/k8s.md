# Funcionamiento de arquitectura 

Información más detallada de cada servicio desplegado en Kubernetes.

## PostgreSQL

Para desplegar postgresql en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/postgresql/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de PostGreSQL. Estos componentes son:

- Un PV (PersistentVolume): Que reservará un espacio de almacenamiento persistente dentro del cluster que podrá usado por otros deployments para almacenar datos que existan más allá de la vida del contenedor.
- Un PVC (PersistentVolumeClaim): Que vinculará un Deployment con un PV para montar un directorio dentro de un Pod en el almacenamiento reservado
- Un Service: Que le permitirá a Django acceder al servicio de PostGreSQL gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
- Un Deployment: Que es el principal componente de despliegue PostGreSQL

## ElasticSearch

Para desplegar la imagen de bitnami/elasticsearch en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/elastic/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de la imagen bitnami/elasticsearch. Estos componentes son:

- Un Service: Que le permitirá a Django acceder al servicio de elastic gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
- Un Deployment: Que es el principal componente de despliegue de la imagen bitnami/elasticsearch

## Kibana

Para desplegar Kibana en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/kibana/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Kibana. Estos componentes son:

- Un Service: Que nos permitira a nosotros acceder a la UI de Kibana
- Un Deployment: Que es el principal componente de despliegue de Kibana

## Logstash

Para desplegar Logstash en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/logstash/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Logstash. Estos componentes son:

- Un ConfigMap: Que indica a Logstash como tiene que parsear los logs que vienen de los distintos pods.
- Un Service: Que permitira a Filebeat comunicarse con Logstash para mandar logs a ser procesados.
- Un Deployment: Que es el principal componente de despliegue de Logstash

## Filebeat

Para desplegar Filebeat en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/filebeat/. Estos archivos crean una serie de componentes de k8s que habilitarán en despliegue de Filebeat. Estos componentes son:

- Un ServiceAccount, asociado con un ClusterRole: El service account le permite a Filebeat acceso de lectura a los recursos necesarios
- Un ConfigMap: Para configurar como manda los logs Filebeat a Logstash.
- Un DaemonSet: Usamos un DaemonSet para que Filebeat corra en todos los nodos del cluster. Asi podemos mandar todos los logs de nuestro cluster entero a Logstash.

## Apache Tika

Para desplegar Tika en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/tika/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de Tika. Estos componentes son:

- Un Service: Que le permitirá a Django acceder al servicio de tika gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
- Un Deployment: Que es el principal componente de despliegue de Tika

## SwiftStack

Para desplegar SwiftStack en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/swift/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de SwiftStack. Estos componentes son:

- Un Service: Que le permitirá a Django acceder al servicio de SwiftStack gracias a la DNS interna de Kubernetes. Este servicio será sólamente visible desde dentro del clúster, y ningún servicio o usuario podrá acceder a ello (a no ser que utilice el kubernetes proxy). Se hace así por problemas de seguridad.
- Un Deployment: Que es el principal componente de despliegue de SwiftStack

## Django

Para desplegar Django en nuestro cluster de k8s utilizaremos los archivos que se encuentran en architecture/templates/swift/. Estos archivos crean una serie de componentes de k8s que habilitarán el despliegue de Django. Estos componentes son:

- Un Service: Que les permitirá a los usuarios acceder al cliente web del framework. Para acceder a este servicio, en vez de averiguar la IP del nodo en el que está desplegado y el puerto que Kubernetes le ha asignado automáticamente, se puede ejecutar el siguiente comando y se abrirá en nuestro navegador predeterminado el servicio:

`minikube service django-service -n cms`

- Un Deployment: Que es el principal componente de despliegue de Django