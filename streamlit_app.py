import streamlit as st
import itertools
import random

# Класс игрока
class Player:
    def __init__(self, name, strength, enemies):
        self.name = name
        self.strength = strength
        self.enemies = enemies
        self.nations = {}
        self.wins = 0

    def choose_nation(self):
        nation = random.choice(["Россия", "Франция", "Османская империя"])
        self.nations[nation] = self.nations.get(nation, 0) + 1
        return nation

# Данные игроков
players_data = {
    "Сережа": {"strength": 95, "enemies": ["Марина"]},
    "Марина": {"strength": 85, "enemies": ["Сережа", "Ваня"]},
    "Ваня": {"strength": 70, "enemies": ["Руслан"]},
    "Руслан": {"strength": 65, "enemies": ["Ваня"]},
    "Аскер": {"strength": 68, "enemies": ["Настя"]},
    "Настя": {"strength": 62, "enemies": ["Аскер"]},
    "Никита": {"strength": 58, "enemies": ["Саша"]},
    "Саша": {"strength": 55, "enemies": ["Никита"]},
}

# Создаём объекты игроков
players = [Player(name, data["strength"], data["enemies"]) for name, data in players_data.items()]

# Функция балансировки команд
def balance_teams(players):
    best_diff = float('inf')
    best_teams = None

    for combo in itertools.combinations(players, 4):
        team1 = list(combo)
        team2 = [p for p in players if p not in team1]

        valid = True
        for p in team1:
            for enemy in p.enemies:
                if enemy in [pl.name for pl in team1]:
                    valid = False
        if not valid:
            continue

        sum1 = sum(p.strength for p in team1)
        sum2 = sum(p.strength for p in team2)
        diff = abs(sum1 - sum2)

        if diff < best_diff:
            best_diff = diff
            best_teams = (team1, team2)

    return best_teams

# Симуляция матча
def simulate_match(team1, team2):
    total_str1 = sum(p.strength for p in team1)
    total_str2 = sum(p.strength for p in team2)
    prob = (total_str1 / (total_str1 + total_str2)) * 100
    return random.choices([team1, team2], weights=[prob, 100 - prob])[0]

# Интерфейс Streamlit
st.title("Казаки 3: Балансировка команд и симуляция матчей")

# Кнопка для балансировки команд
if st.button("Сбалансировать команды"):
    balanced_teams = balance_teams(players)
    if balanced_teams:
        team1, team2 = balanced_teams

        # Вывод команд
        st.subheader("Команда 1:")
        st.write([p.name for p in team1])
        st.subheader("Команда 2:")
        st.write([p.name for p in team2])

        # Симуляция матчей
        st.subheader("Симуляция матчей")
        num_matches = st.slider("Количество матчей", 1, 20, 10)
        for _ in range(num_matches):
            winner = simulate_match(team1, team2)
            for p in winner:
                p.wins += 1

        # Вывод статистики
        st.subheader("Статистика игроков")
        for p in players:
            st.write(f"**{p.name}**:")
            st.write(f"  Побед: {p.wins}")
            st.write(f"  Нации: {p.nations}")
    else:
        st.error("Невозможно сбалансировать команды с текущими ограничениями.")
