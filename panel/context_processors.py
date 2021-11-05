from .models import Catagory, Brand

def cat_links(request):
    links = Catagory.objects.all()
    return dict(links=links)

def brand_links(request):
    links1 = Brand.objects.all()
    return dict(links1=links1)