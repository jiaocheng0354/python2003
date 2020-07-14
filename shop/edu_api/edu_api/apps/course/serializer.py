from rest_framework import serializers, exceptions

from course.models import Course, CourseCategory, Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("name", "role", "title", "signature", "image", "brief")
        exclude = ("is_delete", "create_time", "update_time")


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer

    class Meta:
        model = Course
        fields = ("id", "teacher", "lesson_list", "name", "students", "pub_lessons", "lessons", "price", "course_img",
                  "level_choices", "level","brief")
        depth = 2


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ("id", "name")
