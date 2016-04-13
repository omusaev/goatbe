# -*- coding: utf-8 -*-

from events.models import Step, Event

__all__ = (
    'EVENT_TYPES_DESCRIPTION',
)


EVENT_TYPES_DESCRIPTION = {
    Event.TYPE.HIKING: {
        'en_EN': {
            'title': u'Hiking',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Fill in information about trip',
                    'description': u'',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make list of participants',
                    'description': u'',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Assign roles',
                    'description': u'',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Create route',
                    'description': u'',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Check weather conditions',
                    'description': u'',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.BACKPACK,
                    'title': u'Make list of equipment',
                    'description': u'',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Buy tickets',
                    'description': u'',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Create menu',
                    'description': u'',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Buy products',
                    'description': u'',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Share tents',
                    'description': u'',
                    'order': 10,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent transfer',
                    'description': u'',
                    'order': 11,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent accommodation',
                    'description': u'',
                    'order': 12,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make insurance',
                    'description': u'',
                    'order': 13,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Prepare first aid kit',
                    'description': u'',
                    'order': 14,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Calculate costs',
                    'description': u'',
                    'order': 15,
                },
            ]
        },
        'ru_RU': {
            'title': u'Пеший поход',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Заполнить информацию о походе',
                    'description': u'',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить список участников',
                    'description': u'',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Распределить роли',
                    'description': u'',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить маршрут',
                    'description': u'',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Узнать погодные условия',
                    'description': u'',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.BACKPACK,
                    'title': u'Составить список снаряжения',
                    'description': u'',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Купить билеты',
                    'description': u'',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить меню',
                    'description': u'',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Купить продукты',
                    'description': u'',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Разделить по палаткам',
                    'description': u'',
                    'order': 10,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать трансфер',
                    'description': u'',
                    'order': 11,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать жильё',
                    'description': u'',
                    'order': 12,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Оформить страховку',
                    'description': u'',
                    'order': 13,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Подготовить аптечку',
                    'description': u'',
                    'order': 14,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Подсчитать расходы',
                    'description': u'',
                    'order': 15,
                },
            ]
        },
    },
    Event.TYPE.JOURNEY: {
        'en_EN': {
            'title': u'Journey',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Fill in information about trip',
                    'description': u'',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make list of participants',
                    'description': u'',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Assign roles',
                    'description': u'',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Create route',
                    'description': u'',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Check weather conditions',
                    'description': u'',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Buy tickets',
                    'description': u'',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent transfer',
                    'description': u'',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent accommodation',
                    'description': u'',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make insurance',
                    'description': u'',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Calculate costs',
                    'description': u'',
                    'order': 10,
                },
            ]
        },
        'ru_RU': {
            'title': u'Поездка',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Заполнить информацию о поездке',
                    'description': u'',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить список участников',
                    'description': u'',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Распределить роли',
                    'description': u'',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить маршрут',
                    'description': u'',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Узнать погодные условия',
                    'description': u'',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Купить билеты',
                    'description': u'',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать трансфер',
                    'description': u'',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать жильё',
                    'description': u'',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Оформить страховку',
                    'description': u'',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Подсчитать расходы',
                    'description': u'',
                    'order': 10,
                },
            ]
        },
    },
}

EVENT_DATES_FORMAT = '%Y-%m-%d %H:%M:%S'
