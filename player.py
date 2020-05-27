import datetime


class Player(object):
    """Class to create Player Data"""
    def __init__(self, steam_id: int):
        """Initiate Player"""
        self._steam_id = int(steam_id)
        self._entity_id = []
        self._game_id = None
        self._name = None
        self._connection_history = []
        self._owning_account = None
        self._spawn_save_entity = []
        self._spawn_history = {}
        self._entity_allowed = None
        self._entity_saved = None
        self._dino = []
        self._player_history = str()
        print(f"Инициализирован экземпляр {steam_id}")

    def new_entity(self, entity_id: int) -> print():
        """Собираем уже имеющиеся данные о истории entityID"""
        self._entity_id.append(entity_id)

    def steam_connect(self, time: datetime.time, steam_id: int):
        """Получение запроса на подключение Steam P2P"""
        self._connection_history.append(f'МСК-{time}| Попытка подключения')
        self._player_history += f'МСК-{time}| Попытка подключения {steam_id}\n'

    def set_game_id(self, game_id: int):
        """Присвоение внутриигрового ID"""
        self._game_id = game_id

    def connection(self, time: datetime.time):
        self._player_history += f'МСК-{time}| Подключение {self._steam_id}\n'

    def steam_disconnect(self, time: datetime.time):
        """Отключение соединения Steam P2P"""
        self._connection_history.append(time)
        self._player_history += f'МСК-{time}| {self._name} |{self._steam_id}| Вышел из игры!\n'
        self._game_id = None

    def set_owning(self, owning_id: int):
        """Устанавлеваем ID владелца"""
        if self._owning_account is not None and self._owning_account != owning_id:
            self._player_history += f'{self._name} перезашел на другой аккаунт! Теперь его айди {owning_id}\n'
        self._owning_account = owning_id
        self._player_history += f'Игроку {self._steam_id} установлен ID владельца {owning_id}\n'

    def find_owning(self, steam_id: int) -> int:
        """Проверяем совпадает ли ID игрока с ID владельца"""
        if self._owning_account is not None and steam_id != self._owning_account:
            return self._owning_account
        return steam_id

    def naming(self, name, time):
        if self._name is not None and self._name != name:
            self._player_history += f'МСК-{time}| Игрок {self._name} сменил ник!\nТеперь он {name}\n'
        self._name = name
        self._player_history += f'МСК-{time}| Игроку {self._steam_id} присвоен никнейм {name}\n'

    """Методы для определения слотов игрока и их содержимого"""
    def set_entity_allowed(self, num: int):
        """Количество слотов у игрока"""
        self._entity_allowed = num

    def set_entity_saved(self, num: int):
        """Количество занятых слотов у игрока"""
        self._entity_saved = num

    def add_dino(self, dino):
        """Дино в слотах игрока"""
        self._dino.append(dino)

    def add_spawn(self, time, spawn):
        """Спавн игрока на дино"""
        self._spawn_history[time] = spawn
        self._player_history += f'МСК-{time}| {self._name} заспавнился на {spawn}\n'

    def player_stat(self):
        self._player_history += f'\t\t\t  {self._name} имеет {self._entity_allowed} слотов\n' \
                                f'\t\t\t  Занято слотов: {self._entity_saved}\n'
        for i in range(len(self._dino)):
            self._player_history += f'\t\t\t  В слоте №{i+1}: {self._dino[i]}\n'
        self._dino = []

    def show(self):
        """Print info about Player"""
        description = f'{self._name} with SteamID:{self._steam_id} and GameID:{self._game_id}'
        print(description)

    def add_command(self, time, cmd):
        self._player_history += f'МСК-{time}| {self._name} прописывает консольную комманду {cmd}\n'

    def add_death(self, time, reason, dino, killer, killer_dino):
        if killer is not None:
            self._player_history += f'МСК-{time}| {self._name} |{self._steam_id}| ' \
                                    f'на {dino} {reason} |{killer}| на {killer_dino}\n'
        else:
            self._player_history += f'МСК-{time}| {self._name} |{self._steam_id}| на {dino} {reason}\n'

    def add_kill(self, time, dino, victim):
        self._player_history += f'МСК-{time}| {self._name} |{self._steam_id}| на своём {dino}, убивает {victim}\n'

    def add_message(self, time, mes_type, message):
        self._player_history += f'МСК-{time}| {self._name} {mes_type}{message}'

    @property
    def player_history(self):
        return self._player_history

    @property
    def game_id(self):
        return self._game_id

    @property
    def steam_id(self):
        return self._steam_id

    @property
    def name(self):
        return self._name
