import streamlit as st

# Инициализируем состояние текущей страницы, если оно ещё не задано
if "current_page" not in st.session_state:
    st.session_state.current_page = "Главная"

# Список страниц для навигации
pages = ["Главная", "Профиль", "Выбор участников"]

# Отображаем боковую панель с выбором страницы
selected_page = st.sidebar.selectbox("Навигация", pages, index=pages.index(st.session_state.current_page))
st.session_state.current_page = selected_page

# Пример данных игроков
players = [
    {
        "name": "Сергей",
        "points": 95,
        "color": "red",
        "wins": 20,
        "losses": 5,
        "frequentOpponents": ["Марина", "Ваня"]
    },
    {
        "name": "Марина",
        "points": 90,
        "color": "blue",
        "wins": 18,
        "losses": 7,
        "frequentOpponents": ["Сергей", "Игорь"]
    },
    {
        "name": "Игорь",
        "points": 80,
        "color": "green",
        "wins": 15,
        "losses": 10,
        "frequentOpponents": ["Сергей", "Марина"]
    }
]

# Страница "Главная" – таблица лидеров
if st.session_state.current_page == "Главная":
    st.title("Таблица лидеров")
    data = []
    for player in players:
        # Вычисляем соотношение побед/поражений
        win_loss_ratio = round(player["wins"] / player["losses"], 2) if player["losses"] != 0 else player["wins"]
        data.append({
            "Игрок": player["name"],
            "Очки": player["points"],
            "Победы": player["wins"],
            "Поражения": player["losses"],
            "П/П": win_loss_ratio,
            "Цвет": player["color"]
        })
    st.table(data)
    
    # Кнопка для перехода на страницу выбора участников
    if st.button("Начать лютый разнос"):
        st.session_state.current_page = "Выбор участников"
        st.experimental_rerun()

# Страница "Профиль" – просмотр профиля игрока
elif st.session_state.current_page == "Профиль":
    st.title("Профиль игрока")
    player_name = st.text_input("Введите имя игрока для просмотра профиля")
    if player_name:
        # Ищем игрока по имени (без учёта регистра)
        player = next((p for p in players if p["name"].lower() == player_name.lower()), None)
        if player:
            st.subheader(player["name"])
            st.write("Очки:", player["points"])
            st.write("Победы:", player["wins"])
            st.write("Поражения:", player["losses"])
            st.write("Частые соперники:", ", ".join(player["frequentOpponents"]))
        else:
            st.error("Игрок не найден!")

# Страница "Выбор участников" – выбор игроков для матча
elif st.session_state.current_page == "Выбор участников":
    st.title("Выбор участников матча")
    max_players = 8
    if "selected_players" not in st.session_state:
        st.session_state.selected_players = []

    # Для каждого игрока создаём чекбокс с соответствующей надписью
    for player in players:
        is_selected = player["name"] in st.session_state.selected_players

        if is_selected:
            label = f"{player['name']} — готов"
        elif len(st.session_state.selected_players) >= max_players:
            label = f"{player['name']} — Сегодня отдыхает"
        else:
            label = player["name"]

        # Разрешаем выбор, если игрок уже выбран или лимит ещё не достигнут
        if is_selected or len(st.session_state.selected_players) < max_players:
            if st.checkbox(label, value=is_selected, key=player["name"]):
                if player["name"] not in st.session_state.selected_players:
                    st.session_state.selected_players.append(player["name"])
            else:
                if player["name"] in st.session_state.selected_players:
                    st.session_state.selected_players.remove(player["name"])
        else:
            st.checkbox(label, value=False, key=player["name"], disabled=True)

    st.write("Выбрано:", st.session_state.selected_players)
    if st.button("Подтвердить матч"):
        if len(st.session_state.selected_players) == 0:
            st.error("Выберите хотя бы одного игрока!")
        else:
            st.success("Матч подтвержден! Выбранные игроки: " + ", ".join(st.session_state.selected_players))

