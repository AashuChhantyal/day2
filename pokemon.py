import requests

def get_pokemon_data(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Pokemon '{pokemon_name}' not found. Please check the name and try again.")
        return None

def display_pokemon_info(data):
    if data:
        print(f"\nName: {data['name'].capitalize()}")
        print(f"Sprite: {data['sprites']['font_default']}")
        if data['sprites'].get('other', {}).get('official-artwork', {}.get('font_default')):
            print(f"Official Artwork: {data['sprites']['other']['official-artwork']['font_default']}")
        print("Types:", ", ".join(t['type']['name'] for t in data['types']))
        print("Abilities:", ", ".join(a['ability']['name'] for a in data['abilities']))

        print("\nStats:")
        total_stats = 0
        for stat in data['stats']:
            print(f" - {stat['stat']['name']}: {stat['base_stat']}")
            total_stats += stat['base_stat']
        print(f"Total Stats: {total_stats}")
        return total_stats
    return 0

def compare_pokemons(pokemon1, pokemon2):
    data1 = get_pokemon_data(pokemon1)
    data2 = get_pokemon_data(pokemon2)

    if data1 and data2:
        print("\n============================================")
        print(f"⚔️ Comparing {pokemon1.capitalize()} vs {pokemon2.capitalize()}")
        print("\n============================================")

        total1 = display_pokemon_info(data1)
        total2 = display_pokemon_info(data2)

        print("\nResults:")
        if total1 > total2:
            print(f"{pokemon1.capitalize()} wins with higher total stats ({total1} vs {total2})")
        elif total2 > total1:
            print(f"{pokemon2.capitalize()} wins with higher total stats ({total2} vs {total1})")
        else:
            print(f"It's a tie! Both have total stats of {total1}.")

def main():
    while True:
        print(f"\nOptions:")
        print(f"1. View the Pokemon Info")
        print(f"2. Compare the two Pokemon")
        print(f"q. To quit Enter q...")
        choice = input("Choose an option: ").strip().lower()

        if choice == '1':
            name = input("Enter the Pokemon name: ")
            data = get_pokemon_data(name)
            display_pokemon_info(data)

        elif choice == '2':
            p1 = input("Enter first Pokemon name: ")
            p2 = input("Enter second Pokemon name: ")
            compare_pokemons(p1, p2)

        elif choice == 'q':
            print("Bye Bye Trainer!")
            break
        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()