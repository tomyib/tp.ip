# capa de vista/presentación

from app.layers.services.services import getAllImages
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
#def index(request):
#    images = getAllImages()
#    paginator= Paginator(images, 2)
#    pagina = request.GET.get("page") or 1
#    posts= paginator.get_page(pagina)
#    return render(request, "home.html", {"posts": posts})
    
def home(request):
    images = getAllImages()
    favourite_list = []

    return render(request, 'home.html', { 'images': images,'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')
    
    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        try:
            images = getAllImages(search_msg)
        except Exception as e:
            images = []
            print(f"Error al obtener imágenes: {e}")

        context = {
                'search_msg': search_msg,
                'images': images,
            }

        return render(request, 'home.html', context)
    else:  
        return redirect('home')



# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Llamamos al servicio para obtener los favoritos del usuario autenticado
    favourite_list = services.getAllFavourites(request)

    # Renderizamos el template con la lista de favoritos
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        try:
            favourite_data = {
                'url': request.POST.get('url'),
                'name': request.POST.get('name'),
                'status': request.POST.get('status'),
                'last_location': request.POST.get('last_location'),
                'first_seen': request.POST.get('first_seen'),
                'user': request.user
            }

            result = services.saveFavourite(favourite_data)

            if not result:
                pass
        except Exception as e:
            pass

    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        success = services.deleteFavourite(request)

    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect("home")