#!/usr/bin/env python3
"""
Test suite for Configuration Manager

Tests configuration loading, validation, merging, and management functionality.
"""

import pytest
import tempfile
import yaml
import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from varannote.utils.config_manager import (
    ConfigManager, DatabaseConfig, PerformanceConfig, CacheConfig,
    OutputConfig, LoggingConfig, get_config_manager, get_config,
    get_database_config, get_enabled_databases
)


class TestDatabaseConfig:
    """Test DatabaseConfig dataclass"""
    
    def test_database_config_creation(self):
        """Test database configuration creation"""
        config = DatabaseConfig(
            name="clinvar",
            priority=10,
            api_key="test_key",
            rate_limit=3.0,
            timeout=30,
            enabled=True
        )
        
        assert config.name == "clinvar"
        assert config.priority == 10
        assert config.api_key == "test_key"
        assert config.rate_limit == 3.0
        assert config.timeout == 30
        assert config.enabled is True
    
    def test_database_config_defaults(self):
        """Test database configuration defaults"""
        config = DatabaseConfig(name="test")
        
        assert config.name == "test"
        assert config.priority == 5
        assert config.api_key is None
        assert config.rate_limit == 5.0
        assert config.timeout == 30
        assert config.enabled is True


class TestPerformanceConfig:
    """Test PerformanceConfig dataclass"""
    
    def test_performance_config_creation(self):
        """Test performance configuration creation"""
        config = PerformanceConfig(
            max_workers=8,
            use_parallel=True,
            batch_size=100,
            max_concurrent_requests=50
        )
        
        assert config.max_workers == 8
        assert config.use_parallel is True
        assert config.batch_size == 100
        assert config.max_concurrent_requests == 50
    
    def test_performance_config_defaults(self):
        """Test performance configuration defaults"""
        config = PerformanceConfig()
        
        assert config.max_workers == 4
        assert config.use_parallel is True
        assert config.batch_size == 50
        assert config.max_concurrent_requests == 30


