import streamlit as st
import random

# ----- Глобальные настройки -----

# Инициализация переменных в session_state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Лидерборд"  # Начальная страница
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []
if 'team_assignments' not in st.session_state:
    st.session_state.team_assignments = {}  # Словарь {playerName: 1 или 2}
if 'team1' not in st.session_state:
    st.session_state.team1 = []
if 'team2' not in st.session_state:
    st.session_state.team2 = []
if 'winner_team' not in st.session_state:
    st.session_state.winner_team = None

# Список всех возможных «страниц» в нашем приложении
PAGES = {
    "Лидерборд": "leaderboard_page",
    "Профиль": "profile_page",
    "Выбор участников": "selection_page",
    "Формирование команд": "team_assignment_page",
    "Выбор победителя": "select_winner_page",
}

# ----- Данные игроков -----
# Очки заданы, а победы/поражения (wins/losses) изначально 0
players = [
    {"name": "Сергей",  "points": 95, "wins": 0, "losses": 0, "frequent": "Марина", "color": "red"},
    {"name": "Марина",  "points": 90, "wins": 0, "losses": 0, "frequent": "Сергей", "color": "purple"},
    {"name": "Ваня",    "points": 85, "wins": 0, "losses": 0, "frequent": "Руслан", "color": "white"},
    {"name": "Руслан",  "points": 85, "wins": 0, "losses": 0, "frequent": "Ваня",   "color": "brown"},
    {"name": "Настя",   "points": 83, "wins": 0, "losses": 0, "frequent": "Саша",   "color": "lightblue"},
    {"name": "Аскер",   "points": 85, "wins": 0, "losses": 0, "frequent": "Никита", "color": "green"},
    {"name": "Саша",    "points": 80, "wins": 0, "losses": 0, "frequent": "Настя",  "color": "pink"},
    {"name": "Никита",  "points": 80, "wins": 0, "losses": 0, "frequent": "Аскер",  "color": "darkblue"},
    {"name": "Женя",    "points": 85, "wins": 0, "losses": 0, "frequent": "Егор",   "color": "yellow"},
    {"name": "Егор",    "points": 78, "wins": 0, "losses": 0, "frequent": "Женя",   "color": "white"},
    {"name": "Тоня",    "points": 85, "wins": 0, "losses": 0, "frequent": "Марина", "color": "darkblue"}
]

def get_player_by_name(name):
    """Вспомогательная функция для поиска игрока в списке players по имени."""
    return next((p for p in players if p["name"] == name), None)

