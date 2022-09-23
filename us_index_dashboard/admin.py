# Admin.py

from django.contrib import admin
from .models import DjiTest,IxicTest,NdxTest,Item,Purchase



# Register your models here.
admin.site.register(DjiTest)
admin.site.register(IxicTest)
admin.site.register(NdxTest)

#以下为测试内容
admin.site.register(Item)
admin.site.register(Purchase)
#测试内容结束