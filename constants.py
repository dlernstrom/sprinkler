GALLONS_PER_CLICK = 10
GPIO_PIN = 10
BOUNCE_TIME = 300

NUMATO_USER = 'admin'
NUMATO_PASS = 'admin'
NUMATO_IP = '10.0.0.44'
SHARES_OWNED = 4
HOUR = 60

GALLONS_ALLOC_PER_MIN_PER_SHARE = 10
GALLONS_PER_MIN_ALLOC = SHARES_OWNED * GALLONS_ALLOC_PER_MIN_PER_SHARE
MINUTES_ALLOC = 12 * HOUR  # currently, it's 12 hours, twice a week
TURN_GALLONS_ALLOC = MINUTES_ALLOC * GALLONS_PER_MIN_ALLOC

WATERING_TIME_HOURS = 12

ZONES_CREATED = {
    31: 'Sprinkler 1',  # V
    30: 'Sprinkler 2',  # U
    29: 'Park East',  # T
    28: 'Tardis',  # S
    27: 'Sprinkler 3',  # R
    26: 'Park West',  # Q
    25: 'The Point',  # P
    24: 'Coop',  # O
    # 23: 'BAD',  # N
    22: 'North Corner',  # M
}
ZONES_INT_LIST = list(ZONES_CREATED.keys())
ZONES_USED = [chr(55 + key) for key in ZONES_INT_LIST]
SIMULTANEOUS_ZONES = 2

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    '': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
