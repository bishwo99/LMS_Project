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

# Course details

@api_view(['GET','POST'])
def lession_list_create(request):
    # GET request
    if request.method == 'GET':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail': 'Course id is required.'})
        try:
            course = models.Course.objects.get(pk = course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course does not found.'})
        #teacher kina check korbo, admin, enrolled

        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and request.user == course.instructor
        is_admin = request.user.is_authenticated and request.user.role == 'admin'

        """Ekjon student je ashole ei api te request korche se asholei oi course e enrolled kina. 
        enroll na hole obosshoi shei course er lesson er access she pabena"""

        is_enrolled = models.Enrollment(
            student = request.user,
            course = course,
            status = 'active'
        ).exists() if request.user.is_authenticated and request.user.role == 'student' else False

        if not(is_teacher or is_admin or is_enrolled):
            return Response({'detail' : "Sorry,You don't have permission to view these lessons."})
        lessons = models.Lesson.objects.filter(course = course)
        serializer = serializers.LessonSerializer(lessons, many = True)
        return Response(serializer.data)

    # POST request
    if request.method == 'POST':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail': 'Courese id is required.'})
        try:
            course = models.Course.objects(pk = course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course does not found.'})

        if request.user != course.instructor:
            return Response({'detail': 'You can only add your own lessons.'})

        serializer = serializers.LessonSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
# Lesson Details

        
            

