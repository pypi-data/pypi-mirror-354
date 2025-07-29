"""
Основная логика offline-ai
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.syntax import Syntax
import re

from .config import config
from .ollama_client import ollama_client

console = Console()

class OfflineAI:
    """Основной класс приложения"""
    
    def __init__(self):
        self.history: List[dict] = []
        self.max_history = config.get("ui.max_history", 100)
        self.show_timestamps = config.get("ui.show_timestamps", True)
        self.streaming_mode = config.get("ui.streaming_mode", True)  # По умолчанию показываем в реальном времени
        self.load_history()
        self.optimize_context_for_model()
    
    def load_history(self):
        """Загрузка истории разговоров"""
        try:
            if config.history_file.exists():
                with open(config.history_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-self.max_history:]:
                        if line.strip():
                            try:
                                import json
                                entry = json.loads(line.strip())
                                self.history.append(entry)
                            except:
                                continue
        except Exception as e:
            console.print(f"⚠️  Ошибка загрузки истории: {e}", style="yellow")
    
    def save_to_history(self, user_message: str, ai_response: str):
        """Сохранение в историю"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response
        }
        
        self.history.append(entry)
        
        # Ограничиваем размер истории
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # Сохраняем в файл
        try:
            with open(config.history_file, 'a', encoding='utf-8') as f:
                import json
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            console.print(f"⚠️  Ошибка сохранения истории: {e}", style="yellow")

    def optimize_context_for_model(self):
        """Автоматическая оптимизация контекста для текущей модели"""
        from .ollama_client import ollama_client

        current_model = ollama_client.model
        recommended_models = config.get("models.recommended", [])

        # Ищем настройки для текущей модели
        for model_info in recommended_models:
            if isinstance(model_info, dict) and model_info.get("name") == current_model:
                optimal_context = model_info.get("optimal_context_messages", 8)

                # Обновляем настройку только если она не была изменена пользователем
                current_context = config.get("ui.max_context_messages", 8)
                if current_context == 8 or current_context == 10:  # Значения по умолчанию
                    config.set("ui.max_context_messages", optimal_context)
                    console.print(f"🎯 Контекст оптимизирован для модели {current_model}: {optimal_context} сообщений",
                                style="blue")
                break
    
    def setup(self, auto_install: bool = False) -> bool:
        """Первоначальная настройка"""
        console.print(Panel.fit(
            "🤖 Добро пожаловать в offline-ai!\n"
            "Локальный ИИ-ассистент для терминала",
            title="Offline AI",
            style="blue"
        ))

        # Проверяем и запускаем Ollama
        if not ollama_client.is_ollama_running():
            if not ollama_client.start_ollama():
                return False

        # Проверяем наличие модели
        models = ollama_client.list_models()
        if not models:
            console.print("📦 Модели не найдены.", style="yellow")

            if auto_install:
                # Автоматически загружаем рекомендуемую модель
                demo_model = config.get("models.preferred_default", "llama3.2:3b")
                model_info = ollama_client.get_model_info(demo_model)

                console.print(Panel.fit(
                    f"🎯 Автоматическая загрузка рекомендуемой модели\n\n"
                    f"Модель: {demo_model}\n"
                    f"Размер: {model_info.get('size', 'неизвестно')}\n"
                    f"Описание: {model_info.get('description', '')}\n\n"
                    f"Это займет несколько минут...",
                    title="Загрузка модели",
                    style="blue"
                ))

                if ollama_client.pull_model(demo_model, show_progress=True):
                    config.set("ollama.model", demo_model)
                    ollama_client.model = demo_model
                    console.print(f"✅ Модель {demo_model} готова к использованию!", style="green")
                else:
                    console.print("❌ Не удалось загрузить модель", style="red")
                    return False
            else:
                # Интерактивная настройка
                if not ollama_client.setup_recommended_model():
                    return False
        else:
            console.print(f"✅ Найдены модели: {', '.join(models)}", style="green")
            # Проверяем, есть ли настроенная модель
            if ollama_client.model not in models:
                console.print(f"⚠️  Модель {ollama_client.model} не найдена, использую первую доступную", style="yellow")
                ollama_client.model = models[0]
                config.set("ollama.model", models[0])

        console.print(f"🎯 Используется модель: {ollama_client.model}", style="green")

        # Сохраняем флаг, что настройка завершена
        config.set("setup.completed", True)

        return True

    def is_first_run(self) -> bool:
        """Проверка, первый ли это запуск"""
        return not config.get("setup.completed", False)

    def display_formatted_response(self, response: str):
        """Отображение ответа с подсветкой кода"""
        if not response.strip():
            return

        # Ищем блоки кода в тройных кавычках
        code_pattern = r'```(\w+)?\n(.*?)\n```'
        parts = re.split(code_pattern, response, flags=re.DOTALL)

        i = 0
        while i < len(parts):
            if i % 3 == 0:
                # Обычный текст
                text = parts[i].strip()
                if text:
                    # Проверяем, есть ли markdown
                    if any(marker in text for marker in ['**', '*', '`', '#']):
                        try:
                            console.print(Markdown(text))
                        except:
                            console.print(text, style="white")
                    else:
                        console.print(text, style="white")
            elif i % 3 == 1:
                # Язык программирования
                language = parts[i] or "text"
                i += 1
                if i < len(parts):
                    # Код
                    code = parts[i].strip()
                    if code:
                        try:
                            syntax = Syntax(code, language, theme="monokai", line_numbers=True)
                            console.print(Panel(syntax, title=f"📝 {language.upper()}", border_style="blue"))
                        except:
                            console.print(Panel(code, title="📝 Код", border_style="blue"))
            i += 1

    def detect_inline_code(self, text: str) -> str:
        """Обнаружение и подсветка инлайн кода"""
        # Ищем код в одинарных кавычках
        inline_pattern = r'`([^`]+)`'

        def replace_inline(match):
            code = match.group(1)
            return f"[bold cyan]{code}[/bold cyan]"

        return re.sub(inline_pattern, replace_inline, text)
    
    def chat_once(self, message: str, use_context: bool = True) -> str:
        """Одиночный запрос к ИИ с поддержкой контекста"""
        if not message.strip():
            return "Пожалуйста, введите сообщение."

        console.print(f"\n💭 Вы: {message}", style="cyan")

        response_parts = []
        try:
            # Используем контекст если включен и есть история
            context = self.history if use_context else None

            if self.streaming_mode:
                # Режим реального времени
                console.print("🤖 ИИ: ", style="green", end="")
                for chunk in ollama_client.chat(message, context=context):
                    console.print(chunk, end="", style="white")
                    response_parts.append(chunk)
                console.print()  # Новая строка после ответа
                response = "".join(response_parts)
            else:
                # Режим ожидания полного ответа
                with console.status("🤖 ИИ думает...", spinner="dots"):
                    for chunk in ollama_client.chat(message, context=context):
                        response_parts.append(chunk)
                response = "".join(response_parts)
                console.print("\n🤖 ИИ:", style="green")

            # Обрабатываем и подсвечиваем код в ответе только если не в режиме потока
            if not self.streaming_mode:
                self.display_formatted_response(response)

            # Сохраняем в историю
            self.save_to_history(message, response)

            return response

        except KeyboardInterrupt:
            console.print("\n\n⏹️  Прервано пользователем", style="yellow")
            return "Запрос прерван"
        except Exception as e:
            error_msg = f"Ошибка: {e}"
            console.print(f"\n❌ {error_msg}", style="red")
            return error_msg

    def chat_with_context(self, message: str) -> str:
        """Чат с использованием современного API сообщений"""
        if not message.strip():
            return "Пожалуйста, введите сообщение."

        console.print(f"\n💭 Вы: {message}", style="cyan")

        response_parts = []
        try:
            # Формируем список сообщений для контекста
            messages = []

            # Добавляем историю (последние N сообщений)
            max_context = config.get("ui.max_context_messages", 10)
            recent_history = self.history[-max_context:] if len(self.history) > max_context else self.history

            for entry in recent_history:
                messages.append({"user": entry["user"], "ai": entry["ai"]})

            # Добавляем текущее сообщение
            messages.append(message)

            if self.streaming_mode:
                # Режим реального времени
                console.print("🤖 ИИ: ", style="green", end="")
                for chunk in ollama_client.chat_with_messages(messages):
                    console.print(chunk, end="", style="white")
                    response_parts.append(chunk)
                console.print()  # Новая строка после ответа
                response = "".join(response_parts)
            else:
                # Режим ожидания полного ответа
                with console.status("🤖 ИИ думает...", spinner="dots"):
                    for chunk in ollama_client.chat_with_messages(messages):
                        response_parts.append(chunk)
                response = "".join(response_parts)
                console.print("\n🤖 ИИ:", style="green")

            # Обрабатываем и подсвечиваем код в ответе только если не в режиме потока
            if not self.streaming_mode:
                self.display_formatted_response(response)

            # Сохраняем в историю
            self.save_to_history(message, response)

            return response

        except KeyboardInterrupt:
            console.print("\n\n⏹️  Прервано пользователем", style="yellow")
            return "Запрос прерван"
        except Exception as e:
            error_msg = f"Ошибка: {e}"
            console.print(f"\n❌ {error_msg}", style="red")
            return error_msg
    
    def interactive_mode(self):
        """Интерактивный режим общения с поддержкой контекста"""
        use_context = config.get("ui.use_context", True)
        context_indicator = "🧠" if use_context else "💭"
        stream_indicator = "⚡" if self.streaming_mode else "⏳"

        console.print(Panel.fit(
            f"{context_indicator}{stream_indicator} Интерактивный режим\n"
            f"Память: {'включена' if use_context else 'выключена'} | "
            f"Вывод: {'в реальном времени' if self.streaming_mode else 'после завершения'}\n\n"
            "Команды:\n"
            "• 'exit' или 'quit' - выход\n"
            "• 'history' - показать историю\n"
            "• 'clear' - очистить экран\n"
            "• 'context on/off' - включить/выключить память\n"
            "• 'stream on/off' - режим вывода в реальном времени\n"
            "• 'reset' - очистить память разговора",
            style="blue"
        ))

        while True:
            try:
                stream_indicator = "⚡" if self.streaming_mode else "⏳"
                prompt_text = f"\n{context_indicator}{stream_indicator} Вы"
                message = Prompt.ask(prompt_text, default="")

                if not message:
                    continue

                if message.lower() in ['exit', 'quit', 'выход']:
                    console.print("👋 До свидания!", style="green")
                    break

                if message.lower() in ['history', 'история']:
                    self.show_history()
                    continue

                if message.lower() in ['clear', 'очистить']:
                    console.clear()
                    continue

                if message.lower() == 'context on':
                    use_context = True
                    config.set("ui.use_context", True)
                    context_indicator = "🧠"
                    console.print("✅ Память разговора включена", style="green")
                    continue

                if message.lower() == 'context off':
                    use_context = False
                    config.set("ui.use_context", False)
                    context_indicator = "💭"
                    console.print("⚠️ Память разговора выключена", style="yellow")
                    continue

                if message.lower() == 'stream on':
                    self.streaming_mode = True
                    config.set("ui.streaming_mode", True)
                    console.print("⚡ Режим вывода в реальном времени включен", style="green")
                    continue

                if message.lower() == 'stream off':
                    self.streaming_mode = False
                    config.set("ui.streaming_mode", False)
                    console.print("⏳ Режим ожидания полного ответа включен", style="yellow")
                    continue

                if message.lower() in ['reset', 'сброс']:
                    self.history.clear()
                    # Очищаем файл истории
                    try:
                        config.history_file.write_text("", encoding='utf-8')
                    except:
                        pass
                    console.print("🔄 Память разговора очищена", style="blue")
                    continue

                # Используем контекст в зависимости от настройки
                if use_context:
                    self.chat_with_context(message)
                else:
                    self.chat_once(message, use_context=False)

            except KeyboardInterrupt:
                console.print("\n👋 До свидания!", style="green")
                break
            except EOFError:
                console.print("\n👋 До свидания!", style="green")
                break
    
    def show_history(self, limit: int = 10):
        """Показать историю разговоров"""
        if not self.history:
            console.print("📝 История пуста", style="yellow")
            return
        
        console.print(f"\n📚 Последние {min(limit, len(self.history))} записей:", style="blue")
        
        for entry in self.history[-limit:]:
            timestamp = ""
            if self.show_timestamps and "timestamp" in entry:
                dt = datetime.fromisoformat(entry["timestamp"])
                timestamp = f" [{dt.strftime('%H:%M:%S')}]"
            
            console.print(f"\n💭 Вы{timestamp}: {entry['user']}", style="cyan")
            console.print(f"🤖 ИИ: {entry['ai']}", style="green")

# Глобальный экземпляр приложения
app = OfflineAI()
