from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg, Count, Q

from products.models import Product
from reviews.models  import Review

class ProductListView(View):
    def get(self,request):
        offset = int(request.GET.get('offset' , 0))
        limit  = int(request.GET.get('limit' , 100))
        order  = request.GET.get('order', None)
                
        sorting = {
            'rating'    : '-rating_score',
            'popular'   : '-rating_count',
            'high_price': '-price',
            'low_price' : 'price'
        }

        filter_getlist_set = {
            'country_id': 'winery_id__country_id__in',
            'winery_id' : 'winery_id__in',
            'grape_id'  : 'grape_id__in',
            'type_id'   : 'type_id__in',
            'pairing_id': 'pairings__id__in',
        }
        
        filter_get_set = {
            'min_price': 'price__gte',
            'max_price': 'price__lte',
            'rating'   : 'rating_score__gte'
        }
        
        query = {**{filter_getlist_set[key] : value for key, value in dict(request.GET).items()
                if filter_getlist_set.get(key)},
                **{filter_get_set[key] : value for key, value in request.GET.items()
                if filter_get_set.get(key)}
        }
        
        filter_products = Product.objects.select_related('winery__country', 'grape', 'type')\
        .prefetch_related('productpairings__pairing', 'reviews__user')\
        .annotate(
        rating_score = Avg('reviews__rating'),
        rating_count = Count('reviews__rating')
        ).filter(**query).order_by(sorting.get(order, '-rating_score'))
        
        products = filter_products[offset:offset+limit]
        length   = filter_products.count()

        result = [{
            'id'       : product.id,
            'name'     : product.name,
            'price'    : product.price,
            'grape': {
                'id'  : product.grape.id,
                'name': product.grape.name
            },
            'bold'     : product.bold,
            'tannic'   : product.tannic,
            'sweet'    : product.sweet,
            'acidic'   : product.acidic,
            'country'  : {
                'id'  : product.winery.country.id,
                'name': product.winery.country.name
            },
            'winery'   : {
                'id'  : product.winery.id,
                'name': product.winery.name
            },
            'type'     : {
                'id'  : product.type.id,
                'name': product.type.name
            },
            'image_url': product.image_url,
            'pairing'  : [productpairing.pairing.name for productpairing in product.productpairings.all()],
            'review'   : {
                'rating_count': product.rating_count,
                'rating_score': round(product.rating_score, 2)
            }
        }for product in products]

        return JsonResponse({'result' : result, 'length' : length}, status=200)

class ProductReviewView(View):
    def get(self,request, product_id):
        offset  = int(request.GET.get('offset' , 0))
        limit   = int(request.GET.get('limit' , 20))
        rating  = request.GET.getlist('rating', [1,2,3,4,5])
        
        reviews = Review.objects.select_related('product', 'user')\
        .prefetch_related('images')\
        .filter(
            product_id = product_id,
            rating__in = rating
        ).order_by('-created_at')[offset:offset+limit]
                
        result = {
            'review' : [{
                'id'         : review.id,
                'user'       : review.user.name,
                'product_id' : review.product_id,
                'rating'     : review.rating,
                'content'    : review.content,
                'created_at' : str(review.created_at)[:10],
                'image_url'  : [image.image_url for image in review.images.all()]
            }for review in reviews]
        }
        
        return JsonResponse({'result' : result}, status=200)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.annotate(
                rating_score = Avg('reviews__rating'),
                rating_count = Count('reviews__rating'),
                score_one    = Count('reviews__rating', filter=Q(reviews__rating__exact =1)),
                score_two    = Count('reviews__rating', filter=Q(reviews__rating__exact =2)),
                score_three  = Count('reviews__rating', filter=Q(reviews__rating__exact =3)),
                score_four   = Count('reviews__rating', filter=Q(reviews__rating__exact =4)),
                score_five   = Count('reviews__rating', filter=Q(reviews__rating__exact =5))
                ).get(id=product_id)
        
            winery      = product.winery
            winery_info = Review.objects.filter(product__winery = winery)\
                .aggregate(rating = Avg('rating'))
            
            product_detail = {
                'product':{
                    'name'        : product.name,
                    'price'       : product.price,
                    'rating'      : round(product.rating_score, 2),
                    'rating_count': product.rating_count,
                    'scores'       : {
                        'one'  : product.score_one,
                        'two'  : product.score_two,
                        'three': product.score_three,
                        'four' : product.score_four,
                        'five' : product.score_five
                    },
                    'image'       : product.image_url,
                    'type'        : product.type.name,
                    'grape'       : product.grape.name,
                    'bold'        : product.bold,
                    'tannic'      : product.tannic,
                    'sweet'       : product.sweet,
                    'acidic'      : product.acidic,
                    'pairings'    : [{pairing.name : pairing.image_url} for pairing in product.pairings.all()]
                },
                'winery':{
                'name'       : winery.name,
                'address'    : winery.address,
                'latitude'   : winery.latitude,
                'longitude'  : winery.longitude,
                'description': winery.description,
                'rating'     : round(winery_info['rating'],2),
                'quantity'   : Product.objects.filter(winery=winery).count(),
                'country'    : winery.country.name
                }            
            }
            
            return JsonResponse({'product_detail' : product_detail}, status = 200)
    
        except Product.DoesNotExist:
            return JsonResponse({'message': 'NO_PRODUCT'}, status=404)
        
class SearchView(View):
    def get(self,request):
        offset = int(request.GET.get('offset' , 0))
        limit  = int(request.GET.get('limit' , 6))
        name   = request.GET.get('name', None)
        
        products = Product.objects.filter(name__icontains = name)[offset:offset+limit]

        result = [{
            'id'       : product.id,
            'name'     : product.name,
            'price'    : product.price,
            'bold'     : product.bold,
            'tannic'   : product.tannic,
            'sweet'    : product.sweet,
            'acidic'   : product.acidic,
            'image_url': product.image_url,
        }for product in products]

        return JsonResponse({'result' : result}, status=200)
