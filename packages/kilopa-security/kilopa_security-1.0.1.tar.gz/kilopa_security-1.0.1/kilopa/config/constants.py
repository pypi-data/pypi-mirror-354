"""
Константы для системы защиты Kilopa
"""

# Общие настройки
VERSION = "1.0.0"
LIBRARY_NAME = "kilopa"

# Формат лицензионного ключа
LICENSE_FORMAT = r"^KLP-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
LICENSE_LENGTH = 24  # включая дефисы

# Криптография
RSA_KEY_SIZE = 2048
AES_KEY_SIZE = 256
SIGNATURE_ALGORITHM = 'SHA-256'

# Публичный ключ RSA для проверки подписей (в реальной системе должен быть встроен)
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2J6tB8v2Y9x5K3mR7wQ8
vN4uL9kX3jF2hU8dS6cT1pQ9rE4yI7xN2vK5mL8oP3qR4sT6uV9wX1yZ2aB3cD4e
F5gH6iJ7kL8mN9oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH1iJ2kL3mN4oP5qR6sT7u
V8wX9yZ1aB2cD3eF4gH5iJ6kL7mN8oP9qR1sT2uV3wX4yZ5aB6cD7eF8gH9iJ1k
L2mN3oP4qR5sT6uV7wX8yZ9aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT1uV2wX3yZ4a
B5cD6eF7gH8iJ9kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD1eF2gH3iJ4kL5mN6oP7q
R8sT9uV1wX2yZ3aB4cD5eF6gH7iJ8kL9mN1oP2qR3sT4uV5wX6yZ7aB8cD9eF1g
QIDAQAB
-----END PUBLIC KEY-----"""

# Сетевые настройки
API_BASE_URL = "https://api.kilopa.security"
IP_CHECK_SERVICES = [
    "https://api.ipify.org",
    "https://httpbin.org/ip",
    "https://ifconfig.me/ip"
]

# Файловые пути
LICENSE_FILE = "kilopa.lic"
CONFIG_FILE = "kilopa.cfg"
LOG_FILE = "kilopa.log"
TEMP_DIR = ".kilopa_temp"

# Лимиты и таймауты
MAX_WARNINGS = 3
MAX_ATTEMPTS = 5
NETWORK_TIMEOUT = 10  # секунд
VALIDATION_TIMEOUT = 30  # секунд

# Сообщения UI
MESSAGES = {
    'activation_required': 'Необходима активация лицензии',
    'license_expired': 'Срок действия лицензии истёк',
    'device_banned': 'Устройство заблокировано',
    'ip_banned': 'IP-адрес заблокирован',
    'too_many_attempts': 'Превышено количество попыток',
    'tamper_detected': 'Обнаружена попытка взлома',
    'time_rollback': 'Обнаружен откат системного времени',
    'license_revoked': 'Лицензия отозвана'
}

# Коды состояний
STATUS_CODES = {
    'SUCCESS': 0,
    'LICENSE_REQUIRED': 1,
    'LICENSE_EXPIRED': 2,
    'DEVICE_BANNED': 3,
    'IP_BANNED': 4,
    'LICENSE_REVOKED': 5,
    'TAMPER_DETECTED': 6,
    'TIME_ROLLBACK': 7,
    'NETWORK_ERROR': 8,
    'CRITICAL_ERROR': 9
}

# Системные события
EVENTS = {
    'APP_START': 'application_start',
    'LICENSE_CHECK': 'license_validation',
    'HWID_CHECK': 'hardware_validation',
    'IP_CHECK': 'ip_validation',
    'WARNING_ADDED': 'warning_added',
    'USER_BANNED': 'user_banned',
    'TAMPER_ATTEMPT': 'tamper_attempt',
    'TIME_ANOMALY': 'time_anomaly'
}

# Антиотладочные настройки
DEBUG_DETECTION = {
    'check_debugger': True,
    'check_profiler': True,
    'check_tracer': True,
    'fake_responses': True
}