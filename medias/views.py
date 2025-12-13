from rest_framework.permissions import IsAuthenticated

from medias.models import Media
from rest_framework.generics import GenericAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import  CreateModelMixin
from rest_framework import serializers


# 序列化器
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class CreateMediaAPIView(GenericAPIView,CreateModelMixin):
    serializer_class = MediaSerializer
    queryset = Media
    permission_classes = [IsAuthenticated]

    # 添加图片
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

# 单数据删除修改查看
class RUDAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = MediaSerializer
    queryset = Media
    permission_classes = [IsAuthenticated]

