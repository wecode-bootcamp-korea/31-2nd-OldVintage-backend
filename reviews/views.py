from django.http      import HttpResponse, JsonResponse
from django.views     import View
from django.db        import transaction

from cores.storage      import file_handler
from reviews.models     import Review, Image
from users.utils        import signin_decorator

class ReviewView(View):
    @signin_decorator
    def post(self, request):
        try:
            rating     = request.POST['rating']
            content    = request.POST['content']
            product_id = request.POST['product_id']
            user       = request.user
            images     = request.FILES.getlist('images', None)
            
            if images:
                image_urls = [file_handler.upload(image) for image in images]
            
            with transaction.atomic():
                review = Review.objects.create(
                    rating     = rating,
                    content    = content,
                    product_id = product_id,
                    user       = user,
                )       
                if images:
                    for image_url in image_urls:
                        Image.objects.create(
                            image_url  = image_url,
                            review     = Review.objects.get(id = review.id)
                        )
                
            return HttpResponse(status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)