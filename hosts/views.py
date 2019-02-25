from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User, Group

from rest_framework import viewsets

#from .serializers import UserSerializer, GroupSerializer, ModBusWatcherSerializer, HostSerializer, ModBusResultSerializer
from hosts.serializers import *
#from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result
from hosts.models import *

import django_filters.rest_framework


class IndexView(generic.ListView):
    template_name = 'hosts/index.html'
    context_object_name = 'latest_hosts_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Host.objects.order_by('-added_Date')[:5]


class DetailView(generic.DetailView):
    model = Host
    ordering = 'date'
    template_name = 'hosts/detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['modbus_list'] = self.object.modbus_watcher_set.all()
        return context
        
class ResultsView(generic.DetailView):
    model = Host
    template_name = 'hosts/results.html'

"""
def vote(request, question_id):
    host = get_object_or_404(Host, pk=question_id)
    try:
        selected_ping = Host.ping_set.get(pk=request.POST['choice'])
    except (KeyError, Ping.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    """
    
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_fields = ('__all__')


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = ('__all__')


class HostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_fields = ('__all__')
    
class ModBusConnectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ModBus_Connection.objects.all()
    serializer_class = ModBusConnectionSerializer
    filter_fields = ('__all__')
    
    
class ModBusAddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ModBus_Address.objects.all()
    serializer_class = ModBusAddressSerializer
    filter_fields = ('__all__')
    
    
class ModBusResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ModBus_Result.objects.all()
    serializer_class = ModBusResultSerializer
    filter_fields = ('__all__')
    
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
    
            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True
    
        return super(ModBusResultViewSet, self).get_serializer(*args, **kwargs)
    
    
    
    
