import json
import numpy as np
import streamlit as st
import pandas as pd
import time
import subprocess
import sys

# Установка matplotlib, если он отсутствует
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt

DATA_FILE = "players_data.json"
MATCH_HISTORY_FILE = "match_history.json"

def load_data(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

players_data = load_data(DATA_FILE)
match_history = load_data(MATCH_HISTORY_FILE)
players = list(players_data.keys())

def calculate_strengths():
    base_strengths = {
        "Сережа": 100,
        "Марина": 85,
        "Ваня": 70,
        "Аскер": 65,
        "Настя": 60,
        "Руслан": 75,
        "Никита": 55,
        "Саша": 50
    }
    return base_strengths

player_strengths = calculate_strengths()

satr_constraints = [
    ("Сережа", "Марина"),
    ("Ваня", "Руслан"),
    ("Аскер", "Настя"),
    ("Никита", "Саша")
]

nations = [
    "Австрия", "Алжир", "Англия", "Бавария", "Венгрия", "Венеция", "Дания", "Испания", "Нидерланды", "Польша",
    "Португалия", "Пруссия", "Россия", "Саксония", "Турция", "Украина", "Франция", "Швеция", "Шотландия", "Пьемонт"
]

def generate_balanced_teams():
    from itertools import combinations
    all_combinations = list(combinations(players, 4))
    valid_combinations = []
    
    for team_a in all_combinations:
        team_b = tuple(set(players) - set(team_a))
        if all((p1 in team_a and p2 in team_b) or (p1 in team_b and p2 in team_a) for p1, p2 in satr_constraints):
            valid_combinations.append((team_a, team_b))

    min_diff = float("inf")
    best_teams = None
    
    for team_a, team_b in valid_combinations:
        strength_a = sum(player_strengths[p] for p in team_a)
        strength_b = sum(player_strengths[p] for p in team_b)
        diff = abs(strength_a - strength_b)
        if diff < min_diff:
            min_diff = diff
            best_teams = (team_a, team_b)
    
    return best_teams

st.title("Балансировщик команд для Казаки 3")

if st.button("Перемешать составы"):
    best_teams = generate_balanced_teams()
else:
    best_teams = generate_balanced_teams()

if best_teams:
    st.subheader("Сбалансированные команды")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Команда A")
        for player in best_teams[0]:
            st.write(f"- {player} ({player_strengths[player]} очков)")
    with col2:
        st.write("### Команда B")
        for player in best_teams[1]:
            st.write(f"- {player} ({player_strengths[player]} очков)")

    fig, ax = plt.subplots()
    ax.bar(["Команда A", "Команда B"], [sum(player_strengths[p] for p in best_teams[0]), sum(player_strengths[p] for p in best_teams[1])])
    st.pyplot(fig)

st.subheader("Статистика игроков")
selected_player = st.selectbox("Выберите игрока", players)

if selected_player:
    st.write(f"### {selected_player}")
    st.write(f"**Очки:** {player_strengths[selected_player]}")
    st.write("**Победы против игроков:**")
    for opponent, wins in players_data.get(selected_player, {}).get("wins", {}).items():
        st.write(f"- {opponent}: {wins} побед")
    nation = st.selectbox("Выберите нацию для игрока", nations, index=nations.index(players_data.get(selected_player, {}).get("nation", "Австрия")))
    players_data[selected_player]['nation'] = nation
    save_data(players_data, DATA_FILE)
    st.write(f"**Выбранная нация:** {nation}")

st.subheader("История матчей")
if match_history:
    match_df = pd.DataFrame(match_history)
    st.table(match_df.tail(10))

st.subheader("Добавить победу")
winner = st.selectbox("Кто победил?", players)
loser = st.selectbox("Кого победил?", players)

if winner and loser and winner != loser:
    if st.button("Добавить результат"):
        players_data.setdefault(winner, {}).setdefault("wins", {})[loser] = players_data[winner]["wins"].get(loser, 0) + 1
        save_data(players_data, DATA_FILE)
        match_history.append({"Победитель": winner, "Проигравший": loser})
        save_data(match_history, MATCH_HISTORY_FILE)
        st.success("Результат добавлен!")

if st.button("Начать матч"):
    st.write("Матч начинается через 60 секунд...")
    for i in range(60, 0, -1):
        st.write(f"Осталось времени: {i} секунд")
        time.sleep(1)
    st.write("Матч начался!")
