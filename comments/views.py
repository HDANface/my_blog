from comments.models import Comment
from rest_framework.generics import GenericAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import  CreateModelMixin, RetrieveModelMixin
from rest_framework import serializers


# 序列化器
class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# 创建评论
class CommentsAPIView(CreateModelMixin,GenericAPIView):
    serializer_class = CommentsSerializers
    queryset = Comment

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

