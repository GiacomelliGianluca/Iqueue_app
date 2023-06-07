from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import Shop, Account, Product, TimeSlot, Slot, QR, Advertisement

admin.site.register(Shop)
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(TimeSlot)
admin.site.register(Slot)
admin.site.register(QR)
admin.site.register(Advertisement)

