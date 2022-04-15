from django.contrib.auth.models import Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from my_app.account.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    password = serializers.CharField(max_length=128)
    last_login = serializers.DateTimeField(allow_null=True, required=False)
    is_superuser = serializers.BooleanField(
        help_text=_('Designates that this user has all permissions without explicitly assigning them.'),
        label='Superuser status', required=False)
    username = serializers.CharField(
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        max_length=150, validators=[UnicodeUsernameValidator(),
                                    UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(allow_blank=True, max_length=150, required=False)
    last_name = serializers.CharField(allow_blank=True, max_length=150, required=False)
    email = serializers.EmailField(allow_blank=True, label='Email address', max_length=254, required=False)
    is_staff = serializers.BooleanField(help_text=_('Designates whether the user can log into this admin site.'),
                                        label='Staff status', required=False)
    is_active = serializers.BooleanField(
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        label='Active', required=False)
    date_joined = serializers.DateTimeField(required=False)
    groups = serializers.PrimaryKeyRelatedField(
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        many=True, queryset=Group.objects.all(), required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(help_text=_('Specific permissions for this user.'), many=True,
                                                          queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validated_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(
                _('Old password is wrong!')
            )
        return value

    def save(self):
        self.instance.set_password(self.validated_data.get("new_password"))
        self.instance.save()


class AddToGroupSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(required=True, queryset=Group.objects.all())

    def save(self):
        if self.context['request'].method == 'POST':
            self.instance.groups.add(self.validated_data.get("group"))
        else:
            self.instance.groups.remove(self.validated_data.get("group"))
        self.instance.save()


class TokenObtainPairRequestSerializer(TokenObtainPairSerializer):
    pass


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class TokenRefreshRequestSerializer(TokenRefreshSerializer):
    pass


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)


class UserActivationSerializer(serializers.Serializer):
    pass
