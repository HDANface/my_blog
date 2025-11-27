from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth import get_user_model, login, logout
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

# 用户注册接口
# 生成User序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 接受字段
        fields = ['email', 'username', 'password']
        # 自定义password字段,允许接受但是不返回,且为必须填写值
        extra_kwargs = {'username':
                            {'min_length': 3,
                             'required': True,
                             'allow_blank': False,
                             'error_messages': {
                                 'blank': '用户名不能为空',
                                 'min_length': '用户名至少3位',
                             },
                             'style':{
                                 'placeholder':'请输入用户名',
                             }},
                        'password':
                            {'write_only'    : True,
                             'required'      : True,
                             'min_length'    : 6,
                             'allow_blank' : False,
                             'error_messages': {
                                 'blank' : '密码不能为空',
                                 'min_length': '密码至少需要6位',
                             },
                             'style':{
                                 'input_type': 'password',
                                 'placeholder' : '请输入密码',
                             }},
                        'email':
                            {
                             'required': True,
                             'allow_blank' : False,
                             'error_messages': {
                               'blank' : '请输入一个邮箱',
                             },
                            'style':{
                                'input_type': 'email',
                                'placeholder' : '请输入邮箱',
                            }}
                        }

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
        fields = ['email', 'password']
        extra_kwargs = {'password':
                            {'write_only': True,
                             'required'  : True,
                             'allow_blank' : False,
                             'error_messages': {
                                 'blank' : '密码不能为空',
                             },
                             'style':{
                                 'input_type' : 'password',
                                 'placeholder' : '密码',
                             }
                             },
                        'email':
                            {'required': True,
                             'allow_blank' : False,
                             'error_messages': {
                                 'blank' : '邮箱未填写',
                             },
                             'style':{
                                'placeholder' : '邮箱填写',
                             }

                        }}

# 登录API:
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    # 权限开放
    permission_classes = [AllowAny]
    # 登录接口不需要JWT认证
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            try:
                # 直接通过邮箱查找用户
                user = User.objects.get(email=email)
                # 验证密码
                if user.check_password(password):
                    login(request, user)
                    # 返回JWT token
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'code': 200,
                        'msg': '登录成功',
                        'data': {
                            'id': user.id,
                            'email': user.email,
                            'username': user.username,
                            'token': str(refresh.access_token),
                            'refresh': str(refresh),
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'code': 401,
                        'msg': '邮箱或密码错误',
                        'data': None
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'code': 401,
                    'msg': '该邮箱未注册',
                    'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'code': 400,
                'msg': '请提供邮箱和密码',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

    # 注销
    def delete(self, request):
        logout(request)
        return Response({
            'code': 200,
            'msg': '成功注销',
            'data': None
        })

"""====================================================================================================================="""
