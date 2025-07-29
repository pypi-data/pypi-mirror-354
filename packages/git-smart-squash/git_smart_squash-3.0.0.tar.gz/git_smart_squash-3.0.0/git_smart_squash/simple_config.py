"""Simplified configuration for Git Smart Squash."""

import os
import yaml
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class AIConfig:
    """AI provider configuration."""
    provider: str = "local"
    model: str = "devstral"
    api_key_env: Optional[str] = None


@dataclass
class HunkConfig:
    """Hunk-based grouping configuration."""
    min_hunk_size: int = 3  # Minimum lines for a hunk to be considered
    show_hunk_context: bool = True  # Include context in display
    context_lines: int = 3  # Number of context lines to show


@dataclass 
class Config:
    """Simplified configuration."""
    ai: AIConfig
    hunk: HunkConfig


class ConfigManager:
    """Simplified configuration manager."""
    
    def __init__(self):
        self.default_config_path = os.path.expanduser("~/.git-smart-squash.yml")
        
    def _get_default_model(self, provider: str) -> str:
        """Get the default model for a given provider."""
        defaults = {
            'local': 'devstral',
            'openai': 'gpt-4.1',
            'anthropic': 'claude-sonnet-4-20250514',  # Claude Sonnet 4 model
            'gemini': 'gemini-2.5-pro-preview-06-05'  # Gemini 2.5 Pro model
        }
        return defaults.get(provider, 'devstral')
    
    def load_config(self, config_path: Optional[str] = None) -> Config:
        """Load configuration from file or create default."""
        
        # Try to load from specified path, then default path
        paths_to_try = []
        if config_path:
            paths_to_try.append(config_path)
        
        # Try local project config
        if os.path.exists(".git-smart-squash.yml"):
            paths_to_try.append(".git-smart-squash.yml")
            
        # Try global config
        paths_to_try.append(self.default_config_path)
        
        config_data = {}
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        config_data = yaml.safe_load(f) or {}
                    break
                except Exception:
                    continue
        
        # Create config with provider-aware defaults
        provider = config_data.get('ai', {}).get('provider', 'local')
        model = config_data.get('ai', {}).get('model')
        
        # If no model specified, use provider-specific default
        if not model:
            model = self._get_default_model(provider)
        
        ai_config = AIConfig(
            provider=provider,
            model=model,
            api_key_env=config_data.get('ai', {}).get('api_key_env')
        )
        
        # Create hunk config with defaults
        hunk_data = config_data.get('hunk', {})
        hunk_config = HunkConfig(
            min_hunk_size=hunk_data.get('min_hunk_size', 3),
            show_hunk_context=hunk_data.get('show_hunk_context', True),
            context_lines=hunk_data.get('context_lines', 3)
        )
        
        return Config(ai=ai_config, hunk=hunk_config)
    
    def create_default_config(self, global_config: bool = False) -> str:
        """Create a default config file."""
        config = {
            'ai': {
                'provider': 'local',
                'model': 'devstral',
                'api_key_env': None
            },
            'hunk': {
                'min_hunk_size': 3,
                'show_hunk_context': True,
                'context_lines': 3
            }
        }
        
        if global_config:
            path = self.default_config_path
        else:
            path = ".git-smart-squash.yml"
            
        with open(path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return path