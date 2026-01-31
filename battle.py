import streamlit as st
import time
import base64
import requests
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Pokemon Battle Comparator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for the VS battle style
st.markdown("""
            <style>
            .stApp{
                background-color: #0B0C10; }
            .winner-banner{
                background-color: #EF233C;
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                margin: 20px 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse{
                0%, 100% { transform: scale(1);}
                50% { transform: scale(1.05)}
            }
            </style>
""" , unsafe_allow_html = True)

# --- HELPER FUNCTIONS ---

def get_pokemon_data(pokemon_name):
    """Fetch Pokemon Data from PokeAPI"""
    try:
        # Strip whitespace and convert to lowercase
        clean_name = pokemon_name.strip().lower()
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_name}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
    
def display_pokemon_card(data, column):
    """Display Pokemon Information in a card format"""
    if data:
        with column:
            st.markdown(f"<h1 style='text-align: center; color: #4361EE;'>{data['name'].upper()}</h1>", unsafe_allow_html=True)
            
            # Type Badges
            types = [t['type']['name'] for t in data['types']]
            type_colors = {
                'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
                'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
                'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
                'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
                'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
                'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
            }
            
            type_html = "".join([f"<span style='background-color: {type_colors.get(t, '#777')}; color: white; padding: 5px 15px; border-radius: 10px; margin: 5px;'>{t.upper()}</span>" for t in types])
            st.markdown(f"<div style='text-align: center;'>{type_html}</div>", unsafe_allow_html=True)

            # Calculate Total Stats
            total = sum([s['base_stat'] for s in data['stats']])
            st.metric("Total Stats", total)
            return total
    return 0

    # Main App
    # Initialize session state for comparison
    if 'show_comparison' not in st.session_state:
        st.session_state.show_comparison = False
    # if 'pokemon1_name' not in st.session_state:
    #     st.session_state.pokemon1_name = ""
    # if 'pokemon2_name' not in st.session_state:
    #     st.session_state.pokemon2_name = ""
    
    # Input section - only show if not comparing
    if not st.session_state.show_comparison:
        st.title("🎮 Poke-Battle Arena")
        col1, col2 = st.columns(2)

        # with col1:
        #     # st.markdown('### MY POKEMON')
        #     p1 = st.text_input("Enter second Pokemon name:", value="", key="pokemon2", placeholder="e.g., Charmander")
        
        with col1:
            p1 = st.text_input("Player 1 Pokemon:", placeholder="e.g., pikachu")
        with col2:
            p2 = st.text_input("Player 2 Pokemon:", placeholder="e.g., lucario")

        # Compare button (centered)
        # col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        # with col_btn2:
        #     compare_button = st.button("⚔️ COMPARE", use_container_width=True,type="primary")
        
        # if compare_button and pokemon1 and pokemon2:
        #     st.session_state.show_comparison = True
        #     st.session_state.pokemon1_name = pokemon1
        #     st.session_state.pokemon2_name = pokemon2
        #     st.rerun()
        if st.button("⚔️ FIGHT!"):
            if p1 and p2:
                st.session_state.p1, st.session_state.p2 = p1, p2
                st.session_state.show_comparison = True
                st.rerun()
            else:
                st.warning("Please enter names for both combatants!")
    
    else:
        # THE BATTLE SEQUENCE BEGINS!
        p1_data = get_pokemon_data(st.session_state.p1)
        p2_data = get_pokemon_data(st.session_state.p2)

        if p1_data and p2_data:
            # 1. SHOW THE "FIGHT!" BANNER
            banner_place = st.empty()
            banner_place.image("pokemon.png")
        
            # 2. START THE MUSIC
            st.audio("Aylex - Fighter (freetouse.com).mp3", autoplay=True)
            time.sleep(2) # Dramatic pause!
            banner_place.empty()

            # 3. DISPLAY FIGHTERS
            col_img1, col_img2 = st.columns(2)
            col_img1.image(p1_data['sprites']['other']['official-artwork']['front_default'])
            col_img2.image(p2_data['sprites']['other']['official-artwork']['front_default'])

            # 4. SHOW THE STAT CARDS
            c1, c2 = st.columns(2)
            total1 = display_pokemon_card(p1_data, c1)
            total2 = display_pokemon_card(p2_data, c2)

            # 5. ANNOUNCE THE WINNER
            time.sleep(1)
            if total1 > total2:
                st.image("pikachuwinner.jpg") # Or dynamic winner image!
                st.success(f"🏆 {st.session_state.p1.upper()} WINS!")
            elif total2 > total1:
                st.markdown(f"<div class='winner-banner'>🏆 {st.session_state.p2.upper()} WINS! 🏆</div>", unsafe_allow_html=True)
            else:
                st.info("It's a draw! Both trainers are equally matched!")
        
            if st.button("↩️ New Battle"):
                st.session_state.show_comparison = False
                st.rerun()
        else:
            st.error("One of your Pokemon couldn't be found in the Pokedex! Check your spelling.")
            if st.button("Back"):
                st.session_state.show_comparison = False
                st.rerun()