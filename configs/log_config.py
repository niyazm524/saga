log_config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "short",
            "filename": "saga.log"
        },
    },
    'loggers': {
        'saga': {
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
            'propagate': False
        },
        'devices': {
            'handlers': ['console', 'fileHandler'],
            'level': 'ERROR',
        },
    },
}
