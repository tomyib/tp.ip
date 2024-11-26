# capa de vista/presentación

from app.layers.services.services import getAllImages
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import customUserCreationForms
from django.contrib.auth import authenticate, login

def index_page(request):
    return render(request, 'index.html')

def home(request):
    page = int(request.GET.get('page', 1))  # Obtener el número de página
    images = getAllImages(page=page)  # Llamar al servicio

    # Pasar datos al template
    return render(request, 'home.html', {
        'images': images,
        'favourite_list': [],  # Lista de favoritos
        'current_page': page
    })




def search(request):
    search_msg = request.GET.get('query', '')  # Obtengo el término de búsqueda desde la URL
    page = int(request.GET.get('page', 1))    # Obtengo la página actual

    if search_msg:
        try:
            images = getAllImages(input=search_msg, page=page)  # Llamada con búsqueda y paginación
        except Exception as e:
            print(f"[DEBUG] Error al buscar personajes: {e}")
            images = []

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': [],
            'current_page': page,
            'search_msg': search_msg  # Envio el término de búsqueda al template
        })
    else:
        return redirect('home')
    
def registro(request):
    data = {
        'form': customUserCreationForms()
    }

    if request.method == 'POST':
        formulario = customUserCreationForms(data=request.POST)
        if formulario.is_valid():
            # Guardo el usuario
            formulario.save()

            # Autentico al usuario
            user = authenticate(
                username=formulario.cleaned_data["username"],
                password=formulario.cleaned_data["password1"]
            )
            if user is not None:
                login(request, user)
                return redirect(to="home")
        
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)





# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    # Llamo al servicio para obtener los favoritos del usuario autenticado
    favourite_list = services.getAllFavourites(request)

    # Renderizo el template con la lista de favoritos
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