"""
Plugin system for refinire-rag
プラグインシステム for refinire-rag

This module provides a plugin loader and registry system for dynamically loading
and managing external plugins for refinire-rag.

このモジュールは、refinire-ragの外部プラグインを動的に読み込み、管理するための
プラグインローダーとレジストリシステムを提供します。
"""

from .plugin_loader import PluginLoader, PluginRegistry
from .base import PluginInterface, PluginConfig

__all__ = [
    "PluginLoader",
    "PluginRegistry", 
    "PluginInterface",
    "PluginConfig",
]