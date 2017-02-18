# -*- coding: utf-8 -*-

from events.models import Step, Event

__all__ = (
    'EVENT_TYPES_DESCRIPTION',
)

EVENT_SECRET_ALPHABET = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'j', 'k', 'm', 'n', 'p', 'q',
    'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', '2', '3', '4', '5', '6',
    '7', '8', '9'
)

EVENT_SECRET_LENGTH = 6


EVENT_TYPES_DESCRIPTION = {
    Event.TYPE.HIKING: {
        'en': {
            'title': u'Hiking',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Fill in information about trip',
                    'description': u'Fill in useful information about the trip you are planning. It is good to know travel from and to dates, expected weather conditions.',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make list of participants',
                    'description': u'Invite your friends to participate in the trip, create the list of participants. Knowing the number of travellers will help you plan the trip and share duties.',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Assign roles',
                    'description': u'Distribute roles between participants and each one will know how to help while preparation or during the trip. Most common trip roles are : trip organiser, fire keeper, medic, navigator, cook, steward.',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Create route',
                    'description': u'Create your trip\'s route to know what is planned to do and where you are going to be for each day.',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Check weather conditions',
                    'description': u'Knowing weather conditions in your trip\'s region will help you prepare the necessary equipment well.',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.BACKPACK,
                    'title': u'Make list of equipment',
                    'description': u'Create the list of necessary clothes and equipment for your trip regarding weather conditions and participants\' physical state.',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Buy tickets',
                    'description': u'Buy tickets and plan means of transferring your group to the trip\'s starting point and back.',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Create menu',
                    'description': u'Take care of your food during the trip. Prepare a menu regarding the number of participants, trip\'s duration and complexity.',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Buy products',
                    'description': u'Buy foods necessary for the trip.',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Share tents',
                    'description': u'Distribute trip participants in the tents.',
                    'order': 10,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent transfer',
                    'description': u'Take care of renting the transport necessary in the trip.',
                    'order': 11,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Rent accommodation',
                    'description': u'Take care of lodging rent.',
                    'order': 12,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make insurance',
                    'description': u'Take care of your and your group\'s health insurance for the trip.',
                    'order': 13,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Calculate costs',
                    'description': u'Calculate the cost of travel to avoid additional, unplanned expenses.',
                    'order': 14,
                },
            ]
        },
        'ru': {
            'title': u'Пеший поход',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Заполнить информацию о походе',
                    'description': u'Заполните полезную информацию о вашем путешествии. Планируя поход важно знать : где и когда он будет проходить, какую погоду ожидать.',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить список участников',
                    'description': u'Составьте список участников путешествия, пригласите ваших друзей. Участники помогут вам планировать путешествие, разделят обязанности.',
                    'order': 2,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Распределить роли',
                    'description': u'Распределите походные роли между участниками и каждый будет знать, чем он может помочь в процессе подготовки или во время путешествия. Часто используемые роли : руководитель путешествия, костровой, медик, навигатор, повар, завхоз.',
                    'order': 3,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить маршрут',
                    'description': u'Составьте маршрут путешествия так, чтобы знать в какой день где вы будете находиться и чем будете заниматься.',
                    'order': 4,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Узнать погодные условия',
                    'description': u'Знание погодных условий в регионе путешествия поможет правильно подготовить снаряжение.',
                    'order': 5,
                },
                {
                    'type': Step.TYPE.BACKPACK,
                    'title': u'Составить список снаряжения',
                    'description': u'Составьте список одежды и снаряжения для путешествия с учетом погоды и физической подготовки участников.',
                    'order': 6,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Купить билеты',
                    'description': u'Купите билеты и спланируйте способы транспортировки группы к месту начала путешествия и обратно.',
                    'order': 7,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Составить меню',
                    'description': u'Позаботьтесь о питании во время путешествия. Подготовьте меню заранее с учетом количества участников, длительности и сложности пути.',
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
                    'title': u'Распределить по палаткам',
                    'description': u'Распределите участников по палаткам.',
                    'order': 10,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать трансфер',
                    'description': u'Позаботьтесь об аренде транспорта, необходимого в путешествии.',
                    'order': 11,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Арендовать жильё',
                    'description': u'Арендуйте жилье необходимое в путешествии.',
                    'order': 12,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Оформить страховку',
                    'description': u'Застрахуйте себя и вашу группу на время путешествия.',
                    'order': 13,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Подсчитать расходы',
                    'description': u'Рассчитайте расходы на путешествие, чтобы избежать дополнительных, не запланированных трат.',
                    'order': 14,
                },
            ]
        },
    },
    Event.TYPE.JOURNEY: {
        'en': {
            'title': u'Journey',
            'description': u'',
            'steps': [
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Fill in useful information about the trip you are planning. It is good to know travel from and to dates, expected weather conditions.',
                    'description': u'',
                    'order': 1,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Invite your friends to participate in the trip, create the list of participants. Knowing the number of travellers will help you plan the trip and share duties.',
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
                    'description': u'Take care of lodging rent.',
                    'order': 8,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Make insurance',
                    'description': u'Take care of your and your group\'s health insurance for the trip.',
                    'order': 9,
                },
                {
                    'type': Step.TYPE.COMMON,
                    'title': u'Calculate costs',
                    'description': u'Calculate the cost of travel to avoid additional, unplanned expenses.',
                    'order': 10,
                },
            ]
        },
        'ru': {
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
