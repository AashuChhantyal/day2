import streamlit as st
import time
from pathlib import Path
import base64
from utils import get_pokemon_data

# 1. Page Configuration
st.set_page_config(
    page_title="Pokemon Battle Comparator",
    page_icon="⚡",
    layout="wide"
)

# 2. Custom CSS for the VS battle style
st.markdown("""
            <style>
            .stApp{
                background-color: #0B0C10;
                color: white;
            }
            .pokemon-title {
                text-align: center;
                color: #4361EE;
                text-shadow: 2px 2px #000000;
                font-family: 'Courier New', Courier, monospace;
            }
            .winner-banner{
                background-color: linear-gradient(90deg, #EF233C, #D90429);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                color: white;
                box-shadow: 0px 0px 15px #EF233C;
                animation: pulse 2s infinite;
            }
            @keyframes pulse{
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.02); }
            }
            </style>
""" , unsafe_allow_html = True)

# --- HELPER FUNCTIONS ---

# def get_pokemon_data(pokemon_name):
#     """Fetch Pokemon Data from PokeAPI"""
#     try:
#         # Strip whitespace and convert to lowercase
#         clean_name = pokemon_name.strip().lower()
#         response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{clean_name}")
#         return response.json() if response.status_code == 200 else None
    
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
#         return None
    
def display_pokemon_card(data, column):
    """Display Pokemon Information in a card format"""
    if not data:
        return 0
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

def get_base64_audio(file_path):
    """Converts audio file to base64 so it can be embedded in HTML"""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return None

# Main App

# Ensures music is always ready to play
audio_path = "audio/Aylex - Fighter (freetouse.com).mp3"
audio_b64 = get_base64_audio(audio_path)

# Check if file exists before trying to play it
if audio_b64:
    st.components.v1.html(
        f"""
        <audio id="bg-audio" autoplay loop>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        <script>
            const audio = window.document.getElementById("bg-audio");
            audio.volume = 0.4;

            const startMusic = () => {{
                audio.play().catch(e => console.log("Waiting for user interaction..."));
            }};
            // This ensures the music kicks in the moment they click anywhere!
            window.parent.document.addEventListener('click', startMusic, {{ once: true }});
            window.parent.document.addEventListener('keydown', startMusic, {{ once: true }});
        </script>
        """,
        height=0,
    )

# Initialize session state for comparison

if 'show_comparison' not in st.session_state:
    st.session_state.show_comparison = False

# Input section - only show if not comparing
if not st.session_state.show_comparison:
    st.title("🎮 Poke-Battle Arena")
    st.info("The music will start as soon as you interact with the page!")

    col1, col2 = st.columns(2)
    with col1:
        p1 = st.text_input("Trainer 1 Pokemon:", placeholder="e.g., Charizard, pikachu")
    with col2:
        p2 = st.text_input("Player 2 Pokemon:", placeholder="e.g., Blastoise, lucario")

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
        # 1. Battle Intro Animation
        banner_place = st.empty()
        banner_place.markdown("<h1 style='text-align: center;'>READY...</h1>", unsafe_allow_html=True)
        time.sleep(0.8)
        banner_place.markdown("<h1 style='text-align: center; color: #EF233C;'>FIGHT!</h1>", unsafe_allow_html=True)
        time.sleep(0.8)
        banner_place.empty()

        # 2. SHOW THE "FIGHT!" BANNER
        # banner_place = st.empty()
        # banner_place.image("Images/pokemon.png")
        # time.sleep(0.2) 
        # banner_place.empty()
        
        # 3. DISPLAY FIGHTERS
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            img1= p1_data['sprites']['other']['official-artwork'].get('front_default')
            if img1: st.image(img1, use_container_width=True)
        with col_img2:
            img2= p2_data['sprites']['other']['official-artwork'].get('front_default')
            if img2: st.image(img2, use_container_width=True)
        
        # 4. SHOW THE STAT CARDS
        c1, c2 = st.columns(2)
        total1 = display_pokemon_card(p1_data, c1)
        total2 = display_pokemon_card(p2_data, c2)

        st.markdown("---")
        # 5. ANNOUNCE THE WINNER
        # Use container to make sure winner info sticks to the page!
        # if total1 > total2:
        #     st.image("Images/pikachuwinner.jpg", width=500) # Or dynamic winner image!
        #     st.success(f"🏆 {st.session_state.p1.upper()} WINS!")
        # elif total2 > total1:
        #     st.markdown(f"<div class='winner-banner'>🏆 {st.session_state.p2.upper()} WINS! 🏆</div>", unsafe_allow_html=True)
        # else:
        #     st.info("It's a draw! Both trainers are equally matched!")
    
        if total1 > total2:
            st.markdown(f"<div class='winner-banner'>🏆 {st.session_state.p1.upper()} IS VICTORIOUS!</div>", unsafe_allow_html=True)
        elif total2 > total1:
            st.markdown(f"<div class='winner-banner'>🏆 {st.session_state.p2.upper()} IS VICTORIOUS!</div>", unsafe_allow_html=True)
        else:
            st.info("The battle is a stalemate! Both Pokemon are equally matched.")

        if st.button("↩️ New Battle"):
            st.session_state.show_comparison = False
            st.rerun()
    else:
        st.error("One of those Pokemon names was not recognized by the Pokedex!")
        if st.button("Try Again"):
            st.session_state.show_comparison = False
            st.rerun()