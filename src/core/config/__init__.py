import sys
from dataclasses import dataclass
from core.config import defaults 
from pathlib import Path

@dataclass
class BaseConfig:
    """Base Configuration with explicit type hints for the IDE."""

    DEBUG: bool = False
    DEVELOPMENT: bool = False 
    TESTING: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "default-secret-key"
    PROJECT_ROOT: Path = defaults.PROJECT_ROOT
    STATIC_ROOT: Path = defaults.STATIC_ROOT 
    SITEMAPS_ROOT: Path = defaults.SITEMAPS_ROOT
    TEMPLATES_ROOT: Path = defaults.TEMPLATES_ROOT
    PAGES_ROOT: Path = defaults.PAGES_ROOT
 
    @property
    def is_testing(self) -> bool:
        return self.TESTING

    @property
    def is_development(self) -> bool:
        return self.DEVELOPMENT


# --- Environment Resolution Logic ---


def get_config_obj() -> BaseConfig:
    # 1. Start with safe defaults
    cfg = BaseConfig()

    # 2. Layer local overrides safely if file exists
    try:
        from core.config import local as local_mod

        for key in dir(local_mod):
            if key.isupper() and hasattr(cfg, key):
                setattr(cfg, key, getattr(local_mod, key))
    except ImportError:
        pass  # .local is optional

    # 3. Layer testing overrides if running under pytest
    is_pytest = "pytest" in sys.modules or "pytest" in sys.argv[0]
    if is_pytest:
        cfg.TESTING = True
        cfg.DEBUG = False
        cfg.DATABASE_URL = "sqlite:///test.db"

    return cfg


# Instantiate the typed object
config = get_config_obj()
