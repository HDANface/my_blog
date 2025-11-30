from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from blog.models import *
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


# 文章的序列化器
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('views','likes','comments')
        extra_kwargs = {'title':{
            'required':True,
            'allow_blank':False,
            'error_messages':{
                'blank':"标题未填写,请取一个标题"
            },
            'style':{'input_type':'文章标题'}
        }}

        def create(self):
            pass

# 创建文章
class ArticleViewSet(GenericAPIView,CreateModelMixin,ListModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # 重写鉴权组件
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()

    # 文章查看接口
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    # 文章创建接口
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# 单文章查看,删除更改
class ArticleView(GenericAPIView,DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # 指定认证类型
    authentication_classes = [JWTAuthentication]


    #自定义鉴权组件
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


    # 单文章查看接口
    def get(self,request,pk):
        return self.retrieve(request,pk)

    # 文章更新接口
    def put(self,request,pk):
        return self.update(request,pk)

    # 文章删除接口
    def delete(self,request,pk):
        return self.destroy(request,pk)


# 分类的序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# 标签的序列化器
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'