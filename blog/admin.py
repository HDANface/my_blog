from django.contrib import admin
from blog.models import Article,Category,Tag

admin.site.site_header = f'HDNA管理后台'  # 设置header
admin.site.site_title = f'HDNA管理后台'   # 设置title
admin.site.index_title = f'HDNA管理后台'

class ArticleAdmin(admin.ModelAdmin):
    # 外部显示字段
    list_display = ('title','create_author','created_date','tag','category','views')
    # 支持搜索的字段
    search_fields = ('tag__name','create_author__username')
    # 设置每页显示条数
    list_per_page = 20
    # 按选择字段降序
    ordering = ('-created_date',)






# Register your models here.
admin.site.register(Article,ArticleAdmin)
admin.site.register(Tag)