from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from rest_framework.generics import GenericAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import  CreateModelMixin, ListModelMixin
from rest_framework import serializers


# 序列化器
class CommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            "comment":{
                'error_messages':{
                    'blank':"填写内容为空,请重新填写"
                }
            }

        }
# 创建评论
class CommentsAPIView(CreateModelMixin,ListModelMixin,GenericAPIView):
    serializer_class = CommentsSerializers
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.request.method == "get":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class CommentRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializers
    queryset = Comment
    permission_classes = [IsAuthenticated]