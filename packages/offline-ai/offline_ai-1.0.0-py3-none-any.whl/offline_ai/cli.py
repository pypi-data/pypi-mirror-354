"""
CLI интерфейс для offline-ai
"""

import sys
import click
from rich.console import Console

from .main import app
from .ollama_client import ollama_client
from .config import config

console = Console()

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Показать версию')
@click.option('--setup', is_flag=True, help='Запустить первоначальную настройку')
@click.option('--auto-install', is_flag=True, help='Автоматически загрузить рекомендуемую модель')
@click.pass_context
def main(ctx, version, setup, auto_install):
    """
    🤖 offline-ai - Локальный ИИ-ассистент для терминала

    Работает без интернета с помощью Ollama и локальных моделей.
    """
    if version:
        from . import __version__
        console.print(f"offline-ai версия {__version__}", style="green")
        return

    if setup:
        if app.setup(auto_install=auto_install):
            console.print("✅ Настройка завершена успешно!", style="green")
        else:
            console.print("❌ Ошибка настройки", style="red")
            sys.exit(1)
        return

    # Если нет подкоманды, запускаем интерактивный режим
    if ctx.invoked_subcommand is None:
        # Проверяем, первый ли это запуск
        if app.is_first_run():
            console.print("🎉 Первый запуск offline-ai!", style="blue")
            console.print("🚀 Запускаю автоматическую настройку...", style="yellow")

            if not app.setup(auto_install=True):
                console.print("❌ Не удалось завершить настройку", style="red")
                console.print("💡 Попробуйте: offline-ai --setup", style="blue")
                sys.exit(1)

        # Проверяем настройку
        elif not ollama_client.is_ollama_running():
            console.print("⚠️  Ollama не запущен. Запускаю настройку...", style="yellow")
            if not app.setup():
                sys.exit(1)

        app.interactive_mode()

@main.command()
@click.argument('message', nargs=-1, required=True)
@click.option('--model', '-m', help='Модель для использования')
@click.option('--no-context', is_flag=True, help='Не использовать контекст разговора')
def ask(message, model, no_context):
    """
    Задать вопрос ИИ

    Пример: offline-ai ask "Привет, как дела?"
    """
    question = ' '.join(message)

    if model:
        ollama_client.model = model

    # Проверяем, первый ли это запуск
    if app.is_first_run():
        console.print("🎉 Первый запуск offline-ai!", style="blue")
        console.print("🚀 Запускаю автоматическую настройку...", style="yellow")

        if not app.setup(auto_install=True):
            console.print("❌ Не удалось завершить настройку", style="red")
            console.print("💡 Попробуйте: offline-ai --setup", style="blue")
            sys.exit(1)

    # Проверяем настройку
    elif not ollama_client.is_ollama_running():
        console.print("⚠️  Ollama не запущен. Запускаю настройку...", style="yellow")
        if not app.setup():
            sys.exit(1)

    # Используем контекст если не отключен
    use_context = not no_context and config.get("ui.use_context", True)

    if use_context and len(app.history) > 0:
        app.chat_with_context(question)
    else:
        app.chat_once(question, use_context=False)

@main.command()
@click.option('--limit', '-l', default=10, help='Количество записей для показа')
@click.option('--clear', is_flag=True, help='Очистить историю')
def history(limit, clear):
    """Показать или очистить историю разговоров"""
    if clear:
        app.history.clear()
        try:
            config.history_file.write_text("", encoding='utf-8')
            console.print("🔄 История очищена", style="green")
        except Exception as e:
            console.print(f"❌ Ошибка очистки истории: {e}", style="red")
    else:
        app.show_history(limit)

