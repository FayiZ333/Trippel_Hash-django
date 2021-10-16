from .models import Catagory

def cat_links(request):
    links = Catagory.objects.all()
    return dict(links=links)