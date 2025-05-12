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
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_unit = st.selectbox(
                f"Unit Name {slot_num}",
                options=[""] + unit_names,
                key=f"{key_prefix}_unit_{slot_num}",
                index=0,
                format_func=lambda x: x if x else "Select unit..."
            )
        with col2:
            count = st.number_input(
                "Count", min_value=0, value=0, key=f"{key_prefix}_count_{slot_num}"
            )

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

            stat_col, power_col = st.columns([2, 1])
            with stat_col:
                st.markdown(
                    f"**{ranged_icon}{selected_unit}**"
                    + (f' <span style="background-color:#eee;border-radius:4px;padding:2px 6px;margin-left:8px;cursor:pointer;" title="{abilities}">Ability</span>' if abilities else ""),
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""<div style="margin-top:0.5em;">
                    <b>Stats:</b><br>
                    Attack: {unit.Attack}<br>
                    Defense: {unit.Defence}<br>
                    Damage: {unit['Minimum Damage']}-{unit['Maximum Damage']}<br>
                    Health: {unit.Health}<br>
                    Speed: {unit.Speed}
                    </div>""",
                    unsafe_allow_html=True
                )
            with power_col:
                st.markdown(
                    f"""<div style="text-align:right;">
                    <b>Power per unit:</b> {int(power_per_unit):,}<br>
                    <b>Total slot power:</b> {int(slot_power):,}
                    </div>""",
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