"""
Greeum - 다국어 지원 LLM 독립적인 기억 관리 시스템

This package contains independent modules to provide a human-like 
memory system for Large Language Models.
"""

__version__ = "0.6.1"

# Lazy loading to avoid import timeouts
# Users should import directly from submodules:
# from greeum.text_utils import process_user_input
# from greeum.database_manager import DatabaseManager
# from greeum.block_manager import BlockManager
# etc.

__all__ = [
    "__version__",
]