# ----- Страница 1: ЛИДЕРБОРД -----
def leaderboard_page():
    st.title("Таблица лидеров")
    st.markdown("Нажмите на имя игрока, чтобы перейти в его профиль.")
    
    # Шапка таблицы
    cols = st.columns([2, 1, 1, 1, 1, 1])
    headers = ["Игрок", "Очки", "Победы", "Поражения", "П/П", "Цвет"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    
    # Содержимое таблицы
    for player in players:
        row = st.columns([2, 1, 1, 1, 1, 1])
        # Кнопка с именем для перехода в профиль
        if row[0].button(player["name"], key="btn_" + player["name"]):
            st.session_state.selected_player = player["name"]
            st.session_state.current_page = "Профиль"
        # Очки, победы, поражения
        row[1].write(player["points"])
        row[2].write(player["wins"])
        row[3].write(player["losses"])
        # Соотношение побед/поражений
        ratio = 0
        if player["losses"] != 0:
            ratio = round(player["wins"] / player["losses"], 2)
        row[4].write(ratio)
        # Цветной квадратик
        row[5].markdown(
            f"<div style='width:20px;height:20px;background-color:{player['color']};'></div>",
            unsafe_allow_html=True
        )
    
    st.write("")
    # Кнопка для перехода на страницу выбора участников
    if st.button("Начать лютый разнос"):
        st.session_state.current_page = "Выбор участников"

# ----- Страница 2: ПРОФИЛЬ ИГРОКА -----
def profile_page():
    st.title("Профиль игрока")
    selected = st.session_state.selected_player
    player = get_player_by_name(selected)
    
    if player:
        st.subheader(player["name"])
        st.write("Очки:", player["points"])
        st.write("Победы:", player["wins"])
        st.write("Поражения:", player["losses"])
        ratio = 0
        if player["losses"] != 0:
            ratio = round(player["wins"] / player["losses"], 2)
        st.write("П/П:", ratio)
        st.write("Чаще всего играет с:", player["frequent"])
        st.markdown(
            f"<div style='width:50px;height:50px;background-color:{player['color']};'></div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Игрок не найден.")
    
    if st.button("Вернуться на главную"):
        st.session_state.current_page = "Лидерборд"

# ----- Страница 3: ВЫБОР УЧАСТНИКОВ -----
def selection_page():
    st.title("Выберите людей, которых не нужно уговаривать чтобы играть")
    st.write("Выберите до 8 игроков.")
    
    max_players = 8
    selected = st.session_state.selected_players
    
    # Отрисовка списка игроков
    for player in players:
        cols = st.columns([2, 1])
        with cols[0]:
            # Если игрок не выбран и лимит выбранных достигнут, чекбокс блокируется
            disabled = False
            if player["name"] not in selected and len(selected) >= max_players:
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
            elif len(selected) >= max_players:
                st.markdown("<span style='opacity:0.6'>Сегодня отдыхает</span>", unsafe_allow_html=True)
            else:
                st.write("")
    
    st.write("Выбранные игроки:", ", ".join(selected))
    
    if st.button("Подтвердить матч"):
        if len(selected) == 0:
            st.error("Выберите хотя бы одного игрока!")
        else:
            # Переходим на страницу формирования команд
            st.session_state.current_page = "Формирование команд"
            # Сбросим/очистим предыдущие назначения команд, если были
            st.session_state.team_assignments = {}
            st.session_state.team1 = []
            st.session_state.team2 = []

    if st.button("Вернуться на главную", key="back_from_selection"):
        st.session_state.current_page = "Лидерборд"

# ----- Страница 4: ФОРМИРОВАНИЕ КОМАНД -----
def team_assignment_page():
    st.title("Формирование команд")
    st.write("Распределите выбранных игроков по командам. Можно перемешивать или расставить вручную.")

    # Если нет выбранных игроков, вернёмся на выбор участников
    if len(st.session_state.selected_players) == 0:
        st.warning("Нет выбранных игроков. Вернёмся на предыдущий шаг.")
        st.session_state.current_page = "Выбор участников"
        return

    # Инициализируем назначение команды (1 или 2) для каждого игрока, если ещё не сделано
    for name in st.session_state.selected_players:
        if name not in st.session_state.team_assignments:
            st.session_state.team_assignments[name] = 1  # По умолчанию команда 1

    # Кнопка перемешать – случайно раскидывает игроков по командам
    if st.button("Перемешать команды"):
        for name in st.session_state.selected_players:
            st.session_state.team_assignments[name] = random.choice([1, 2])

    # Отрисовка списка игроков с селектбоксом
    for name in st.session_state.selected_players:
        col1, col2 = st.columns([2,1])
        with col1:
            st.write(name)
        with col2:
            current_team = st.session_state.team_assignments[name]
            new_team = st.selectbox(
                "Команда",
                [1, 2],
                index=(current_team - 1),
                key=f"team_select_{name}"
            )
            st.session_state.team_assignments[name] = new_team

    st.write("")

    # Кнопка "Начать игру" – формируем списки команд и переходим на выбор победителя
    if st.button("Начать игру"):
        team1 = [n for n in st.session_state.selected_players if st.session_state.team_assignments[n] == 1]
        team2 = [n for n in st.session_state.selected_players if st.session_state.team_assignments[n] == 2]
        st.session_state.team1 = team1
        st.session_state.team2 = team2

        # Если одна из команд пуста, предупредим
        if len(team1) == 0 or len(team2) == 0:
            st.error("Одна из команд пуста! Распределите хотя бы по одному игроку в каждую команду.")
        else:
            st.session_state.current_page = "Выбор победителя"

    if st.button("Вернуться на главную", key="back_from_team_assignment"):
        st.session_state.current_page = "Лидерборд"

# ----- Страница 5: ВЫБОР ПОБЕДИТЕЛЯ -----
def select_winner_page():
    st.title("Выбор победителя")
    team1 = st.session_state.team1
    team2 = st.session_state.team2

    # Если нет команд, вернёмся на страницу формирования
    if len(team1) == 0 or len(team2) == 0:
        st.warning("Команды не сформированы. Вернёмся на предыдущий шаг.")
        st.session_state.current_page = "Формирование команд"
        return

    st.subheader("Команда 1:")
    st.write(", ".join(team1))

    st.subheader("Команда 2:")
    st.write(", ".join(team2))

    # Радиокнопка для выбора победителя
    winner = st.radio("Кто победил?", ("Команда 1", "Команда 2"))
    
    if st.button("Подтвердить результат"):
        if winner == "Команда 1":
            # Команда 1 получает +1 к победам, Команда 2 +1 к поражениям
            for pName in team1:
                p = get_player_by_name(pName)
                if p:
                    p["wins"] += 1
            for pName in team2:
                p = get_player_by_name(pName)
                if p:
                    p["losses"] += 1
        else:
            # Команда 2 победила
            for pName in team2:
                p = get_player_by_name(pName)
                if p:
                    p["wins"] += 1
            for pName in team1:
                p = get_player_by_name(pName)
                if p:
                    p["losses"] += 1

        # После обновления статистики возвращаемся на Лидерборд
        st.success(f"Результат подтверждён! {winner} победила.")
        st.session_state.current_page = "Лидерборд"

    if st.button("Вернуться на главную", key="back_from_winner"):
        st.session_state.current_page = "Лидерборд"

# ----- ЛОГИКА ПЕРЕКЛЮЧЕНИЯ СТРАНИЦ -----
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

