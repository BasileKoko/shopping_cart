from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from model_mommy import mommy
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


@pytest.mark.django_db
class TestView(TestCase):

    def setUp(self):
        user = User(username='test', email='test@example.com')
        user.set_password('test123')
        user.save()
        self.user = User.objects.get(username='test')

        self.client = Client()
        self.client.login(username='test', password='test123')

        self.rest_client = APIClient()
        self.rest_client.login(username='test', password='test123')

    def test_user_not_authenticated(self):
        rest_client_no_credentials = APIClient()
        response = rest_client_no_credentials.get('/api/v1/items/', format='json')

        assert response.status_code == 403

    def test_user_authenticated(self):

        response = self.rest_client.get('/api/v1/items/', format='json')
        assert response.status_code == 200

    def test_endpoint_items(self):
        response = self.rest_client.get('/api/v1/items/', format='json')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_endpoint_basket_add(self):
        response = self.rest_client.get('/api/v1/basket/add/', format='json')

        assert response.status_code == 200

    def test_endpoint_basket_change(self):
        mommy.make(
            'Basket',
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
        mommy.make(
            'api.models.Trolley',
            id=3,
            user=self.user,
            items=['item1', 'item2'],
            total_price=Decimal('25.00'),
        )
        trolley = Trolley.objects.get(user=self.user)
        response = self.rest_client.get('/api/v1/trolley/change/%s' % trolley.id, format='json')

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


@pytest.mark.django_db
class TestUtilsFunction(TestCase):
    def setUp(self):
        self.user = User(username='test', email='test@example.com')
        self.user.set_password('test123')
        self.user.save()

    def test_trolley_items_not_found(self):
        result = trolley_items(self.user)

        assert len(result) == 0

    def test_trolley_items_found(self):
        mommy.make(
            'api.Trolley',
            user=self.user,
            items=[1, 2],
            total_price=Decimal('25.00'),
        )
        result = trolley_items(self.user)

        assert len(result) == 1

    def test_delete_trolley_items_case_trolley_not_deleted(self):
        mommy.make(
            'api.Trolley',
            user=self.user,
            items=[1, 2],
            total_price=Decimal('25.00'),
        )
        delete_trolley_items(self.user, 'incomplete', Decimal('0'))
        result = Trolley.objects.filter(user=self.user)

        assert len(result) == 1

    def test_delete_trolley_items_case_trolley_deleted(self):
        mommy.make(
            'api.Trolley',
            user=self.user,
            items=[1, 2],
            total_price=Decimal('25.00'),
        )
        delete_trolley_items(self.user, 'complete', Decimal('25.00'))
        result = Trolley.objects.filter(user=self.user).first().items

        assert len(result) == 0

    def test_calculate_total_price_item_found(self):
        mommy.make(
            'api.Trolley',
            user=self.user,
            items=[1, 2, 3],
        )
        result = calculate_trolley_total_price([1, 2, 3])
        assert result == Decimal('162.46')

    def test_calculate_total_price_item_not_found(self):
        result = calculate_trolley_total_price([15])

        assert result == Decimal()
