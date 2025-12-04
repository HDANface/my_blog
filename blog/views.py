from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,

)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog.models import *

# 分类的序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# 标签的序列化器
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

# 文章的序列化器
class ArticleSerializer(serializers.ModelSerializer):
    tag_name = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False,
    )


    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'create_author', 'Cover', 'status',
            'created_date', 'updated_date', 'likes', 'comments', 'views',
            'category', 'tags', 'tag_name'
        ]

        read_only_fields = ("views", "likes", "comments")
        extra_kwargs = {
            "title": {
                "required": True,
                "allow_blank": False,
                "error_messages": {"blank": "标题未填写,请取一个标题"},
                "style": {"input_type": "文章标题"},
            }
        }

        # 重写create方法
        def create(self, validated_data):

            tag_name = validated_data.pop['tag_name',[]]

            article = Article.objects.create(**validated_data)

            for name in tag_name:
                tag,_ = Tag.objects.get_or_create(name=name.strip())
                article.tags.add(tag)

            return article

        # 重写update方法
        def update(self, instance, validated_data):
            # 提取标签名称
            tag_names = validated_data.pop('tag_name', None)

            # 更新其他字段
            super().update(instance, validated_data)

            # 更新标签
            if tag_names is not None:
                instance.tags.clear()
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name.strip())
                    instance.tags.add(tag)

            return instance

"========================================================"

# 创建文章
class ArticleViewSet(GenericAPIView, CreateModelMixin, ListModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # 重写鉴权组件
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    # 文章查看接口
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 文章创建接口
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# 单文章查看,删除更改
class ArticleView(
    GenericAPIView, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # 指定认证类型
    authentication_classes = [JWTAuthentication]

    # 自定义鉴权组件
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    # 单文章查看接口
    def get(self, request, pk):
        return self.retrieve(request, pk)

    # 文章更新接口
    def put(self, request, pk):
        return self.update(request, pk)

    # 文章删除接口
    def delete(self, request, pk):
        return self.destroy(request, pk)


"""==================================================="""

# 分类的创建和查看
class CategoryView(GenericAPIView, ListModelMixin,CreateModelMixin, UpdateModelMixin,DestroyModelMixin):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]



    def get(self, request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def put(self, request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

"""==================================================="""


# 标签的序列化器
class TagView(GenericAPIView, ListModelMixin,CreateModelMixin, UpdateModelMixin,DestroyModelMixin):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = []

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get(self, request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self, request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def put(self, request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)