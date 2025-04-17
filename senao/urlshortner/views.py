# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from urlshortner.models import UrlData
from urlshortner.serializer import UrlDataSerializer
from urlshortner.ratelimit import check_rate_limit

from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django_redis import get_redis_connection
import hashlib
import datetime

def redirect_origin(request, hash):
    try:
        
        if not check_rate_limit(hash):
            return JsonResponse({
                "success": False,
                "reason": "ratelimited",
            }, status=429)

        r = get_redis_connection("default")
        origin_url = r.get(hash)
        
        if not origin_url:
            return JsonResponse({
                "success": False,
                "reason": "short url invalid",
            }, status=404)
        
        return redirect(origin_url.decode("utf-8"))

    except Exception as e:
        return JsonResponse({
            "success": False,
            "reason": str(e),
        })

@api_view(['POST'])
def create_shorturl(request):
    if 'origin_url' in request.data:
        origin_url = request.data['origin_url']
        if len(origin_url) > 2048:
            return JsonResponse({
                "success": False,
                "reason": "URL too long",
            })
       
        
        try:    

            hash = hashlib.md5(origin_url.encode()).hexdigest()[:10]
            expire_at = datetime.datetime.now() + datetime.timedelta(days=30)

            url_existed = UrlData.objects.filter(hash=hash)
            if url_existed.exists(): # update exist expiration when re-create this shorturl
                url_existed.update(expire_at=expire_at)
            else:
                url = UrlData.objects.create(
                    origin_url = origin_url,
                    hash=hash,
                    expire_at=expire_at
                )
            
            r = get_redis_connection("default")
            r.setex(hash, 30*24*3600, origin_url) # expire after 30 days

            if request.is_secure():
                protocol = "https"
            else:
                protocol = "http"

            return JsonResponse({
                "short_url": f'{protocol}://{request.get_host()}/url/{hash}',
                "expiration_date": expire_at,
                "success": True,
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                "success": False,
                "reason": str(e),
            })

    return JsonResponse({
                "success": False,
                "reason": "missing origin_url",
            })

@api_view(['GET'])
def get_urldata(request, hash):
    try:
        url = UrlData.objects.get(hash=hash)
        serializer = UrlDataSerializer(url)
        return Response(serializer.data)

    except UrlData.DoesNotExist:
        return HttpResponseNotFound("error hash not found")