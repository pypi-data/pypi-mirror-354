# kilopa/config.py
"""Конфигурация Kilopa Protection"""

DEFAULT_CONFIG = {
    'product_id': 'kilopa-protected',
    'demo_time': 60,
    'time_unit': 'seconds',
    'price': 1500,
    'admin_port': 8888,
    'max_demo_operations': 15,
    'silent_mode': False,
    'blocked_functions': ['open'],
}

def update_config(config, updates):
    """Обновление конфигурации безопасным способом"""
    for key, value in updates.items():
        if key in DEFAULT_CONFIG:
            config[key] = value
        else:
            raise ValueError(f"Неизвестный параметр: {key}")

def validate_config(config):
    """Валидация конфигурации"""
    if config['demo_time'] <= 0:
        raise ValueError("demo_time должно быть больше 0")
    
    if config['time_unit'] not in ['seconds', 'minutes', 'hours']:
        raise ValueError("time_unit должно быть 'seconds', 'minutes' или 'hours'")
    
    if config['price'] <= 0:
        raise ValueError("price должно быть больше 0")
    
    if config['admin_port'] < 1024 or config['admin_port'] > 65535:
        raise ValueError("admin_port должен быть между 1024 и 65535")