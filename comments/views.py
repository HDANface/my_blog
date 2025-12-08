from comments.models import Comment
from rest_framework.generics import GenericAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import  CreateModelMixin
from rest_framework import serializers


# 序列化器
class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'