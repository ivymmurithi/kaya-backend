from api.views import update_balance, list_accounts
from django.urls import path


urlpatterns = [
    path('update/balance/<int:account_id>', view=update_balance, name="update_balance"),
    path('', view=list_accounts, name="list_accounts"),
]