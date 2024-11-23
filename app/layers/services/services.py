# capa de servicio/lógica de negocio

from ..transport.transport import getAllImages as fetchAllImages
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = fetchAllImages(input)

    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for item in json_collection:
        if 'image' in item:  
            images.append({
                'url': item['image'],  
                'name': item['name'],  
                'status': item['status'],  
                'last_location': item['location']['name'],  
                'first_seen': item['origin']['name'] 
            })
    return images

def saveFavourite(favourite_data):
    try:
        fav = type('FavouriteObject', (object,), favourite_data)
        return repositories.saveFavourite(fav)
    except Exception as e:
        print(f"Error en saveFavourite (services.py): {e}")
        return None

# usados desde el template 'favourites.html'
def getAllFavourites(request):

    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        favourite_list = repositories.getAllFavourites(user)
        mapped_favourites = []
        for favourite in favourite_list:
            mapped_favourites.append(favourite)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId)