from django.views     import View
from django.http      import JsonResponse
from django.db.models import Avg, Count

from products.models import Product

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
