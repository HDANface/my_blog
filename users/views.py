from sqlite3 import IntegrityError

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from rest_framework.response import Response

from users.models import User


# 用户注册接口
# 生成User序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 接受字段
        fields = ['username', 'email']
        # 自定义password字段,允许接受但是不返回,且为必须填写值
        extra_kwargs = {'password': {'write_only': True,'required': True}}

        # 判断邮箱是否被注册
        def validate_email(self, emails):
            UserDate = User.objects.filter(email = emails)
            if UserDate.exists():
                raise serializers.ValidationError('该邮箱已被注册')
            return emails

        #自定义创建方法(使用create_user对密码进行加密)
        def create(self, validated_data):
            try:
                Users = User.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )

                return Users
            except:
                if validated_data['password'] != validated_data['password2']:
                    raise serializers.ValidationError('两次密码不统一')

                if validated_data['username'] is None:
                    raise serializers.ValidationError('用户名为空，请重新输入')
                else:
                    pass


# 注册接口
class UserCreateAPIView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        return self.create(request)
