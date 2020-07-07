from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from emp.emppagination import EmpPagination
from emp.models import Emp
from emp.serializers import EmpModelSerializer
from utils.response import APIResponse


# Create your views here.
class EmpView(GenericAPIView,
              RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Emp.objects.filter()
    serializer_class = EmpModelSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            results = self.retrieve(request, *args, **kwargs)
        else:
            results = self.list(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)

    def post(self, request, *args, **kwargs):
        results = self.create(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)

    def patch(self, request, *args, **kwargs):
        results = self.update(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        Emp.objects.filter(id=pk).delete()
        results = self.list(request, *args, **kwargs)
        return APIResponse(204, True, results=results.data)


class EmpListView(ListAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "salary"]
    ordering = ["id"]

    queryset = Emp.objects.all()
    serializer_class = EmpModelSerializer
    pagination_class = EmpPagination
