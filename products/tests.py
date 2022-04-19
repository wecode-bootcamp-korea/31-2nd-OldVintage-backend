from django.test     import TestCase, Client

from products.models import Country, Winery, Type, Grape, Product, Pairing, ProductPairing
from reviews.models  import Review
from users.models    import User

class ProductListViewTest(TestCase):
    def setUp(self):
        Country.objects.bulk_create([
            Country(id = 1, name = '1번 나라'),
            Country(id = 2, name = '2번 나라')
        ])
        
        Winery.objects.bulk_create([
            Winery(
                id          = 1,
                name        = '1번 양조장',
                address     = '1번 주소',
                latitude    = 1,
                longitude   = 1,
                description = '1번 내용',
                country_id  = 1
            ),
            Winery(
                id          = 2,
                name        = '2번 양조장',
                address     = '2번 주소',
                latitude    = 2,
                longitude   = 2,
                description = '2번 내용',
                country_id  = 2
            )
        ])
        
        Type.objects.bulk_create([
            Type(id = 1, name = '1번 타입'),
            Type(id = 2, name = '2번 타입')
        ])
        
        Grape.objects.bulk_create([
            Grape(id = 1, name = '1번 품종'),
            Grape(id = 2, name = '2번 품종')
        ])
        
        Product.objects.bulk_create([
            Product(
                id        = 1,
                name      = '1번 상품',
                price     = 10000,
                grape_id  = 1,
                bold      = 0.1,
                tannic    = 0.1,
                sweet     = 0.1,
                acidic    = 0.1,
                type_id   = 1,
                winery_id = 1,
                image_url = '1.jpg'
            ),
            Product(
                id        = 2,
                name      = '2번 상품',
                price     = 20000,
                grape_id  = 2,
                bold      = 0.2,
                tannic    = 0.2,
                sweet     = 0.2,
                acidic    = 0.2,
                type_id   = 2,
                winery_id = 2,
                image_url = '2.jpg'
            ),
        ])
        
        Pairing.objects.bulk_create([
            Pairing(id = 1, name = '1번 페어링', image_url = '1.jpg'),
            Pairing(id = 2, name = '2번 페어링', image_url = '2.jpg')
        ])
        
        ProductPairing.objects.bulk_create([
            ProductPairing(id = 1, pairing_id = 1, product_id = 1),
            ProductPairing(id = 2, pairing_id = 2, product_id = 2)
        ])
        
        User.objects.bulk_create([
            User(id = 1, email = 'user1@gmail.com', name = 'user1', kakao_id = 1111111111),
            User(id = 2, email = 'user2@gmail.com', name = 'user2', kakao_id = 2222222222)
        ])
        
        Review.objects.bulk_create([
            Review(id = 1, rating = 5,content = '1번 콘텐츠', product_id = 1, user_id = 1),
            Review(id = 2, rating = 4,content = '2번 콘텐츠', product_id = 2, user_id = 2),
        ])
    
    def tearDown(self):
        Country.objects.all().delete()
        Winery.objects.all().delete()
        Type.objects.all().delete()
        Product.objects.all().delete()
        Pairing.objects.all().delete()
        ProductPairing.objects.all().delete()
        User.objects.all().delete()
        Review.objects.all().delete()

    def test_success_product_list_view_get(self):
        client = Client()
        response = client.get('/products')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result": [
                {
                    "id": 1,
                    "name": "1번 상품",
                    "price": "10000.00",
                    "grape": {
                        "id": 1,
                        "name": "1번 품종"
                    },
                    "bold": "0.10",
                    "tannic": "0.10",
                    "sweet": "0.10",
                    "acidic": "0.10",
                    "country": {
                        "id": 1,
                        "name": "1번 나라"
                    },
                    "winery": {
                        "id": 1,
                        "name": "1번 양조장"
                    },
                    "type": {
                        "id": 1,
                        "name": "1번 타입"
                    },
                    "image_url": "1.jpg",
                    "pairing": [
                        "1번 페어링",
                    ],
                    "review": {
                        "rating_count": 1,
                        "rating_score": 5
                    }
                },
                {
                    "id": 2,
                    "name": "2번 상품",
                    "price": "20000.00",
                    "grape": {
                        "id": 2,
                        "name": "2번 품종"
                    },
                    "bold": "0.20",
                    "tannic": "0.20",
                    "sweet": "0.20",
                    "acidic": "0.20",
                    "country": {
                        "id": 2,
                        "name": "2번 나라"
                    },
                    "winery": {
                        "id": 2,
                        "name": "2번 양조장"
                    },
                    "type": {
                        "id": 2,
                        "name": "2번 타입"
                    },
                    "image_url": "2.jpg",
                    "pairing": [
                        "2번 페어링",
                    ],
                    "review": {
                        "rating_count": 1,
                        "rating_score": 4
                    }
                }
            ],
            "length": 2
        })

    def test_fail_filter_product_list_view_get(self):
        client = Client()
        response = client.get('/products', {'winery_id' : 10})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result": [],
            "length": 0
        })
        
    def test_success_filter_product_list_view_get(self):
        client = Client()
        response = client.get('/products', {'winery_id' : 1, 'type_id' : 1, 'rating' : 4.5})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result": [
                {
                    "id": 1,
                    "name": "1번 상품",
                    "price": "10000.00",
                    "grape": {
                        "id": 1,
                        "name": "1번 품종"
                    },
                    "bold": "0.10",
                    "tannic": "0.10",
                    "sweet": "0.10",
                    "acidic": "0.10",
                    "country": {
                        "id": 1,
                        "name": "1번 나라"
                    },
                    "winery": {
                        "id": 1,
                        "name": "1번 양조장"
                    },
                    "type": {
                        "id": 1,
                        "name": "1번 타입"
                    },
                    "image_url": "1.jpg",
                    "pairing": [
                        "1번 페어링",
                    ],
                    "review": {
                        "rating_count": 1,
                        "rating_score": 5
                    }
                }
            ],
            "length": 1
        })

