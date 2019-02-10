from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Host, ICMP_Watcher, ICMP_Result, ModBus_Watcher, ModBus_Result


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
    
    
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, ModBusWatcherSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class ModBusWatcherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ModBus_Watcher.objects.all()
    serializer_class = ModBusWatcherSerializer
    

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

@csrf_exempt
def ModBusWatcher_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        modbus = ModBus_Watcher.objects.all()
        serializer = ModBusWatcherSerializer(modbus, many=True,context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ModBusWatcherSerializer(data=data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



