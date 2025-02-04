import streamlit as st
import random

# Инициализация переменных в session_state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Лидерборд"
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []
if 'team_assignments' not in st.session_state:
    st.session_state.team_assignments = {}  # Формат: {имя: 1 или 2}
if 'team1' not in st.session_state:
    st.session_state.team1 = []
if 'team2' not in st.session_state:
    st.session_state.team2 = []
if 'winner_team' not in st.session_state:
    st.session_state.winner_team = None

# Данные игроков – начальные очки заданы, победы/поражения = 0, а также пустой словарь для частоты игры с товарищами
players = [
    {"name": "Сергей",  "points": 95, "wins": 0, "losses": 0, "color": "red",       "teammate_frequency": {}},
    {"name": "Марина",  "points": 90, "wins": 0, "losses": 0, "color": "purple",    "teammate_frequency": {}},
    {"name": "Ваня",    "points": 85, "wins": 0, "losses": 0, "color": "white",     "teammate_frequency": {}},
    {"name": "Руслан",  "points": 85, "wins": 0, "losses": 0, "color": "brown",     "teammate_frequency": {}},
    {"name": "Настя",   "points": 83, "wins": 0, "losses": 0, "color": "lightblue", "teammate_frequency": {}},
    {"name": "Аскер",   "points": 85, "wins": 0, "losses": 0, "color": "green",     "teammate_frequency": {}},
    {"name": "Саша",    "points": 80, "wins": 0, "losses": 0, "color": "pink",      "teammate_frequency": {}},
    {"name": "Никита",  "points": 80, "wins": 0, "losses": 0, "color": "darkblue",  "teammate_frequency": {}},
    {"name": "Женя",    "points": 85, "wins": 0, "losses": 0, "color": "yellow",    "teammate_frequency": {}},
    {"name": "Егор",    "points": 78, "wins": 0, "losses": 0, "color": "white",     "teammate_frequency": {}},
    {"name": "Тоня",    "points": 85, "wins": 0, "losses": 0, "color": "darkblue",  "teammate_frequency": {}}
]

def get_player_by_name(name):
    return next((p for p in players if p["name"] == name), None)

def update_teammate_frequency(team):
    """
    Обновляет статистику частоты игры с товарищами для всех игроков в команде.
    Для каждой пары игроков в команде увеличиваем счётчик.
    """
    for i in range(len(team)):
        player_a = get_player_by_name(team[i])
        if player_a is None:
            continue
        for j in range(len(team)):
            if i == j:
                continue
            teammate_name = team[j]
            freq = player_a["teammate_frequency"].get(teammate_name, 0)
            player_a["teammate_frequency"][teammate_name] = freq + 1

def get_most_frequent_teammate(player):
    """Возвращает имя товарища, с которым игрок играл чаще всего, или сообщение, если данных нет."""
    freq_dict = player.get("teammate_frequency", {})
    if not freq_dict:
        return "Нет данных"
    most_common = max(freq_dict, key=freq_dict.get)
    return most_common

