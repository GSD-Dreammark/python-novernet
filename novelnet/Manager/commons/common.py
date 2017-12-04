from os import path
from django.http import HttpResponse
def show_image(request):
    imgurl=request.GET['imgurl']
    d=path.dirname(__file__)
    imgpath=path.join(d,'../static/imgs/',imgurl)
    img_data=open(imgpath,'rb')
    return HttpResponse(img_data,content_type="image/png")