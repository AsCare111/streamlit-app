<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Leaderboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .leader-table { width: 100%; border-collapse: collapse; }
        .leader-table td, .leader-table th { padding: 12px; border: 1px solid #ddd; }
        .color-box { width: 20px; height: 20px; display: inline-block; }
        .profile { display: none; }
        .nav-button { margin: 10px; padding: 8px 16px; }
        .player-row:hover { background-color: #f5f5f5; cursor: pointer; }
        .selected-players { margin-top: 30px; }
        .ready-text { opacity: 0.5; margin-left: 10px; }
        .resting-text { opacity: 0.5; color: #666; }
    </style>
</head>
<body>
    <!-- Главная страница -->
    <div id="main-page">
        <h1>Лидерборд</h1>
        <table class="leader-table">
            <thead>
                <tr>
                    <th>Игрок</th>
                    <th>Очки</th>
                    <th>Цвет</th>
                    <th>Победы</th>
                    <th>Поражения</th>
                    <th>Соотношение</th>
                </tr>
            </thead>
            <tbody id="leaderboard-body">
                <!-- Данные заполняются скриптом -->
            </tbody>
        </table>
        <button class="nav-button" onclick="showMatchSetup()">Начать лютый разнос</button>
    </div>

    <!-- Страница профиля -->
    <div id="profile-page" class="profile">
        <button class="nav-button" onclick="showMainPage()">Назад</button>
        <div id="profile-content"></div>
    </div>

    <!-- Страница выбора игроков -->
    <div id="match-setup" class="profile">
        <button class="nav-button" onclick="showMainPage()">Назад</button>
        <h2>Выберите участников (максимум 8)</h2>
        <div id="players-list"></div>
    </div>

    <script>
        const players = [
            { name: 'Сергей', points: 95, color: 'red', wins: 20, losses: 5, frequentOpponents: ['Марина', 'Ваня'] },
            { name: 'Марина', points: 90, color: 'purple', wins: 18, losses: 7, frequentOpponents: ['Сергей', 'Ваня'] },
            { name: 'Ваня', points: 85, color: 'white', wins: 15, losses: 10, frequentOpponents: ['Сергей', 'Марина'] },
            // Добавьте остальных игроков по аналогии
        ];

        // Инициализация таблицы лидеров
        function initLeaderboard() {
            const tbody = document.getElementById('leaderboard-body');
            tbody.innerHTML = players.map(player => `
                <tr class="player-row" onclick="showProfile('${player.name}')">
                    <td>${player.name}</td>
                    <td>${player.points}</td>
                    <td><div class="color-box" style="background-color: ${player.color};"></div></td>
                    <td>${player.wins}</td>
                    <td>${player.losses}</td>
                    <td>${(player.wins / player.losses).toFixed(2)}</td>
                </tr>
            `).join('');
        }

        // Показать профиль игрока
        function showProfile(playerName) {
            const player = players.find(p => p.name === playerName);
            document.getElementById('main-page').style.display = 'none';
            document.getElementById('profile-page').style.display = 'block';
            document.getElementById('profile-content').innerHTML = `
                <h2>Профиль ${player.name}</h2>
                <p>Победы: ${player.wins}</p>
                <p>Поражения: ${player.losses}</p>
                <p>Частые соперники: ${player.frequentOpponents.join(', ')}</p>
            `;
        }

        // Навигация
        function showMainPage() {
            document.getElementById('main-page').style.display = 'block';
            document.getElementById('profile-page').style.display = 'none';
            document.getElementById('match-setup').style.display = 'none';
        }

        // Страница выбора игроков
        function showMatchSetup() {
            document.getElementById('main-page').style.display = 'none';
            document.getElementById('match-setup').style.display = 'block';
            const container = document.getElementById('players-list');
            container.innerHTML = players.map(player => `
                <div class="player-item" onclick="togglePlayer(this, '${player.name}')">
                    ${player.name}
                    <span class="ready-text"></span>
                </div>
            `).join('');
        }

        let selectedPlayers = [];
        function togglePlayer(element, playerName) {
            const index = selectedPlayers.indexOf(playerName);
            if (index > -1) {
                selectedPlayers.splice(index, 1);
                element.querySelector('.ready-text').textContent = '';
            } else {
                if (selectedPlayers.length < 8) {
                    selectedPlayers.push(playerName);
                    element.querySelector('.ready-text').textContent = 'готов';
                }
            }
            updatePlayersList();
        }

        function updatePlayersList() {
            document.querySelectorAll('.player-item').forEach(item => {
                const name = item.textContent.replace('готов', '').trim();
                if (!selectedPlayers.includes(name) && selectedPlayers.length >= 8) {
                    item.querySelector('.resting-text')?.remove();
                    item.insertAdjacentHTML('beforeend', '<span class="resting-text">Сегодня отдыхает</span>');
                }
            });
        }

        // Инициализация при загрузке
        window.onload = initLeaderboard;
    </script>
</body>
</html>
