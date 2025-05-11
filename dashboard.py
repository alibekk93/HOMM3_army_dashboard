import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(layout="wide", page_title="HoMM III Army Calculator")
st.title("Heroes of Might and Magic III Army Power Calculator")

# Load unit data
@st.cache_data
def load_data():
    return pd.read_csv("H3Units_Enhanced.csv").set_index("Unit_name")

df = load_data()

# Army columns
col_own, col_enemy = st.columns(2)

def create_army_section(col, army_type):
    total_power = 0
    max_speed = 0
    
    with col:
        st.header(f"{army_type} Army")
        
        for i in range(1, 8):
            with st.expander(f"Slot {i}", expanded=True):
                c1, c2 = st.columns(2)
                unit_name = c1.text_input(f"Unit Name {i}", key=f"{army_type}_unit_{i}")
                count = c2.number_input(f"Count", min_value=0, value=0, key=f"{army_type}_count_{i}")
                
                if unit_name in df.index and count > 0:
                    unit = df.loc[unit_name]
                    power_per_unit = (unit.Attack + unit.Defence + unit.Speed + 
                                    (unit['Minimum Damage'] + unit['Maximum Damage'])/2) * unit.Health
                    total_power += power_per_unit * count
                    max_speed = max(max_speed, unit.Speed)
                    
                    st.write(f"""
                    **Stats:**  
                    Attack: {unit.Attack}  
                    Defense: {unit.Defence}  
                    Damage: {unit['Minimum Damage']}-{unit['Maximum Damage']}  
                    Health: {unit.Health}  
                    Speed: {unit.Speed}  
                    **Power per unit:** {power_per_unit:,.0f}  
                    **Total slot power:** {power_per_unit * count:,.0f}
                    """)
                elif unit_name:
                    st.error("Unit not found in database")

        st.markdown("---")
        st.subheader(f"Total Army Power: {total_power:,.0f}")
        st.subheader(f"Maximum Army Speed: {max_speed}")

# Create both army sections
create_army_section(col_own, "Own")
create_army_section(col_enemy, "Enemy")
