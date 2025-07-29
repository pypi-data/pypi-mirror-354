# tests/test_kilopa.py
import pytest
import kilopa

def test_import():
    """Тест успешного импорта"""
    assert hasattr(kilopa, 'configure')
    assert hasattr(kilopa, 'is_licensed')
    assert hasattr(kilopa, 'get_demo_info')

def test_configure():
    """Тест конфигурации"""
    kilopa.configure(
        product_id="test-app",
        demo_time=30,
        silent_mode=True
    )
    assert True

def test_demo_info():
    """Тест получения информации о демо"""
    info = kilopa.get_demo_info()
    assert 'licensed' in info
    assert 'time_left' in info
    assert 'operations_left' in info

def test_protect_decorator():
    """Тест декоратора защиты"""
    @kilopa.protect_function("test")
    def test_func():
        return "works"
    
    # В демо версии должен вернуть None
    result = test_func()
    assert result is None  # Потому что не лицензировано

def test_version():
    """Тест версии"""
    assert hasattr(kilopa, '__version__')
    assert kilopa.__version__ == '1.0.0'

if __name__ == "__main__":
    pytest.main([__file__])