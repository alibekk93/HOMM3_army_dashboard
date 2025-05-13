import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="HoMM III Army Power Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# --- CUSTOM STYLES ---
st.markdown("""
<style>
body {
    background: #f7f8fa;
}
.stApp {
    background: #f7f8fa;
}
.header-title {
    font-size: 2.1em;
    font-weight: 700;
    letter-spacing: 0.01em;
    margin-bottom: 0.1em;
}
.header-army {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.2em;
    font-weight: 600;
    margin-bottom: 0.2em;
}
.header-army-stats {
    font-size: 1em;
    margin-bottom: 0.2em;
}
.info-icon {
    font-size: 1.13em;
    color: #ffe066;
    cursor: pointer;
    margin-left: 6px;
    border-radius: 50%;
    padding: 1px 4px;
    transition: background 0.2s;
}
.info-icon:hover {
    background: #232526;
}
.army-card {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 2px 16px 0 rgba(44,123,229,0.05);
    padding: 1.4em 1.2em 1.2em 1.2em;
    margin-bottom: 1.5em;
    min-height: 600px;
}
.st-expander {
    background: #f4f6fa !important;
    border-radius: 13px !important;
    margin-bottom: 0.7em;
    border: 1px solid #e1e8ed !important;
    transition: box-shadow 0.2s;
}
.st-expander:hover {
    box-shadow: 0 2px 12px 0 rgba(44,123,229,0.10);
    border-color: #b1d0fa !important;
}
.unit-title {
    font-size: 1.08em;
    font-weight: 600;
    color: #2c7be5;
    margin-bottom: 0.1em;
}
.ability-badge {
    background: #ffe066;
    color: #232526;
    border-radius: 5px;
    padding: 2px 8px;
    font-size: 0.93em;
    margin-left: 8px;
    cursor: pointer;
}
.stats-table {
    font-size: 1em;
    color: #444;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
}
.power-block {
    text-align: right;
    font-size: 1.1em;
    color: #1e6a9e;
    font-weight: 700;
    margin-top: 0.8em;
}
@media (max-width: 1100px) {
    .army-card { min-height: 0; }
}
</style>
""", unsafe_allow_html=True)

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

# --- HEADER ---
with st.container():
    st.markdown('<div class="header-bar">', unsafe_allow_html=True)
    st.markdown('<div class="header-title">🛡️ Heroes of Might and Magic III Army Power Dashboard</div>', unsafe_allow_html=True)
    col_own, col_enemy = st.columns(2)
    own_army_title = '<div class="header-army">Own Army</div>'
    enemy_info = """
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
    enemy_army_title = f'<div class="header-army">Enemy Army {enemy_info}</div>'
    own_stats_placeholder = col_own.empty()
    enemy_stats_placeholder = col_enemy.empty()
    col_own.markdown(own_army_title, unsafe_allow_html=True)
    col_enemy.markdown(enemy_army_title, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SLOT UI ---
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
                    f'<span class="unit-title">{ranged_icon}{selected_unit}'
                    + (f'<span class="ability-badge" title="{abilities}">Ability</span>' if abilities else "") +
                    '</span>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"""<div class="stats-table">
                    <b>Stats:</b><br>
                    Attack: <b>{unit.Attack}</b> &nbsp;|&nbsp;
                    Defense: <b>{unit.Defence}</b> &nbsp;|&nbsp;
                    Damage: <b>{unit['Minimum Damage']}-{unit['Maximum Damage']}</b> &nbsp;|&nbsp;
                    Health: <b>{unit.Health}</b> &nbsp;|&nbsp;
                    Speed: <b>{unit.Speed}</b>
                    </div>""",
                    unsafe_allow_html=True
                )
            with power_col:
                st.markdown(
                    f"""<div class="power-block">
                    Power/unit<br><span style="font-size:1.05em;">{int(power_per_unit):,}</span><br>
                    Total<br><span style="font-size:1.05em;">{int(slot_power):,}</span>
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
    slot_inputs = []
    # First, gather slot inputs without rendering
    for i in range(1, 8):
        # Save the current state for each slot to render after stats
        slot_inputs.append((i, army_type, key_prefix))
        # Compute stats for slots that already have values
        selected_unit = st.session_state.get(f"{key_prefix}_unit_{i}", "")
        count = st.session_state.get(f"{key_prefix}_count_{i}", 0)
        if selected_unit and selected_unit in df.index and count > 0:
            unit = df.loc[selected_unit]
            power_per_unit = (
                unit.Attack + unit.Defence + unit.Speed +
                ((unit['Minimum Damage'] + unit['Maximum Damage']) / 2)
            ) * unit.Health
            slot_power = power_per_unit * count
            speed = unit.Speed
            slot_stats.append({"power": slot_power, "speed": speed})
    # Calculate and display stats at the top
    total_power, max_speed = army_stats(slot_stats)
    st.markdown(
        f'<div class="header-army-stats" style="margin-bottom:1.2em;">'
        f'Total Power: <b>{total_power:,}</b> &nbsp;|&nbsp; Max Speed: <b>{max_speed}</b>'
        f'</div>', unsafe_allow_html=True)
    # Now render the slots
    for args in slot_inputs:
        slot_ui(*args)
    return total_power, max_speed


# --- MAIN CONTENT ---
col_own_body, col_enemy_body = st.columns(2, gap="large")
with col_own_body:
    own_total_power, own_max_speed = army_ui("Own", key_prefix="own")
with col_enemy_body:
    enemy_total_power, enemy_max_speed = army_ui("Enemy", key_prefix="enemy")

# --- UPDATE HEADER WITH STATS ---
with st.container():
    col_own, col_enemy = st.columns(2)
    col_own.markdown(
        f'<div class="header-army-stats">'
        f'Total Power: <b>{own_total_power:,}</b> &nbsp;|&nbsp; Max Speed: <b>{own_max_speed}</b>'
        f'</div>', unsafe_allow_html=True)
    col_enemy.markdown(
        f'<div class="header-army-stats">'
        f'Total Power: <b>{enemy_total_power:,}</b> &nbsp;|&nbsp; Max Speed: <b>{enemy_max_speed}</b>'
        f'</div>', unsafe_allow_html=True)
