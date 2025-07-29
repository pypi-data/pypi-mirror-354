# -*- coding, utf-8 -*-
# coding=utf-8
"""
additional language support for python-dateutil lib
see http//stackoverflow.com/questions/8896038/
    how-to-use-python-dateutil-1-5-parse-function-to-work-with-unicode

TODO, create separated package of this python-dateutil-language
"""

# noinspection SpellCheckingInspection

MONTHS = {
    # russian
    'Января': 'January',
    'Февраля': 'February',
    'Марта': 'March',
    'Апреля': 'April',
    'Мая': 'May',
    'Июня': 'June',
    'Июля': 'July',
    'Августа': 'August',
    'Сентября': 'September',
    'Октября': 'October',
    'Ноября': 'November',
    'Декабря': 'December',

    'Янв': 'January',
    'Февр': 'February',
    'Март': 'March',
    'Апр': 'April',
    'Май': 'May',
    'Июнь': 'June',
    'Июль': 'July',
    'Авг': 'August',
    'Сент': 'September',
    'Окт': 'October',
    'Нояб': 'November',
    'Дек': 'December',

    # ukranian
    'Січня': 'January',
    'Лютого': 'February',
    'Березня': 'March',
    'Квітня': 'April',
    'Травня': 'May',
    'Червня': 'June',
    'Липня': 'July',
    'серпня': 'August',
    'Вересня': 'September',
    'Жовтня': 'October',
    'Листопада': 'November',
    'Грудня': 'December',

    'Січень': 'January',
    'Лютий': 'February',
    'Березень': 'March',
    'Квітень': 'April',
    'Травень': 'May',
    'Червень': 'June',
    'Липень': 'July',
    'Серпень': 'August',
    'Вересень': 'September',
    'Жовтень': 'October',
    'Листопад': 'November',
    'Грудень': 'December',

    # romanian
    'ianuarie': 'January',
    'februarie': 'February',
    'martie': 'March',
    'aprilie': 'April',
    'mai': 'May',
    'iunie': 'June',
    'iulie': 'July',
    'august': 'August',
    'septembrie': 'September',
    'octombrie': 'October',
    'noiembrie': 'November',
    'decembrie': 'December',

    'ian.': 'January'
}


for foreign, eng in dict(MONTHS).items():
    MONTHS[foreign.lower()] = eng
    MONTHS[foreign.lower()] = eng
    MONTHS[foreign.capitalize()] = eng
