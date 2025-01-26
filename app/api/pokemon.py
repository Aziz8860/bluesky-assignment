from flask import Blueprint, jsonify, make_response
from app.models.pokemon import Pokemon
from app.utils.jsonapi import jsonapi_response, jsonapi_error

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