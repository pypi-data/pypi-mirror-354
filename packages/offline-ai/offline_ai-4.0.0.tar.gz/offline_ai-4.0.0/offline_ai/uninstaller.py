"""
Модуль для полного удаления offline-ai и Ollama
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()

def stop_ollama():
    """Остановить процессы Ollama"""
    console.print("🛑 Останавливаю процессы Ollama...", style="yellow")
    
    try:
        if platform.system() == "Windows":
            # Останавливаем процессы Ollama на Windows
            subprocess.run(["taskkill", "/F", "/IM", "ollama.exe"], 
                         capture_output=True, check=False)
        else:
            # Останавливаем процессы Ollama на Linux/Mac
            subprocess.run(["pkill", "-f", "ollama"], 
                         capture_output=True, check=False)
        
        console.print("✅ Процессы Ollama остановлены", style="green")
    except Exception as e:
        console.print(f"⚠️ Ошибка остановки процессов: {e}", style="yellow")

def uninstall_ollama_windows():
    """Удалить Ollama на Windows"""
    console.print("🗑️ Удаляю Ollama на Windows...", style="blue")
    
    success = False
    
    # Пробуем через winget
    try:
        result = subprocess.run(["winget", "uninstall", "Ollama.Ollama"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            console.print("✅ Ollama удален через winget", style="green")
            success = True
    except:
        pass
    
    # Пробуем через стандартный деинсталлятор
    if not success:
        try:
            # Ищем деинсталлятор в стандартных местах
            uninstall_paths = [
                Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "Uninstall Ollama.exe",
                Path("C:/Program Files/Ollama/Uninstall Ollama.exe"),
                Path("C:/Program Files (x86)/Ollama/Uninstall Ollama.exe")
            ]
            
            for uninstall_path in uninstall_paths:
                if uninstall_path.exists():
                    console.print(f"🚀 Запускаю деинсталлятор: {uninstall_path}", style="blue")
                    subprocess.run([str(uninstall_path), "/S"], timeout=120)  # /S для тихой установки
                    success = True
                    break
        except Exception as e:
            console.print(f"⚠️ Ошибка запуска деинсталлятора: {e}", style="yellow")
    
    # Удаляем папки вручную
    folders_to_remove = [
        Path.home() / "AppData" / "Local" / "Programs" / "Ollama",
        Path.home() / "AppData" / "Local" / "Ollama",
        Path.home() / ".ollama",
        Path("C:/Program Files/Ollama"),
        Path("C:/Program Files (x86)/Ollama")
    ]
    
    for folder in folders_to_remove:
        try:
            if folder.exists():
                shutil.rmtree(folder)
                console.print(f"🗑️ Удалена папка: {folder}", style="green")
        except Exception as e:
            console.print(f"⚠️ Не удалось удалить {folder}: {e}", style="yellow")
    
    return success

def uninstall_ollama_linux():
    """Удалить Ollama на Linux"""
    console.print("🗑️ Удаляю Ollama на Linux...", style="blue")
    
    success = False
    
    # Удаляем портативную установку
    portable_path = Path.home() / ".local" / "bin" / "ollama"
    if portable_path.exists():
        try:
            portable_path.unlink()
            console.print("✅ Удален портативный Ollama из ~/.local/bin/", style="green")
            success = True
        except Exception as e:
            console.print(f"⚠️ Ошибка удаления портативного Ollama: {e}", style="yellow")
    
    # Удаляем системную установку (если есть права)
    system_paths = ["/usr/local/bin/ollama", "/usr/bin/ollama"]
    for path in system_paths:
        try:
            if Path(path).exists():
                # Пробуем удалить с sudo
                result = subprocess.run(["sudo", "rm", path], 
                                      capture_output=True, timeout=30)
                if result.returncode == 0:
                    console.print(f"✅ Удален системный Ollama: {path}", style="green")
                    success = True
        except:
            pass
    
    # Удаляем папки данных
    folders_to_remove = [
        Path.home() / ".ollama",
        Path.home() / ".local" / "share" / "ollama"
    ]
    
    for folder in folders_to_remove:
        try:
            if folder.exists():
                shutil.rmtree(folder)
                console.print(f"🗑️ Удалена папка: {folder}", style="green")
        except Exception as e:
            console.print(f"⚠️ Не удалось удалить {folder}: {e}", style="yellow")
    
    # Удаляем из PATH в .bashrc
    try:
        bashrc_path = Path.home() / ".bashrc"
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                lines = f.readlines()
            
            # Фильтруем строки, связанные с offline-ai
            new_lines = []
            skip_next = False
            for line in lines:
                if "# Добавлено offline-ai" in line:
                    skip_next = True
                    continue
                elif skip_next and "export PATH" in line and ".local/bin" in line:
                    skip_next = False
                    continue
                else:
                    skip_next = False
                    new_lines.append(line)
            
            with open(bashrc_path, 'w') as f:
                f.writelines(new_lines)
            
            console.print("✅ Очищен ~/.bashrc от записей offline-ai", style="green")
    except Exception as e:
        console.print(f"⚠️ Ошибка очистки ~/.bashrc: {e}", style="yellow")
    
    return success

def remove_offline_ai_data():
    """Удалить данные offline-ai"""
    console.print("🗑️ Удаляю данные offline-ai...", style="blue")
    
    # Папки для удаления
    folders_to_remove = [
        Path.home() / ".config" / "offline-ai",
        Path.home() / ".local" / "share" / "offline-ai",
        Path.home() / ".cache" / "offline-ai"
    ]
    
    if platform.system() == "Windows":
        folders_to_remove.extend([
            Path.home() / "AppData" / "Local" / "offline-ai",
            Path.home() / "AppData" / "Roaming" / "offline-ai"
        ])
    
    for folder in folders_to_remove:
        try:
            if folder.exists():
                shutil.rmtree(folder)
                console.print(f"🗑️ Удалена папка: {folder}", style="green")
        except Exception as e:
            console.print(f"⚠️ Не удалось удалить {folder}: {e}", style="yellow")

def uninstall_offline_ai_package():
    """Удалить пакет offline-ai"""
    console.print("🗑️ Удаляю пакет offline-ai...", style="blue")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "uninstall", "offline-ai", "-y"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            console.print("✅ Пакет offline-ai удален", style="green")
            return True
        else:
            console.print(f"⚠️ Ошибка удаления пакета: {result.stderr}", style="yellow")
            return False
    except Exception as e:
        console.print(f"⚠️ Ошибка удаления пакета: {e}", style="yellow")
        return False

def uninstall_all():
    """Полное удаление offline-ai и Ollama"""
    console.print(Panel.fit(
        "🗑️ Полное удаление offline-ai и Ollama\n\n"
        "Это действие удалит:\n"
        "• Пакет offline-ai\n"
        "• Ollama и все модели\n"
        "• Все конфигурации и данные\n"
        "• Историю разговоров\n\n"
        "⚠️ Это действие необратимо!",
        title="Удаление",
        style="red"
    ))
    
    if not Confirm.ask("🤔 Вы уверены, что хотите удалить все?"):
        console.print("❌ Удаление отменено", style="yellow")
        return
    
    console.print("🚀 Начинаю полное удаление...", style="blue")
    
    # 1. Останавливаем Ollama
    stop_ollama()
    
    # 2. Удаляем Ollama
    system = platform.system()
    if system == "Windows":
        uninstall_ollama_windows()
    elif system == "Linux":
        uninstall_ollama_linux()
    elif system == "Darwin":  # macOS
        console.print("🍎 Для macOS удалите Ollama вручную:", style="yellow")
        console.print("  • Если установлен через Homebrew: brew uninstall ollama", style="blue")
        console.print("  • Если установлен через .dmg: удалите из Applications", style="blue")
    
    # 3. Удаляем данные offline-ai
    remove_offline_ai_data()
    
    # 4. Удаляем пакет offline-ai (в последнюю очередь)
    console.print("\n🎯 Удаляю пакет offline-ai...", style="blue")
    console.print("⚠️ После этого команда offline-ai перестанет работать", style="yellow")
    
    if Confirm.ask("Продолжить удаление пакета?"):
        if uninstall_offline_ai_package():
            console.print(Panel.fit(
                "🎉 Удаление завершено!\n\n"
                "Удалено:\n"
                "✅ Пакет offline-ai\n"
                "✅ Ollama и модели\n"
                "✅ Все конфигурации\n"
                "✅ История разговоров\n\n"
                "Спасибо за использование offline-ai! 👋",
                title="Готово",
                style="green"
            ))
        else:
            console.print("⚠️ Пакет offline-ai не удален, но данные очищены", style="yellow")
    else:
        console.print("✅ Данные очищены, пакет offline-ai оставлен", style="green")
