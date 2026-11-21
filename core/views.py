from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET','POST'])

def category_list_create(request):
    if request.method == 'GET':
        category = models.Catergory.objects.all()
        serializer = serializers.CatergorySerializer(category, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'admin':
            return ({'detail' : 'Only admin can create categories.'})
        serializer = serializers.CatergorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
