"""
Клиент для работы с Ollama
"""

import json
import time
import subprocess
import platform
import requests
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Generator
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from rich.panel import Panel
from rich.prompt import Confirm

from .config import config

console = Console()

class OllamaClient:
    """Клиент для работы с Ollama API"""
    
    def __init__(self):
        self.base_url = config.get("ollama.base_url", "http://localhost:11434")
        self.timeout = config.get("ollama.timeout", 30)
        self.model = config.get("ollama.model", "llama3.2:3b")
    
    def is_ollama_running(self) -> bool:
        """Проверка, запущен ли Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def install_ollama_windows(self) -> bool:
        """Автоматическая установка Ollama на Windows"""
        console.print("📦 Пытаюсь установить Ollama автоматически...", style="blue")

        try:
            # Пробуем через winget
            console.print("🔧 Установка через winget...", style="blue")
            result = subprocess.run(["winget", "install", "Ollama.Ollama", "--accept-package-agreements", "--accept-source-agreements"],
                                  capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                console.print("✅ Ollama установлен через winget!", style="green")
                console.print("⏳ Ожидание инициализации...", style="yellow")
                time.sleep(5)  # Даем время на инициализацию
                return True
            else:
                console.print("⚠️ Winget не сработал, пробую скачать установщик...", style="yellow")

        except (FileNotFoundError, subprocess.TimeoutExpired):
            console.print("⚠️ Winget недоступен, пробую скачать установщик...", style="yellow")

        # Пробуем скачать и запустить установщик
        try:
            import urllib.request
            import tempfile

            console.print("📥 Скачиваю установщик Ollama...", style="blue")

            # URL установщика Ollama для Windows
            installer_url = "https://ollama.ai/download/OllamaSetup.exe"

            with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tmp_file:
                urllib.request.urlretrieve(installer_url, tmp_file.name)
                installer_path = tmp_file.name

            console.print("🚀 Запускаю установщик...", style="blue")
            console.print("💡 Следуйте инструкциям в окне установщика", style="yellow")

            # Запускаем установщик
            result = subprocess.run([installer_path], timeout=600)

            # Удаляем временный файл
            try:
                os.unlink(installer_path)
            except:
                pass

            if result.returncode == 0:
                console.print("✅ Ollama установлен!", style="green")
                console.print("⏳ Ожидание инициализации...", style="yellow")
                time.sleep(10)  # Даем время на инициализацию
                return True

        except Exception as e:
            console.print(f"❌ Ошибка скачивания установщика: {e}", style="red")

        # Если автоматическая установка не сработала, показываем инструкции
        console.print(Panel(
            "🔧 Автоматическая установка не удалась.\n\n"
            "Пожалуйста, установите Ollama вручную:\n\n"
            "1. Перейдите на: https://ollama.ai\n"
            "2. Скачайте установщик для Windows\n"
            "3. Запустите установщик\n"
            "4. Перезапустите offline-ai\n\n"
            "Или попробуйте через командную строку:\n"
            "winget install Ollama.Ollama",
            title="Ручная установка Ollama",
            style="blue"
        ))
        return False

    def install_ollama_linux_mac(self) -> bool:
        """Автоматическая установка Ollama на Linux/Mac"""
        console.print("📦 Пытаюсь установить Ollama автоматически...", style="blue")

        try:
            console.print("📥 Скачиваю и запускаю установочный скрипт...", style="blue")

            # Используем официальный установочный скрипт
            result = subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh"
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                # Запускаем скрипт через sh
                install_result = subprocess.run([
                    "sh", "-c", result.stdout
                ], timeout=300)

                if install_result.returncode == 0:
                    console.print("✅ Ollama установлен!", style="green")
                    console.print("⏳ Ожидание инициализации...", style="yellow")
                    time.sleep(5)
                    return True

        except Exception as e:
            console.print(f"❌ Ошибка автоматической установки: {e}", style="red")

        # Если автоматическая установка не сработала
        system_name = "Linux" if platform.system() == "Linux" else "macOS"
        console.print(Panel(
            f"🔧 Автоматическая установка не удалась.\n\n"
            f"Пожалуйста, установите Ollama вручную на {system_name}:\n\n"
            f"Способ 1 - Официальный скрипт:\n"
            f"curl -fsSL https://ollama.ai/install.sh | sh\n\n"
            f"Способ 2 - Скачать с сайта:\n"
            f"https://ollama.ai\n\n"
            f"После установки запустите: ollama serve",
            title=f"Ручная установка Ollama ({system_name})",
            style="blue"
        ))
        return False

    def start_ollama(self) -> bool:
        """Попытка запустить Ollama"""
        if self.is_ollama_running():
            return True

        console.print("🚀 Запускаю Ollama...", style="yellow")

        try:
            if platform.system() == "Windows":
                subprocess.Popen(["ollama", "serve"],
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["ollama", "serve"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

            # Ждем запуска
            for i in range(15):
                time.sleep(1)
                if self.is_ollama_running():
                    console.print("✅ Ollama запущен!", style="green")
                    return True
                console.print(f"⏳ Ожидание запуска... ({i+1}/15)", style="yellow")

            console.print("❌ Не удалось запустить Ollama", style="red")
            return False

        except FileNotFoundError:
            console.print("❌ Ollama не найден", style="red")

            # Пытаемся установить автоматически
            system = platform.system()
            if Confirm.ask("🤖 Попробовать установить Ollama автоматически?"):
                success = False

                if system == "Windows":
                    success = self.install_ollama_windows()
                elif system in ["Linux", "Darwin"]:  # Darwin = macOS
                    success = self.install_ollama_linux_mac()

                if success:
                    # Пробуем запустить снова после установки
                    console.print("🔄 Пытаюсь запустить Ollama после установки...", style="blue")
                    time.sleep(5)
                    return self.start_ollama()
                else:
                    console.print("❌ Автоматическая установка не удалась", style="red")

            console.print(Panel(
                "❌ Не удалось запустить Ollama.\n\n"
                "Пожалуйста, установите Ollama вручную:\n"
                "• Windows/Mac: https://ollama.ai\n"
                "• Linux: curl -fsSL https://ollama.ai/install.sh | sh\n\n"
                "После установки запустите: ollama serve",
                title="Ручная установка",
                style="red"
            ))
            return False
        except Exception as e:
            console.print(f"❌ Ошибка запуска Ollama: {e}", style="red")
            return False
    
    def list_models(self) -> list:
        """Получение списка установленных моделей"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            console.print(f"❌ Ошибка получения списка моделей: {e}", style="red")
            return []
    
    def pull_model(self, model_name: str, show_progress: bool = True) -> bool:
        """Загрузка модели с прогресс-баром"""
        if not show_progress:
            console.print(f"📥 Загружаю модель {model_name}...", style="blue")

        try:
            # Получаем информацию о размере модели
            model_info = self.get_model_info(model_name)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                console=console
            ) as progress:

                if show_progress:
                    task = progress.add_task(f"📥 Загрузка {model_name}", total=100)
                else:
                    task = progress.add_task(f"Загрузка {model_name}...", total=None)

                response = requests.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model_name},
                    stream=True,
                    timeout=600  # 10 минут на загрузку
                )

                total_size = 0
                downloaded = 0

                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            status = data.get("status", "")

                            if "total" in data and "completed" in data:
                                total_size = data["total"]
                                downloaded = data["completed"]

                                if total_size > 0:
                                    percent = (downloaded / total_size) * 100
                                    progress.update(task, completed=percent,
                                                  description=f"📥 {model_name}: {status}")
                            else:
                                progress.update(task, description=f"📥 {model_name}: {status}")

                            if data.get("status") == "success":
                                progress.update(task, completed=100,
                                              description=f"✅ {model_name}: Загружено!")
                                break

                        except json.JSONDecodeError:
                            continue

            console.print(f"✅ Модель {model_name} загружена!", style="green")
            return True

        except Exception as e:
            console.print(f"❌ Ошибка загрузки модели: {e}", style="red")
            return False

    def get_model_info(self, model_name: str) -> dict:
        """Получить информацию о модели"""
        recommended_models = config.get("models.recommended", [])
        for model_info in recommended_models:
            if isinstance(model_info, dict) and model_info.get("name") == model_name:
                return model_info
        return {"name": model_name, "size": "неизвестно", "description": ""}
    
    def ensure_model(self, model_name: Optional[str] = None) -> bool:
        """Убедиться, что модель доступна"""
        model_name = model_name or self.model
        models = self.list_models()
        
        if model_name in models:
            return True
        
        # Пытаемся загрузить модель
        console.print(f"🔍 Модель {model_name} не найдена, загружаю...", style="yellow")
        return self.pull_model(model_name)
    
    def chat(self, message: str, model_name: Optional[str] = None, context: Optional[list] = None) -> Generator[str, None, None]:
        """Отправка сообщения и получение ответа потоком с поддержкой контекста"""
        model_name = model_name or self.model

        try:
            # Формируем промпт с контекстом
            if context and len(context) > 0:
                # Берем последние N сообщений для контекста
                max_context = config.get("ui.max_context_messages", 10)
                recent_context = context[-max_context:] if len(context) > max_context else context

                # Формируем промпт с историей
                prompt_parts = []
                for entry in recent_context:
                    prompt_parts.append(f"Пользователь: {entry['user']}")
                    prompt_parts.append(f"Ассистент: {entry['ai']}")

                prompt_parts.append(f"Пользователь: {message}")
                prompt_parts.append("Ассистент:")

                full_prompt = "\n".join(prompt_parts)
            else:
                full_prompt = message

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": full_prompt,
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                },
                stream=True,
                timeout=self.timeout
            )

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            yield f"❌ Ошибка: {e}"

    def chat_with_messages(self, messages: list, model_name: Optional[str] = None) -> Generator[str, None, None]:
        """Чат с использованием формата сообщений (более современный подход)"""
        model_name = model_name or self.model

        try:
            # Преобразуем историю в формат сообщений
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, dict):
                    if 'user' in msg:
                        formatted_messages.append({"role": "user", "content": msg['user']})
                    if 'ai' in msg:
                        formatted_messages.append({"role": "assistant", "content": msg['ai']})
                elif isinstance(msg, str):
                    formatted_messages.append({"role": "user", "content": msg})

            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model_name,
                    "messages": formatted_messages,
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                },
                stream=True,
                timeout=self.timeout
            )

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            # Fallback на обычный метод
            yield from self.chat(messages[-1] if messages else "", model_name)
    
    def setup_recommended_model(self) -> bool:
        """Настройка рекомендуемой модели"""
        recommended_models = config.get("models.recommended", [])

        # Показываем доступные модели
        console.print("📦 Рекомендуемые модели:", style="blue")
        for i, model_info in enumerate(recommended_models, 1):
            if isinstance(model_info, dict):
                name = model_info["name"]
                size = model_info.get("size", "неизвестно")
                desc = model_info.get("description", "")
                console.print(f"  {i}. {name} ({size}) - {desc}", style="white")
            else:
                console.print(f"  {i}. {model_info}", style="white")

        # Пытаемся использовать модель для демо (самую компактную)
        demo_model = config.get("models.preferred_for_demo")
        if demo_model:
            console.print(f"🎯 Для демо-экзамена рекомендуется: {demo_model}", style="yellow")
            console.print(f"🔍 Проверяю модель {demo_model}...", style="blue")
            if self.ensure_model(demo_model):
                config.set("ollama.model", demo_model)
                self.model = demo_model
                console.print(f"✅ Модель {demo_model} готова к использованию!", style="green")
                return True

        # Если демо-модель не подошла, пробуем остальные
        for model_info in recommended_models:
            model_name = model_info["name"] if isinstance(model_info, dict) else model_info
            console.print(f"🔍 Проверяю модель {model_name}...", style="blue")
            if self.ensure_model(model_name):
                config.set("ollama.model", model_name)
                self.model = model_name
                console.print(f"✅ Модель {model_name} готова к использованию!", style="green")
                return True

        console.print("❌ Не удалось настроить ни одну рекомендуемую модель", style="red")
        return False

# Глобальный экземпляр клиента
ollama_client = OllamaClient()
