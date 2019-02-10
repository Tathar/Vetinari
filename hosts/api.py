#posts/api.py
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result


class HostResource(DjangoResource):
    
    paginate = True
    page_size = 10
    
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'common_name': 'common_name',
        'mac_address': 'mac_address',
        'ip_address': 'ip_address',
        'host_Name': 'host_Name',
        'dns_Name': 'dns_Name',
    })
    
    def is_authenticated(self):
#         return self.request.user.is_authenticated
        return True

    # GET /api/posts/ (but not hooked up yet)
    def list(self):
        return Host.objects.all()

    # GET /api/posts/<pk>/ (but not hooked up yet)
    def detail(self, pk):
        return Host.objects.get(id=pk)

    # POST /api/posts/
    def create(self):
        return Host.objects.create(
            common_name=self.data['common_name'],
            mac_address=self.data['mac_address'],
            ip_address=self.data['ip_address'],
            host_Name=self.data['host_Name'],
            dns_Name=self.data['dns_Name'],
        )

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            host = Host.objects.get(id=pk)
        except Host.DoesNotExist:
            host = Host()

        host.common_name = self.data['common_name']
        host.mac_address = self.data['mac_address']
        host.ip_address = self.data['ip_address']
        host.host_Name = self.data['host_Name']
        host.dns_Name = self.data['dns_Name']
        host.save()
        return host

    # DELETE /api/posts/<pk>/
    def delete(self, pk):
        Host.objects.get(id=pk).delete()


class ICMPWatcherResource(DjangoResource):
    
    paginate = True
    page_size = 10
    
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'host': 'host.id',
    })
    
    def is_authenticated(self):
#         return self.request.user.is_authenticated
        return True

    # GET /api/posts/ (but not hooked up yet)
    def list(self):
        return ICMP_Watcher.objects.all()

    # GET /api/posts/<pk>/ (but not hooked up yet)
    def detail(self, pk):
        return ICMP_Watcher.objects.get(id=pk)

    # POST /api/posts/
    def create(self):
        return ICMP_Watcher.objects.create(
            host = Host.objects.get( pk = self.data['host'] ),
        )

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            icmp = ICMP_Watcher.objects.get(id=pk)
        except ICMP_Watcher.DoesNotExist:
            icmp = ICMP_Watcher()

        icmp.host = Host.objects.get( pk = self.data['host'] )
        icmp.save()
        return icmp

    # DELETE /api/posts/<pk>/
    def delete(self, pk):
        ICMP_Watcher.objects.get(id=pk).delete()


class ICMPResultResource(DjangoResource):
    
    paginate = True
    page_size = 10
    
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'icmp_watcher': 'icmp_watcher.id',
        'date': 'date',
        'result': 'result',
        'avg': 'avg',
    })

    
    def is_authenticated(self):
#         return self.request.user.is_authenticated
        return True

    # GET /api/posts/ (but not hooked up yet)
    def list(self):
        return ICMP_Result.objects.all()

    # GET /api/posts/<pk>/ (but not hooked up yet)
    def detail(self, pk):
        return ICMP_Result.objects.get(id=pk)

    # POST /api/posts/
    def create(self):
        return ICMP_Result.objects.create(
            icmp_watcher = ModBus_Watcher.objects.get( pk = self.data['icmp_watcher'] ),
            result=self.data['result'],
            avg=self.data['avg'],
        )

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            icmp = ICMP_Result.objects.get(id=pk)
        except ICMP_Result.DoesNotExist:
            icmp = ICMP_Result()

        icmp.icmp_watcher = ModBus_Watcher.objects.get( pk = self.data['icmp_watcher'] )
        icmp.result = self.data['result']
        icmp.avg = self.data['avg']
        icmp.save()
        return icmp

    # DELETE /api/posts/<pk>/
    def delete(self, pk):
        ICMP_Result.objects.get(id=pk).delete()
             

class ModBusWatcherResource(DjangoResource):
    
    paginate = True
    page_size = 10
    
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'host': 'host.id',
        'port': 'port',
        'unit_ID': 'unit_ID',
        'address': 'address',
        'common_name': 'common_name',
        'unit': 'unit',
        'factor': 'factor',
    })
    
    def is_authenticated(self):
#         return self.request.user.is_authenticated
        return True

    # GET /api/posts/ (but not hooked up yet)
    def list(self):
        return ModBus_Watcher.objects.all()

    # GET /api/posts/<pk>/ (but not hooked up yet)
    def detail(self, pk):
        return ModBus_Watcher.objects.get(id=pk)

    # POST /api/posts/
    def create(self):
        return ModBus_Watcher.objects.create(
            host = Host.objects.get( pk = self.data['host'] ),
            port=self.data['port'],
            unit_ID=self.data['unit_ID'],
            address=self.data['address'],
            common_name=self.data['common_name'],
            unit=self.data['unit'],
            factor=self.data['factor'],
        )

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            modbus = ModBus_Watcher.objects.get(id=pk)
        except ModBus_Watcher.DoesNotExist:
            modbus = ModBus_Watcher()

        modbus.host = Host.objects.get( pk = self.data['host'] )
        modbus.port = self.data['port']
        modbus.unit_ID = self.data['unit_ID']
        modbus.address = self.data['address']
        modbus.common_name = self.data['common_name']
        modbus.unit = self.data['unit']
        modbus.factor = self.data['factor']
        modbus.save()
        return modbus

    # DELETE /api/posts/<pk>/
    def delete(self, pk):
        ModBus_Watcher.objects.get(id=pk).delete()
        
        
class ModBusResultResource(DjangoResource):
    
    paginate = True
    page_size = 10
    
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'modbus_watcher': 'modbus_watcher.id',
        'date': 'date',
        'data': 'data',
    })
    
    def is_authenticated(self):
#         return self.request.user.is_authenticated
        return True

    # GET /api/posts/ (but not hooked up yet)
    def list(self):
        return ModBus_Result.objects.all()

    # GET /api/posts/<pk>/ (but not hooked up yet)
    def detail(self, pk):
        return ModBus_Result.objects.get(id=pk)

    # POST /api/posts/
    def create(self):
        return ModBus_Result.objects.create(
            modbus_watcher = ModBus_Watcher.objects.get( pk = self.data['modbus_watcher'] ),
            data=self.data['data'],
        )

    # PUT /api/posts/<pk>/
    def update(self, pk):
        try:
            modbus = ModBus_Result.objects.get(id=pk)
        except ModBus_Result.DoesNotExist:
            modbus = ModBus_Result()

        modbus.modbus_watcher = ModBus_Watcher.objects.get( pk = self.data['modbus_watcher'] )
        modbus.data = self.data['data']
        modbus.save()
        return modbus

    # DELETE /api/posts/<pk>/
    def delete(self, pk):
        ModBus_Result.objects.get(id=pk).delete()
        
        
        
        
        