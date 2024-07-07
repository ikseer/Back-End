
# -*- coding: utf-8 -*-

from accounts.filters import *
from accounts.models import *
from accounts.pagination import *
from accounts.permissions import DoctorPermission
from accounts.serializers import *
from accounts.utils import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import mixins, viewsets

# -*- coding: utf-8 -*-




class DoctorViewSet(

                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet
):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [DoctorPermission]
    pagination_class=CustomPagination
    filter_backends = [
            DjangoFilterBackend,
            rest_filters.SearchFilter,
            rest_filters.OrderingFilter,
        ]
    filterset_class = DoctorFilter


    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'method', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['soft', 'hard'],
    #             description='Specify the delete method (soft or hard). Default is soft.'
    #         )
    #     ]
    # )
    # def destroy(self, request, *args, **kwargs):
    #     if  request.query_params.get('method')=='hard':
    #             instance = self.get_object()
    #             instance.delete(force_policy=HARD_DELETE)
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return super().destroy(request, *args, **kwargs)

    # # @method_decorator(cache_page(60))
    # def get_deleted(self, request, *args, **kwargs):
    #     if not request.user.is_staff:
    #         return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    #     paginator = self.pagination_class()
    #     deleted_doctors = Doctor.deleted_objects.all()
    #     result_page = paginator.paginate_queryset( deleted_doctors, request)
    #     serializer = self.get_serializer(result_page, many=True)
    #     return paginator.get_paginated_response(serializer.data)


# class DeletedDoctorView(viewsets.ViewSet):
#     serializer_class = RestoreDoctorSerializer
#     queryset = Doctor.deleted_objects.all()
#     permission_classes = [StaffPermission]
#     def restore(self, request, *args, **kwargs):
#         serializer = RestoreDoctorSerializer(data={'id':kwargs['pk']})
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         instance = serializer.validated_data['id']
#         instance.undelete()
#         return Response(status=status.HTTP_200_OK)
#     def destroy(self, request, *args, **kwargs):
#         serializer = RestoreDoctorSerializer(data={'id':kwargs['pk']})
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         instance = serializer.validated_data['id']
#         instance.delete(force_policy=HARD_DELETE)
#         return Response(status=status.HTTP_204_NO_CONTENT)
