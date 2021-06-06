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

ZONES_USED = ['V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M']

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
