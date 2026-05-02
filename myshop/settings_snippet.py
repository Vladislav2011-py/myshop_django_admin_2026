from django.conf.global_settings import SESSION_ENGINE, SESSION_COOKIE_AGE, MESSAGE_STORAGE, LOGGING

from myshop.settings import INSTALLED_APPS

LIQPAY_PUBLIC_KEY = 'sandbox_i17489931786'

LIQPAY_PRIVATE_KEY = 'sandbox_000000000000000000'
#LIQPAY_PRIVATE_KEY - треба приховувати у окремий файл (.env)

#True - тестовий режим
#False - реальні платежі
LIQPAY_SANDBOX = True

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400 * 7 # СЕСІЯ ЖИВЕ 7 ДНІВ

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger"
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'class':'logging.StreamHandler',
        },
        'file':{
            'class':'logging.FileHandler',
            'filename': 'payments.log',
        }
    },
    "loggers": {
        'product': {
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    }
}