class TestConfigManager:
    """Test ConfigManager class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.yaml"
        self.user_config_dir = Path(self.temp_dir) / "user_config"
        
        # Sample configuration data
        self.sample_config = {
            'databases': {
                'priorities': {
                    'clinvar': 10,
                    'gnomad': 9,
                    'dbsnp': 8
                },
                'api_keys': {
                    'clinvar': None,
                    'gnomad': None,
                    'dbsnp': None
                },
                'rate_limits': {
                    'clinvar': 3.0,
                    'gnomad': 10.0,
                    'dbsnp': 3.0
                },
                'timeouts': {
                    'clinvar': 45,
                    'gnomad': 30,
                    'dbsnp': 30
                }
            },
            'performance': {
                'max_workers': 4,
                'use_parallel': True,
                'batch_size': 50
            },
            'cache': {
                'enabled': True,
                'directory': "~/.varannote/cache",
                'max_age_days': 30
            },
            'logging': {
                'level': 'INFO',
                'directory': "~/.varannote/logs"
            }
        }
        
        # Write sample config file
        with open(self.config_file, 'w') as f:
            yaml.dump(self.sample_config, f)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
    
    def test_config_manager_initialization(self):
        """Test configuration manager initialization"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        assert config_manager.config_file.resolve() == self.config_file.resolve()
        assert config_manager.user_config_dir.resolve() == self.user_config_dir.resolve()
        assert isinstance(config_manager.databases, dict)
        assert isinstance(config_manager.performance, PerformanceConfig)
        assert isinstance(config_manager.cache, CacheConfig)
    
    def test_config_file_loading(self):
        """Test configuration file loading"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        # Check that databases were loaded
        assert 'clinvar' in config_manager.databases
        assert 'gnomad' in config_manager.databases
        assert 'dbsnp' in config_manager.databases
        
        # Check database priorities
        assert config_manager.databases['clinvar'].priority == 10
        assert config_manager.databases['gnomad'].priority == 9
        assert config_manager.databases['dbsnp'].priority == 8
    
    def test_default_config_fallback(self):
        """Test fallback to default configuration"""
        # Use non-existent config file
        non_existent_file = Path(self.temp_dir) / "non_existent.yaml"
        
        config_manager = ConfigManager(
            config_file=non_existent_file,
            user_config_dir=self.user_config_dir
        )
        
        # Should still have default databases
        assert len(config_manager.databases) > 0
        assert 'clinvar' in config_manager.databases
        assert config_manager.performance.max_workers == 4
    
    def test_user_config_merging(self):
        """Test user configuration merging"""
        # Create user config
        user_config_file = self.user_config_dir / "user_config.yaml"
        user_config_file.parent.mkdir(parents=True, exist_ok=True)
        
        user_config = {
            'performance': {
                'max_workers': 8  # Override default
            },
            'logging': {
                'level': 'DEBUG'  # Override default
            }
        }
        
        with open(user_config_file, 'w') as f:
            yaml.dump(user_config, f)
        
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        # Check that user config overrode defaults
        assert config_manager.performance.max_workers == 8
        assert config_manager.logging_config.level == 'DEBUG'
    
    def test_environment_variable_overrides(self):
        """Test environment variable overrides"""
        with patch.dict(os.environ, {
            'VARANNOTE_CLINVAR_API_KEY': 'test_api_key',
            'VARANNOTE_LOG_LEVEL': 'ERROR',
            'VARANNOTE_MAX_WORKERS': '16'
        }):
            config_manager = ConfigManager(
                config_file=self.config_file,
                user_config_dir=self.user_config_dir
            )
            
            # Check environment overrides
            assert config_manager.databases['clinvar'].api_key == 'test_api_key'
            assert config_manager.logging_config.level == 'ERROR'
            assert config_manager.performance.max_workers == 16
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        # Create invalid config
        invalid_config = self.sample_config.copy()
        invalid_config['databases']['priorities']['clinvar'] = 15  # Invalid priority
        invalid_config['performance']['max_workers'] = -1  # Invalid workers
        
        invalid_config_file = Path(self.temp_dir) / "invalid_config.yaml"
        with open(invalid_config_file, 'w') as f:
            yaml.dump(invalid_config, f)
        
        # Should raise validation error
        with pytest.raises(ValueError, match="Configuration validation errors"):
            ConfigManager(
                config_file=invalid_config_file,
                user_config_dir=self.user_config_dir
            )
    
    def test_get_configuration_value(self):
        """Test getting configuration values"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        # Test nested key access
        assert config_manager.get('databases.priorities.clinvar') == 10
        assert config_manager.get('performance.max_workers') == 4
        assert config_manager.get('cache.enabled') is True
        
        # Test default values
        assert config_manager.get('non.existent.key', 'default') == 'default'
    
    def test_set_configuration_value(self):
        """Test setting configuration values"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        # Set a value
        config_manager.set('performance.max_workers', 16)
        assert config_manager.get('performance.max_workers') == 16
        
        # Set nested value
        config_manager.set('new.nested.key', 'value')
        assert config_manager.get('new.nested.key') == 'value'
    
    def test_get_database_config(self):
        """Test getting database configuration"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        clinvar_config = config_manager.get_database_config('clinvar')
        assert isinstance(clinvar_config, DatabaseConfig)
        assert clinvar_config.name == 'clinvar'
        assert clinvar_config.priority == 10
        
        # Test non-existent database
        assert config_manager.get_database_config('non_existent') is None
    
    def test_get_enabled_databases(self):
        """Test getting enabled databases"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        enabled_dbs = config_manager.get_enabled_databases()
        assert isinstance(enabled_dbs, list)
        assert len(enabled_dbs) > 0
        
        # Should be sorted by priority (highest first)
        priorities = [config_manager.databases[db].priority for db in enabled_dbs]
        assert priorities == sorted(priorities, reverse=True)
    
    def test_save_user_config(self):
        """Test saving user configuration"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        # Save user config updates
        updates = {
            'performance': {
                'max_workers': 12
            },
            'new_setting': 'test_value'
        }
        
        config_manager.save_user_config(updates)
        
        # Check that user config file was created
        user_config_file = self.user_config_dir / "user_config.yaml"
        assert user_config_file.exists()
        
        # Check that configuration was updated
        assert config_manager.performance.max_workers == 12
        assert config_manager.get('new_setting') == 'test_value'
    
    def test_export_config_yaml(self):
        """Test exporting configuration to YAML"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        export_file = Path(self.temp_dir) / "exported_config.yaml"
        config_manager.export_config(export_file, format="yaml")
        
        assert export_file.exists()
        
        # Verify exported content
        with open(export_file, 'r') as f:
            exported_data = yaml.safe_load(f)
        
        assert 'databases' in exported_data
        assert 'performance' in exported_data
    
    def test_export_config_json(self):
        """Test exporting configuration to JSON"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        export_file = Path(self.temp_dir) / "exported_config.json"
        config_manager.export_config(export_file, format="json")
        
        assert export_file.exists()
        
        # Verify exported content
        with open(export_file, 'r') as f:
            exported_data = json.load(f)
        
        assert 'databases' in exported_data
        assert 'performance' in exported_data
    
    def test_export_config_invalid_format(self):
        """Test exporting configuration with invalid format"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        export_file = Path(self.temp_dir) / "exported_config.invalid"
        
        with pytest.raises(ValueError, match="Unsupported format"):
            config_manager.export_config(export_file, format="invalid")
    
    def test_get_config_summary(self):
        """Test getting configuration summary"""
        config_manager = ConfigManager(
            config_file=self.config_file,
            user_config_dir=self.user_config_dir
        )
        
        summary = config_manager.get_config_summary()
        
        assert isinstance(summary, dict)
        assert 'config_file' in summary
        assert 'user_config_dir' in summary
        assert 'databases' in summary
        assert 'performance' in summary
        assert 'cache' in summary
        assert 'logging' in summary
        
        # Check database summary
        db_summary = summary['databases']
        assert 'enabled' in db_summary
        assert 'total' in db_summary
        assert 'priorities' in db_summary


class TestGlobalConfigFunctions:
    """Test global configuration functions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        # Reset global config manager
        import varannote.utils.config_manager
        varannote.utils.config_manager._config_manager = None
        
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "test_config.yaml"
        
        # Sample configuration
        sample_config = {
            'databases': {
                'priorities': {'clinvar': 10, 'gnomad': 9},
                'api_keys': {'clinvar': None, 'gnomad': None},
                'rate_limits': {'clinvar': 3.0, 'gnomad': 10.0},
                'timeouts': {'clinvar': 30, 'gnomad': 30}
            },
            'performance': {'max_workers': 4},
            'test_key': 'test_value'
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(sample_config, f)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
        
        # Reset global config manager
        import varannote.utils.config_manager
        varannote.utils.config_manager._config_manager = None
    
    def test_get_config_manager(self):
        """Test get_config_manager function"""
        config_manager = get_config_manager(config_file=self.config_file)
        
        assert isinstance(config_manager, ConfigManager)
        
        # Should return same instance on subsequent calls
        config_manager2 = get_config_manager()
        assert config_manager is config_manager2
    
    def test_get_config(self):
        """Test get_config function"""
        # Initialize with test config
        get_config_manager(config_file=self.config_file)
        
        # Test getting values
        assert get_config('databases.priorities.clinvar') == 10
        assert get_config('performance.max_workers') == 4
        assert get_config('test_key') == 'test_value'
        assert get_config('non_existent', 'default') == 'default'
    
    def test_get_database_config(self):
        """Test get_database_config function"""
        # Initialize with test config
        get_config_manager(config_file=self.config_file)
        
        clinvar_config = get_database_config('clinvar')
        assert isinstance(clinvar_config, DatabaseConfig)
        assert clinvar_config.name == 'clinvar'
        assert clinvar_config.priority == 10
        
        assert get_database_config('non_existent') is None
    
    def test_get_enabled_databases(self):
        """Test get_enabled_databases function"""
        # Initialize with test config
        get_config_manager(config_file=self.config_file)
        
        enabled_dbs = get_enabled_databases()
        assert isinstance(enabled_dbs, list)
        assert 'clinvar' in enabled_dbs
        assert 'gnomad' in enabled_dbs
        
        # Should be sorted by priority
        assert enabled_dbs[0] == 'clinvar'  # Higher priority
        assert enabled_dbs[1] == 'gnomad'   # Lower priority


class TestConfigurationEdgeCases:
    """Test edge cases and error conditions"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            pass
    
    def test_malformed_yaml_config(self):
        """Test handling of malformed YAML configuration"""
        malformed_config_file = Path(self.temp_dir) / "malformed.yaml"
        
        # Write malformed YAML
        with open(malformed_config_file, 'w') as f:
            f.write("invalid: yaml: content: [unclosed")
        
        # Should fall back to default config
        config_manager = ConfigManager(config_file=malformed_config_file)
        assert len(config_manager.databases) > 0  # Should have defaults
    
    def test_empty_config_file(self):
        """Test handling of empty configuration file"""
        empty_config_file = Path(self.temp_dir) / "empty.yaml"
        
        # Create empty file
        empty_config_file.touch()
        
        # Should fall back to default config
        config_manager = ConfigManager(config_file=empty_config_file)
        assert len(config_manager.databases) > 0  # Should have defaults
    
    def test_permission_error_handling(self):
        """Test handling of permission errors"""
        # This test might not work on all systems, so we'll mock it
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            config_manager = ConfigManager()
            # Should fall back to default config
            assert len(config_manager.databases) > 0
    
    def test_deep_merge_edge_cases(self):
        """Test deep merge with edge cases"""
        config_manager = ConfigManager()
        
        # Test merging with None values
        dict1 = {'a': {'b': 1}, 'c': 2}
        dict2 = {'a': {'d': 3}, 'c': None}
        
        result = config_manager._deep_merge(dict1, dict2)
        
        assert result['a']['b'] == 1  # Preserved
        assert result['a']['d'] == 3  # Added
        assert result['c'] is None    # Overwritten
    
    def test_nested_value_operations(self):
        """Test nested value get/set operations"""
        config_manager = ConfigManager()
        
        # Test getting from empty dict
        assert config_manager._get_nested_value({}, ['a', 'b'], 'default') == 'default'
        
        # Test setting nested values
        data = {}
        config_manager._set_nested_value(data, ['a', 'b', 'c'], 'value')
        assert data['a']['b']['c'] == 'value'


if __name__ == "__main__":
    pytest.main([__file__]) 