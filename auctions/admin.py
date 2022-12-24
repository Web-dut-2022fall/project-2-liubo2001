from django.contrib import admin

from .models import User, Listings, Category, Comment, Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
