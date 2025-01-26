from flask import Blueprint
from app.models.pokemon import Pokemon
from app.utils.jsonapi import jsonapi_response, jsonapi_error
from flask import request

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/', methods=['GET'])
def get_all_pokemon():
    pokemons = Pokemon.query.all()
    return jsonapi_response(
        data=[format_pokemon(p) for p in pokemons],
        status=200
    )

@pokemon_bp.route('/<int:id>', methods=['GET'])
def get_pokemon(id):
    pokemon = Pokemon.query.get(id)
    if not pokemon:
        return jsonapi_error(
            status=404,
            title="Not Found",
            detail=f"Pokémon with ID {id} not found"
        ), 404
    return jsonapi_response(data=format_pokemon(pokemon))

def format_pokemon(pokemon):
    return {
        'type': 'pokemon',
        'id': str(pokemon.id),
        'attributes': {
            'name': pokemon.name,
            'height': pokemon.height,
            'weight': pokemon.weight,
            'types': pokemon.types,
            'abilities': pokemon.abilities,
            'sprite_url': pokemon.sprite_url
        }
    }

@pokemon_bp.route('/paginated', methods=['GET'])
def get_paginated_pokemon():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('pageSize', default=10, type=int)
    
    if page < 1:
        return jsonapi_error(
            status=400,
            title="Bad Request",
            detail="Page must be greater than or equal to 1"
        ), 400
    
    if page_size < 1 or page_size > 100:
        return jsonapi_error(
            status=400,
            title="Bad Request",
            detail="Page size must be between 1 and 100"
        ), 400
    
    paginated_pokemon = Pokemon.query.paginate(
        page=page,
        per_page=page_size,
        error_out=False
    )
    
    return jsonapi_response(
        data=[format_pokemon(p) for p in paginated_pokemon.items],
        meta={
            'page': paginated_pokemon.page,
            'pageSize': paginated_pokemon.per_page,
            'totalPages': paginated_pokemon.pages,
            'totalItems': paginated_pokemon.total
        },
        status=200
    )