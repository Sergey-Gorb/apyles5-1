from pathlib import Path
from collections import defaultdict
from pprint import pprint
import functools
import datetime


def decorator_with_arguments(file_log):

    fh = open(Path('.').cwd() / file_log, 'w', encoding='UTF-8')

    def logging(func):
        """
        Декоратор, логирующий работу кода с записью в файл <fh>.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            fh.write(f'call {wrapper.__name__!r} at {datetime.datetime.now()}\n')
            fh.write(f'with args {args}, kwargs {kwargs} ')
            res = func(*args, **kwargs)
            fh.write(f'result ({res})\n')
            return res
        return wrapper
    return logging


@decorator_with_arguments('decor_recipes.log')
def read_to_dict(str_list, dic_f, str_i):

    receipt_name = str_list[str_i].strip()
    receipt_ingr_count = int(str_list[str_i + 1])
    n_o= 2
    for i in range(receipt_ingr_count):
        l_in_s = []
        i_name, i_count, i_m = str_list[str_i + n_o + i].split('|')
        l_in_s.append(str(i_name).strip())
        l_in_s.append(int(i_count))
        l_in_s.append(str(i_m).strip())

        new_dict = {'ingredient_name': l_in_s[0],
                    'quantity': l_in_s[1],
                    'measure': l_in_s[2]}

        dic_f[receipt_name].append(new_dict)
    n_o += receipt_ingr_count
    return n_o


def get_shop_by_dishes(cook_book, *dishes, person=1):
    ingr_dict = defaultdict(dict)
    dish_key = 'ingredient_name'
    quan_key = 'quantity'
    for dish in dishes:
        if dish in cook_book.keys():
            ingrs = cook_book[dish]
            for ingr in ingrs:
                if ingr[dish_key] in ingr_dict.keys():
                    ingr_dict[ingr[dish_key]][quan_key] += int(ingr[quan_key])
                else:
                    new_dict ={quan_key: int(ingr[quan_key]),
                               'measure': ingr['measure']}
                    ingr_dict[ingr[dish_key]] = new_dict
        else:
            print('Неизвестное блюдо',dish)
            return

    if person > 1:
        for ingr in ingr_dict.values():
            ingr[quan_key] *= int(person)
    return ingr_dict


cook_book = defaultdict(list)
p = Path('.')

f_name = p.cwd() / 'recipes.txt'
with open(f_name, 'r', encoding='UTF-8') as f:
    str_list = f.readlines()
    for s_t in str_list:
        if s_t.isspace():
            str_list.remove(s_t)
    len_str_list = len(str_list)
    n_cur = 0
    while n_cur < len_str_list:
        n_r = read_to_dict(str_list, cook_book,n_cur)
        n_cur += n_r
    pprint(cook_book)
    shop_list = get_shop_by_dishes(cook_book, 'Запеченный картофель', 'Омлет', person=2)
    pprint(shop_list)