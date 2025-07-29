#!/usr/bin/env python3
"""
Configuration Management System for VarAnnote v1.0.0

Provides comprehensive configuration management including:
- YAML configuration file loading
- Environment variable overrides
- User preference management
- Configuration validation
- Default value handling
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, asdict
import logging
from datetime import datetime

from .logger import get_logger


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    name: str
    priority: int = 5
    api_key: Optional[str] = None
    rate_limit: float = 5.0
    timeout: int = 30
    enabled: bool = True


@dataclass
class PerformanceConfig:
    """Performance configuration settings"""
    max_workers: int = 4
    use_parallel: bool = True
    batch_size: int = 50
    max_concurrent_requests: int = 30
    max_cache_size_mb: int = 500
    cache_cleanup_interval: int = 3600
    max_connections: int = 100
    max_connections_per_host: int = 30


@dataclass
class CacheConfig:
    """Cache configuration settings"""
    enabled: bool = True
    directory: str = "~/.varannote/cache"
    max_age_days: int = 30
    max_size_gb: float = 2.0
    compression: bool = True
    strategies: Dict[str, str] = None


@dataclass
class OutputConfig:
    """Output configuration settings"""
    default_format: str = "vcf"
    available_formats: List[str] = None
    include_fields: List[str] = None
    filters: Dict[str, Any] = None


@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = "INFO"
    directory: str = "~/.varannote/logs"
    max_file_size_mb: int = 10
    backup_count: int = 5
    categories: Dict[str, bool] = None


class ConfigManager:
    """
    Comprehensive configuration manager for VarAnnote
    
    Features:
    - YAML configuration file loading
    - Environment variable overrides
    - Configuration validation
    - Default value management
    - User preference handling
    - Configuration merging and inheritance
    """
    
    def __init__(self, 
                 config_file: Optional[Union[str, Path]] = None,
                 user_config_dir: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to main configuration file
            user_config_dir: Directory for user-specific configurations
        """
        self.logger = get_logger("config_manager")
        
        # Configuration paths
        self.config_file = self._resolve_config_file(config_file)
        self.user_config_dir = self._resolve_user_config_dir(user_config_dir)
        
        # Configuration data
        self._config_data: Dict[str, Any] = {}
        self._user_config: Dict[str, Any] = {}
        self._env_overrides: Dict[str, Any] = {}
        
        # Configuration objects
        self.databases: Dict[str, DatabaseConfig] = {}
        self.performance: PerformanceConfig = PerformanceConfig()
        self.cache: CacheConfig = CacheConfig()
        self.output: OutputConfig = OutputConfig()
        self.logging_config: LoggingConfig = LoggingConfig()
        
        # Load configurations
        self._load_configurations()
        
        self.logger.info(f"Configuration manager initialized")
        self.logger.info(f"Config file: {self.config_file}")
        self.logger.info(f"User config dir: {self.user_config_dir}")
    
    def _resolve_config_file(self, config_file: Optional[Union[str, Path]]) -> Path:
        """Resolve configuration file path"""
        if config_file:
            return Path(config_file).expanduser().resolve()
        
        # Search order: current dir, package dir, user config dir
        search_paths = [
            Path.cwd() / "config.yaml",
            Path(__file__).parent.parent / "config.yaml",
            Path.home() / ".varannote" / "config.yaml"
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        # Return default path (will be created if needed)
        return Path(__file__).parent.parent / "config.yaml"
    
    def _resolve_user_config_dir(self, user_config_dir: Optional[Union[str, Path]]) -> Path:
        """Resolve user configuration directory"""
        if user_config_dir:
            path = Path(user_config_dir).expanduser().resolve()
        else:
            path = Path.home() / ".varannote"
        
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def _load_configurations(self):
        """Load all configuration sources"""
        # 1. Load main configuration file
        self._load_main_config()
        
        # 2. Load user-specific configuration
        self._load_user_config()
        
        # 3. Load environment variable overrides
        self._load_env_overrides()
        
        # 4. Merge configurations
        self._merge_configurations()
        
        # 5. Create configuration objects
        self._create_config_objects()
        
        # 6. Validate configuration
        self._validate_configuration()
    
    def _load_main_config(self):
        """Load main configuration file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_data = yaml.safe_load(f)
                    self._config_data = loaded_data if loaded_data else self._get_default_config()
                self.logger.info(f"Loaded main config from {self.config_file}")
            else:
                self.logger.warning(f"Main config file not found: {self.config_file}")
                self._config_data = self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading main config: {e}")
            self._config_data = self._get_default_config()
    
    def _load_user_config(self):
        """Load user-specific configuration"""
        user_config_file = self.user_config_dir / "user_config.yaml"
        try:
            if user_config_file.exists():
                with open(user_config_file, 'r', encoding='utf-8') as f:
                    self._user_config = yaml.safe_load(f) or {}
                self.logger.info(f"Loaded user config from {user_config_file}")
            else:
                self._user_config = {}
        except Exception as e:
            self.logger.error(f"Error loading user config: {e}")
            self._user_config = {}
    
    def _load_env_overrides(self):
        """Load environment variable overrides"""
        self._env_overrides = {}
        
        # Database API keys
        for db_name in ['clinvar', 'gnomad', 'dbsnp', 'ensembl', 'cosmic', 
                       'pharmgkb', 'omim', 'clingen', 'hgmd']:
            env_key = f"VARANNOTE_{db_name.upper()}_API_KEY"
            if env_key in os.environ:
                if 'databases' not in self._env_overrides:
                    self._env_overrides['databases'] = {'api_keys': {}}
                self._env_overrides['databases']['api_keys'][db_name] = os.environ[env_key]
        
        # Other environment variables
        env_mappings = {
            'VARANNOTE_LOG_LEVEL': ['logging', 'level'],
            'VARANNOTE_CACHE_DIR': ['cache', 'directory'],
            'VARANNOTE_MAX_WORKERS': ['performance', 'max_workers'],
            'VARANNOTE_DEBUG': ['advanced', 'debug_mode']
        }
        
        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                # Convert numeric values
                if config_path[-1] == 'max_workers':
                    value = int(value)
                elif config_path[-1] == 'debug_mode':
                    value = value.lower() in ('true', '1', 'yes')
                self._set_nested_value(self._env_overrides, config_path, value)
        
        if self._env_overrides:
            self.logger.info(f"Loaded {len(self._env_overrides)} environment overrides")
    
    def _merge_configurations(self):
        """Merge all configuration sources"""
        # Start with main config
        merged_config = self._config_data.copy()
        
        # Merge user config
        merged_config = self._deep_merge(merged_config, self._user_config)
        
        # Merge environment overrides
        merged_config = self._deep_merge(merged_config, self._env_overrides)
        
        self._config_data = merged_config
    
    def _create_config_objects(self):
        """Create typed configuration objects"""
        # Database configurations
        db_config = self._config_data.get('databases', {})
        priorities = db_config.get('priorities', {})
        api_keys = db_config.get('api_keys', {})
        rate_limits = db_config.get('rate_limits', {})
        timeouts = db_config.get('timeouts', {})
        
        for db_name in priorities.keys():
            self.databases[db_name] = DatabaseConfig(
                name=db_name,
                priority=priorities.get(db_name, 5),
                api_key=api_keys.get(db_name),
                rate_limit=rate_limits.get(db_name, 5.0),
                timeout=timeouts.get(db_name, 30),
                enabled=True
            )
        
        # Performance configuration
        perf_config = self._config_data.get('performance', {})
        self.performance = PerformanceConfig(
            max_workers=perf_config.get('max_workers', 4),
            use_parallel=perf_config.get('use_parallel', True),
            batch_size=perf_config.get('batch_size', 50),
            max_concurrent_requests=perf_config.get('max_concurrent_requests', 30),
            max_cache_size_mb=perf_config.get('max_cache_size_mb', 500),
            cache_cleanup_interval=perf_config.get('cache_cleanup_interval', 3600),
            max_connections=perf_config.get('max_connections', 100),
            max_connections_per_host=perf_config.get('max_connections_per_host', 30)
        )
        
        # Cache configuration
        cache_config = self._config_data.get('cache', {})
        self.cache = CacheConfig(
            enabled=cache_config.get('enabled', True),
            directory=cache_config.get('directory', "~/.varannote/cache"),
            max_age_days=cache_config.get('max_age_days', 30),
            max_size_gb=cache_config.get('max_size_gb', 2.0),
            compression=cache_config.get('compression', True),
            strategies=cache_config.get('strategies', {})
        )
        
        # Output configuration
        output_config = self._config_data.get('output', {})
        self.output = OutputConfig(
            default_format=output_config.get('default_format', 'vcf'),
            available_formats=output_config.get('available_formats', ['vcf', 'tsv', 'json']),
            include_fields=output_config.get('include_fields', []),
            filters=output_config.get('filters', {})
        )
        
        # Logging configuration
        log_config = self._config_data.get('logging', {})
        self.logging_config = LoggingConfig(
            level=log_config.get('level', 'INFO'),
            directory=log_config.get('directory', "~/.varannote/logs"),
            max_file_size_mb=log_config.get('max_file_size_mb', 10),
            backup_count=log_config.get('backup_count', 5),
            categories=log_config.get('categories', {})
        )
    
    def _validate_configuration(self):
        """Validate configuration values"""
        errors = []
        
        # Validate database priorities
        for db_name, db_config in self.databases.items():
            if not (1 <= db_config.priority <= 10):
                errors.append(f"Database {db_name} priority must be between 1-10")
            
            if db_config.rate_limit <= 0:
                errors.append(f"Database {db_name} rate limit must be positive")
            
            if db_config.timeout <= 0:
                errors.append(f"Database {db_name} timeout must be positive")
        
        # Validate performance settings
        if self.performance.max_workers <= 0:
            errors.append("max_workers must be positive")
        
        if self.performance.batch_size <= 0:
            errors.append("batch_size must be positive")
        
        # Validate cache settings
        if self.cache.max_age_days <= 0:
            errors.append("cache max_age_days must be positive")
        
        if self.cache.max_size_gb <= 0:
            errors.append("cache max_size_gb must be positive")
        
        # Validate logging level
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.logging_config.level.upper() not in valid_levels:
            errors.append(f"logging level must be one of {valid_levels}")
        
        if errors:
            error_msg = "Configuration validation errors:\n" + "\n".join(f"  - {e}" for e in errors)
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.logger.info("Configuration validation passed")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self._get_nested_value(self._config_data, key.split('.'), default)
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        self._set_nested_value(self._config_data, key.split('.'), value)
    
    def get_database_config(self, database_name: str) -> Optional[DatabaseConfig]:
        """Get database configuration"""
        return self.databases.get(database_name)
    
    def get_enabled_databases(self) -> List[str]:
        """Get list of enabled databases sorted by priority"""
        enabled_dbs = [(name, config) for name, config in self.databases.items() if config.enabled]
        enabled_dbs.sort(key=lambda x: x[1].priority, reverse=True)
        return [name for name, _ in enabled_dbs]
    
    def save_user_config(self, config_updates: Dict[str, Any]):
        """Save user configuration updates"""
        user_config_file = self.user_config_dir / "user_config.yaml"
        
        # Merge with existing user config
        updated_config = self._deep_merge(self._user_config, config_updates)
        
        try:
            with open(user_config_file, 'w', encoding='utf-8') as f:
                yaml.dump(updated_config, f, default_flow_style=False, indent=2)
            
            self.logger.info(f"Saved user config to {user_config_file}")
            
            # Reload configurations
            self._load_configurations()
            
        except Exception as e:
            self.logger.error(f"Error saving user config: {e}")
            raise
    
    def export_config(self, output_file: Union[str, Path], format: str = "yaml"):
        """Export current configuration to file"""
        output_path = Path(output_file)
        
        try:
            if format.lower() == "yaml":
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self._config_data, f, default_flow_style=False, indent=2)
            elif format.lower() == "json":
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(self._config_data, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Exported config to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting config: {e}")
            raise
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        return {
            'config_file': str(self.config_file),
            'user_config_dir': str(self.user_config_dir),
            'databases': {
                'enabled': len([db for db in self.databases.values() if db.enabled]),
                'total': len(self.databases),
                'priorities': {name: config.priority for name, config in self.databases.items()}
            },
            'performance': asdict(self.performance),
            'cache': {
                'enabled': self.cache.enabled,
                'directory': self.cache.directory,
                'max_size_gb': self.cache.max_size_gb
            },
            'logging': {
                'level': self.logging_config.level,
                'directory': self.logging_config.directory
            }
        }
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'databases': {
                'priorities': {
                    'clinvar': 10, 'gnomad': 9, 'dbsnp': 8, 'ensembl': 7,
                    'cosmic': 6, 'pharmgkb': 5, 'omim': 4, 'clingen': 3, 'hgmd': 2
                },
                'api_keys': {db: None for db in ['clinvar', 'gnomad', 'dbsnp', 'ensembl', 
                                               'cosmic', 'pharmgkb', 'omim', 'clingen', 'hgmd']},
                'rate_limits': {
                    'clinvar': 3.0, 'gnomad': 10.0, 'dbsnp': 3.0, 'ensembl': 15.0,
                    'cosmic': 1.0, 'pharmgkb': 5.0, 'omim': 2.0, 'clingen': 5.0, 'hgmd': 1.0
                },
                'timeouts': {db: 30 for db in ['clinvar', 'gnomad', 'dbsnp', 'ensembl', 
                                             'cosmic', 'pharmgkb', 'omim', 'clingen', 'hgmd']}
            },
            'performance': {
                'max_workers': 4, 'use_parallel': True, 'batch_size': 50,
                'max_concurrent_requests': 30, 'max_cache_size_mb': 500,
                'cache_cleanup_interval': 3600, 'max_connections': 100,
                'max_connections_per_host': 30
            },
            'cache': {
                'enabled': True, 'directory': "~/.varannote/cache",
                'max_age_days': 30, 'max_size_gb': 2.0, 'compression': True
            },
            'output': {
                'default_format': 'vcf',
                'available_formats': ['vcf', 'tsv', 'json'],
                'include_fields': ['variant_id', 'gene_symbol', 'consequence'],
                'filters': {}
            },
            'logging': {
                'level': 'INFO', 'directory': "~/.varannote/logs",
                'max_file_size_mb': 10, 'backup_count': 5
            }
        }
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _get_nested_value(self, data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
        """Get nested dictionary value"""
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def _set_nested_value(self, data: Dict[str, Any], keys: List[str], value: Any):
        """Set nested dictionary value"""
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager(**kwargs) -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(**kwargs)
    return _config_manager


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value"""
    return get_config_manager().get(key, default)


def get_database_config(database_name: str) -> Optional[DatabaseConfig]:
    """Get database configuration"""
    return get_config_manager().get_database_config(database_name)


def get_enabled_databases() -> List[str]:
    """Get enabled databases sorted by priority"""
    return get_config_manager().get_enabled_databases() 