from django.contrib import admin
from .models import Products
from .models import ContactForm
from .models import Cart



# Register your models here.
admin.site.register(Products)
admin.site.register(ContactForm)
admin.site.register(Cart)