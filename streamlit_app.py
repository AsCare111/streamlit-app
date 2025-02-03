import json
import numpy as np
import pandas as pd
import streamlit as st
from itertools import combinations

DATA_FILE = "players_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

players_data = load_data()
players = list(players_data.keys())

def calculate_strengths(data):
    strengths = {}
    for player, stats in data.items():
        total_wins = sum(stats["wins"].values())
        strengths[player] = np.log1p(total_wins) * 100 / max(1, np.log1p(max(total_wins, 1)))
    return strengths

player_strengths = calculate_strengths(players_data)

satr_constraints = [
    ("Сережа", "Марина"),
    ("Ваня", "Руслан"),
    ("Аскер", "Настя"),
    ("Никита", "Саша")
]

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

st.title("Балансировщик команд для Казаки 3")

if best_teams:
    st.subheader("Сбалансированные команды")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Команда A")
        for player in best_teams[0]:
            st.write(f"- {player} ({round(player_strengths[player], 2)} очков)")
    with col2:
        st.write("### Команда B")
        for player in best_teams[1]:
            st.write(f"- {player} ({round(player_strengths[player], 2)} очков)")

st.subheader("Статистика игроков")
selected_player = st.selectbox("Выберите игрока", players)

if selected_player:
    st.write(f"### {selected_player}")
    st.write(f"**Очки:** {round(player_strengths[selected_player], 2)}")
    st.write("**Победы против игроков:**")
    for opponent, wins in players_data[selected_player]["wins"].items():
        st.write(f"- {opponent}: {wins} побед")
    st.write(f"**Чаще всего играет за:** {players_data[selected_player]['nation']}")

st.subheader("Добавить победу")
winner = st.selectbox("Кто победил?", players)
loser = st.selectbox("Кого победил?", players)

if winner and loser and winner != loser:
    if st.button("Добавить результат"):
        players_data[winner]["wins"][loser] = players_data[winner]["wins"].get(loser, 0) + 1
        save_data(players_data)
        st.success("Результат добавлен!")
