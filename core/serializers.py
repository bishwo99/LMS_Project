from . import models
from rest_framework import serializers

class CatergorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catergory
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

class QuestionAnswer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswer
        fields = '__all__'


