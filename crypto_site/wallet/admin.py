from django.contrib import admin
from .models import Crypto
from .models import Wallet
from .models import History

@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'price_usd', 'last_updated')
    search_fields = ('name', 'symbol')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto', 'amount')
    search_fields = ('user_username', 'crypto_name')
    
    
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "operation", "crypto", "amount", "getter", "time_stamp")
    search_fields = ("user","operation","getter",)
