from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','listing','buyer','seller','amount','currency','status','created_at')
    list_filter = ('status','payment_method')
    search_fields = ('buyer__username','seller__username','gateway_id')
