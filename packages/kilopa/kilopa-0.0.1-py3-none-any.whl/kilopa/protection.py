# kilopa/protection.py - Исправленная версия для Windows
import os
import json
import time
import sys
import threading
import subprocess
from pathlib import Path
from datetime import datetime

class ProtectionManager:
    """Тихий менеджер системы защиты - исправленная Windows версия"""
    
    def __init__(self, config):
        self.config = config.copy()
        self.config['silent_mode'] = True
        
        if self.config['time_unit'] == 'minutes':
            self.demo_seconds = self.config['demo_time'] * 60
        elif self.config['time_unit'] == 'hours':
            self.demo_seconds = self.config['demo_time'] * 3600
        else:
            self.demo_seconds = self.config['demo_time']
        
        self.data_file = Path.home() / f".{self.config['product_id']}_license.json"
        self.user_data = None
        self.operations_count = 0
        self.status_window_process = None
        self.registration_done = False
        
        self._load_user_data()
        self._check_license_status()
        self._start_protection_interface()
    
    def _silent_register_new_user(self):
        """Тихая регистрация пользователя без вывода в основную консоль"""
        import secrets
        
        random_names = ["User", "Player", "Guest", "Client", "Tester"]
        import random
        nickname = random.choice(random_names) + str(random.randint(1000, 9999))
        
        self.user_data = {
            'nickname': nickname,
            'user_id': secrets.token_hex(4).upper(),
            'registration_date': time.time(),
            'demo_started': time.time(),
            'full_license': False,
            'blocked': False,
            'operations_count': 0,
            'product_id': self.config['product_id']
        }
        
        self._save_user_data(self.user_data)
        self.registration_done = True
    
    def _create_status_window_script(self):
        """Создание скрипта для окна статуса"""
        script_content = f'''
import time
import os
import sys
import json
from datetime import datetime
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_license_file():
    data_file = Path.home() / ".{self.config['product_id']}_license.json"
    try:
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return None

def main():
    while True:
        try:
            user_data = check_license_file()
            
            if not user_data:
                clear_screen()
                print("❌ Системная ошибка")
                time.sleep(5)
                break
            
            if user_data.get('full_license'):
                clear_screen()
                print("╔═══════════════════════════════════════════════════════════════╗")
                print("║                    ✅ СИСТЕМА АКТИВНА                         ║")
                print("║                   Полный доступ разрешен                      ║")
                print("╚═══════════════════════════════════════════════════════════════╝")
                print()
                print("🎉 Все функции доступны!")
                print("🚀 Система работает без ограничений")
                print()
                print("💡 Это окно закроется через 10 секунд...")
                time.sleep(10)
                break
            
            demo_start = user_data.get('demo_started', time.time())
            demo_seconds = {self.demo_seconds}
            demo_end_timestamp = demo_start + demo_seconds
            demo_end_date = datetime.fromtimestamp(demo_end_timestamp)
            
            time_left = max(0, demo_end_timestamp - time.time())
            total_ops = user_data.get('operations_count', 0)
            max_ops = {self.config['max_demo_operations']}
            ops_left = max(0, max_ops - total_ops)
            
            clear_screen()
            
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%d.%m.%Y")
            
            print("╔═══════════════════════════════════════════════════════════════╗")
            print("║                   📊 СИСТЕМНЫЙ МОНИТОР                        ║")
            if time_left > 0:
                print("║                    ПРОБНАЯ ВЕРСИЯ АКТИВНА                     ║")
            else:
                print("║                     ПРОБНЫЙ ПЕРИОД ИСТЕК                      ║")
            print("╚═══════════════════════════════════════════════════════════════╝")
            print()
            print(f"👤 Пользователь: {{user_data.get('nickname', 'Unknown')}}")
            print(f"🆔 ID сессии: {{user_data.get('user_id', 'Unknown')}}")
            print(f"🕐 Текущее время: {{current_time}}")
            print(f"📅 Дата: {{current_date}}")
            print()
            print("─" * 63)
            
            if time_left > 0:
                if {self.config['time_unit'] == 'hours'}:
                    hours = int(time_left // 3600)
                    minutes = int((time_left % 3600) // 60)
                    seconds = int(time_left % 60)
                    time_str = f"{{hours:02d}}:{{minutes:02d}}:{{seconds:02d}}"
                elif {self.config['time_unit'] == 'minutes'}:
                    minutes = int(time_left // 60)
                    seconds = int(time_left % 60)
                    time_str = f"{{minutes:02d}}:{{seconds:02d}}"
                else:
                    time_str = f"{{int(time_left)}} сек"
                
                print(f"⏰ Время сессии: {{time_str}}")
                print(f"📅 Истекает: {{demo_end_date.strftime('%d.%m.%Y в %H:%M:%S')}}")
                print(f"🔢 Операций доступно: {{ops_left}}")
                print()
                
                total_demo_time = demo_seconds
                elapsed_time = total_demo_time - time_left
                progress = min(40, int((elapsed_time / total_demo_time) * 40))
                
                print("⏳ Прогресс времени:")
                print("┌" + "─" * 42 + "┐")
                bar = "█" * progress + "░" * (40 - progress)
                percentage = min(100, int((elapsed_time / total_demo_time) * 100))
                print(f"│{{bar}}│ {{percentage:3d}}%")
                print("└" + "─" * 42 + "┘")
                print()
                
                used_ops = max_ops - ops_left
                ops_progress = min(40, int((used_ops / max_ops) * 40))
                
                print("🔢 Использование ресурсов:")
                print("┌" + "─" * 42 + "┐")
                ops_bar = "█" * ops_progress + "░" * (40 - ops_progress)
                ops_percentage = min(100, int((used_ops / max_ops) * 100))
                print(f"│{{ops_bar}}│ {{ops_percentage:3d}}%")
                print("└" + "─" * 42 + "┘")
                print()
            else:
                print("❌ ПРОБНЫЙ ПЕРИОД ИСТЕК!")
                print("🔒 Система ограничена")
                print("💳 Требуется активация полной версии")
                print()
            
            print("─" * 63)
            print(f"💰 Стоимость полной версии: {self.config.get('price', 1500)}₽")
            print(f"🌐 Активация: http://localhost:{self.config['admin_port']}/pay?userId={{user_data['user_id']}}&product={self.config['product_id']}")
            print()
            print("📊 Мониторинг обновляется автоматически")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)
            break

if __name__ == "__main__":
    main()
'''
        
        # Используем нормальное имя файла без точки в начале
        temp_script = Path.home() / f"kilopa_monitor_{self.config['product_id'].replace('-', '_')}.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return temp_script
    
    def _start_status_window(self):
        """Запуск окна мониторинга в отдельной консоли - исправленная Windows версия"""
        try:
            script_path = self._create_status_window_script()
            
            if os.name == 'nt':  # Windows
                # Исправленная команда для Windows
                cmd = f'start "System Monitor" cmd /c "python "{script_path}" & del "{script_path}" & pause"'
                self.status_window_process = subprocess.Popen(cmd, shell=True)
            else:  # Linux/Mac
                try:
                    cmd = ['gnome-terminal', '--title=System Monitor', '--', 'python3', str(script_path)]
                    self.status_window_process = subprocess.Popen(cmd)
                except FileNotFoundError:
                    try:
                        cmd = ['xterm', '-title', 'System Monitor', '-e', f'python3 {script_path}']
                        self.status_window_process = subprocess.Popen(cmd)
                    except FileNotFoundError:
                        pass
            
            return True
            
        except Exception as e:
            print(f"Ошибка создания окна: {e}")
            return False
    
    def _load_user_data(self):
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.user_data = json.load(f)
        except:
            self.user_data = None
    
    def _save_user_data(self, data):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.user_data = data
        except:
            pass
    
    def _check_license_status(self):
        if not self.user_data:
            self._silent_register_new_user()
        elif self.user_data.get('blocked'):
            sys.exit(1)
    
    def _start_protection_interface(self):
        """Запуск интерфейса защиты"""
        if not self.is_licensed():
            # Запускаем окно мониторинга через 2 секунды
            threading.Timer(2.0, self._start_status_window).start()
    
    def _check_if_blocked(self):
        """Тихая проверка блокировки"""
        if self.is_licensed():
            return False
            
        demo_start = self.user_data.get('demo_started', time.time()) if self.user_data else time.time()
        demo_end = demo_start + self.demo_seconds
        time_left = demo_end - time.time()
        
        if time_left <= 0:
            return True
            
        total_ops = (self.user_data.get('operations_count', 0) if self.user_data else 0) + self.operations_count
        if total_ops >= self.config['max_demo_operations']:
            return True
            
        return False
    
    def _increment_operation(self):
        if not self.is_licensed():
            self.operations_count += 1
            
            if self.operations_count % 3 == 0 and self.user_data:
                self.user_data['operations_count'] = self.user_data.get('operations_count', 0) + self.operations_count
                self._save_user_data(self.user_data)
                self.operations_count = 0
    
    def _cleanup(self):
        """Тихая очистка при выходе"""
        if self.user_data and self.operations_count > 0:
            self.user_data['operations_count'] = self.user_data.get('operations_count', 0) + self.operations_count
            self._save_user_data(self.user_data)
        
        if self.status_window_process:
            try:
                self.status_window_process.terminate()
            except:
                pass
        
        # Удаляем временные файлы
        try:
            temp_script = Path.home() / f"kilopa_monitor_{self.config['product_id'].replace('-', '_')}.py"
            if temp_script.exists():
                temp_script.unlink()
        except:
            pass
    
    def is_licensed(self):
        self._load_user_data()
        return self.user_data and self.user_data.get('full_license', False)
    
    def get_demo_info(self):
        if not self.user_data:
            return {'licensed': False, 'time_left': 0, 'operations_left': 0, 'user_id': 'Unknown'}
        
        if self.is_licensed():
            return {'licensed': True, 'time_left': float('inf'), 'operations_left': float('inf'), 'user_id': self.user_data.get('user_id', 'Unknown')}
        
        demo_start = self.user_data.get('demo_started', time.time())
        demo_end = demo_start + self.demo_seconds
        time_left = max(0, demo_end - time.time())
        
        total_ops = self.user_data.get('operations_count', 0) + self.operations_count
        ops_left = max(0, self.config['max_demo_operations'] - total_ops)
        
        return {
            'licensed': False,
            'time_left': time_left,
            'operations_left': ops_left,
            'user_id': self.user_data.get('user_id', 'Unknown')
        }
    
    def get_user_info(self):
        if not self.user_data:
            return None
        
        return {
            'nickname': self.user_data.get('nickname', 'Unknown'),
            'user_id': self.user_data.get('user_id', 'Unknown'),
            'registration_date': self.user_data.get('registration_date'),
            'full_license': self.user_data.get('full_license', False),
            'blocked': self.user_data.get('blocked', False),
            'product_id': self.user_data.get('product_id', self.config['product_id'])
        }
    
    def update_config(self, new_config):
        self.config.update(new_config)