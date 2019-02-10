from django.contrib import admin


from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result



# class PingAdmin(admin.TabularInline):
#     model = Ping

class HostAdmin(admin.ModelAdmin):
    model = Host

class ICMP_WatcherAdmin(admin.ModelAdmin):
    model = ICMP_Watcher

class ICMP_ResultAdmin(admin.ModelAdmin):
    model = ICMP_Result

class ModBus_WatcherAdmin(admin.ModelAdmin):
    model = ModBus_Watcher

class ModBus_ResultAdmin(admin.ModelAdmin):
    model = ModBus_Result


admin.site.register(Host, HostAdmin)
admin.site.register(ICMP_Watcher, ICMP_WatcherAdmin)
admin.site.register(ICMP_Result, ICMP_ResultAdmin)
admin.site.register(ModBus_Watcher, ModBus_WatcherAdmin)
admin.site.register(ModBus_Result, ModBus_ResultAdmin)
#admin.site.register(Choice)
