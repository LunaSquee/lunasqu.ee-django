from django.db import models
from ipcalc import Network

class IP(models.Model):
    ip = models.CharField('IP network', max_length=18, help_text='IP address or IP network')

    def __unicode__(self):
        return self.ip

    def network(self):
        return Network(self.ip)

    class Meta:
        abstract = True

class DeniedIP(IP):
    class Meta:
        verbose_name = 'Denied IP'
        verbose_name_plural = 'Denied IPs'

class AllowedIP(IP):
    class Meta:
        verbose_name = 'Allowed IP'
        verbose_name_plural = 'Allowed IPs'