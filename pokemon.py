import requests

def get_pokemon_data(pokemon_name: str):
    try:
        clean_name = pokemon_name.strip().lower()
        if not clean_name:
            return None
        
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"❌ Error: Pokemon '{pokemon_name}' not found. Check your spelling!")
        else:
            print(f"⚠️ API Error: Status code {response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"📡 Connection Error: Could not reach the Pokemon Lab. ({e})")
        return None

def display_pokemon_info(data: dict) -> int:
    if not data:
        return 0
    
    print(f"\n{'='*30}")
    print(f"✨ POKEDEX ENTRY: {data['name'].upper()} ✨")
    print(f"{'='*30}")
    
    print(f"Types:     {', '.join(t['type']['name'].capitalize() for t in data['types'])}")
    print(f"Abilities: {', '.join(a['ability']['name'].capitalize() for a in data['abilities'])}")
    
    # Official Artwork Safe-Check
    artwork = data['sprites'].get('other', {}).get('official-artwork', {}).get('front_default')
    if artwork:
        print(f"Artwork:   {artwork}")

    print("\nBASE STATS:")
    total_stats = 0
    for stat_entry in data['stats']:
        stat_name = stat_entry['stat']['name'].replace('-', ' ').capitalize()
        stat_val = stat_entry['base_stat']
        print(f"📊 {stat_name:15}: {stat_val}")
        total_stats += stat_val
    
    print(f"{'-'*30}")
    print(f"TOTAL POWER: {total_stats}")
    print(f"{'-'*30}")
    
    return total_stats

def compare_pokemons(p1_name: str, p2_name: str):
    data1 = get_pokemon_data(p1_name)
    data2 = get_pokemon_data(p2_name)

    if data1 and data2:
        print(f"⚔️ Comparison failed: One or both Pokemon were not found.")
        return
    
    print(f"\n⚔️  BATTLE ARENA: {p1_name.upper()} VS {p2_name.upper()}  ⚔️")

    total1 = display_pokemon_info(data1)
    total2 = display_pokemon_info(data2)
    print("\n" + "🏁" * 15)
    print("\nResults:")
    if total1 > total2:
        print(f"🏆 {data1['name'].upper()} wins with total {total1} power")
    elif total2 > total1:
        print(f"🏆 {data2['name'].upper()} wins with total {total2} power")
    else:
        print(f"🤝 It's a tie! Both have {total1}.")

def main():
    print("Welcome to the Python Pokemon Arena!")

    while True:
        print(f"\nOptions:")
        print(f"1. View the Pokemon Info")
        print(f"2. Compare the two Pokemon")
        print(f"q. Quit")

        choice = input("\nChoose an option: ").strip().lower()

        if choice == '1':
            name = input("Enter the Pokemon name: ")
            data = get_pokemon_data(name)
            display_pokemon_info(data)

        elif choice == '2':
            p1 = input("Enter first Pokemon: ")
            p2 = input("Enter second Pokemon: ")
            compare_pokemons(p1, p2)

        elif choice == 'q':
            print("Bye Bye Trainer! Come back soon!")
            break
        else:
            print("Invalid choice. Please try 1, 2, or q.")
        
if __name__ == "__main__":
    main()