from django.contrib import admin

from .models import Bid, Contract, User


# register models with admin site
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Contract)