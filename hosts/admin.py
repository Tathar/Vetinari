from django.contrib import admin


from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Result, ModBus_Address, ModBus_Connection



# class PingAdmin(admin.TabularInline):
#     model = Ping

class HostAdmin(admin.ModelAdmin):
    model = Host

class ICMP_WatcherAdmin(admin.ModelAdmin):
    model = ICMP_Watcher

class ICMP_ResultAdmin(admin.ModelAdmin):
    model = ICMP_Result

class ModBus_ConnectionAdmin(admin.ModelAdmin):
    model = ModBus_Connection

class ModBus_AddressAdmin(admin.ModelAdmin):
    model = ModBus_Address

class ModBus_ResultAdmin(admin.ModelAdmin):
    model = ModBus_Result


admin.site.register(Host, HostAdmin)
admin.site.register(ICMP_Watcher, ICMP_WatcherAdmin)
admin.site.register(ICMP_Result, ICMP_ResultAdmin)
admin.site.register(ModBus_Connection, ModBus_ConnectionAdmin)
admin.site.register(ModBus_Address, ModBus_AddressAdmin)
admin.site.register(ModBus_Result, ModBus_ResultAdmin)
#admin.site.register(Choice)
