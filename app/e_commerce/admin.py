from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Quantity)
admin.site.register(Cart)
admin.site.register(CartItem)