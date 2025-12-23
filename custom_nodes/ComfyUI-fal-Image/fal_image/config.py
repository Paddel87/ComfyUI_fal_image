import os
import configparser

def _read_ini():
    cfg = configparser.ConfigParser()
    ini_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    ini_path = os.path.normpath(ini_path)
    if os.path.exists(ini_path):
        cfg.read(ini_path, encoding='utf-8')
    return cfg

def get_api_key():
    key = os.getenv('FAL_KEY')
    if key:
        return key.strip()
    cfg = _read_ini()
    if cfg.has_section('fal') and cfg.has_option('fal', 'key'):
        val = cfg.get('fal', 'key')
        if val:
            return val.strip()
    return None

def get_timeout_default():
    cfg = _read_ini()
    if cfg.has_section('fal') and cfg.has_option('fal', 'timeout_sec'):
        try:
            return int(cfg.get('fal', 'timeout_sec'))
        except Exception:
            pass
    return 60

def get_retries_default():
    cfg = _read_ini()
    if cfg.has_section('fal') and cfg.has_option('fal', 'retries'):
        try:
            return int(cfg.get('fal', 'retries'))
        except Exception:
            pass
    return 2

