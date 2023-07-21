from django.contrib import admin
from .models import User, Posts, FFowers, Comments
# Register your models here.


admin.site.register(Posts)
admin.site.register(User)
admin.site.register(FFowers)
admin.site.register(Comments)
