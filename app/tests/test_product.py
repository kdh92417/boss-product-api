import random

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Product
from app.tests.helper import create_fake_user, create_product_list, create_product, fake


class ProductTests(APITestCase):
    def setUp(self):
        pass

    def test_success_create_product_by_user(self):
        create_product_user, create_product_user_password = create_fake_user()

        product_data = {
            "category": "food",
            "barcode": "faefa2414124",
            "price": 3000,
            "cost": 1000,
            "name": "신선만두",
            "description": "만두",
            "size": "small",
            "expiration_date": "2024-12-30",
            "user": create_product_user.id,
        }

        self.client.force_authenticate(user=create_product_user)

        resp = self.client.post(
            reverse("product-list"), HTTP_ACCEPT="application/json", data=product_data
        )
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        resp_json = resp.json()
        resp_json_data = resp_json["data"]

        self.assertIsNotNone(resp_json_data)
        self.assertEqual(resp_json_data["user"], create_product_user.id)
        self.assertEqual(resp_json_data["name"], product_data["name"])

    def test_fail_create_product_by_anonymous_user(self):
        create_product_user, create_product_user_password = create_fake_user()

        product_data = {
            "category": "food",
            "barcode": "faefa2414124",
            "price": 3000,
            "cost": 1000,
            "name": "신선만두",
            "description": "만두",
            "size": "small",
            "expiration_date": "2024-12-30",
            "user": create_product_user.id,
        }

        resp = self.client.post(
            reverse("product-list"), HTTP_ACCEPT="application/json", data=product_data
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)

    def test_success_get_product_list(self):
        user, user_password = create_fake_user()

        user_product_count = random.randint(11, 20)
        create_product_list(n=user_product_count, user=user)
        create_product_list(n=5)

        self.client.force_authenticate(user=user)
        resp = self.client.get(reverse("product-list"), HTTP_ACCEPT="application/json")
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        resp_json = resp.json()
        resp_json_data = resp_json["data"]

        self.assertIsNotNone(resp_json_data)
        self.assertEqual(user_product_count, resp_json_data["count"])

    def test_success_get_product(self):
        user, user_password = create_fake_user()
        user_product_count = random.randint(3, 10)
        user_products = create_product_list(n=user_product_count, user=user)
        random_product: Product = random.choice(user_products)

        self.client.force_authenticate(user=user)
        resp = self.client.get(
            reverse(
                "product-detail",
                kwargs={
                    "pk": random_product.id,
                },
            ),
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        resp_json = resp.json()
        resp_json_data = resp_json["data"]

        self.assertIsNotNone(resp_json_data)
        self.assertEqual(random_product.id, resp_json_data["id"])

    def test_success_patch_product(self):
        user, user_password = create_fake_user()
        user_product = create_product(user=user)

        patch_data = {
            "name": fake.name(),
            "barcode": fake.ssn(),
            "price": random.randint(1, 100) * 1000,
            "cost": random.randint(1, 100) * 1000,
        }

        self.client.force_authenticate(user=user)
        resp = self.client.patch(
            reverse(
                "product-detail",
                kwargs={
                    "pk": user_product.id,
                },
            ),
            HTTP_ACCEPT="application/json",
            data=patch_data,
        )

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        resp_json = resp.json()
        resp_json_data = resp_json["data"]

        self.assertIsNotNone(resp_json_data)

        user_product.refresh_from_db()
        self.assertEqual(patch_data["name"], user_product.name)
        self.assertEqual(patch_data["barcode"], user_product.barcode)
        self.assertEqual(patch_data["price"], user_product.price)
        self.assertEqual(patch_data["cost"], user_product.cost)

    def test_delete_product(self):
        user, user_password = create_fake_user()
        user_product = create_product(user=user)

        self.client.force_authenticate(user=user)
        resp = self.client.delete(
            reverse(
                "product-detail",
                kwargs={
                    "pk": user_product.id,
                },
            ),
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, resp.status_code)
        self.assertIsNone(Product.objects.filter(id=user_product.id).first())

    def test_search_product_by_name(self):
        user, user_password = create_fake_user()
        product = create_product(name="슈크림 라떼", user=user)

        correctly_search_param = ["슈크림", "크림", "ㄹㄸ", "ㅅㅋㄹ", "ㄹㄸ"]
        incorrectly_search_param = ["잘못된"]
        random_search = random.choice(correctly_search_param + incorrectly_search_param)
        search_param = {"search": random_search}

        self.client.force_authenticate(user=user)
        resp = self.client.get(
            reverse("product-list"), HTTP_ACCEPT="application/json", data=search_param
        )
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        resp_json = resp.json()
        resp_json_data = resp_json["data"]

        self.assertIsNotNone(resp_json_data)
        if search_param["search"] in incorrectly_search_param:
            self.assertEqual(resp_json_data["count"], 0)
        else:
            self.assertEqual(resp_json_data["count"], 1)
