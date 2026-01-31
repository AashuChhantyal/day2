import streamlit as st
import time
import base64
import requests

# Page Configuration
st.set_page_config(
    page_title="Pokemon Battle Comparator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for the VS battle style
st.markdown("""
            <style>
            .main{
                background-color: #0B0C10;
            }
            .stApp{
                background-color: #0B0C10;
            }
            .pokemon-card{
                background-color: rgba(67, 97, 238, 0.1);
                border: 2px solid #4361EE;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            .vs-header{
                text-align: center;
                margin-bottom: 30px;
            }
            .vs-text{
                font-size: 80px;
                font-weight: bold;
                color: #EF233C;
                margin: 15px 0;
            }
            .pokemon-name{
                font-size: 32px;
                font-weight: bold;
                color: #4361EE;
                margin: 15px 0;
            }
            .stat-container{
                background-color: rgba(249, 199, 79, 0.2);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
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
            # Pokemon Name - Clean and Bold
            st.markdown(f"""
                    <div style='
                        text-align: center;
                        font-size: 48px;
                        font-weight: 900;
                        color: #4361EE;
                        margin: 30px 0 20px 0;
                        letter-spacing: 2px;
                        text-transform: uppercase;
                    '>
                        {data['name']}
                    </div>

                """, unsafe_allow_html=True)
            
            # Types with colored badges
            types = [t['type']['name'] for t in data['types']]
            type_colors = {
                'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
                'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
                'fighting': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
                'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
                'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
                'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
            }

            # Type section with header
            st.markdown("""
                    <div style='
                        text-align: center;
                        margin: 30px 0 15px 0;
                    '>
                        <span style='
                            color: #EF233C;
                            font-size: 24px;
                            font-weight: bold;
                            text-transform: uppercase;
                        '>Type</span>
                    </div>
            """, unsafe_allow_html=True)
            
            type_html = " ".join([
                f"<span style='background-color: {type_colors.get(t, '#777')}; color: white; padding: 8px 20px; border radius: 25px; margin: 5px; display: inline-block; font-size: 18px; font-weight: 600;'>{t.upper()}</span>"
                for t in types
            ])
            st.markdown(f"<div style='text-align: center; margin: 15px 0;'>{type_html}</div>", unsafe_allow_html=True)

            # Stats section
            st.markdown("""
                    <div style='
                        text-align: center;
                        margin: 30px 0 15px 0;
                    '>
                        <span style='
                            color: #EF233C;
                            font-size: 24px;
                            font-weight: bold;
                            text-transform: uppercase;
                        '>Stats</span>
            """, unsafe_allow_html=True)

            # Display individual stats
            total_stats = 0
            for stat in data['stats']:
                stat_name = stat['stat']['name'].replace('-', ' ').upper()
                stat_value = stat['base_stat']
                total_stats += stat_value

                # Create stat bar
                st.markdown(f"""
                    <div style='margin: 10px 0; text-align: left;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                            <span style='color: #F9C74F; font-weight: 600;  font-size: 16px;'>{stat_name}</span>
                            <span style='color: #FFFFFF; font-weight: bold; font-size: 16px;'>{stat_value}</span>
                        </div>
                        <div style='background-color: rgba(67, 97, 238, 0.3); border-radius: 10px; height: 20px; overflow: hidden;'>
                            <div style='background-color: #4361EE; height: 100%; width: {(stat_value/255)*100}%; border-radius: 10px;'></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Total Stats section
                st.markdown(f"""
                    <div style='
                        text-align:center;
                        margin= 30px 0 15px 0;
                    '>
                        <span style='
                            color: #EF233C;
                            font-size: 24px;
                            font-weight: bold;
                            text-transform: uppercase;
                        '>Total Stats</span>
                    </div>
                    <div style='
                        text-align: center;
                        font-size: 42px;
                        font-weight: bold;
                        color: #F9C74F;
                    '>
                        {total_stats}
                    </div>
                """, unsafe_allow_html=True)

                # Abilities section
                st.markdown("""
                    <div style='
                        text-align: center;
                        margin: 30px 0 15px 0;
                    '>
                        <span style='
                            color: #EF233C;
                            font-size: 24px;
                            font-weight: bold;
                            test-transform: uppercase;
                        '>Abilities</span>
                    </div>
                """, unsafe_allow_html=True)

                abilities= [a['ability']['name'].replace('-', ' ').title() for a in data['abilities']]
                abilities_html = ",".join([
                    f"<span style='color: #F9C74F; font-size: 20px; font-weight: 600;'>{ability}</span>"
                    for ability in abilities
                ])
                st.markdown(f"<div style='text-align: center; margin: 10px 0;'>{abilities_html}</div>", unsafe_allow_html=True)

                return total_stats
    return 0
    
    # Main App
    # Initialize session state for comparison
    if 'show_comparison' not in st.session_state:
        st.session_state.show_comparison = False
    if 'pokemon1_name' not in st.session_state:
        st.session_state.pokemon1_name = ""
    if 'pokemon2_name' not in st.session_state:
        st.session_state.pokemon2_name = ""
    
    # Input section - only show if not comparing
    if not st.session_state.show_comparison:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### MY POKEMON')
            pokemon2 = st.text_input("Enter second Pokemon name:", value="", key="pokemon2", placeholder="e.g., Charmander")
        
        # Compare button (centered)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            compare_button = st.button("⚔️ COMPARE", use_container_width=True,type="primary")
        
        if compare_button and pokemon1 and pokemon2:
            st.session_state.show_comparison = True
            st.session_state.pokemon1_name = pokemon1
            st.session_state.pokemon2_name = pokemon2
            st.rerun()
    
    # Show comparison results
    if st.session_state.show_comparison:
        # Add a reset button
        if st.button("↩️ Compare New Pokemon"):
            st.session_state.show_comparison = False
            st.session_state.pokemon1_name = ""
            st.session_state.pokemon2_name = ""
            st.rerun()
        
        pokemon1 = st.session_state.pokemon1_name
        pokemon2 = st.session_state.pokemon2_name
        # Fetch data for both Pokemon
        data1 = get_pokemon_data(pokemon1)
        data2 = get_pokemon_data(pokemon2)

        if data and data2:
            # Get Pokemon Sprites
            sprite1 = data1['sprites']['other']['official-artwork']['front-default']
            sprite2 = data2['sprites']['other']['official-artwork']['front_default']

            # Use st.image with columns for overlay effect
            import base64
            from pathlib import Path

            # Read and encode the VS image
            vs_image_path = Path("images/pokemon.png")
            if vs_image_path.exists():
                with open(vs_image_path, "rb") as f:
                    vs_image_data = base64.b64encode(f.read()).decode()

                # Create HTML with base64 encoded image
                vs_html = f"""
                <div style="position: relative; width: 100%; margin: 20px 0;">
                    <img src="data:image/png;base64,{vs_image_data}" style="width: 100%; display: block;">
                    <img src="{sprite1}" style="position: absolute; left: 8%; top:50%; transform: translateY(-50%); width: 350px; max-width: 25%;">
                    <img src="{sprite2}" style="position: absolute; right: 8%; top: 50%; transform: translateY(-50%); width: 350px; max-width: 25%;">
                </div>
                """
                st.markdown(vs_html, unsafe_allow_html = True)
            else:
                st.error("VS background image not found!")
            
            st.markdown("---")

            # Display Pokemon cards side by side
            col1, col2 = st.columns(2)

            total1 = display_pokemon_card(data1, col1)
            total2 = display_pokemon_card(data2, col2)

            # Winner announcement
            st.markdown("---")
            if total1 > total2:
                st.markdown(f"""
                   <div class='winner-banner'>
                      🏆 {pokemon1.upper()} WINS! 🏆<br>
                      <span style='font-size: 20px;'>Total Stats: {total1} vs {total2}</span>
                    </div>
                """, unsafe_allow_html = True)
            elif total2 > total1:
                st.markdown(f"""
                   <div class='winner-banner'>
                        🏆 {pokemon2.upper()} WINS! 🏆<br>
                        <span style='font-size: 20px;'>Total Stats: {total2} vs {total1}</span>
                    </div>         
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                   <div class='winner-banner' style='background-color: #4361EE;'>
                        🤝 IT'S A TIE! 🤝<br>
                        <span style="font-size: 20px;">Both have {total1} total stats!</span>
                    </div>
                """, unsafe_allow_html = True)
        elif not data1:
            st.error(f"❌ Pokemon '{pokemon1}' not found! Please check the name and try again.")
        elif not data2:
            st.error(f"❌ Pokemon '{pokemon2}' not found! Please check the name and try again.")