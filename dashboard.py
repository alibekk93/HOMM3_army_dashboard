import streamlit as st
import pandas as pd

# Streamlit page config
st.set_page_config(layout="wide", page_title="HoMM III Army Power Calculator")
st.title("Heroes of Might and Magic III Army Power Calculator")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("H3Units_Enhanced.csv")
    df['Unit_name'] = df['Unit_name'].astype(str)
    return df.set_index("Unit_name")

df = load_data()
unit_names = sorted(df.index.tolist())

def is_ranged(special_abilities):
    if not isinstance(special_abilities, str):
        return False
    return "Ranged" in special_abilities

def get_abilities(special_abilities):
    if not isinstance(special_abilities, str) or special_abilities.strip() in ["-", ""]:
        return None
    # Add spaces after commas for readability
    return ", ".join(special_abilities.split(","))

def slot_ui(slot_num, army_type, key_prefix=""):
    with st.expander(f"Slot {slot_num}", expanded=True):
        # Row for unit name and count (with info icon)
        name_col, count_col, info_col = st.columns([2, 1, 0.15])
        with name_col:
            selected_unit = st.selectbox(
                f"Unit Name {slot_num}",
                options=[""] + unit_names,
                key=f"{key_prefix}_unit_{slot_num}",
                index=0,
                format_func=lambda x: x if x else "Select unit..."
            )
        with count_col:
            count = st.number_input(
                "Count", min_value=0, value=0, key=f"{key_prefix}_count_{slot_num}"
            )
        with info_col:
            info_html = """
            <span style="font-size: 1.1em; cursor:pointer; color:#2c7be5;" 
                title="Few 1-4
Several 5-9
Pack 10-19
Lots 20-49
Horde 50-99
Throng 100-249
Swarm 250-499
Zounds 500-999
Legion 1000+">&#8505;</span>
            """
            st.markdown(f"<div style='margin-top:2em'>{info_html}</div>", unsafe_allow_html=True)

        stats = None
        power_per_unit = 0
        slot_power = 0
        speed = 0

        if selected_unit and selected_unit in df.index and count > 0:
            unit = df.loc[selected_unit]
            power_per_unit = (
                unit.Attack + unit.Defence + unit.Speed +
                ((unit['Minimum Damage'] + unit['Maximum Damage']) / 2)
            ) * unit.Health
            slot_power = power_per_unit * count
            speed = unit.Speed

            ranged_icon = "🏹 " if is_ranged(unit.Special_abilities) else ""
            abilities = get_abilities(unit.Special_abilities)

            # Stats and power in one column, as in your screenshot
            st.markdown(
                f"**Stats:**<br>"
                f"Attack: {unit.Attack}<br>"
                f"Defense: {unit.Defence}<br>"
                f"Damage: {unit['Minimum Damage']}-{unit['Maximum Damage']}<br>"
                f"Health: {unit.Health}<br>"
                f"Speed: {unit.Speed}<br>"
                f"<b>Power per unit:</b> {int(power_per_unit):,}<br>"
                f"<b>Total slot power:</b> {int(slot_power):,}",
                unsafe_allow_html=True
            )
            stats = {
                "power": slot_power,
                "speed": speed
            }
        elif selected_unit:
            st.error("Unit not found in database")
        return stats

def army_ui(army_type, key_prefix=""):
    st.header(f"{army_type} Army")
    slot_stats = []
    for i in range(1, 8):
        stats = slot_ui(i, army_type, key_prefix=key_prefix)
        if stats:
            slot_stats.append(stats)
    total_power = int(sum(s["power"] for s in slot_stats))
    max_speed = int(max([s["speed"] for s in slot_stats], default=0))
    st.markdown("---")
    st.subheader(f"Total Army Power: {total_power:,}")
    st.subheader(f"Maximum Army Speed: {max_speed}")

col_own, col_enemy = st.columns(2)
with col_own:
    army_ui("Own", key_prefix="own")
with col_enemy:
    
    army_ui("Enemy", key_prefix="enemy")