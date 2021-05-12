"""
Author: Sanidhya Mangal, Ravinder Singh
github:sanidhyamangal
email: sanidhya.mangal@engineerbabu
"""
from django.contrib.auth.hashers import make_password
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .permissions import (BaseViewSetPermissionMixin, IsManager,
                          IsOwnerAttributes, IsOwnerOrReadOnly,
                          IsSuperAdminOrStaff)


class BaseAPIViewSet(ModelViewSet):
    model_class = None
    serializer_class = None
    instance_name = None
    log_activity = True
    logger = None

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        return self.model_class.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data={
                "status": True,
                "message":
                f"{self.instance_name}s list reterieved sucessfully",
                "data": serializer.data
            })

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self.logger:
                self.logger.info("created %s with %s", self.instance_name,
                                 serializer.data)
            return Response(data={
                "status": True,
                "message": f"{self.instance_name} created sucessfully",
                "data": serializer.data
            },
                            status=status.HTTP_201_CREATED)

        return Response(data={
            "status": False,
            "message": f"{self.instance_name} creation failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            raise ValidationError({
                'status': False,
                'message': f"failed to find {self.instance_name}",
                "data": {}
            })

    def retrieve(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj)
        return Response(
            data={
                "status": True,
                "message": f"{self.instance_name} retrieved sucessfully",
                "data": serializer.data
            })

    def update(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if self.logger:
                self.logger.info("updated %s with %s", self.instance_name,
                                 request.data)
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if self.logger:
                self.logger.info("updated %s with %s for %s",
                                 self.instance_name, request.data, pk)
            return Response(
                data={
                    "status": True,
                    "message": f"{self.instance_name} updated sucessfully",
                    "data": serializer.data
                })
        return Response(data={
            "status": False,
            "message": f"{self.instance_name} update failed",
            "data": serializer.errors
        },
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        obj.delete()
        if self.logger:
            self.logger.info("deleted %s with %s", self.instance_name, pk)
        return Response(data={
            "status": True,
            "message": f"{self.instance_name} deleted sucessfully",
            "data": {}
        },
                        status=status.HTTP_200_OK)
