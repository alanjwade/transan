# src/config.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIRS = {
    'raw': PROJECT_ROOT / 'data' / 'raw',
    'processed': PROJECT_ROOT / 'data' / 'processed',
    'mappings': PROJECT_ROOT / 'data' / 'mappings'
}