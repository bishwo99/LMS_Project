from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET','POST'])

def category_list_create(request):
    if request.method == 'GET':
        category = models.Catergory.objects.all()
        serializer = serializers.CatergorySerializer(category, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response ({'detail' : 'Only admin can create categories.'})
        serializer = serializers.CatergorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET','POST'])
def course_list_create(request):
    if request.method == 'GET':
        # category and search

        category = request.query_params.get('category')
        search = request.query_params.get('search')
        queryset = models.Course.objects.all()

        if category:
            queryset = queryset.filter(category__title__icontains = category)

        if search:
            queryset = queryset.filter(
                Q(title__icontains = search) | Q(description__icontains = search)
            )

        if request.user.is_authenticated and request.user == 'teacher':
            queryset = queryset.filter(instructor = request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset,request)

        serializer = serializers.CourseSerializer(paginated_queryset, many = True, context = {'request' : request})
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'detail' : 'Only teacher can create courses.'})
        serializer =serializers.CourseSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)



        
            

