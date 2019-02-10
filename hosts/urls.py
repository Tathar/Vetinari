from django.urls import path , include

from . import views

from . import api

from rest_framework import routers

app_name = 'hosts'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename = "test")
router.register(r'groups', views.GroupViewSet)
router.register(r'modbuswatcher', views.ModBusWatcherViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('rest/', api.HostResource.as_list(), name='rest_list'),
#     path('rest/<int:pk>/', api.HostResource.as_detail(), name='rest_detail'),
    path('api/hosts/', include(api.HostResource.urls())),
    path('api/icmp_watcher/', include(api.ICMPWatcherResource.urls())),
    path('api/icmp_result/', include(api.ICMPResultResource.urls())),
    path('api/modbus_watcher/', include(api.ModBusWatcherResource.urls())),
    path('api/modbus_result/', include(api.ModBusResultResource.urls())),
#    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('rest/', include((router.urls, "rest-api"), namespace='rest_framework' )),
    path('rest/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('restapi/', views.ModBusWatcher_list),
]

print(urlpatterns)


