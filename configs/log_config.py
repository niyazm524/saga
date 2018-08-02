log_config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "datefmt": "[%d/%m/%Y %H:%M:%S]"
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
        "fileHandler": {
            "level": "NOTSET",
            "class": "logging.FileHandler",
            "formatter": "short",
            "filename": "saga.log"
        },
        "reqHandler": {
            "level": "NOTSET",
            "class": "logging.FileHandler",
            "formatter": "short",
            "filename": "requests.log"
        },
    },
    'loggers': {
        'werkzeug': {
            'handlers': ['console', 'reqHandler'],
            'level': 'DEBUG'
        },
        'Main': {
            'handlers': ['console', 'fileHandler'],
            'level': 'DEBUG',
        },
        'quest': {
            'handlers': ['console', 'fileHandler'],
            'level': 'DEBUG',
        },
        'observer': {
            'handlers': ['console', 'fileHandler'],
            'level': 'DEBUG',
        },
        'devices': {
            'handlers': ['console', 'fileHandler'],
            'level': 'DEBUG',
        },
    },
}
