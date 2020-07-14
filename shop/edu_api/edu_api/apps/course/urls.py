from django.urls import path

from course import views

urlpatterns = [
    path('list/', views.CourseListView.as_view()),
    path('category/', views.CourseCategoryView.as_view()),
    path('retrieve/<str:id>/', views.CourseRetrieveView.as_view()),
]