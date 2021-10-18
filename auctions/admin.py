from django.contrib import admin
from .models import *

# Register your 
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)

