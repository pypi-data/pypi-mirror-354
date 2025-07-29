"""
Окно активации лицензии
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ..tools.logger import log_info, log_warning, log_error
from ..core.license import activate_license, validate_license
from ..runtime.attempt_counter import add_attempt

class ActivationWindow:
    """Окно активации лицензии"""
    
    def __init__(self, validation_result=None):
        self.validation_result = validation_result
        self.root = None
        self.license_entry = None
        self.status_label = None
        self.activate_button = None
        self.attempts_count = 0
        self.max_attempts = 3
        
    def show(self):
        """Показать окно активации"""
        try:
            self.root = tk.Tk()
            self._setup_window()
            self._create_widgets()
            self._center_window()
            
            log_info("Отображено окно активации лицензии")
            
            # Запускаем главный цикл
            self.root.mainloop()
            
        except Exception as e:
            log_error(f"Ошибка отображения окна активации: {e}")
            self._fallback_console_activation()
    
    def _setup_window(self):
        """Настроить главное окно"""
        self.root.title("Kilopa - Активация лицензии")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Иконка и стиль
        try:
            self.root.iconname("Kilopa")
        except:
            pass
        
        # Настройка стилей
        style = ttk.Style()
        style.theme_use('clam')
        
        # Обработчик закрытия
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_widgets(self):
        """Создать виджеты интерфейса"""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(
            main_frame, 
            text="🔐 Активация лицензии Kilopa",
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Описание
        desc_text = (
            "Для продолжения работы требуется активация лицензии.\n"
            "Введите лицензионный ключ в формате:\n"
            "KLP-XXXX-XXXX-XXXX-XXXX"
        )
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Поле ввода лицензии
        ttk.Label(main_frame, text="Лицензионный ключ:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.license_entry = ttk.Entry(main_frame, width=30, font=("Courier", 10))
        self.license_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        self.license_entry.bind('<Return>', lambda e: self._activate_license())
        self.license_entry.bind('<KeyRelease>', self._on_key_release)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        self.activate_button = ttk.Button(
            button_frame, 
            text="Активировать", 
            command=self._activate_license
        )
        self.activate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_button = ttk.Button(
            button_frame, 
            text="Выход", 
            command=self._on_close
        )
        exit_button.pack(side=tk.LEFT)
        
        # Статус
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        # Информация о попытках
        attempts_text = f"Попыток осталось: {self.max_attempts - self.attempts_count}"
        attempts_label = ttk.Label(main_frame, text=attempts_text, foreground="gray")
        attempts_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Настройка веса столбцов
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Фокус на поле ввода
        self.license_entry.focus()
    
    def _center_window(self):
        """Центрировать окно на экране"""
        try:
            self.root.update_idletasks()
            
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
        except Exception:
            pass
    
    def _on_key_release(self, event):
        """Обработчик нажатия клавиш"""
        try:
            # Форматирование ввода
            current_text = self.license_entry.get().upper()
            
            # Удаляем всё кроме букв и цифр
            clean_text = ''.join(c for c in current_text if c.isalnum())
            
            # Форматируем в блоки по 4 символа
            if len(clean_text) > 0:
                formatted = '-'.join([clean_text[i:i+4] for i in range(0, len(clean_text), 4)])
                
                # Ограничиваем длину
                if len(clean_text) <= 16:  # 4 блока по 4 символа
                    if formatted != current_text:
                        cursor_pos = self.license_entry.index(tk.INSERT)
                        self.license_entry.delete(0, tk.END)
                        self.license_entry.insert(0, formatted)
                        
                        # Восстанавливаем позицию курсора
                        new_pos = min(cursor_pos, len(formatted))
                        self.license_entry.icursor(new_pos)
            
            # Активируем кнопку если ключ полный
            if len(clean_text) == 16:
                self.activate_button.configure(state='normal')
            else:
                self.activate_button.configure(state='disabled')
                
        except Exception as e:
            log_warning(f"Ошибка обработки ввода: {e}")
    
    def _activate_license(self):
        """Активировать лицензию"""
        try:
            license_key = self.license_entry.get().strip()
            
            if not license_key:
                self._show_status("Введите лицензионный ключ", "red")
                return
            
            # Проверяем попытки
            self.attempts_count += 1
            
            if self.attempts_count > self.max_attempts:
                self._show_status("Превышено количество попыток", "red")
                add_attempt('license_activation', False, 'Too many attempts')
                self._on_close()
                return
            
            self._show_status("Проверка лицензии...", "blue")
            self.activate_button.configure(state='disabled')
            self.root.update()
            
            # Записываем попытку
            add_attempt('license_activation', False, f'Attempt {self.attempts_count}')
            
            # Сначала валидируем
            license_obj = validate_license(license_key)
            
            if not license_obj or not license_obj.is_valid:
                error_msg = "Недействительный лицензионный ключ"
                if license_obj and license_obj.errors:
                    error_msg = license_obj.errors[0]
                
                self._show_status(error_msg, "red")
                self.activate_button.configure(state='normal')
                
                log_warning(f"Неудачная попытка активации: {error_msg}")
                return
            
            # Активируем лицензию
            if activate_license(license_key):
                self._show_status("✅ Лицензия успешно активирована!", "green")
                
                # Записываем успешную попытку
                add_attempt('license_activation', True, 'License activated successfully')
                
                log_info("Лицензия успешно активирована через UI")
                
                # Закрываем окно через 2 секунды
                self.root.after(2000, self._close_success)
                
            else:
                self._show_status("Ошибка активации лицензии", "red")
                self.activate_button.configure(state='normal')
                
        except Exception as e:
            log_error(f"Ошибка активации лицензии: {e}")
            self._show_status(f"Ошибка: {e}", "red")
            self.activate_button.configure(state='normal')
    
    def _show_status(self, message, color="black"):
        """Показать статусное сообщение"""
        try:
            self.status_label.configure(text=message, foreground=color)
            self.root.update()
        except Exception:
            pass
    
    def _close_success(self):
        """Закрыть окно после успешной активации"""
        try:
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass
    
    def _on_close(self):
        """Обработчик закрытия окна"""
        try:
            log_info("Окно активации закрыто пользователем")
            
            # Записываем попытку выхода
            add_attempt('activation_window_close', False, 'User closed activation window')
            
            self.root.quit()
            self.root.destroy()
            
            # Завершаем программу
            sys.exit(1)
            
        except Exception:
            sys.exit(1)
    
    def _fallback_console_activation(self):
        """Консольная активация как fallback"""
        try:
            print("\n" + "="*50)
            print("АКТИВАЦИЯ ЛИЦЕНЗИИ KILOPA")
            print("="*50)
            print("Графический интерфейс недоступен.")
            print("Используется консольный режим активации.\n")
            
            for attempt in range(self.max_attempts):
                try:
                    license_key = input(f"Введите лицензионный ключ (попытка {attempt + 1}/{self.max_attempts}): ").strip()
                    
                    if not license_key:
                        print("❌ Ключ не может быть пустым\n")
                        continue
                    
                    print("⏳ Проверка лицензии...")
                    
                    # Записываем попытку
                    add_attempt('console_license_activation', False, f'Console attempt {attempt + 1}')
                    
                    # Валидируем и активируем
                    license_obj = validate_license(license_key)
                    
                    if license_obj and license_obj.is_valid:
                        if activate_license(license_key):
                            print("✅ Лицензия успешно активирована!")
                            add_attempt('console_license_activation', True, 'Console activation successful')
                            return
                        else:
                            print("❌ Ошибка активации лицензии\n")
                    else:
                        error_msg = "Недействительный ключ"
                        if license_obj and license_obj.errors:
                            error_msg = license_obj.errors[0]
                        print(f"❌ {error_msg}\n")
                
                except KeyboardInterrupt:
                    print("\n❌ Активация прервана пользователем")
                    break
                except Exception as e:
                    print(f"❌ Ошибка: {e}\n")
            
            print("❌ Превышено количество попыток активации")
            print("Программа будет закрыта.")
            
        except Exception as e:
            log_error(f"Ошибка консольной активации: {e}")
        
        finally:
            sys.exit(1)

def show_activation_window(validation_result=None):
    """Показать окно активации"""
    try:
        window = ActivationWindow(validation_result)
        window.show()
    except Exception as e:
        log_error(f"Ошибка создания окна активации: {e}")
        sys.exit(1)