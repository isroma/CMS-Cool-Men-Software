# Lanzamiento del producto

Con estos pasos se puede desplegar el producto para su funcionamiento mediante Kubernetes, para lanzar una demo más ligera referirse a la documentación de [Docker legacy](/doc/legacy.md).

Todos los componentes de arquitectura se desplegarán dentro de un namespace que no es el (default) por problemas de compatibilidad con otros proyectos de los integrantes. Por defecto, se ha decidido el namespace "cms", y todos los comandos que utilizen el CLI de K8s (kubectl) deberán de ir acompañados de -n cms

Para crear el namespace "cms" dentro de nuestro cluster de minikube se debe ejecutar:

```
kubectl create namespace cms
```

**TL;DR** - Ejecutar:

```
kubectl apply -f cms.yml
```

Para acceder a Django:

```
minikube service django-service -n cms
```

# Documentación extra

- [Info de Django](/doc/django.md)
- [Docker legacy](/doc/legacy.md)
- [Guía de uso GitHub](/doc/help.md)