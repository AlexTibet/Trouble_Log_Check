import re
import io
from player import Player
import log_patterns as pattern
from detect import time_detect, death_reason_detect

players = {}


def check_all_player(filename, check_id=None):
    game_id = 255
    with io.open(filename, 'r', encoding='utf-8') as log:
        for line in log:
            # проходим по известным взаимосвязям entityID и steamID
            if re.search(pattern.entity, line):
                entity_id, steam_id = line[re.search(pattern.entity, line).end():].split('and player')
                entity_id, steam_id = int(entity_id.strip()), int(steam_id.strip())
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                players[steam_id].new_entity(entity_id)
            # ловим попытки подключения
            elif re.search(pattern.steam_connect, line):
                time = time_detect(line)
                steam_id = int(line[re.search(pattern.steam_connect, line).end():].split()[0].strip())
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                players[steam_id].steam_connect(time, steam_id)
                if players[steam_id].game_id is None:
                    game_id += 1
                    players[steam_id].set_game_id(game_id)

    with io.open(filename, 'r', encoding='utf-8') as log:
        for line in log:
            # для игрового айди
            if re.search(pattern.for_game_id, line):
                time = time_detect(line)
                # game_id += 1
                steam_id = int(line[re.search(pattern.for_game_id, line).end():].split(':')[-2].strip())
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                if players[steam_id].game_id is None:
                    game_id += 1
                    players[steam_id].set_game_id(game_id)
            # успешное подключение ?
            elif re.search(pattern.registered, line):
                time = time_detect(line)
                steam_id = int(line.split(':')[-1].split()[2])
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                if players[steam_id].game_id is None:
                    game_id += 1
                    players[steam_id].set_game_id(game_id)
            # вытягиваем данные о слотах и дино
            elif re.search(pattern.new_profile, line):
                time = time_detect(line)
                owning_id, steam_id = line[re.search(pattern.new_profile, line).end():].split('| Owning account ID')
                owning_id, steam_id = int(owning_id.strip()), int(steam_id.strip())
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                players[steam_id].set_owning(time, owning_id)
                steam_id = players[steam_id].find_owning(steam_id)
                # проход по следующим строчкам для определения содержимого слотов
                for next_line in log:
                    if re.search(pattern.en_allowed, next_line):
                        players[steam_id].set_entity_allowed(int(next_line.split('=')[1]))
                    elif re.search(pattern.sav_allowed, next_line):
                        players[steam_id].set_entity_saved(int(next_line.split('=')[1]))
                        if int(next_line.split('=')[1]) == 0:
                            break
                    elif re.search(r'{', next_line):
                        gender = next_line.split('=')[-1].strip()
                        growth = log.__next__().split('=')[-1].strip()
                        dino_type = log.__next__().split('=')[-1].strip()
                        dino = f'{dino_type}, Рост: {growth[:5]} ({gender})'
                        players[steam_id].add_dino(dino)
                    elif re.search(pattern.end_slots, next_line):
                        break
            # успешное подключение с присвоением внутриигрового ID, никнейма, и выводом инфо о слотах
            elif re.search(pattern.connect_start, line):
                time = time_detect(line)
                nik_name, steam_id = line[re.search(pattern.connect_start, line).end():].strip().split('with ID')
                nik_name, steam_id = nik_name.strip(), int(steam_id.strip())
                if steam_id not in players.keys():
                    players[steam_id] = Player(steam_id)
                players[steam_id].connection(time)
                players[steam_id].naming(nik_name, time)
                players[steam_id].player_stat(time)
            # информация о спавнах и сменах слотов
            elif re.search(pattern.spawned_saved_entity, line):
                time = time_detect(line)
                s_entity, steam_id = line[re.search(pattern.spawned_saved_entity, line).end():].split('owning account')
                s_entity, steam_id = int(s_entity.strip().strip(',')), int(steam_id.strip())
                steam_id = players[steam_id].find_owning(steam_id)

                # ищем в следующих строчках на ком игрок заспавнился
                for next_line in log:
                    if re.search(pattern.spawn, next_line):
                        try:
                            time = time_detect(next_line)
                        except IndexError:
                            continue
                        spawn = next_line[re.search(pattern.spawn, next_line).end():].strip()
                        players[steam_id].add_spawn(time, spawn)
                        break
            elif re.search(pattern.ret_in_slots, line):
                dino = line[re.search(pattern.ret_in_slots, line).end():].strip()
                for player in players.values():
                    if player._spawn_history == dino:
                        time = time_detect(line)
                        player.add_ret_in_slots(time)
            # консольные комманды
            elif re.search(pattern.user_command, line):
                time = time_detect(line)
                steam_id = int(line[re.search(pattern.user_command, line).end():].split('|')[-3].replace('ID=', '').strip())
                cmd = line.split('|')[-1].strip()[:-1]
                players[steam_id].add_command(time, cmd)
            # выход из игры или потеря соединения
            elif re.search(pattern.disconnect, line):
                time = time_detect(line)
                steam_id = int(line.split(':')[-1].split()[0])
                players[steam_id].steam_disconnect(time)
            # смерти
            elif re.search(pattern.death, line):
                time = time_detect(line)
                reason = death_reason_detect(line)
                steam_id, dino, growth = line.split(r'Dead Player ID:')[-1].split(',')
                steam_id = int(steam_id.strip())
                dino = dino.replace('Dead Player Creature:', '').strip()
                growth = growth.replace('Dead Player Growth:', '').strip()
                dino = f'{dino} {growth[:5]}'
                if reason in pattern.death_reasons:
                    players[steam_id].add_death(time, reason, dino, None, None)
                else:
                    killer_info = log.__next__()
                    k_id, k_dino, k_growth = killer_info[re.search(r'Killing Player ID', killer_info).end():].split(',')
                    k_id = int(k_id.strip())
                    k_dino = k_dino.replace('Killing Player Creature:', '').strip()
                    k_growth = k_growth.replace('Killing Player Growth:', '').strip()
                    k_dino = f'{k_dino} {k_growth[:5]}'
                    victim = f'{players[steam_id].name} |{steam_id}| на {dino}'
                    players[steam_id].add_death(time, reason, dino, k_id, k_dino)
                    players[k_id].add_kill(time, k_dino, victim)
            elif re.search(pattern.global_message, line):
                time = time_detect(line)
                steam_id, message = line[re.search(pattern.global_message, line).end():].split('|| Msg:')
                steam_id = int(steam_id.split('[')[-1].replace(']', '').strip())
                players[steam_id].add_message(time, 'в Глобал чат:        ', message)
            elif re.search(pattern.private_message, line):
                time = time_detect(line)
                steam_id, message = line[re.search(pattern.private_message, line).end():].split('|| Msg:')
                steam_id = int(steam_id.split('[')[-1].replace(']', '').strip())
                players[steam_id].add_message(time, 'в ЛС/Групп/Локал чат:', message)
    return generate_output(check_id)


def generate_output(check_id):
    if check_id is None:
        output = ''
        global_history = {}
        for player in players.values():
            for time, history in player.player_history.items():
                if time not in global_history.keys():
                    global_history[time] = ''.join(history)
                else:
                    global_history[time] += ''.join(history)
            player.clear_player_info()
        a = sorted(global_history.keys())
        for i in a:
            output += ''.join(global_history[i])
        return output
    else:
        output = ''
        for time, history in players[int(check_id.strip())].player_history.items():
            output += ''.join(history)
        for player in players.values():
            player.clear_player_info()
    return output
