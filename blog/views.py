from django.http import HttpResponse
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated

from blog.models import *
from rest_framework import serializers, viewsets


# 文章的序列化器
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
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
class ArticleViewSet(GenericAPIView,CreateModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



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