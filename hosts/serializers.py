from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.urls import reverse_lazy

from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result, ModBus_Result

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class HostSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Host
        fields = ('url', 'id', 'common_name', 'mac_address', 'ip_address', 'host_Name', 'dns_Name', 'added_Date')
        
        
class ModBusWatcherSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Watcher
        #fields = ('url', 'id', 'host', 'port', 'unit_ID', 'word','byte_bigEndian' ,'word_bigEndian' ,'vartype', 'address', 'common_name', 'unit', 'factor')
        fields = ('__all__')

class ModBusResultSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Result
        fields = ('url', 'id', 'modbus_watcher', 'date', 'data')
        
        
class ICMPWatcherSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Watcher
        fields = ('url', 'id', 'host')
        

class ICMPResultSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Result
        fields = ('url', 'id', 'icmp_watcher', 'date', 'data', 'avg')
        
        
        
    