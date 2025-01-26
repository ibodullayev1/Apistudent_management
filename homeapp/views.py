from rest_framework import viewsets, mixins
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count



class StudentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['age', 'grade']
    search_fields = ['first_name', 'last_name']


class CourseViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name']

    def get_queryset(self):

        queryset = Course.objects.annotate(students_count=Count('students'))
        return queryset

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            course.students.add(student)
            return Response({'status': 'talaba kursga muvaffaqiyatli qoshildi'})
        except Student.DoesNotExist:
            return Response({'status': 'talaba mavjud emas'})

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            course.students.remove(student)
            return Response({'status': 'talaba kursdan muvaffaqiyatli chetlashtirildi'})
        except Student.DoesNotExist:
            return Response({'status': 'talaba mavjud emas'})