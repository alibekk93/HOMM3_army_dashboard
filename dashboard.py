import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(layout="wide", page_title="HoMM III Army Power Calculator")
st.title("Heroes of Might and Magic III Army Power Calculator")

# Load unit data
@st.cache_data
def load_data():
    df = pd.read_csv("H3Units_Enhanced.csv")
    df['Unit_name'] = df['Unit_name'].astype(str)
    return df.set_index("Unit_name")

df = load_data()
unit_names = sorted(df.index.tolist())

# Army columns
col_own, col_enemy = st.columns(2)

def create_army_section(col, army_type):
    total_power = 0
    max_speed = 0
    slot_units = []
    
    with col:
        st.header(f"{army_type} Army")
        
        for i in range(1, 8):
            with st.expander(f"Slot {i}", expanded=True):
                c1, c2 = st.columns(2)
                selected_unit = c1.selectbox(
                    f"Unit Name {i}",
                    options=[""] + unit_names,
                    key=f"{army_type}_unit_{i}",
                    index=0,
                    format_func=lambda x: x if x else "Select unit..."
                )
                count = c2.number_input(
                    f"Count", min_value=0, value=0, key=f"{army_type}_count_{i}"
                )
                
                if selected_unit and selected_unit in df.index and count > 0:
                    unit = df.loc[selected_unit]
                    # Calculate power per unit
                    power_per_unit = (
                        unit.Attack + unit.Defence + unit.Speed +
                        ((unit['Minimum Damage'] + unit['Maximum Damage']) / 2)
                    ) * unit.Health
                    slot_power = power_per_unit * count
                    total_power += slot_power
                    max_speed = max(max_speed, unit.Speed)
                    
                    st.write(f"""
**Stats:**  
Attack: {unit.Attack}  
Defense: {unit.Defence}  
Damage: {unit['Minimum Damage']}-{unit['Maximum Damage']}  
Health: {unit.Health}  
Speed: {unit.Speed}  
**Power per unit:** {power_per_unit:,.0f}  
**Total slot power:** {slot_power:,.0f}
""")
                elif selected_unit:
                    st.error("Unit not found in database")

        st.markdown("---")
        st.subheader(f"Total Army Power: {total_power:,.0f}")
        st.subheader(f"Maximum Army Speed: {max_speed}")

# Create both army sections
create_army_section(col_own, "Own")
create_army_section(col_enemy, "Enemy")
