import streamlit as st

# Инициализация переменных в session_state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Лидерборд"  # главная страница
if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []

# Данные игроков
# Победы (wins) и поражения (losses) по умолчанию 0
players = [
    {"name": "Сергей", "points": 95, "wins": 0, "losses": 0, "frequent": "Марина", "color": "red"},
    {"name": "Марина", "points": 90, "wins": 0, "losses": 0, "frequent": "Сергей", "color": "purple"},
    {"name": "Ваня", "points": 85, "wins": 0, "losses": 0, "frequent": "Руслан", "color": "white"},
    {"name": "Руслан", "points": 85, "wins": 0, "losses": 0, "frequent": "Ваня", "color": "brown"},
    {"name": "Настя", "points": 83, "wins": 0, "losses": 0, "frequent": "Саша", "color": "lightblue"},
    {"name": "Аскер", "points": 85, "wins": 0, "losses": 0, "frequent": "Никита", "color": "green"},
    {"name": "Саша", "points": 80, "wins": 0, "losses": 0, "frequent": "Настя", "color": "pink"},
    {"name": "Никита", "points": 80, "wins": 0, "losses": 0, "frequent": "Аскер", "color": "darkblue"},
    {"name": "Женя", "points": 85, "wins": 0, "losses": 0, "frequent": "Егор", "color": "yellow"},
    {"name": "Егор", "points": 78, "wins": 0, "losses": 0, "frequent": "Женя", "color": "white"},
    {"name": "Тоня", "points": 85, "wins": 0, "losses": 0, "frequent": "Марина", "color": "darkblue"}
]

# ----- Страница ЛИДЕРБОРД -----
def leaderboard_page():
    st.title("Таблица лидеров")
    st.markdown("Нажмите на имя игрока, чтобы перейти в его профиль.")
    
    # Заголовок таблицы
    cols = st.columns([2, 1, 1, 1, 1, 1])
    headers = ["Игрок", "Очки", "Победы", "Поражения", "П/П", "Цвет"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")
    
    # Содержимое таблицы
    for player in players:
        row = st.columns([2, 1, 1, 1, 1, 1])
        # Имя игрока – кнопка
        if row[0].button(player["name"], key="btn_" + player["name"]):
            st.session_state.selected_player = player["name"]
            st.session_state.current_page = "Профиль"
        row[1].write(player["points"])
        row[2].write(player["wins"])
        row[3].write(player["losses"])
        # Защита от деления на ноль
        ratio = round(player["wins"] / player["losses"], 2) if player["losses"] != 0 else 0
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

# ----- Страница ПРОФИЛЬ -----
def profile_page():
    st.title("Профиль игрока")
    selected = st.session_state.selected_player
    player = next((p for p in players if p["name"] == selected), None)
    
    if player:
        st.subheader(player["name"])
        st.write("Очки:", player["points"])
        st.write("Победы:", player["wins"])
        st.write("Поражения:", player["losses"])
        ratio = round(player["wins"] / player["losses"], 2) if player["losses"] != 0 else 0
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

# ----- Страница ВЫБОР УЧАСТНИКОВ -----
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
            st.success("Матч подтвержден! Выбранные игроки: " + ", ".join(selected))
    
    if st.button("Вернуться на главную", key="back_from_selection"):
        st.session_state.current_page = "Лидерборд"

# ----- ЛОГИКА ПЕРЕКЛЮЧЕНИЯ СТРАНИЦ -----
if st.session_state.current_page == "Лидерборд":
    leaderboard_page()
elif st.session_state.current_page == "Профиль":
    profile_page()
elif st.session_state.current_page == "Выбор участников":
    selection_page()

