# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

def getAllImages(input=None, page=1):
    try:
        # URL según búsqueda o listado general
        if input is None:
            url = f"https://rickandmortyapi.com/api/character?page={page}"
        else:
            url = f"https://rickandmortyapi.com/api/character?name={input}&page={page}"

        print(f"[DEBUG] URL solicitada: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Validar errores HTTP
        json_response = response.json()

        if 'error' in json_response:
            print(f"[DEBUG] Error en la búsqueda: {json_response['error']}")
            return []

        return json_response.get('results', [])

    except requests.exceptions.RequestException as e:
        print(f"[transport.py]: Error al obtener datos de la API: {e}")
        return []
