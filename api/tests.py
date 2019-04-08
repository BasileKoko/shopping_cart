from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework.test import APIClient

from api.models import (
    Item,
    Basket,
    Trolley,
)
from api.utils import (
    trolley_items,
    delete_trolley_items,
    calculate_trolley_total_price,
)


class AuthenticatedUserTest(TestCase):

    def setUp(self):
        user = User(username='test', email='test@example.com')
        user.set_password('test123')
        user.save()

        self.client = Client()
        self.client.login(username=user.username, password=user.password)

        self.rest_client = APIClient()
        self.rest_client.login(username=user.username, password=user.password)

    def test_user_not_authenticated(self):
        rest_client_no_credentials = APIClient()
        response = rest_client_no_credentials.get('/api/v1/items/', format='json')

        self.assertEquals(response.status_code, 401)

    def test_endpoint_items(self):
        response = self.rest_client.get('/api/v1/items/', format='json')
        Item.objects.create(
            id=1,
            user=self.user,
            price=Decimal('10.35'),
            discounted=False,
        )

        expected_json = [
            {
                "id": 1,
                "price": Decimal('10.35'),
                "discounted": False,
            }
        ]

        self.assertEqual(response.data, expected_json)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_basket_add(self):
        response = self.rest_client.get('/api/v1/basket/add/', format='json')

        self.assertEqual(response.status_code, 200)

    def test_endpoint_basket_change(self):
        Basket.objects.create(
            id=1,
            user=self.user,
            items=['item1', 'item2'],
            discounted=False,
        )
        response = self.rest_client.get('/api/v1/basket/change/1', format='json')

        expected_json = [
            {
                "items": ['item1', 'item2'],
            }
        ]

        self.assertEqual(response.data, expected_json)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_basket_change_not_found(self):
        response = self.rest_client.get('/api/v1/basket/change/2', format='json')

        expected_json = [
            {
                "items": ['item1', 'item2'],
            }
        ]

        self.assertNotEqual(response.data, expected_json)
        self.assertEqual(response.status_code, 404)

    def test_endpoint_trolley_add(self):
        response = self.rest_client.get('/api/v1/trolley/add/', format='json')

        self.assertEqual(response.status_code, 200)

    def test_endpoint_trolley_change(self):
        Trolley.objects.create(
            id=1,
            user=self.user,
            items=['item1', 'item2'],
            total_price=Decimal('25.00'),
        )
        response = self.rest_client.get('/api/v1/trolley/change/1', format='json')

        expected_json = [
            {
                "items": ['item1', 'item2'],
                "total_price": Decimal('25.00'),
            }
        ]

        self.assertEqual(response.data, expected_json)
        self.assertEqual(response.status_code, 200)

    def test_endpoint_trolley_change_not_found(self):
        response = self.rest_client.get('/api/v1/trolley/change/2', format='json')
        expected_json = [
            {
                "items": ['item1', 'item2'],
                "total_price": Decimal('25.00'),
            }
        ]

        self.assertNotEqual(response.data, expected_json)
        self.assertEqual(response.status_code, 404)


class UtilsFunctionTest(TestCase):
    def setUp(self):
        user = User(username='test', email='test@example.com')
        user.set_password('test123')
        user.save()

    def test_trolley_items_not_found(self):
        result = trolley_items(self.user)

        self.assertEqual(len(result), 0)

    def test_trolley_items_found(self):
        Trolley.objects.create(
            id=1,
            user=self.user,
            items=['item1', 'item2'],
            total_price=Decimal('25.00'),
        )
        result = trolley_items(self.user)

        self.assertEqual(len(result), 1)

    def test_delete_trolley_items_case_1(self):
        Trolley.objects.create(
            id=1,
            user=self.user,
            items=['item1', 'item2'],
            total_price=Decimal('25.00'),
        )
        delete_trolley_items(self.user, 'incomplete', Decimal('0'))
        result = Trolley.objects.get(user=self.user)

        self.assertEqual(len(result), 1)

    def test_delete_trolley_items_case_2(self):
        Trolley.objects.create(
            id=1,
            user=self.user,
            items=['item1', 'item2'],
            total_price=Decimal('25.00'),
        )
        delete_trolley_items(self.user, 'complete', Decimal('10'))
        result = Trolley.objects.get(user=self.user)

        self.assertEqual(len(result), 0)

    def test_calculate_total_price_item_found(self):
        Item.objects.create(
            id=1,
            user=self.user,
            price=Decimal('10.35'),
            discounted=False,
        )
        result = calculate_trolley_total_price([1])
        self.assertEqual(result, Decimal('10.35'))

    def test_calculate_total_price_item_not_found(self):
        result = calculate_trolley_total_price([2])

        self.assertEqual(result, Decimal())
