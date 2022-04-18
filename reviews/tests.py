import jwt

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock                  import MagicMock, patch

from products.models     import Country, Winery, Type, Grape, Product, Pairing, ProductPairing
from users.models        import User
from oldvintage.settings import SECRET_KEY, ALGORITHM

class ReviewViewTest(TestCase):
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
        
        self.token = jwt.encode({'id' :User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        Country.objects.all().delete()
        Winery.objects.all().delete()
        Type.objects.all().delete()
        Product.objects.all().delete()
        Pairing.objects.all().delete()
        ProductPairing.objects.all().delete()
        User.objects.all().delete()
    
    @patch('cores.storage.boto3.client')
    def test_review_post_success(self, mocked_s3):
        client = Client()
        header = {'HTTP_Authorization' : self.token}
        
        images = SimpleUploadedFile(
            name         = 'test1.jpg',
            content      = b'file_content',
            content_type = 'image/jpg',
        )
        
        data = {
            'product_id': 1,
            'rating'    : 5,
            'content'   : '1번 콘텐츠',
            'images'    : [images]
        }
        
        class MockedResponse:
            def upload(self):
                return None    
                
        mocked_s3.upload = MagicMock(return_value=MockedResponse())
        response         = client.post('/reviews/1', data, content_type='multipart/form-data', **header)
        self.assertEqual(response.status_code, 201)