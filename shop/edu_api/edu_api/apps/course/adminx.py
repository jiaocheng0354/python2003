import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryAdmin(object):
    pass
xadmin.site.register(CourseCategory, CourseCategoryAdmin)

class CourseAdmin(object):
    pass
xadmin.site.register(Course, CourseAdmin)

class TeacherAdmin(object):
    pass
xadmin.site.register(Teacher, TeacherAdmin)

class CourseChapterAdmin(object):
    pass
xadmin.site.register(CourseChapter, CourseChapterAdmin)

class CourseLessonAdmin(object):
    pass
xadmin.site.register(CourseLesson, CourseLessonAdmin)