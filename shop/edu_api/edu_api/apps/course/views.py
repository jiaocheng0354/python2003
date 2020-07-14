from django.shortcuts import render

# Create your views here.
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import Course, CourseCategory
from course.pagination import CoursePagination
from course.serializer import CourseSerializer, CourseCategorySerializer
from django_filters.rest_framework import DjangoFilterBackend

class CourseCategoryView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False)
    serializer_class = CourseCategorySerializer

class CourseListView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    ordering_fields = ("id", "students", "price")
    pagination_class = CoursePagination

class CourseRetrieveView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseSerializer
    lookup_field = "id"

