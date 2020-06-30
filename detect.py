import datetime
import re


def hour_detect(a: str) -> int:
    """ перевод времени на мск, надо найти способ получше """
    if int(a) + 3 > 23:
        if int(a) + 2 > 23:
            if int(a) + 1 > 23:
                a = 2
            else:
                a = 1
        else:
            a = 0
    else:
        a = int(a) + 3.
    return int(a)


def time_detect(a: str) -> datetime.time:
    """Определяет время только в стандартных строках, на начальных строках выдаст ошибку"""
    time = a[1:20].split('-')
    hour, minutes, sec = time[1].split(':')[0].split('.')
    time = datetime.time(hour_detect(hour), int(minutes), int(sec))
    # return f'\nМСК-{str(time)} | '
    return time


def death_reason_detect(line):
    if re.search(r'Вы были убиты', line):
        killer_name = line[re.search(r'Вы были убиты', line).end():re.search(r', Dead Player Name:', line).start()]
        return f'Убит игроком:{killer_name}'
    elif re.search(r'Переродился', line):
        return 'Переродился'
    elif re.search(r'Смертельное падение', line):
        return 'Разбился'
    elif re.search(r'Вы умерли от удара молнией', line):
        return 'Умер от удара молнии'
    elif re.search(r'Вы умерли от сильного стресса', line):
        return 'Умер от сильного стресса'