# --- Страница 1: Лидерборд (сортировка по убыванию очков) ---
def leaderboard_page():
    st.title("Таблица лидеров")
    st.markdown("Нажмите на имя игрока для просмотра профиля.")
    sorted_players = sorted(players, key=lambda x: x["points"], reverse=True)
    
    # Заголовок таблицы
    cols = st.columns([2, 1, 1, 1, 1, 1])
    headers = ["Игрок", "Очки", "Победы", "Поражения", "П/П", "Цвет"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    
    for player in sorted_players:
        row = st.columns([2, 1, 1, 1, 1, 1])
        if row[0].button(player["name"], key="btn_" + player["name"]):
            st.session_state.selected_player = player["name"]
            st.session_state.current_page = "Профиль"
        row[1].write(player["points"])
        row[2].write(player["wins"])
        row[3].write(player["losses"])
        ratio = round(player["wins"] / player["losses"], 2) if player["losses"] != 0 else 0
        row[4].write(ratio)
        row[5].markdown(
            f"<div style='width:20px;height:20px;background-color:{player['color']};'></div>",
            unsafe_allow_html=True
        )
    
    st.write("")
    if st.button("Начать лютый разнос"):
        st.session_state.current_page = "Выбор участников"

# --- Страница 2: Профиль игрока ---
def profile_page():
    st.title("Профиль игрока")
    selected = st.session_state.selected_player
    player = get_player_by_name(selected)
    if player:
        st.subheader(player["name"])
        st.write("Очки:", player["points"])
        st.write("Победы:", player["wins"])
        st.write("Поражения:", player["losses"])
        ratio = round(player["wins"] / player["losses"], 2) if player["losses"] != 0 else 0
        st.write("П/П:", ratio)
        st.write("Чаще всего играет с:", get_most_frequent_teammate(player))
        st.markdown(
            f"<div style='width:50px;height:50px;background-color:{player['color']};'></div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Игрок не найден.")
    
    if st.button("Вернуться на главную"):
        st.session_state.current_page = "Лидерборд"

# --- Страница 3: Выбор участников (ровно 8 игроков) ---
def selection_page():
    st.title("Выберите людей, которых не нужно уговаривать чтобы играть")
    st.write("Выберите ровно 8 игроков для матча.")
    
    selected = st.session_state.selected_players
    for player in players:
        cols = st.columns([2, 1])
        with cols[0]:
            disabled = False
            if player["name"] not in selected and len(selected) >= 8:
                disabled = True
            is_checked = st.checkbox(
                player["name"],
                value=(player["name"] in selected),
                key="select_" + player["name"],
                disabled=disabled
            )
            if is_checked and player["name"] not in selected:
                selected.append(player["name"])
            elif not is_checked and player["name"] in selected:
                selected.remove(player["name"])
        with cols[1]:
            if player["name"] in selected:
                st.markdown("<span style='opacity:0.6'>готов</span>", unsafe_allow_html=True)
    
    st.write("Выбранные игроки:", ", ".join(selected))
    
    if len(selected) != 8:
        st.warning("Для формирования команд требуется ровно 8 игроков.")
    
    if st.button("Подтвердить матч") and len(selected) == 8:
        st.session_state.current_page = "Формирование команд"
        st.session_state.team_assignments = {}
        st.session_state.team1 = []
        st.session_state.team2 = []
    
    if st.button("Вернуться на главную", key="back_from_selection"):
        st.session_state.current_page = "Лидерборд"

# --- Страница 4: Формирование команд (4 на 4) ---
def team_assignment_page():
    st.title("Формирование команд (4 на 4)")
    st.write("Распределите выбранных игроков по командам. Можно перемешать команды или задать вручную.")
    
    if len(st.session_state.selected_players) != 8:
        st.error("Выбранных игроков должно быть ровно 8!")
        return
    
    # Инициализация назначений, если еще не сделана
    for name in st.session_state.selected_players:
        if name not in st.session_state.team_assignments:
            st.session_state.team_assignments[name] = 1  # по умолчанию команда 1
    
    # Кнопка перемешивания – случайное распределение 4 на 4
    if st.button("Перемешать команды"):
        shuffled = st.session_state.selected_players.copy()
        random.shuffle(shuffled)
        for i, name in enumerate(shuffled):
            st.session_state.team_assignments[name] = 1 if i < 4 else 2
    
    st.write("Настройте команды вручную:")
    for name in st.session_state.selected_players:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(name)
        with col2:
            current_team = st.session_state.team_assignments.get(name, 1)
            new_team = st.selectbox("Команда", [1, 2], index=(current_team - 1), key=f"team_select_{name}")
            st.session_state.team_assignments[name] = new_team
    
    # Формирование списков команд
    team1 = [name for name in st.session_state.selected_players if st.session_state.team_assignments[name] == 1]
    team2 = [name for name in st.session_state.selected_players if st.session_state.team_assignments[name] == 2]
    
    st.subheader("Состав команд:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Команда 1:**")
        for name in team1:
            st.write(name)
    with col2:
        st.markdown("**Команда 2:**")
        for name in team2:
            st.write(name)
    
    st.session_state.team1 = team1
    st.session_state.team2 = team2
    
    if st.button("Начать игру"):
        if len(team1) != 4 or len(team2) != 4:
            st.error("Команды должны состоять ровно из 4 игроков каждая!")
        else:
            st.session_state.current_page = "Выбор победителя"
    
    if st.button("Вернуться на главную", key="back_from_team_assignment"):
        st.session_state.current_page = "Лидерборд"

# --- Страница 5: Выбор победителя и обновление статистики ---
def select_winner_page():
    st.title("Выбор победителя")
    team1 = st.session_state.team1
    team2 = st.session_state.team2
    
    if len(team1) != 4 or len(team2) != 4:
        st.error("Команды сформированы некорректно. Проверьте распределение.")
        return
    
    st.subheader("Команда 1:")
    for name in team1:
        st.write(name)
    st.subheader("Команда 2:")
    for name in team2:
        st.write(name)
    
    winner = st.radio("Кто победил?", ("Команда 1", "Команда 2"))
    
    if st.button("Подтвердить результат"):
        if winner == "Команда 1":
            winning_team = team1
            losing_team = team2
        else:
            winning_team = team2
            losing_team = team1
        
        # Обновление статистики для выигравшей команды: +1 победа, +5 очков (не более 100)
        for name in winning_team:
            player = get_player_by_name(name)
            if player:
                player["wins"] += 1
                player["points"] = min(player["points"] + 5, 100)
        # Обновление статистики для проигравшей команды: +1 поражение, -5 очков (не менее 0)
        for name in losing_team:
            player = get_player_by_name(name)
            if player:
                player["losses"] += 1
                player["points"] = max(player["points"] - 5, 0)
        
        # Обновление частоты игры с товарищами для обоих составов
        update_teammate_frequency(winning_team)
        update_teammate_frequency(losing_team)
        
        st.success(f"Результат подтверждён! {winner} победила.")
        
        # Сброс состояния и переход к Лидерборду
        st.session_state.current_page = "Лидерборд"
        st.session_state.selected_players = []
        st.session_state.team_assignments = {}
        st.session_state.team1 = []
        st.session_state.team2 = []
    
    if st.button("Вернуться на главную", key="back_from_winner"):
        st.session_state.current_page = "Лидерборд"

def main():
    if st.session_state.current_page == "Лидерборд":
        leaderboard_page()
    elif st.session_state.current_page == "Профиль":
        profile_page()
    elif st.session_state.current_page == "Выбор участников":
        selection_page()
    elif st.session_state.current_page == "Формирование команд":
        team_assignment_page()
    elif st.session_state.current_page == "Выбор победителя":
        select_winner_page()

if __name__ == "__main__":
    main()


