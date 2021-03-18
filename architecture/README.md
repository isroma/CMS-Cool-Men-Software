--------------------
DESPLEGAR ECK EN K8S 
--------------------

- Desplegaremos Elastic Cloud (ECK) en nuestro cluster local de kubernetes
- Al desplegar ECK en nuestro cluster tendremos acceso a la API de objetos de Elastic, que nos permitira desplegar un cluster de Elasticsearch y Kibana

1. Instalamos los crds y el operador de elastic con sus reglas de RBAC

```
kubectl apply -f https://download.elastic.co/downloads/eck/1.4.1/all-in-one.yaml
```

2. Para comprobar el estado del operador:

```
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```

ECK se despliega en su propio namespace, llamado elastic-system

--------------------------------------------
PASOS PARA INSTALAR CLUSTER DE ELASTICSEARCH
--------------------------------------------

Nuestro cluster de nodos de Elasticsearch se compone por default de 1 solo nodo. Esto se puede cambiar en la configuraciona del archivo que utilizaremos a continuacion

1.  Aplicamos la conmfiguracion del archivo

```
kubectl apply -f elastic-cluster.yaml
```

2. Monitorizar el estado del cluster y el proceso de creacion

```
kubectl get elasticsearch -n elastic
```

3. Ver el estado de los pods de elastic

```
kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-name=quickstart' -n elastic
```

----------------------------
PEDIR ACCESO A ELASTICSEARCH
----------------------------

1. Creamos un namespace especifico para el cluster de elasticsearch

```
kubectl create namespace elastic
```

2. El servicio ClusterIP es creado automaticamente en el cluster

```
kubectl get service quickstart-es-http -n elastic
```

3. Obtener contraseña
Un usuario llamado elastic es automaticamente creado y su contraseña esta almacenada en un secreto de k8s

```
PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
```

4. Desde una terminal diferente, correr este comando

```
kubectl port-forward service/quickstart-es-http 9200
```

5. Request localhost

```
curl -u "elastic:$PASSWORD" -k "https://localhost:9200"
```

https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-kibana.html
