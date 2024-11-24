from ..transport.transport import getAllImages as fetchAllImages
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None, page=1):
    json_collection = fetchAllImages(input=input, page=page)
    print(f"[DEBUG] Resultados obtenidos para la página {page}: {len(json_collection)} personajes")  # Log para depurar
    images = []
    for item in json_collection:
        images.append({
            'url': item.get('image'),
            'name': item.get('name'),
            'status': item.get('status'),
            'last_location': item.get('location', {}).get('name'),
            'first_seen': item.get('origin', {}).get('name')  # Primer episodio
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
        mapped_favourites = [favourite for favourite in favourite_list]
        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId)
