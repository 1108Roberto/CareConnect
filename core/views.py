from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Client, Policy
from core.serializers import ClientSerializer, PolicySerializer


def client_dashboard(request, client_id=None):
    context = {"client_id": client_id or "all"}
    return render(request, "core/client_dashboard.html", context)


@api_view(["GET"])
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def client_detail(request, pk):
    client = Client.objects.get(pk=pk)
    serializer = ClientSerializer(client)
    return Response(serializer.data)


@api_view(["GET"])
def client_policies(request, client_id):
    policies = Policy.objects.filter(client_id=client_id)
    serializer = PolicySerializer(policies, many=True)
    return Response(serializer.data)
