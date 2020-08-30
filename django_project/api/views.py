from django.shortcuts import render, HttpResponse,HttpResponseRedirect,HttpResponsePermanentRedirect
from django.views.decorators.csrf import csrf_exempt

import random, string
from .utils import *
from .models import URLToUniqueCode

# Create your views here.


@csrf_exempt
def generate_shorten(request):
    
    return_msg = ''

    base_url = 'http://' + request.get_host() + '/'

    url: str = request.POST['url']
    url = ''.join(url.split())

    if not url:
        return_msg = 'url cannot be empty'
        response = HttpResponse(return_msg)
    elif not url.startswith(('http://', 'https://')):
        return_msg = 'Invalid URLs, supported value should be started with http:// or https://'
        response = HttpResponse(return_msg)
    else:
        now = datetime.datetime.now()
        try:
            # already exist
            o = URLToUniqueCode.objects.get(url=url)
            return_msg = "Already converted to " + base_url + o.unique_code
            response = HttpResponse(return_msg)
        except URLToUniqueCode.DoesNotExist:
            # Generate a random unique code
            chars = string.ascii_lowercase + string.ascii_uppercase + string.digits;
            unique_code = ''
            for _ in range(6):
                unique_code += random.choice(chars)

            while True:
                try:
                    o = URLToUniqueCode.objects.get(unique_code=unique_code)
                except URLToUniqueCode.DoesNotExist:
                    o = URLToUniqueCode(url=url, unique_code=unique_code,
                                creation_time=now)
                    o.save()
                    break

            return_msg = base_url + unique_code

            #return render(request, 'result.html', results)
            response = HttpResponse(return_msg)
            #response.__setitem__('Location', url)
            #response.status_code = 301
    
    return response
    

def redirect(request, unique_code):
    base_url = 'http://' + request.get_host() + '/'
    try:
        o = URLToUniqueCode.objects.get(unique_code=unique_code)
        return HttpResponsePermanentRedirect(o.url)
    except URLToUniqueCode.DoesNotExist:
        return HttpResponse(base_url + unique_code + ' does not exist!!!')

@csrf_exempt
def main_page(request):
    return render(request, 'index.html')

