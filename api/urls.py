from api.views import update_balance, list_accounts, get_transactions
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('update/balance/<int:account_id>', view=update_balance, name="update_balance"),
    path('', view=list_accounts, name="list_accounts"),
    path("transactions/", view=get_transactions, name="list_transactions"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)