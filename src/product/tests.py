from django.test import TestCase, Client
from .models import Comment, Product


class TestProductList(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_list(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)


class TestProductDetail(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_view(self):
        test_product = Product.objects.create(name='test_product_name',
                                                  description='test_product_description',
                                                  price=11.11)
        # product created
        self.assertEqual(test_product.pk, 1)

        test_product_link = "/products/{}/".format(test_product.slug)
        response = self.client.get(test_product_link)
        # page received correctly
        self.assertEqual(response.status_code, 200)
