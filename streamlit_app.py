import itertools
import random

# Класс игрока с параметрами силы и ограничениями
class Player:
    def __init__(self, name, strength, enemies):
        self.name = name
        self.strength = strength  # Общая сила (суммарный % побед)
        self.enemies = enemies    # Игроки, с которыми нельзя быть в команде (S.A.T.R)
        self.nations = {}         # Статистика выбора наций
        self.wins = 0             # Счётчик побед

    def choose_nation(self):
        # Симулируем выбор нации (пример: 3 варианта)
        nation = random.choice(["Россия", "Франция", "Османская империя"])
        self.nations[nation] = self.nations.get(nation, 0) + 1
        return nation

# Данные игроков (пример)
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

    # Перебираем возможные комбинации с учётом ограничений S.A.T.R
    for combo in itertools.combinations(players, 4):
        team1 = list(combo)
        team2 = [p for p in players if p not in team1]

        # Проверяем ограничения S.A.T.R
        valid = True
        for p in team1:
            for enemy in p.enemies:
                if enemy in [pl.name for pl in team1]:
                    valid = False
        if not valid:
            continue

        # Считаем разницу в силе команд
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
    
    # Вероятность победы команды 1
    prob = (total_str1 / (total_str1 + total_str2)) * 100
    return random.choices([team1, team2], weights=[prob, 100 - prob])[0]

# Запуск симуляции
balanced_teams = balance_teams(players)
if balanced_teams:
    team1, team2 = balanced_teams

    # Выбор наций
    for p in team1 + team2:
        p.choose_nation()

    # Симулируем 10 матчей
    for _ in range(10):
        winner = simulate_match(team1, team2)
        for p in winner:
            p.wins += 1

    # Вывод статистики
    print("Команда 1:", [p.name for p in team1])
    print("Команда 2:", [p.name for p in team2])
    print("\nСтатистика игроков:")
    for p in players:
        print(f"{p.name}:")
        print(f"  Побед: {p.wins}")
        print(f"  Нации: {p.nations}")
else:
    print("Невозможно сбалансировать команды с текущими ограничениями.")
