from rest_framework import status
from rest_framework.exceptions import NotFound

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, \
    UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Admin, AdminPermissions
from .permissions import IsAdmin, ManageAdmins, IsOwnProfileAdmin
from .serializers import CreateAdminSerializer, GetAdminSerializer, \
    UpdateAdminSerializer, GetAdminPermissionsSerializer, \
    AdminPermissionsSerializer, ColorSerializer, CategorySerializer, \
    CreateSubCategorySerializer
from product.models import Color, Category, SubCategory


class AdminAPIView(GenericAPIView, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsAdmin, ManageAdmins]
    lookup_field = 'id'

    def get_queryset(self):
        return Admin.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetAdminSerializer
        elif self.request.method == 'PUT':
            return UpdateAdminSerializer

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request, id=None):
        serializer = CreateAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data

        admin = Admin.objects.create(
            username=obj.get('username'),
            first_name=obj.get('first_name'),
            last_name=obj.get('last_name'),
            phone_number=obj.get('phone_number'),
            email=obj.get('email'),
        )
        admin.set_password(obj.get('password'))
        admin.save()
        data = {'detail': 'Admin successfully created'}
        return Response(data=data, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        return self.update(request)

    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            raise NotFound


class AdminProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin, IsOwnProfileAdmin]
    serializer_class = UpdateAdminSerializer

    def get_object(self):
        return self.request.user


class AdminPermissionsAPIView(GenericAPIView, RetrieveModelMixin):
    """
    API For Return Permission Of Admin
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = GetAdminPermissionsSerializer

    def get_object(self):
        return AdminPermissions.objects.select_related('admin_id') \
            .get(admin_id=self.request.user.id)

    def get(self, request):
        return self.retrieve(request)


class SetPermissionForAdminAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    permission_classes = [IsAuthenticated, IsAdmin, ManageAdmins]
    serializer_class = AdminPermissionsSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            return AdminPermissions.objects.select_related('admin_id') \
                .get(admin_id=self.kwargs.get('id'))
        except AdminPermissions.DoesNotExist:
            raise NotFound

    def put(self, request, id):
        return self.update(request)


class APIColor(GenericAPIView, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = ColorSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Color.objects.all()
        name = self.request.query_params.get('name')
        code = self.request.query_params.get('code')
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        if code is not None:
            queryset = queryset.filter(code=code)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data
        Color.objects.create(**obj)

        return Response(data=obj, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        else:
            raise NotFound

    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            raise NotFound


class APICategory(GenericAPIView, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data
        Category.objects.create(**obj)

        return Response(data=obj, status=status.HTTP_201_CREATED)

    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        else:
            raise NotFound

    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            raise NotFound


class APISubCategory(GenericAPIView, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin):
    serializer_class = CreateSubCategorySerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAuthenticated, IsAdmin]
        return super().get_permissions()

    def get_queryset(self):
        queryset = SubCategory.objects.select_related('category').all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset

    def get(self, request, id=None):
        if id:
            return self.get(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        else:
            raise NotFound

    def patch(self, request, id=None):
        if id:
            return self.partial_update(request, id)
        else:
            raise NotFound

    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            raise NotFound

