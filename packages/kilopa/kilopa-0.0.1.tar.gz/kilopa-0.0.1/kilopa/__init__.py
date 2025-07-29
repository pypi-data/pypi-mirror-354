# kilopa/__init__.py - Исправленная безопасная версия
"""
🛡️ Kilopa Protection - Невидимая система защиты Python приложений
"""

__version__ = "2.1.1"
__author__ = "KilopaDev"
__email__ = "dev@kilopa.com"
__license__ = "MIT"

import os
import sys
import time
import threading
import builtins
import inspect
from pathlib import Path

# Импортируем основные компоненты
from .config import DEFAULT_CONFIG, update_config
from .protection import ProtectionManager

# ============================================================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ============================================================================

_protection_manager = None
_is_initialized = False
_config = DEFAULT_CONFIG.copy()

# Сохраняем оригинальные функции
_original_input = builtins.input
_original_open = builtins.open
_original_eval = builtins.eval
_original_exec = builtins.exec

# ============================================================================
# БЕЗОПАСНЫЕ ЗАЩИЩЕННЫЕ ФУНКЦИИ
# ============================================================================

def _is_system_call():
    """Проверка, вызывается ли функция системными модулями"""
    import inspect
    
    frame = inspect.currentframe()
    try:
        # Поднимаемся по стеку вызовов
        while frame:
            filename = frame.f_code.co_filename
            # Разрешаем системные модули Python и библиотеки
            if any(path in filename for path in [
                'site-packages',
                'Python313\\Lib',
                'python3.',
                '/usr/lib/python',
                'importlib',
                'flask',
                'werkzeug',
                'threading',
                'multiprocessing'
            ]):
                return True
            frame = frame.f_back
    except:
        pass
    finally:
        del frame
    
    return False

def _protected_input(*args, **kwargs):
    """Безопасная защищенная версия input"""
    # Разрешаем системные вызовы
    if _is_system_call():
        return _original_input(*args, **kwargs)
        
    if _protection_manager and not _protection_manager.is_licensed():
        if _protection_manager._check_if_blocked():
            return ""
        _protection_manager._increment_operation()
    return _original_input(*args, **kwargs)

def _protected_open(*args, **kwargs):
    """Безопасная защищенная версия open"""
    # Разрешаем системные вызовы
    if _is_system_call():
        return _original_open(*args, **kwargs)
        
    if _protection_manager and not _protection_manager.is_licensed():
        mode = 'r'
        if len(args) > 1:
            mode = args[1]
        elif 'mode' in kwargs:
            mode = kwargs['mode']
        
        if any(m in mode for m in ['w', 'a', 'x', '+']):
            if _protection_manager._check_if_blocked():
                raise PermissionError("Доступ ограничен")
            else:
                raise PermissionError("Функция недоступна")
    
    return _original_open(*args, **kwargs)

def _protected_eval(*args, **kwargs):
    """Безопасная защищенная версия eval"""
    # Разрешаем системные вызовы
    if _is_system_call():
        return _original_eval(*args, **kwargs)
        
    if _protection_manager and not _protection_manager.is_licensed():
        if _protection_manager._check_if_blocked():
            raise RuntimeError("Операция недоступна")
        _protection_manager._increment_operation()
    return _original_eval(*args, **kwargs)

def _protected_exec(*args, **kwargs):
    """Безопасная защищенная версия exec"""
    # ВСЕГДА разрешаем системные вызовы для exec!
    if _is_system_call():
        return _original_exec(*args, **kwargs)
        
    # Только блокируем пользовательские вызовы exec
    if _protection_manager and not _protection_manager.is_licensed():
        if _protection_manager._check_if_blocked():
            raise RuntimeError("Функция заблокирована")
        else:
            raise RuntimeError("Функция недоступна")
    return _original_exec(*args, **kwargs)

# ============================================================================
# ПУБЛИЧНЫЕ ФУНКЦИИ API
# ============================================================================

