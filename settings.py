from os import environ
import os

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
environ.__setitem__('OTREE_PRODUCTION','0') ################
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': ""
    }

"""dict(
        name='hl_mpl',
        display_name='Risk Lottery',
        num_demo_participants=10,
        app_sequence=['hl_mpl'],
        num_choices=8,
        multiplier=10,
    ),"""

SESSION_CONFIGS = [

    {
        'name':'CTB',
        'display_name': 'encuesta',
        'num_demo_participants':1,
        'app_sequence': ['CTB'],
        'Rounds':None,
        'doc':"""
        """
    },
    {
        'name':'otdm_master',
        'display_name': 'otdm',
        'num_demo_participants':1,
        'app_sequence': ['otdm_master'],
        'Rounds':None,
        'doc':"""
        """
    },
    {
        'name': 'mpl',
        'display_name': 'MultiplePriceList (Holt/Laury)',
        'num_demo_participants': 1,
        'app_sequence': ['mpl']
    },
    {
        'name': 'otime',
        'display_name': 'otime',
        'num_demo_participants': 1,
        'app_sequence': ['otime']
    },
    {
        'name': 'BRET',
        'display_name': 'BRET',
        'num_demo_participants': 1,
        'app_sequence': ['BRET']
    },
    {
        'name': 'torneo',
        'display_name': 'Juego de encriptación',
        'num_demo_participants': 4,
        'app_sequence': ['torneo'],
        'observabilidad': False,
        'meritocracia': False,
    }

]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'Ferley Rincon'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'jtq+07qbt-tvcu(si_j6-&2m2x-*d6btl0qbwss*(pkv6l#$p0'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

#variables to otdm game
#: The total number of weeks
NUM_WEEKS = 52

#: The gain to be paid out per week
GAIN_PER_WEEK = 20
	
STATIC_URL = '/static/'