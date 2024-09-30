from django.test import TestCase
from capybuyra.models import Orders, Client
from rest_framework.test import APIClient
from model_bakery import baker
# Create your tests here.
class ClientViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        clnt = Client.objects.create(
            name = "Петров Андрей",
        )
        order = Orders.objects.create(
            address = "Иркутск",
            client = clnt,
        )

        r = self.client.get('/api/orders/')
        data = r.json()
        print(data)

        assert order.address == data[0]['address']
        assert order.id == data[0]['id']

    def test_create_order(self):
        clnt = baker.make("Client")
        orders = baker.make("Orders", client=clnt)
        r = self.client.post('/api/orders/', {
            "address": "Адрес",
            "client": clnt.id
        })

        new_order_id = r.json()['id']

        orders = Orders.objects.all()
        assert len(orders) == 2

        new_order = Orders.objects.filter(id=new_order_id).first()
        assert new_order.address == "Адрес"
        assert new_order.client == clnt

    def test_delete_client(self):
        clnt = baker.make("Client", 10)
        r = self.client.post('/api/clients/')
        data = r.json()
        assert len(data) == 10

        client_id_to_delete = clnt[3].id
        self.client.delete(f'/api/clients/{client_id_to_delete}')

        r = self.client.get('/api/clients')
        data = r.json()
        assert len(data) == 9

        assert client_id_to_delete not in [i['id'] for i in data]