class ProductReviewViewTest(TestCase):
    def setUp(self):
        Country.objects.bulk_create([
            Country(id = 1, name = '1번 나라'),
            Country(id = 2, name = '2번 나라')
        ])
        
        Winery.objects.bulk_create([
            Winery(
                id          = 1,
                name        = '1번 양조장',
                address     = '1번 주소',
                latitude    = 1,
                longitude   = 1,
                description = '1번 내용',
                country_id  = 1
            ),
            Winery(
                id          = 2,
                name        = '2번 양조장',
                address     = '2번 주소',
                latitude    = 2,
                longitude   = 2,
                description = '2번 내용',
                country_id  = 2
            )
        ])
        
        Type.objects.bulk_create([
            Type(id = 1, name = '1번 타입'),
            Type(id = 2, name = '2번 타입')
        ])
        
        Grape.objects.bulk_create([
            Grape(id = 1, name = '1번 품종'),
            Grape(id = 2, name = '2번 품종')
        ])
        
        Product.objects.bulk_create([
            Product(
                id        = 1,
                name      = '1번 상품',
                price     = 10000,
                grape_id  = 1,
                bold      = 0.1,
                tannic    = 0.1,
                sweet     = 0.1,
                acidic    = 0.1,
                type_id   = 1,
                winery_id = 1,
                image_url = '1.jpg'
            ),
            Product(
                id        = 2,
                name      = '2번 상품',
                price     = 20000,
                grape_id  = 2,
                bold      = 0.2,
                tannic    = 0.2,
                sweet     = 0.2,
                acidic    = 0.2,
                type_id   = 2,
                winery_id = 2,
                image_url = '2.jpg'
            ),
        ])
        
        Pairing.objects.bulk_create([
            Pairing(id = 1, name = '1번 페어링', image_url = '1.jpg'),
            Pairing(id = 2, name = '2번 페어링', image_url = '2.jpg')
        ])
        
        ProductPairing.objects.bulk_create([
            ProductPairing(id = 1, pairing_id = 1, product_id = 1),
            ProductPairing(id = 2, pairing_id = 2, product_id = 2)
        ])
        
        User.objects.bulk_create([
            User(id = 1, email = 'user1@gmail.com', name = 'user1', kakao_id = 1111111111),
            User(id = 2, email = 'user2@gmail.com', name = 'user2', kakao_id = 2222222222)
        ])
        
        Review.objects.bulk_create([
            Review(id = 1, rating = 5,content = '1번 콘텐츠', product_id = 1, user_id = 1),
            Review(id = 2, rating = 4,content = '2번 콘텐츠', product_id = 2, user_id = 2),
        ])
    
    def tearDown(self):
        Country.objects.all().delete()
        Winery.objects.all().delete()
        Type.objects.all().delete()
        Product.objects.all().delete()
        Pairing.objects.all().delete()
        ProductPairing.objects.all().delete()
        User.objects.all().delete()
        Review.objects.all().delete()

    def test_success_product_review_view_get(self):
        client = Client()
        response = client.get('/products/1/reviews')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
            "result": {
                "review": [
                    {
                        "id": 1,
                        "user": "user1",
                        "product_id": 1,
                        "rating": 5,
                        "content": "1번 콘텐츠",
                        "created_at": "2022-04-19",
                        "image_url": []
                    }
                ]
            }
        })