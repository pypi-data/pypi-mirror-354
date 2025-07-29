"""
Конфигурация для offline-ai
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Класс для управления конфигурацией"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".offline-ai"
        self.config_file = self.config_dir / "config.yaml"
        self.history_file = self.config_dir / "history.txt"
        self.config_dir.mkdir(exist_ok=True)
        
        # Настройки по умолчанию
        self.default_config = {
            "ollama": {
                "base_url": "http://localhost:11434",
                "model": "llama3.2:3b",
                "timeout": 30
            },
            "ui": {
                "max_history": 100,
                "show_timestamps": True,
                "color_scheme": "auto",
                "use_context": True,
                "max_context_messages": 8,
                "syntax_highlighting": True,
                "code_theme": "monokai",
                "streaming_mode": True
            },
            "models": {
                "recommended": [
                    {
                        "name": "llama3.2:3b",
                        "size": "~2.0 GB",
                        "description": "🏆 Лучшее качество и производительность",
                        "context_window": 128000,
                        "optimal_context_messages": 8,
                        "performance": "отличная"
                    },
                    {
                        "name": "phi3:mini",
                        "size": "~2.3 GB",
                        "description": "От Microsoft, отличная для кода",
                        "context_window": 128000,
                        "optimal_context_messages": 6,
                        "performance": "хорошая для кода"
                    },
                    {
                        "name": "qwen2.5:3b",
                        "size": "~2.0 GB",
                        "description": "Новая модель от Alibaba, очень умная",
                        "context_window": 32000,
                        "optimal_context_messages": 8,
                        "performance": "отличная"
                    },
                    {
                        "name": "gemma2:2b",
                        "size": "~1.4 GB",
                        "description": "Компактная от Google",
                        "context_window": 8192,
                        "optimal_context_messages": 6,
                        "performance": "хорошая, быстрая"
                    },
                    {
                        "name": "llama3.2:1b",
                        "size": "~1.3 GB",
                        "description": "Для слабых ПК",
                        "context_window": 128000,
                        "optimal_context_messages": 4,
                        "performance": "базовая, очень быстрая"
                    }
                ],
                "auto_download": True,
                "preferred_default": "llama3.2:3b"
            }
        }
        
        self._config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    # Объединяем с настройками по умолчанию
                    return self._merge_configs(self.default_config, config)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
                return self.default_config.copy()
        else:
            # Создаем файл конфигурации с настройками по умолчанию
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Сохранение конфигурации в файл"""
        config_to_save = config or self._config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_to_save, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Объединение конфигураций"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default=None):
        """Получение значения из конфигурации"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Установка значения в конфигурации"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()

# Глобальный экземпляр конфигурации
config = Config()
