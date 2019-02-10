from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ModBusWatcherSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ModBus_Watcher
        fields = ('url', 'host', 'port', 'unit_ID', 'unit_ID', 'address', 'common_name', 'unit', 'factor')
