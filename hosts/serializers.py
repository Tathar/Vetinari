from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.urls import reverse_lazy

#from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result, ModBus_Connection, ModBus_Address

from hosts.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')


class HostSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Host
        fields = ("url", 'id', 'common_name', 'mac_address', 'ip_address', 'host_Name', 'dns_Name', 'added_Date')
        
        
class ModBusConnectionSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Connection
        fields = ("url", 'id', 'name', 'port', 'unit_ID', 'host', 'byte_bigEndian', 'word_bigEndian')
#        fields = ('__all__')        
        
class ModBusAddressSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Address
        fields = ("url", 'id', 'common_name', 'unit', 'connection', 'address', 'count','vartype', 'factor', 'delay', 'crit_min', 'warn_min', 'warn_max', 'crit_max')
#         fields = ('__all__')
        
class ModBusResultSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Result
        fields = ("url", 'id', 'modbus_address', 'date', 'data')
        
        
class ICMPWatcherSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ICMP_Watcher
        fields = ("url", 'id', 'host')
        

class ICMPResultSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ICMP_Result
        fields = ("url", 'id', 'icmp_watcher', 'date', 'data', 'avg')
        
        
        
    