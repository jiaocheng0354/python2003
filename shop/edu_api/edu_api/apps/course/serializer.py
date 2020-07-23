from rest_framework import serializers, exceptions

from course.models import Course, CourseCategory, Teacher, CourseLesson, CourseChapter


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("name", "role", "title", "signature", "image", "brief")


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ("id", "lesson_list", "name", "students", "price", "course_img","brief_html","course_video",
                  "level", "brief", "level_title","discount_name", "real_price","teacher","active_time")
        # depth = 2


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ("id", 'name', "section_link", "free_trail")


class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ("id", "coursesections", "name", "chapter", "course")
