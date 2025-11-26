from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

# 用户注册接口
# 生成User序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 接受字段
        fields = ['username', 'email', 'password']
        # 自定义password字段,允许接受但是不返回,且为必须填写值
        extra_kwargs = {'username':
                            {'min_length': 3,
                             'error_messages': {
                                 'min_length': '用户名至少3位',
                             }},
                        'password':
                            {'write_only': True,
                             'required': True,
                             'min_length': 6,
                             'error_messages': {
                                 'min_length': '密码至少需要6位',
                             }}}

    # 验证邮箱重复性
    def validate_email(self, email):
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return email

    def validate_username(self, username):
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError('该用户已被注册')
        return username

    #自定义创建方法(使用create_user对密码进行加密)
    def create(self, validated_data):
        Users = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
                )
        return Users


# 注册接口
class UserCreateAPIView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # 给与接口访问权限（任何人都能访问）
    permission_classes = [AllowAny]

    def post(self, request):
        return self.create(request)

"""====================================================================================================================="""

# 登录的序列化器
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True,'required': True}}


# 登录API:
class UserLoginAPIView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # 权限开放
    permission_classes = [AllowAny]

    def post(self, request):
        pass