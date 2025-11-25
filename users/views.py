from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response

User = get_user_model()


# 用户注册接口
# 生成User序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 接受字段
        fields = ['username', 'email', 'password']
        # 自定义password字段,允许接受但是不返回,且为必须填写值
        extra_kwargs = {'password': {'write_only': True,'required': True}}
    
    def validate_email(self, emails):
        UserEmail = User.objects.filter(email = emails)
        if UserEmail.exists():
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
        except Exception as e:
            # 验证邮箱是否重复
            if User.objects.filter(email=validated_data.get('email', '')).exists():
                raise serializers.ValidationError({'email': '该邮箱已被注册'})
            
            # 检查用户名是否为空
            if validated_data.get('username') is None or validated_data.get('username') == '':
                raise serializers.ValidationError({'username': '用户名为空，请重新输入'})
            
            # 检查密码一致性（需要额外字段验证）
            if 'password2' in validated_data and validated_data['password'] != validated_data['password2']:
                raise serializers.ValidationError({'password': '两次密码不统一'})
            
            # 抛出其他异常
            raise serializers.ValidationError(str(e))


# 注册接口
class UserCreateAPIView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        return self.create(request)
