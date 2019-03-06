from django.db import models
from hosts.fields import *
#from django.utils import timezone
#import datetime

class Host(models.Model):
    common_name = models.CharField(max_length=64)
    mac_address = models.CharField(max_length=17,blank=True) #AA:BB:CC:DD:EE:FF
    ip_address = models.GenericIPAddressField() #IPv4 or IPv6
    host_Name = models.CharField(max_length=64,blank=True)
    dns_Name = models.CharField(max_length=254,blank=True)
    added_Date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.common_name + " (" + self.ip_address + ")"


class ICMP_Watcher(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    
    def __str__(self):
        return "icmp watcher (" + str(self.host.common_name) +")"
        
    class Meta:
        verbose_name = "ICMP Watcher"


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
        
    class Meta:
        verbose_name = "ICMP Result"

class ModBus_Connection(models.Model):
    
    class Meta:
        verbose_name = "Modbus Connection"
        
    name = models.CharField(max_length=64)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    port = models.IntegerField(default=502)
    unit_ID = models.IntegerField(default=0) #cannal modbus
    byte_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
    word_bigEndian =  models.BooleanField(default=True) #False for Little endian or True for BigEndian 
        

    
    def __str__(self):
        return "%s -> %s (%i)" % (self.host.common_name, self.name, self.unit_ID )
    
class ModBus_Address(models.Model):
    
    class Meta:
        verbose_name = "Modbus Address"
        ordering = ["address"]
    
    VARTYPE_CHOICES = ((0, 'bits'),
                       (1, '8bit_int'),
                       (2, '8bit_uint'),
                       (3, '16bit_int'),
                       (4, '16bit_uint'),
                       (5, '32bit_float'),
                       (6, '32bit_int'),
                       (7, '32bit_uint'),
                       (8, '64bit_float'),
                       (9, '64bit_int'),
                       (10, '64bit_uint'),
                       (11, 'string'))
    
    
    common_name = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)
    connection = models.ForeignKey(ModBus_Connection, on_delete=models.CASCADE)
    address = ModbusAddress(max_length=5, default=0)
    count = models.IntegerField(default=1)
    vartype = models.IntegerField(default=0, choices=VARTYPE_CHOICES)
    factor = models.FloatField(default=1)
    delay = models.IntegerField(default=60) #interval entre deux requette
    crit_min = models.FloatField(default=0)
    warn_min = models.FloatField(default=0)
    warn_max = models.FloatField(default=0)
    crit_max = models.FloatField(default=0)
        

    
    def Get_min(self):
        return self.modbus_result_set.all().aggregate(min('data'))
        
    def Get_max(self):
        return self.modbus_result_set.all().aggregate(max('data'))
        
    def Get_avg(self):
        return self.modbus_result_set.all().aggregate(min('data'))
    
    def __str__(self):
        return "%s -> %s" % (self.connection.name, self.common_name)
    
    def __unicode__(self):
        return u"%s -> %s" % (self.connection.name, self.common_name)

class ModBus_Result(models.Model):
    
    class Meta:
        verbose_name = "Modbus Result"
        verbose_name_plural = "Modbus Results"
        ordering = ["-date"]
        
    modbus_address = models.ForeignKey(ModBus_Address, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    data = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.data)



"""
from hosts.models import Host,Ping
h = Host.objects.get(pk=1)
p = h.ping_set.get(pk=1)
"""