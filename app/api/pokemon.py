from flask import Blueprint
from app.models.pokemon import Pokemon
from app.utils.jsonapi import jsonapi_response, jsonapi_error
from flask import request

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/', methods=['GET'])
def get_all_pokemon():
    try:
        pokemons = Pokemon.query.all()
        if not pokemons:
            return jsonapi_error(
                message="No Pokémon found",
                error="Database is empty",
                status=404
            )
        return jsonapi_response(
            data=[format_pokemon(p) for p in pokemons],
            message="All Pokémon retrieved successfully"
        )
    except Exception as e:
        return jsonapi_error(
            message="Failed to retrieve Pokémon",
            error=str(e),
            status=500
        )

@pokemon_bp.route('/<int:id>', methods=['GET'])
def get_pokemon(id):
    try:
        pokemon = Pokemon.query.get(id)
        if not pokemon:
            return jsonapi_error(
                message="Pokémon not found",
                error=f"Pokémon with ID {id} does not exist",
                status=404
            )
        return jsonapi_response(
            data=format_pokemon(pokemon),
            message="Pokémon retrieved successfully"
        )
    except Exception as e:
        return jsonapi_error(
            message="Failed to retrieve Pokémon",
            error=str(e),
            status=500
        )

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
    try:
        # Get query parameters for pagination
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('pageSize', default=10, type=int)
        
        # Validate page and page_size
        if page < 1:
            return jsonapi_error(
                message="Invalid page number",
                error="Page must be greater than or equal to 1",
                status=400
            )
        
        if page_size < 1 or page_size > 100:
            return jsonapi_error(
                message="Invalid page size",
                error="Page size must be between 1 and 100",
                status=400
            )
        
        # Query the database with pagination
        paginated_pokemon = Pokemon.query.paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )
        
        if not paginated_pokemon.items:
            return jsonapi_error(
                message="No Pokémon found",
                error="No data available for the requested page",
                status=404
            )
        
        # Format the response
        return jsonapi_response(
            data=[format_pokemon(p) for p in paginated_pokemon.items],
            message="Pokémon retrieved successfully",
            meta={
                'page': paginated_pokemon.page,
                'pageSize': paginated_pokemon.per_page,
                'totalPages': paginated_pokemon.pages,
                'totalItems': paginated_pokemon.total
            }
        )
    except Exception as e:
        return jsonapi_error(
            message="Failed to retrieve Pokémon",
            error=str(e),
            status=500
        )