@main.command()
@click.argument('setting', type=click.Choice(['context', 'stream']))
@click.argument('action', type=click.Choice(['on', 'off', 'status']))
def config_cmd(setting, action):
    """
    Управление настройками

    context - управление памятью разговора
    stream - управление режимом вывода в реальном времени

    Действия: on, off, status
    """
    if setting == 'context':
        if action == 'on':
            config.set("ui.use_context", True)
            console.print("🧠 Память разговора включена", style="green")
            console.print("ИИ будет помнить предыдущие сообщения в разговоре", style="blue")

        elif action == 'off':
            config.set("ui.use_context", False)
            console.print("💭 Память разговора выключена", style="yellow")
            console.print("Каждое сообщение будет обрабатываться независимо", style="blue")

        elif action == 'status':
            use_context = config.get("ui.use_context", True)
            max_context = config.get("ui.max_context_messages", 10)

            status_icon = "🧠" if use_context else "💭"
            status_text = "включена" if use_context else "выключена"

            console.print(f"{status_icon} Память разговора: {status_text}",
                         style="green" if use_context else "yellow")

            if use_context:
                console.print(f"📊 Максимум сообщений в контексте: {max_context}", style="blue")
                console.print(f"📚 Сообщений в истории: {len(app.history)}", style="blue")

    elif setting == 'stream':
        if action == 'on':
            config.set("ui.streaming_mode", True)
            console.print("⚡ Режим вывода в реальном времени включен", style="green")
            console.print("Ответы ИИ будут показываться по мере генерации", style="blue")

        elif action == 'off':
            config.set("ui.streaming_mode", False)
            console.print("⏳ Режим ожидания полного ответа включен", style="yellow")
            console.print("Ответы ИИ будут показываться после завершения с форматированием", style="blue")

        elif action == 'status':
            streaming_mode = config.get("ui.streaming_mode", True)

            status_icon = "⚡" if streaming_mode else "⏳"
            status_text = "в реальном времени" if streaming_mode else "после завершения"

            console.print(f"{status_icon} Режим вывода: {status_text}",
                         style="green" if streaming_mode else "yellow")

@main.command()
@click.option('--recommended', '-r', is_flag=True, help='Показать рекомендуемые модели')
@click.option('--pull', '-p', help='Загрузить модель')
@click.option('--use', '-u', help='Установить модель по умолчанию')
@click.option('--demo', is_flag=True, help='Загрузить рекомендуемую модель')
def models(recommended, pull, use, demo):
    """Управление моделями ИИ"""

    # Загрузка модели для демо
    if demo:
        if not ollama_client.is_ollama_running():
            console.print("❌ Ollama не запущен", style="red")
            return

        demo_model = config.get("models.preferred_default", "llama3.2:3b")
        console.print(f"🎯 Загружаю рекомендуемую модель: {demo_model}", style="blue")

        if ollama_client.pull_model(demo_model):
            console.print(f"✅ Модель {demo_model} загружена!", style="green")
            config.set("ollama.model", demo_model)
            ollama_client.model = demo_model
            console.print(f"🎯 Модель {demo_model} установлена по умолчанию", style="green")
        else:
            console.print(f"❌ Не удалось загрузить модель {demo_model}", style="red")
        return

    # Загрузка конкретной модели
    if pull:
        if not ollama_client.is_ollama_running():
            console.print("❌ Ollama не запущен", style="red")
            return

        if ollama_client.pull_model(pull):
            console.print(f"✅ Модель {pull} загружена!", style="green")
            config.set("ollama.model", pull)
            ollama_client.model = pull
            console.print(f"🎯 Модель {pull} установлена по умолчанию", style="green")
        else:
            console.print(f"❌ Не удалось загрузить модель {pull}", style="red")
        return

    # Установка модели по умолчанию
    if use:
        models_list = ollama_client.list_models()
        if use not in models_list:
            console.print(f"❌ Модель {use} не найдена", style="red")
            console.print("Доступные модели:", style="blue")
            for model in models_list:
                console.print(f"  • {model}", style="white")
            return

        config.set("ollama.model", use)
        ollama_client.model = use
        console.print(f"✅ Модель {use} установлена по умолчанию", style="green")
        return

    # Показ рекомендуемых моделей
    if recommended:
        console.print("🎯 Рекомендуемые модели для offline-ai:", style="blue")
        recommended_models = config.get("models.recommended", [])

        for i, model_info in enumerate(recommended_models, 1):
            if isinstance(model_info, dict):
                name = model_info["name"]
                size = model_info.get("size", "неизвестно")
                desc = model_info.get("description", "")
                context_window = model_info.get("context_window", "неизвестно")
                optimal_context = model_info.get("optimal_context_messages", "неизвестно")
                performance = model_info.get("performance", "")

                console.print(f"  {i}. [bold]{name}[/bold] ({size})", style="white")
                console.print(f"     {desc}", style="dim white")
                console.print(f"     📊 Контекст: {context_window} токенов, оптимально {optimal_context} сообщений", style="dim cyan")
                console.print(f"     ⚡ Производительность: {performance}", style="dim green")
            else:
                console.print(f"  {i}. {model_info}", style="white")

        demo_model = config.get("models.preferred_default")
        if demo_model:
            console.print(f"\n🏆 Рекомендуемая модель: [bold]{demo_model}[/bold]", style="green")

        console.print("\n💡 Для загрузки модели используйте: offline-ai models --pull <имя_модели>", style="blue")
        console.print("💡 Для загрузки рекомендуемой модели: offline-ai models --demo", style="blue")
        return

    # Показ установленных моделей (по умолчанию)
    if not ollama_client.is_ollama_running():
        console.print("❌ Ollama не запущен", style="red")
        console.print("💡 Используйте --recommended для просмотра рекомендуемых моделей", style="blue")
        return

    models_list = ollama_client.list_models()
    if models_list:
        console.print("📦 Установленные модели:", style="blue")
        current_model = ollama_client.model
        for model in models_list:
            marker = "👉" if model == current_model else "  "
            console.print(f"{marker} {model}", style="green" if model == current_model else "white")

        console.print(f"\n💡 Для смены модели: offline-ai models --use <имя_модели>", style="blue")
    else:
        console.print("📦 Модели не найдены", style="yellow")
        console.print("💡 Используйте --recommended для просмотра рекомендуемых моделей", style="blue")
        console.print("💡 Для загрузки рекомендуемой модели: offline-ai models --demo", style="blue")



