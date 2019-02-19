from django.db import models
#from django.utils import timezone
#import datetime

class Host(models.Model):
    common_name = models.CharField(max_length=64)
    mac_address = models.CharField(max_length=17,blank=True) #AA:BB:CC:DD:EE:FF
    ip_address = models.CharField(max_length=39) #IPv4 or IPv6
    host_Name = models.CharField(max_length=64,blank=True)
    dns_Name = models.CharField(max_length=254,blank=True)
    added_Date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.common_name + " (" + self.ip_address + ")"


class ICMP_Watcher(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    
    def __str__(self):
        return "icmp watcher (" + str(self.host.common_name) +")"


class ICMP_Result(models.Model):
    icmp_watcher = models.ForeignKey(ICMP_Watcher, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField()
    avg = models.FloatField(blank=True )
    def __str__(self):
        if self.result:
            return "True (avg=" + str(self.avg) + ")"
        else:
            return  "False"

class ModBus_Connection(models.Model):
    
    
    name = models.CharField(max_length=64)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    port = models.IntegerField(default=502)
    unit_ID = models.IntegerField(default=0) #cannal modbus
    
class ModBus_Address(models.Model):
    
    VARTYPE_CHOICES = ((0, '32bit_int'),
                  (1, '64bit_long'))
    
    connection = models.ForeignKey(ModBus_Connection, on_delete=models.CASCADE)
    address = models.IntegerField(default=0)
    word = models.IntegerField(default=1)
    byte_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
    word_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
    vartype = models.IntegerField(default=0, choices=VARTYPE_CHOICES)
    common_name = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)
    factor = models.FloatField(default=1)
    delay = models.IntegerField(default=60) #interval entre deux requette

    crit_min = models.FloatField(default=0)
    warn_min = models.FloatField(default=0)
    warn_max = models.FloatField(default=0)
    crit_max = models.FloatField(default=0)
        
class ModBus_Watcher(models.Model):
    
    VARTYPE_CHOICES = ((0, '32bit_int'),
                  (1, '64bit_long'))
    
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    port = models.IntegerField(default=502)
    unit_ID = models.IntegerField(default=0) #cannal modbus
    address = models.IntegerField(default=0)
    word = models.IntegerField(default=1)
    byte_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
    word_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
    vartype = models.IntegerField(default=0, choices=VARTYPE_CHOICES)
    common_name = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)
    factor = models.FloatField(default=1)
    delay = models.IntegerField(default=60) #interval entre deux requette
    
    crit_min = models.FloatField(default=0)
    warn_min = models.FloatField(default=0)
    warn_max = models.FloatField(default=0)
    crit_max = models.FloatField(default=0)

    class Meta:
        verbose_name = "Modbus Watcher"
        verbose_name_plural = "Modbus Watchers"
    
    def Get_min(self):
        return self.modbus_result_set.all().aggregate(min('data'))
        
    def Get_max(self):
        return self.modbus_result_set.all().aggregate(max('data'))
        
    def Get_avg(self):
        return self.modbus_result_set.all().aggregate(min('data'))
    
    def __str__(self):
        return "modbus " + str(self.common_name) + " (" + str(self.host.common_name) +")"
    
    def __unicode__(self):
        return "modbus " + str(self.common_name) + " (" + str(self.host.common_name) +")"

class ModBus_Result(models.Model):
    
    class Meta:
        verbose_name = "Modbus Result"
        verbose_name_plural = "Modbus Results"
        
    modbus_watcher = models.ForeignKey(ModBus_Watcher, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    data = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.data)


"""
from hosts.models import Host,Ping
h = Host.objects.get(pk=1)
p = h.ping_set.get(pk=1)
"""