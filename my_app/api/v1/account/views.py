import reversion
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as DefaultTokenObtainPairView,
    TokenRefreshView as DefaultTokenRefreshView
)

from my_app.account.models import User
from my_app.api.v1.account.serializers import (
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    ChangePasswordSerializer,
    AddToGroupSerializer, UserActivationSerializer, UserSerializer,
)


class TokenObtainPairView(DefaultTokenObtainPairView):
    def post(self, request, *args, **kwargs):
        request_serializer = self.get_serializer(data=request.data)

        try:
            request_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_serializer = TokenObtainPairResponseSerializer(request_serializer.validated_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class TokenRefreshView(DefaultTokenRefreshView):
    def post(self, request, *args, **kwargs):
        request_serializer = self.get_serializer(data=request.data)

        try:
            request_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response_serializer = TokenRefreshResponseSerializer(request_serializer.validated_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        with reversion.create_revision():
            response = super(UserViewSet, self).create(request, *args, **kwargs)
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Created User")
            return response

    def update(self, request, *args, **kwargs):
        with reversion.create_revision():
            response = super(UserViewSet, self).update(request, *args, **kwargs)
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Updated User")
            return response

    def partial_update(self, request, *args, **kwargs):
        with reversion.create_revision():
            response = super(UserViewSet, self).partial_update(request, *args, **kwargs)
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Updated Partially User")
            return response

    def destroy(self, request, *args, **kwargs):
        with reversion.create_revision():
            response = super(UserViewSet, self).destroy(request, *args, **kwargs)
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Destroyed User")
            return response

    @action(methods=['post', 'delete'], detail=True, serializer_class=UserActivationSerializer)
    def activation(self, request, *args, **kwargs):
        with reversion.create_revision():
            instance = self.get_object()
            instance.activate(method=request.method)
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            comment = 'Activated User'
            if not instance.is_active:
                comment = 'Deactivated User'
            reversion.set_comment(comment)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True, serializer_class=AddToGroupSerializer)
    def add_to_group(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AddToGroupSerializer(instance=instance, data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        with reversion.create_revision():
            serializer.save()
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Added User to Group")
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, serializer_class=ChangePasswordSerializer)
    def passport_change(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ChangePasswordSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        with reversion.create_revision():
            serializer.save()
            reversion.set_user(request.user)
            reversion.set_date_created(timezone.now())
            reversion.set_comment("Changed Password")
        return Response(status=status.HTTP_200_OK)