@main.command()
def status():
    """Показать статус системы"""
    console.print("🔍 Статус offline-ai:", style="blue")

    # Проверка первого запуска
    if app.is_first_run():
        console.print("🆕 Статус: Первый запуск (настройка не завершена)", style="yellow")
        console.print("💡 Запустите: offline-ai --setup --auto-install", style="blue")
    else:
        console.print("✅ Статус: Настроен", style="green")

    # Проверка Ollama
    if ollama_client.is_ollama_running():
        console.print("✅ Ollama: Запущен", style="green")

        # Проверка моделей
        models_list = ollama_client.list_models()
        if models_list:
            console.print(f"✅ Модели: {len(models_list)} доступно", style="green")
            console.print(f"👉 Текущая модель: {ollama_client.model}", style="blue")
        else:
            console.print("⚠️  Модели: Не найдены", style="yellow")
            console.print("💡 Загрузите модель: offline-ai models --demo", style="blue")
    else:
        console.print("❌ Ollama: Не запущен", style="red")
        console.print("💡 Запустите настройку: offline-ai --setup", style="blue")

    # Информация о конфигурации
    use_context = config.get("ui.use_context", True)
    streaming_mode = config.get("ui.streaming_mode", True)

    context_icon = "🧠" if use_context else "💭"
    stream_icon = "⚡" if streaming_mode else "⏳"

    console.print(f"{context_icon} Память разговора: {'включена' if use_context else 'выключена'}",
                 style="green" if use_context else "yellow")
    console.print(f"{stream_icon} Режим вывода: {'в реальном времени' if streaming_mode else 'после завершения'}",
                 style="green" if streaming_mode else "yellow")
    console.print(f"📁 Конфигурация: {config.config_file}", style="blue")
    console.print(f"📚 История: {len(app.history)} записей", style="blue")



if __name__ == "__main__":
    main()
