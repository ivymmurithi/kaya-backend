from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Account

class APITestCase(TestCase):

    def setUp(self):
        self.account1 = Account.objects.create(username="Mukami", balance=0.0)
        self.account2 = Account.objects.create(username="Mogendi", balance=0.0)
        self.client = APIClient()
    
    def test_deposit(self):
        update_data = {
            "amount": 120000000.0,
            "action": "DEPOSIT"
        }
        pre_update_balance = self.account1.balance

        self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")
        
        self.account1.refresh_from_db()
        assert self.account1.balance == pre_update_balance + update_data["amount"]
    
    def test_withdraw(self):
        self.account1.balance = 2000000000000.0
        self.account1.save()
        update_data = {
            "amount": 120000000.0,
            "action": "WITHDRAW"
        }
        pre_update_balance = self.account1.balance

        self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")
        
        self.account1.refresh_from_db()
        assert self.account1.balance == pre_update_balance - update_data["amount"]   
        
        self.account1.refresh_from_db()
        pre_update_balance = self.account1.balance
        update_data["amount"] = self.account1.balance + 1000

        res = self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")

        self.account1.refresh_from_db()
        assert self.account1.balance == pre_update_balance
    
    def test_transfer(self):
        self.account1.balance = 2000000000000.0
        self.account1.save()
        update_data = {
            "amount": 120000000.0,
            "action": "TRANSFER",
            "target_id": str(self.account2.id),
        }
        pre_update_balance = self.account1.balance

        self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")
        
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        assert self.account1.balance == pre_update_balance - update_data["amount"]
        assert self.account2.balance == update_data["amount"]   
        
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        pre_update_balance = self.account1.balance
        pre_update_target_balance = self.account2.balance
        update_data["amount"] = self.account1.balance + 1000

        res = self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")

        self.account1.refresh_from_db()
        assert self.account1.balance == pre_update_balance  
        assert self.account2.balance == pre_update_target_balance

        update_data.pop("target_id")

        res = self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")

        assert res.status_code == 400
    
    def test_list_accounts(self):
        res = self.client.get("/api/")

        assert res.json()
        returned_ids = [account['id'] for account in res.json()]
        account_ids = [self.account1.id, self.account2.id]
        for id in account_ids:
            assert str(id) in returned_ids

    def test_list_transactions(self):
        self.account1.balance = 2000000000000.0
        self.account1.save()
        update_data = {
            "amount": 120000000.0,
            "action": "TRANSFER",
            "target_id": str(self.account2.id),
        }
        pre_update_balance = self.account1.balance

        self.client.put(f"/api/update/balance/{self.account1.id}", data=update_data, format="json")

        res = self.client.get(f"/api/transactions/")

        assert res.json()["transactions"] == [f"TRANSFER:{self.account1.username}:{self.account2.username}:120000000.0"]