def configure(**kwargs):
    """Настройка параметров защиты"""
    global _config
    update_config(_config, kwargs)
    
    if _protection_manager:
        _protection_manager.update_config(_config)

def is_licensed():
    """Проверка статуса лицензии"""
    if _protection_manager:
        return _protection_manager.is_licensed()
    return False

def get_demo_info():
    """Получение информации о демо-периоде"""
    if _protection_manager:
        return _protection_manager.get_demo_info()
    return {'licensed': False, 'time_left': 0, 'operations_left': 0, 'user_id': 'Unknown'}

def get_user_info():
    """Получение информации о пользователе"""
    if _protection_manager:
        return _protection_manager.get_user_info()
    return None

def start_admin_server(port=None):
    """Запуск админ-сервера вручную"""
    from .admin_server import start_server
    
    if port:
        _config['admin_port'] = port
    
    start_server(_config['admin_port'])

def protect_function(func_name="функция"):
    """Декоратор для защиты функций"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_licensed():
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ============================================================================
# ВНУТРЕННИЕ ФУНКЦИИ (ПОЛНОСТЬЮ ТИХИЕ)
# ============================================================================

def _initialize_protection():
    """Тихая инициализация системы защиты"""
    global _protection_manager, _is_initialized
    
    if _is_initialized:
        return
    
    try:
        # Создаем менеджер защиты в тихом режиме
        _config['silent_mode'] = True
        # Увеличиваем время демо для тестирования
        if _config['demo_time'] < 5:
            _config['demo_time'] = 5  # Минимум 5 минут
            
        _protection_manager = ProtectionManager(_config)
        _is_initialized = True
        
        # Заменяем системные функции на безопасные защищенные версии
        builtins.input = _protected_input
        builtins.open = _protected_open
        builtins.eval = _protected_eval
        builtins.exec = _protected_exec
        
    except Exception:
        # Тихо игнорируем ошибки
        pass

def _get_caller_info():
    """Получение информации о вызывающем модуле"""
    import inspect
    
    frame = inspect.currentframe()
    try:
        while frame:
            filename = frame.f_code.co_filename
            if not any(part in filename for part in ['kilopa', 'importlib', 'site-packages']):
                return {'filename': os.path.basename(filename), 'directory': os.path.dirname(filename)}
            frame = frame.f_back
    except:
        pass
    finally:
        del frame
    
    return {'filename': 'unknown', 'directory': ''}

def _auto_initialize():
    """Автоматическая тихая инициализация при импорте"""
    caller_info = _get_caller_info()
    
    if caller_info['filename'] != 'unknown':
        base_name = os.path.splitext(caller_info['filename'])[0]
        if _config['product_id'] == DEFAULT_CONFIG['product_id']:
            _config['product_id'] = f"kilopa-{base_name}"
    
    # Запускаем инициализацию в отдельном потоке с задержкой
    def delayed_init():
        time.sleep(0.5)  # Даем всем модулям загрузиться
        _initialize_protection()
    
    threading.Thread(target=delayed_init, daemon=True).start()

def _cleanup():
    """Тихая очистка при выходе программы"""
    global _protection_manager
    
    if _protection_manager:
        _protection_manager._cleanup()
    
    # Восстанавливаем оригинальные функции
    try:
        builtins.input = _original_input
        builtins.open = _original_open
        builtins.eval = _original_eval
        builtins.exec = _original_exec
    except:
        pass

# Регистрируем тихую очистку при выходе
import atexit
atexit.register(_cleanup)

# Запускаем тихую автоинициализацию при импорте
_auto_initialize()

# ============================================================================
# ЭКСПОРТ ПУБЛИЧНЫХ ФУНКЦИЙ
# ============================================================================

__all__ = [
    'configure',
    'is_licensed', 
    'get_demo_info',
    'get_user_info',
    'start_admin_server',
    'protect_function',
    '__version__'
]

# Алиасы для удобства
licensed = is_licensed
demo_info = get_demo_info
user_info = get_user_info
protect = protect_function
is_full_version = is_licensed
is_demo = lambda: not is_licensed()