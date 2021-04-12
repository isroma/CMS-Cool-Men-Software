# Configuracion del cluster de Kubernetes

Abajo estan las instrucciones para la configuracion de los recursos que necesitamos en Kubernetes

## ELK y ECK (falta Logstash)

1. Primero tenemos que instalar los recursos necesarios para poder correr ECK:

    `kubectl apply -f https://download.elastic.co/downloads/eck/1.1.1/all-in-one.yaml`

2. Ahora vamos a crear un par de volumenes persistentes para no perder los datos de los containers si "desaparecen" (se creara uno para cada nodo de ES):

    `kubectl apply -f ./k8/recursos/elk/elasticsearch/volumen-persistente.yaml`
    
3. Creamos pods para correr un nodo master y un nodo de datos de Elasticsearch:

    `kubectl apply -f ./k8/recursos/elk/elasticsearch/elasticsearch.yaml`

4. Creamos el pod para kibana:

    `kubectl apply -f ./k8/recursos/elk/kibana/kibana.yaml`
    
5. Esperamos un rato, y corremos el siguiente comando para comprobar que el estado de los pods de "es-cluster-cms" y "kibana-cms-kb..." pasan todos a 1/1:

    `kubectl get pods -A`

6. Una vez todos los pods esten creados, extraemos la password de elasticsearch que se nos habra creado para el cluster y la guardamos en un sitio seguro, con:
    
    `kubectl get secret es-cluster-cms-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo`

7. Ya deberiamos poder acceder a:

    - Kibana dashboard (usar password del usuario de elasticsearch): `https://{IP DEL NODO}:31560`
    - Cluster de elasticsearch (usar password del usuario de elasticsearch): `https://{IP DEL NODO}:31920`
    
8. Podemos ver los dos nodos de elasticsearch (el master y el data node) end:

    `https://{IP DEL NODO}:31920/_cat/nodes?v`