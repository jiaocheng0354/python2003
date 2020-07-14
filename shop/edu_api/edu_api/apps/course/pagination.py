from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 4
    max_page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page"
