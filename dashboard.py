import streamlit as st
import pandas as pd

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv("H3Units_Enhanced.csv")
    df['Unit_name'] = df['Unit_name'].astype(str)
    return df.set_index("Unit_name")

df = load_data()
unit_names = sorted(df.index.tolist())

# --- HELPERS ---
def is_ranged(special_abilities):
    if not isinstance(special_abilities, str):
        return False
    return "Ranged" in special_abilities

def get_abilities(special_abilities):
    if not isinstance(special_abilities, str) or special_abilities.strip() in ["-", ""]:
        return None
    return ", ".join(special_abilities.split(","))

def slot_ui(slot_num, army_type, key_prefix=""):
    with st.expander(f"Slot {slot_num}", expanded=True):
        name_col, count_col = st.columns([2, 1])
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

def army_stats(slot_stats):
    total_power = int(sum(s["power"] for s in slot_stats))
    max_speed = int(max([s["speed"] for s in slot_stats], default=0))
    return total_power, max_speed

def army_ui(army_type, key_prefix=""):
    slot_stats = []
    for i in range(1, 8):
        stats = slot_ui(i, army_type, key_prefix=key_prefix)
        if stats:
            slot_stats.append(stats)
    total_power, max_speed = army_stats(slot_stats)
    return total_power, max_speed

# --- PAGE TITLE (optional, not sticky) ---
st.title("Heroes of Might and Magic III Army Power Calculator")

# --- STICKY HEADER CSS ---
st.markdown("""
<style>
div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
    position: sticky;
    top: 2.875rem;
    background-color: white;
    z-index: 999;
}
.fixed-header {
    padding: 0.5em 0 0.5em 0;
}
.header-army-title {
    font-size: 1.3em;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 0.5em;
}
.header-army-stats {
    font-size: 1em;
    color: #555;
    margin-top: 0.2em;
}
.info-icon {
    font-size: 1.15em;
    color: #2c7be5;
    cursor: pointer;
    margin-left: 6px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER LAYOUT ---
header = st.container()
with header:
    st.markdown('<div class="fixed-header"></div>', unsafe_allow_html=True)
    col_own, col_enemy = st.columns(2)
    # These will be filled after army_ui runs, so use placeholders
    own_power_placeholder = col_own.empty()
    enemy_power_placeholder = col_enemy.empty()
    # Header titles
    col_own.markdown('<div class="header-army-title">Own Army</div>', unsafe_allow_html=True)
    # Enemy Army with info icon
    info_html = """
    <span class="info-icon" title="Few 1-4
Several 5-9
Pack 10-19
Lots 20-49
Horde 50-99
Throng 100-249
Swarm 250-499
Zounds 500-999
Legion 1000+">&#8505;</span>
    """
    col_enemy.markdown(
        f'<div class="header-army-title">Enemy Army {info_html}</div>',
        unsafe_allow_html=True
    )

# --- MAIN CONTENT ---
col_own_body, col_enemy_body = st.columns(2)
with col_own_body:
    own_total_power, own_max_speed = army_ui("Own", key_prefix="own")
with col_enemy_body:
    enemy_total_power, enemy_max_speed = army_ui("Enemy", key_prefix="enemy")

# --- UPDATE HEADER WITH STATS ---
with header:
    col_own, col_enemy = st.columns(2)
    col_own.markdown(
        f'<div class="header-army-stats">'
        f'Total Power: <b>{own_total_power:,}</b> &nbsp;|&nbsp; Max Speed: <b>{own_max_speed}</b>'
        f'</div>', unsafe_allow_html=True)
    col_enemy.markdown(
        f'<div class="header-army-stats">'
        f'Total Power: <b>{enemy_total_power:,}</b> &nbsp;|&nbsp; Max Speed: <b>{enemy_max_speed}</b>'
        f'</div>', unsafe_allow_html=True)