import click
import requests
import time
from app import db
from app.models.pokemon import Pokemon

@click.command("scrape")
@click.option('--limit', default=50, type=int, help='Maximum number of Pokémon to scrape (default: 50)')
def scrape_cli(limit):
    """Scrape Pokémon data into the database"""
    print(f"Starting Pokémon scrape (limit: {'all' if not limit else limit})...")
    
    id = 1
    count = 0
    while True:
        if limit and count >= limit:
            break
            
        url = f'https://pokeapi.co/api/v2/pokemon/{id}'
        response = requests.get(url)
        
        if response.status_code == 404:
            print("Reached end of Pokémon list")
            break
            
        if response.status_code != 200:
            print(f"Error fetching Pokémon {id}: {response.status_code}")
            id += 1
            continue
            
        data = response.json()
        pokemon = {
            'id': data['id'],
            'name': data['name'],
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'] for t in data['types']],
            'abilities': [a['ability']['name'] for a in data['abilities']],
            'sprite_url': data['sprites']['front_default']
        }
        
        if not Pokemon.query.get(pokemon['id']):
            db.session.add(Pokemon(**pokemon))
            print(f"Added {pokemon['name']}")
            count += 1
        
        id += 1
        time.sleep(0.2)
        
        if id % 20 == 0:
            db.session.commit()
    
    db.session.commit()
    print(f"Scraping complete! Added {count} Pokémon")