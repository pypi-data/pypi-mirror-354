import pytest
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tbh_secure_agents.memory import FileBasedPersistentKnowledgeBase, FileBasedPersistentSharedKnowledge

@pytest.fixture
def temp_kb_path():
    """Create a temporary directory for the knowledge base and clean it up afterward."""
    path = "./.test_kb_temp"
    os.makedirs(path, exist_ok=True)
    yield path
    shutil.rmtree(path)

@pytest.fixture
def expert_kb(temp_kb_path):
    """Create a FileBasedPersistentKnowledgeBase instance for testing."""
    expert_id = "test_expert_123"
    return FileBasedPersistentKnowledgeBase(expert_id=expert_id, base_path=temp_kb_path)

def test_recall_returns_value_when_key_exists(expert_kb):
    """Verify that recall() returns the direct string value for an existing key."""
    key = "fact_a"
    value = "This is the value for fact_a"
    
    # Store a fact using the correct 'remember' method
    expert_kb.remember(key, value)
    expert_kb.save()

    # Recall should return only the 'value' field as a string
    recalled_value = expert_kb.recall(key=key)

    assert recalled_value == value

def test_recall_returns_none_when_key_does_not_exist_and_no_default(expert_kb):
    """Verify that recall() returns None for a non-existent key with no default."""
    recalled_value = expert_kb.recall("another_non_existent_key")
    assert recalled_value is None

def test_recall_returns_custom_default_when_key_does_not_exist(expert_kb):
    """Verify that recall() returns a custom default value for a non-existent key."""
    custom_default = "No value found"
    recalled_value = expert_kb.recall(key="non_existent_key", default=custom_default)

    assert recalled_value == custom_default

# --- Squad Shared Knowledge Tests ---

@pytest.fixture
def squad_kb():
    """Create a temporary shared knowledge base for a squad and clean it up afterward."""
    kb_path = Path("./.pytest_squad_kb_test")
    kb_path.mkdir(exist_ok=True)
    
    squad_id = "test_squad_456"
    kb = FileBasedPersistentSharedKnowledge(base_path=str(kb_path))
    kb.set_active_squad(squad_id)
    
    yield kb
    
    shutil.rmtree(kb_path)


def test_squad_kb_contribution_and_access(squad_kb):
    """Verify that a fact contributed in a session can be accessed in the same session."""
    session_id = "session_1"
    squad_kb.set_active_session(session_id)
    
    key = "shared_fact_1"
    value = "This is a shared fact."
    contributor = "expert_A"
    
    squad_kb.contribute(key, value, contributor_id=contributor)
    
    retrieved_value = squad_kb.access(key)
    assert retrieved_value == value

def test_squad_kb_session_isolation(squad_kb):
    """Verify that knowledge is isolated between different sessions."""
    # Session 1
    session_1_id = "session_A"
    squad_kb.set_active_session(session_1_id)
    squad_kb.contribute("fact_A", "value_A")
    
    # Session 2
    session_2_id = "session_B"
    squad_kb.set_active_session(session_2_id)
    squad_kb.contribute("fact_B", "value_B")
    
    # Check that fact_A is not in session_B
    assert squad_kb.access("fact_A") is None
    # Check that fact_B is in session_B
    assert squad_kb.access("fact_B") == "value_B"
    
    # Switch back to Session 1
    squad_kb.set_active_session(session_1_id)
    # Check that fact_A is in session_A
    assert squad_kb.access("fact_A") == "value_A"
    # Check that fact_B is not in session_A
    assert squad_kb.access("fact_B") is None
