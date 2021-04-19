from django.db import models

class StorageObject(models.Model):
    prefix = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    container = models.CharField(max_length=1024)
    objectname = models.CharField(max_length=1024)

    class Meta:
        unique_together = ("container", "objectname")

    def __unicode__(self):
        return u'%s/%s' % (self.container, self.objectname)