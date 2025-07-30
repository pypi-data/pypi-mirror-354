import logging
import sys
import os
import shutil
from datetime import datetime, timezone

# Forceful logger setup for memory.py
memory_logger = logging.getLogger(__name__ + '_memory_specific') # Added suffix to avoid potential conflicts
memory_logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
stream_handler.setFormatter(formatter)
# Check if handlers already exist to prevent duplication if module is reloaded
if not any(isinstance(h, logging.StreamHandler) and h.stream == sys.stdout for h in memory_logger.handlers):
    memory_logger.addHandler(stream_handler)
memory_logger.propagate = False # Prevent messages from going to the root logger

"""
Defines the memory structures for the SecureAgents framework.

This module includes definitions for:
- WorkingMemory: Short-term, in-memory storage for an Expert.
- PersistentKnowledgeBase: Long-term, persistent storage for an Expert.
- SharedScratchpad: Short-term, in-memory shared storage for a Squad.
- PersistentSharedKnowledge: Long-term, persistent shared storage for a Squad.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from filelock import FileLock, Timeout
import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# --- Expert-Specific Memory --- #

class WorkingMemory(ABC):
    """Abstract base class for an Expert's working memory, treated as a log."""

    @abstractmethod
    def add(self, entry: Dict[str, Any]) -> None:
        """Add an entry to the working memory log."""
        pass

    @abstractmethod
    def get_recent(self, count: int) -> List[Dict[str, Any]]:
        """Retrieve the most recent 'count' entries from working memory."""
        pass

    @abstractmethod
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Retrieve all entries from working memory."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from working memory."""
        pass

class DefaultWorkingMemory(WorkingMemory):
    """A simple list-based implementation of WorkingMemory, acting as a log."""
    def __init__(self, max_entries: Optional[int] = None):
        self._memory_log: List[Dict[str, Any]] = []
        self.max_entries = max_entries # Optional: to cap memory size

    def add(self, entry: Dict[str, Any]) -> None:
        self._memory_log.append(entry)
        if self.max_entries is not None and len(self._memory_log) > self.max_entries:
            self._memory_log.pop(0) # Remove oldest entry if max_entries is exceeded

    def get_recent(self, count: int) -> List[Dict[str, Any]]:
        return self._memory_log[-count:]

    def get_all_entries(self) -> List[Dict[str, Any]]:
        return list(self._memory_log) # Return a copy

    def clear(self) -> None:
        self._memory_log.clear()


class PersistentKnowledgeBase(ABC):
    """Abstract base class for an Expert's persistent knowledge base."""

    @abstractmethod
    def load(self, identifier: str) -> None:
        """Load knowledge for a given identifier (e.g., expert_id)."""
        pass

    @abstractmethod
    def save(self, identifier: str) -> None:
        """Save knowledge for a given identifier."""
        pass

    @abstractmethod
    def remember(self, key: str, value: Any) -> None:
        """Store a piece of knowledge."""
        pass

    @abstractmethod
    def recall(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Retrieve a piece of knowledge."""
        pass

    @abstractmethod
    def forget(self, key: str) -> None:
        """Remove a piece of knowledge."""
        pass

    @abstractmethod
    def clear_all_knowledge(self) -> None:
        """Clear all knowledge from this knowledge base."""
        pass

# --- Squad-Specific Memory --- #

class SharedScratchpad(ABC):
    """Abstract base class for a Squad's shared scratchpad."""

    @abstractmethod
    def write(self, key: str, value: Any) -> None:
        """Write a value to the shared scratchpad."""
        pass

    @abstractmethod
    def read(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Read a value from the shared scratchpad."""
        pass

    @abstractmethod
    def remove(self, key: str) -> None:
        """Remove a value from the shared scratchpad."""
        pass

    @abstractmethod
    def clear_scratchpad(self) -> None:
        """Clear all items from the shared scratchpad."""
        pass

class DefaultSharedScratchpad(SharedScratchpad):
    """A simple dictionary-based implementation of SharedScratchpad."""
    def __init__(self):
        self._scratchpad: Dict[str, Any] = {}

    def write(self, key: str, value: Any) -> None:
        self._scratchpad[key] = value

    def read(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return self._scratchpad.get(key, default)

    def remove(self, key: str) -> None:
        if key in self._scratchpad:
            del self._scratchpad[key]

    def clear_scratchpad(self) -> None:
        self._scratchpad.clear()


class PersistentSharedKnowledge(ABC):
    """Abstract base class for a Squad's persistent shared knowledge."""

    @abstractmethod
    def load_shared(self, identifier: str) -> None:
        """Load shared knowledge for a given identifier (e.g., squad_id)."""
        pass

    @abstractmethod
    def save_shared(self, identifier: str) -> None:
        """Save shared knowledge for a given identifier."""
        pass

    @abstractmethod
    def contribute(self, key: str, value: Any, contributor_id: Optional[str] = None) -> None:
        """Contribute a piece of knowledge to the shared store."""
        pass

    @abstractmethod
    def access(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Access a piece of shared knowledge."""
        pass

    @abstractmethod
    def retract(self, key: str, contributor_id: Optional[str] = None) -> None:
        """Retract a piece of knowledge (requires appropriate permissions or ownership)."""
        pass

    @abstractmethod
    def clear_all_shared_knowledge(self) -> None:
        """Clear all shared knowledge from this store."""
        pass

# Placeholder for a simple file-based persistent knowledge implementation
# This would be fleshed out later or replaced with a database solution.
class FileBasedPersistentKnowledgeBase(PersistentKnowledgeBase):
    """
    Stores knowledge in a JSON file, with file locking for safety.
    Session-aware: knowledge is partitioned by session_id.
    """
    def __init__(self, expert_id: str, base_path: str = "./.tbh_secure_agents_knowledge_bases", 
                 lock_timeout: int = 10, initial_session_id: str = "default_expert_session"):
        if not expert_id:
            raise ValueError("expert_id must be provided for FileBasedPersistentKnowledgeBase")
        if not initial_session_id:
            raise ValueError("initial_session_id must be provided and cannot be empty")
            
        self.expert_id = expert_id
        self.base_path = Path(base_path)
        self.lock_timeout = lock_timeout
        self._knowledge: Dict[str, Any] = {}
        self._current_session_id = initial_session_id
        
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.load() # Auto-load for the initial session
        logger.debug(f"FileBasedPersistentKnowledgeBase initialized for expert '{self.expert_id}', initial session '{self._current_session_id}'. Path: {self._get_current_file_path()}")

    def _get_current_file_path(self) -> Path:
        return self.base_path / f"expert_{self.expert_id}_session_{self._current_session_id}_kb.json"

    def _get_current_lock_path(self) -> Path:
        return self.base_path / f"expert_{self.expert_id}_session_{self._current_session_id}_kb.json.lock"

    def set_active_session(self, session_id: str) -> None:
        if not session_id:
            raise ValueError("session_id cannot be empty when setting active session.")
        if self._current_session_id == session_id:
            logger.debug(f"Session for expert '{self.expert_id}' is already '{session_id}'. No change needed.")
            return
        
        logger.info(f"Expert '{self.expert_id}': Changing active session from '{self._current_session_id}' to '{session_id}'.")
        self._current_session_id = session_id
        self.load() # Load data for the new session

    def load(self, identifier: Optional[str] = None) -> None: # identifier is not used internally, relies on self.expert_id and self._current_session_id
        file_path = self._get_current_file_path()
        lock_path = self._get_current_lock_path()
        lock = FileLock(lock_path, timeout=self.lock_timeout)
        try:
            with lock.acquire():
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            self._knowledge = json.load(f)
                        logger.info(f"Knowledge base loaded for expert '{self.expert_id}', session '{self._current_session_id}' from {file_path}")
                    except (json.JSONDecodeError, IOError) as e:
                        logger.error(f"Error loading knowledge base for expert '{self.expert_id}', session '{self._current_session_id}' from {file_path}: {e}")
                        self._knowledge = {} # Start fresh if loading fails
                else:
                    logger.info(f"No existing KB file for expert '{self.expert_id}', session '{self._current_session_id}' at {file_path}. Initializing empty KB.")
                    self._knowledge = {}
        except Timeout:
            logger.error(f"Timeout acquiring lock for loading KB for expert '{self.expert_id}', session '{self._current_session_id}' at {lock_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during KB load for expert '{self.expert_id}', session '{self._current_session_id}': {e}")

    def save(self, identifier: Optional[str] = None) -> None: # Modified to match ABC
        # Identifier is self.expert_id
        file_path = self._get_current_file_path()
        lock_path = self._get_current_lock_path()
        lock = FileLock(lock_path, timeout=self.lock_timeout)
        lock_acquired_successfully = False
        tmp_file_path_str = str(file_path) + ".tmp" # Define tmp_file_path_str early for logging in case of early errors

        try:
            with lock.acquire():
                lock_acquired_successfully = True
                memory_logger.debug(f"Attempting to save KB for expert '{self.expert_id}', session '{self._current_session_id}'. Knowledge size: {len(self._knowledge) if hasattr(self._knowledge, '__len__') else 'N/A'}")
                # tmp_file_path_str is already defined
            try:
                memory_logger.debug(f"Attempting to write to temporary file {tmp_file_path_str} for expert '{self.expert_id}', session '{self._current_session_id}'.")
                with open(tmp_file_path_str, 'w') as f:
                    json.dump(self._knowledge, f, indent=4)
                    f.flush()
                    os.fsync(f.fileno())
                memory_logger.debug(f"Successfully wrote and synced temporary file {tmp_file_path_str}.")

                if os.path.exists(tmp_file_path_str):
                    memory_logger.debug(f"PRE-RENAME CHECK: Temp file {tmp_file_path_str} EXISTS.")
                    try:
                        with open(tmp_file_path_str, 'r') as verify_f:
                            content_on_disk = verify_f.read()
                        if not content_on_disk.strip():
                            raise ValueError("Temporary file is empty or contains only whitespace.")
                        json.loads(content_on_disk)
                        memory_logger.debug(f"PRE-RENAME CHECK: Temp file {tmp_file_path_str} content (length {len(content_on_disk)}) is valid JSON.")
                    except Exception as verify_err:
                        memory_logger.error(f"PRE-RENAME CHECK: Temp file {tmp_file_path_str} failed validation: {verify_err}")
                        raise
                else:
                    memory_logger.error(f"PRE-RENAME CHECK: Temp file {tmp_file_path_str} DOES NOT EXIST after write attempt.")
                    raise FileNotFoundError(f"Temporary file {tmp_file_path_str} not found after write attempt.")

                memory_logger.debug(f"Attempting to rename {tmp_file_path_str} to {file_path}.")
                os.rename(tmp_file_path_str, file_path)
                memory_logger.info(f"Successfully renamed temporary file to {file_path}. Atomic write complete.")
                memory_logger.info(f"Knowledge base saved for expert '{self.expert_id}', session '{self._current_session_id}' to {file_path}")

            except Exception as write_err:
                memory_logger.exception(f"Error during atomic save for expert '{self.expert_id}', session '{self._current_session_id}' (temp file {tmp_file_path_str}): {write_err}")
                if os.path.exists(tmp_file_path_str):
                    try:
                        os.remove(tmp_file_path_str)
                        memory_logger.info(f"Cleaned up temporary file {tmp_file_path_str} after error.")
                    except OSError as cleanup_err:
                        memory_logger.error(f"Failed to clean up temporary file {tmp_file_path_str}: {cleanup_err}")
                raise
        except Timeout:
            memory_logger.error(f"Timeout acquiring lock for saving KB for expert '{self.expert_id}', session '{self._current_session_id}' at {lock_path}")
            raise
        except Exception as e:
            memory_logger.exception(f"Unexpected error during KB save for expert '{self.expert_id}', session '{self._current_session_id}': {e}")
            raise
        finally:
            if lock_acquired_successfully:
                if os.path.exists(lock_path):
                    memory_logger.info(f"POST-LOCK-RELEASE (finally): Lock file {lock_path} found for expert '{self.expert_id}', session '{self._current_session_id}'. Attempting os.remove().")
                    try:
                        os.remove(lock_path)
                        if not os.path.exists(lock_path):
                            memory_logger.info(f"POST-LOCK-RELEASE (finally): os.remove() on {lock_path} succeeded for expert '{self.expert_id}', session '{self._current_session_id}'.")
                        else:
                            memory_logger.error(f"POST-LOCK-RELEASE (finally): os.remove() on {lock_path} CALLED, but file STILL EXISTS for expert '{self.expert_id}', session '{self._current_session_id}'.")
                    except OSError as e_remove:
                        memory_logger.error(f"POST-LOCK-RELEASE (finally): os.remove() on {lock_path} FAILED for expert '{self.expert_id}', session '{self._current_session_id}': {e_remove}")
                else:
                    memory_logger.debug(f"POST-LOCK-RELEASE (finally): Lock file {lock_path} was already deleted for expert '{self.expert_id}', session '{self._current_session_id}'.")
            else:
                memory_logger.debug(f"POST-LOCK-RELEASE (finally): Lock was not acquired for expert '{self.expert_id}', session '{self._current_session_id}' from this instance's save method.")

    def remember(self, key: str, value: Any, category: Optional[str] = None) -> None: # Added category to match old implementation's store method
        self._knowledge[key] = {
            "value": value,
            "category": category,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.save() # Save handles its own locking

    def recall(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        lock_path = self._get_current_lock_path()
        lock = FileLock(lock_path, timeout=self.lock_timeout)
        try:
            with lock.acquire(timeout=0.1): 
                item = self._knowledge.get(key)
                return item["value"] if item and isinstance(item, dict) and "value" in item else default
        except Timeout:
            memory_logger.warning(f"Timeout acquiring lock for recalling from KB for expert '{self.expert_id}', session '{self._current_session_id}'. Serving from in-memory data.")
            item = self._knowledge.get(key)
            return item["value"] if item and isinstance(item, dict) and "value" in item else default
        except Exception as e:
            memory_logger.error(f"An unexpected error occurred during KB recall for expert '{self.expert_id}', session '{self._current_session_id}': {e}")
            return default

    def forget(self, key: str) -> None:
        if key in self._knowledge:
            del self._knowledge[key]
            self.save() # Save handles its own locking
            memory_logger.info(f"Fact '{key}' forgotten by expert '{self.expert_id}', session '{self._current_session_id}'.")
        else:
            memory_logger.info(f"Fact '{key}' not found in KB for expert '{self.expert_id}', session '{self._current_session_id}'.")

    def get_all_facts(self) -> Dict[str, Any]:
        lock_path = self._get_current_lock_path()
        lock = FileLock(lock_path, timeout=self.lock_timeout)
        try:
            with lock.acquire(timeout=0.1):
                return self._knowledge.copy()
        except Timeout:
            memory_logger.warning(f"Timeout acquiring lock for get_all_facts for expert '{self.expert_id}', session '{self._current_session_id}'. Serving from in-memory data.")
            return self._knowledge.copy()
        except Exception as e:
            memory_logger.error(f"An unexpected error occurred during KB get_all_facts for expert '{self.expert_id}', session '{self._current_session_id}': {e}")
            return {}
    
    def clear_all_knowledge(self) -> None:
        self._knowledge = {}
        self.save()
        memory_logger.info(f"All knowledge cleared for expert '{self.expert_id}', session '{self._current_session_id}'.")

# Similarly, a placeholder for FileBasedPersistentSharedKnowledge
class FileBasedPersistentSharedKnowledge(PersistentSharedKnowledge):
    """Manages persistent shared knowledge for squads using file-based storage.

    This class handles the loading, saving, and session management of shared
    facts stored in JSON files. It uses file locks to prevent race conditions
    during concurrent access and includes mechanisms for handling corrupted files
    and configurable timeouts.

    Key features:
    - Session-specific knowledge files: Each squad and session combination has its own file.
    - Atomic writes: Uses a temporary file and rename operation for saving to minimize data corruption.
    - File locking: Employs `filelock` to manage concurrent access to session files.
    - Corrupted file handling: Backs up corrupted session files before initializing a new one.
    - Configurable lock timeout: Lock timeout can be set via an environment variable
      (TBH_MEMORY_LOCK_TIMEOUT) or constructor argument.
    """
    def __init__(self, base_path: str = './.squad_knowledge', lock_timeout: int = 10):
        """Initializes FileBasedPersistentSharedKnowledge.

        Args:
            base_path (str): The base directory where session files will be stored.
            lock_timeout (int): Default timeout in seconds for acquiring file locks.
                This can be overridden by the TBH_MEMORY_LOCK_TIMEOUT environment variable.
        """
        self.base_path = Path(base_path)
        self._shared_knowledge: Dict[str, Any] = {}
        self._current_identifier: Optional[str] = None  # Represents current squad_id
        self._current_session_id: Optional[str] = None # Represents current session_id
        
        # Configure lock_timeout from environment variable or constructor argument
        env_lock_timeout_str = os.environ.get('TBH_MEMORY_LOCK_TIMEOUT')
        if env_lock_timeout_str:
            try:
                env_lock_timeout = int(env_lock_timeout_str)
                if env_lock_timeout > 0:
                    self.lock_timeout = env_lock_timeout
                    memory_logger.info(f"Using lock timeout from TBH_MEMORY_LOCK_TIMEOUT: {self.lock_timeout}s")
                else:
                    self.lock_timeout = lock_timeout # Use constructor default if env var is invalid
                    memory_logger.warning(f"Invalid TBH_MEMORY_LOCK_TIMEOUT value '{env_lock_timeout_str}'. Using default: {self.lock_timeout}s")
            except ValueError:
                self.lock_timeout = lock_timeout # Use constructor default if env var is not an int
                memory_logger.warning(f"TBH_MEMORY_LOCK_TIMEOUT value '{env_lock_timeout_str}' is not a valid integer. Using default: {self.lock_timeout}s")
        else:
            self.lock_timeout = lock_timeout # Use constructor default if env var is not set

        self.base_path.mkdir(parents=True, exist_ok=True)
        memory_logger.debug(f"FileBasedPersistentSharedKnowledge initialized. Base path: {self.base_path}, Lock Timeout: {self.lock_timeout}s")

    def _get_file_path(self) -> Path:
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot get file path: squad_id or session_id is not set.")
            raise ValueError("Squad ID and Session ID must be set to determine file path.")
        return self.base_path / f"squad_{self._current_identifier}_session_{self._current_session_id}_shared.json"

    def _get_lock_path(self) -> Path:
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot get lock path: squad_id or session_id is not set.")
            raise ValueError("Squad ID and Session ID must be set to determine lock path.")
        return self.base_path / f"squad_{self._current_identifier}_session_{self._current_session_id}_shared.json.lock"

    def set_active_squad(self, squad_id: str) -> None:
        """Sets the active squad context, preparing for session management."""
        memory_logger.info(f"Setting active squad to: {squad_id}")
        if self._current_identifier != squad_id:
            self._current_identifier = squad_id
            # When the squad changes, the session context is no longer valid and must be reset.
            self._current_session_id = None
            self._shared_knowledge = {}
            memory_logger.info(f"Active squad set to '{squad_id}'. Session has been reset.")

    def set_active_session(self, session_id: str) -> None:
        """Sets the active session for the current squad, loading its knowledge."""
        if not self._current_identifier:
            memory_logger.error("Cannot set session without an active squad. Call set_active_squad() first.")
            raise ValueError("Cannot set session without an active squad. Call set_active_squad() first.")
        
        memory_logger.info(f"Attempting to set active session to '{session_id}' for squad '{self._current_identifier}'.")
        if self._current_session_id == session_id:
            memory_logger.info(f"Session '{session_id}' is already active for squad '{self._current_identifier}'. No change.")
            return

        self._current_session_id = session_id
        memory_logger.info(f"Active session for squad '{self._current_identifier}' set to '{self._current_session_id}'.")
        self.load_shared() # Load data for the new session

    def load_shared(self) -> None:
        """Loads shared knowledge for the currently active squad and session from its file.

        If the session file is found to be corrupted (e.g., invalid JSON), it attempts
        to back up the corrupted file by renaming it with a '.corrupted.<timestamp>'
        suffix, and then initializes an empty knowledge base for the session.
        If no file exists, an empty knowledge base is initialized.
        File locking is used to ensure safe concurrent access during loading.
        """
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot load shared knowledge: Squad ID or Session ID is not set.")
            self._shared_knowledge = {}
            return

        file_path = self._get_file_path()
        lock_path = self._get_lock_path()
        lock = FileLock(str(lock_path), timeout=self.lock_timeout)
        lock_acquired_successfully = False

        try:
            memory_logger.debug(f"Attempting to acquire lock for loading shared KB for Squad '{self._current_identifier}', Session '{self._current_session_id}': {lock_path}")
            with lock.acquire():
                lock_acquired_successfully = True
                memory_logger.debug(f"Lock acquired for Squad '{self._current_identifier}', Session '{self._current_session_id}': {lock_path}")
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            self._shared_knowledge = json.load(f)
                        memory_logger.info(f"Shared knowledge for Squad '{self._current_identifier}', Session '{self._current_session_id}' loaded from {file_path}")
                    except (json.JSONDecodeError, IOError) as e:
                        memory_logger.error(f"Error loading/decoding shared knowledge for Squad '{self._current_identifier}', Session '{self._current_session_id}' from {file_path}: {e}")
                        try:
                            backup_file_path = file_path.parent / f"{file_path.name}.corrupted.{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
                            shutil.move(str(file_path), str(backup_file_path))
                            memory_logger.info(f"Corrupted shared knowledge file {file_path} backed up to {backup_file_path}")
                        except Exception as backup_err:
                            memory_logger.error(f"Failed to back up corrupted file {file_path}: {backup_err}")
                        self._shared_knowledge = {} # Initialize to empty after attempting backup
                else:
                    memory_logger.info(f"No existing shared knowledge file for Squad '{self._current_identifier}', Session '{self._current_session_id}' at {file_path}. Initializing empty.")
                    self._shared_knowledge = {}
        except Timeout:
            memory_logger.error(f"Timeout acquiring lock for loading shared KB for Squad '{self._current_identifier}', Session '{self._current_session_id}' at {lock_path}")
        except Exception as e:
            memory_logger.exception(f"An unexpected error occurred during shared knowledge load for Squad '{self._current_identifier}', Session '{self._current_session_id}': {e}")
            self._shared_knowledge = {} # Ensure a consistent state
        finally:
            if lock_acquired_successfully:
                if lock.is_locked:
                    try:
                        lock.release()
                        memory_logger.info(f"Lock explicitly released for {lock_path} in finally block after load.")
                    except Exception as release_err:
                        memory_logger.error(f"Error explicitly releasing lock {lock_path} in finally block after load: {release_err}")
                else:
                    memory_logger.debug(f"Lock for {lock_path} was already released before finally block after load.")

            lock_file_str = str(lock_path)
            if os.path.exists(lock_file_str):
                try:
                    os.remove(lock_file_str)
                    memory_logger.info(f"Successfully deleted stray lock file after loading: {lock_file_str}")
                except OSError as e:
                    memory_logger.error(f"Error deleting stray lock file {lock_file_str} after loading: {e}. This might be okay.")
            else:
                memory_logger.debug(f"Lock file {lock_file_str} was not found post-load, no explicit deletion needed.")

    def save_shared(self) -> None:
        """Saves the current in-memory shared knowledge to a file for the active session.

        Uses an atomic write operation (write to temp file, then rename) to prevent
        data corruption. File locking is used to ensure safe concurrent access.
        Includes pre-rename checks to validate the temporary file's content.
        """
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Error: Squad ID or Session ID not set. Cannot save shared knowledge.")
            return

        file_path = self._get_file_path()
        lock_path = self._get_lock_path()
        lock = FileLock(str(lock_path), timeout=self.lock_timeout)
        lock_acquired_successfully = False

        try:
            memory_logger.debug(f"Attempting to acquire lock for saving shared KB for Squad '{self._current_identifier}', Session '{self._current_session_id}': {lock_path}")
            with lock.acquire():
                lock_acquired_successfully = True
                memory_logger.debug(f"Lock acquired for saving shared KB: {lock_path}")
                
                tmp_file_path = Path(str(file_path) + ".tmp")
                try:
                    memory_logger.debug(f"Attempting to write shared knowledge to temporary file {tmp_file_path} for Squad '{self._current_identifier}', Session '{self._current_session_id}'.")
                    with open(tmp_file_path, 'w') as f:
                        json.dump(self._shared_knowledge, f, indent=4)
                        f.flush()
                        os.fsync(f.fileno())
                    memory_logger.debug(f"Successfully wrote and synced temporary file {tmp_file_path}.")

                    if os.path.exists(tmp_file_path):
                        memory_logger.debug(f"PRE-RENAME CHECK: Temp file {tmp_file_path} EXISTS.")
                        try:
                            with open(tmp_file_path, 'r') as verify_f:
                                content_on_disk = verify_f.read()
                            if not content_on_disk.strip():
                                raise ValueError("Temporary file is empty or contains only whitespace.")
                            json.loads(content_on_disk)
                            memory_logger.debug(f"PRE-RENAME CHECK: Temp file {tmp_file_path} content (length {len(content_on_disk)}) is valid JSON.")
                        except Exception as verify_err:
                            memory_logger.error(f"PRE-RENAME CHECK: Temp file {tmp_file_path} failed validation: {verify_err}")
                            raise
                    else:
                        memory_logger.error(f"PRE-RENAME CHECK: Temp file {tmp_file_path} DOES NOT EXIST after write attempt.")
                        raise FileNotFoundError(f"Temporary file {tmp_file_path} not found after write attempt.")

                    memory_logger.debug(f"Attempting to rename {tmp_file_path} to {file_path}.")
                    os.rename(tmp_file_path, file_path)
                    memory_logger.info(f"Successfully renamed temporary file to {file_path}. Atomic write for shared KB complete for Squad '{self._current_identifier}', Session '{self._current_session_id}'.")

                except Exception as write_err:
                    memory_logger.exception(f"Error during atomic save for Squad '{self._current_identifier}', Session '{self._current_session_id}' (temp file {tmp_file_path}): {write_err}")
                    if os.path.exists(tmp_file_path):
                        try:
                            os.remove(tmp_file_path)
                            memory_logger.info(f"Cleaned up temporary file {tmp_file_path} after error.")
                        except OSError as cleanup_err:
                            memory_logger.error(f"Failed to clean up temporary file {tmp_file_path}: {cleanup_err}")
                    raise
        except Timeout:
            memory_logger.error(f"Timeout acquiring lock for saving shared KB for Squad '{self._current_identifier}', Session '{self._current_session_id}' at {lock_path}")
            raise
        except Exception as e:
            memory_logger.exception(f"An unexpected error occurred during shared KB save for Squad '{self._current_identifier}', Session '{self._current_session_id}': {e}")
            raise
        finally:
            if lock_acquired_successfully:
                if lock.is_locked:
                    try:
                        lock.release()
                        memory_logger.info(f"Lock explicitly released for {lock_path} in finally block after save.")
                    except Exception as release_err:
                        memory_logger.error(f"Error explicitly releasing lock {lock_path} in finally block after save: {release_err}")
                else:
                    memory_logger.debug(f"Lock for {lock_path} was already released before finally block after save.")
        
            lock_file_str = str(lock_path)
            if os.path.exists(lock_file_str):
                try:
                    os.remove(lock_file_str)
                    memory_logger.info(f"Successfully deleted stray lock file after saving: {lock_file_str}")
                except OSError as e:
                    memory_logger.error(f"Error deleting stray lock file {lock_file_str} after saving: {e}. This might be okay.")
            else:
                memory_logger.debug(f"Lock file {lock_file_str} was not found post-save, no explicit deletion needed.")

    def contribute(self, key: str, value: Any, contributor_id: Optional[str] = None) -> None:
        """Contributes a fact to the shared knowledge for the active session, including metadata.

        The fact is stored as a dictionary containing the value, contributor_id,
        and a UTC timestamp. Changes are immediately persisted to the session file.

        Args:
            key (str): The key for the fact.
            value (Any): The value of the fact.
            contributor_id (Optional[str]): An optional identifier for the contributor.
        """
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot contribute: Squad ID or Session ID not set.")
            return
        self._shared_knowledge[key] = {
            "value": value,
            "contributor_id": contributor_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.save_shared() # Persist changes to the active session file

    def access(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Accesses a fact from shared knowledge for the active session.

        This method attempts to acquire a read lock with a short timeout.
        If the lock times out, it may serve from (potentially stale) in-memory data.
        If the key is not found, it returns the provided default value.
        The stored fact is expected to be a dictionary; this method returns the 'value' field.

        Args:
            key (str): The key of the fact to access.
            default (Optional[Any]): The default value to return if the key is not found.

        Returns:
            Optional[Any]: The value of the fact, or the default value.
        """
        if not self._current_identifier or not self._current_session_id:
            memory_logger.warning("Accessing shared knowledge without an active squad/session. Data might be from an unexpected context or empty.")
            # Fallback to potentially stale in-memory data or default if no session is active
            item = self._shared_knowledge.get(key)
            return item["value"] if item and isinstance(item, dict) and "value" in item else default

        lock_path = self._get_lock_path() # Uses internal squad/session IDs
        lock = FileLock(str(lock_path), timeout=self.lock_timeout)
        try:
            # Using a short timeout for read access to avoid blocking writes for too long
            with lock.acquire(timeout=0.1):
                # Re-read from file for freshest data if lock acquired, though current design loads on session set.
                # For strict consistency, one might re-load here, but that adds overhead.
                # Current model: load on set_active_session, then in-memory ops until next set_active_session.
                item = self._shared_knowledge.get(key)
                return item["value"] if item and isinstance(item, dict) and "value" in item else default
        except Timeout:
            memory_logger.warning(f"Timeout acquiring lock for accessing shared KB for Squad '{self._current_identifier}', Session '{self._current_session_id}'. Serving from (potentially stale) in-memory data.")
            item = self._shared_knowledge.get(key) # Serve from in-memory cache on timeout
            return item["value"] if item and isinstance(item, dict) and "value" in item else default
        except ValueError as ve:
            memory_logger.error(f"Error accessing shared knowledge (likely session not set): {ve}")
            return default # Or raise, depending on desired strictness
        except Exception as e:
            memory_logger.exception(f"An unexpected error occurred during shared KB access for Squad '{self._current_identifier}', Session '{self._current_session_id}': {e}")
            return default

    def retract(self, key: str, contributor_id: Optional[str] = None) -> None:
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot retract: Squad ID or Session ID not set.")
            return
        if key in self._shared_knowledge:
            del self._shared_knowledge[key]
            self.save_shared() # Persist changes
            memory_logger.info(f"Shared knowledge entry '{key}' retracted for Squad '{self._current_identifier}', Session '{self._current_session_id}'.")
        else:
            memory_logger.info(f"Shared knowledge entry '{key}' not found for retraction in Squad '{self._current_identifier}', Session '{self._current_session_id}'.")

    def get_all_shared_entries(self) -> Dict[str, Any]:
        if not self._current_identifier or not self._current_session_id:
            memory_logger.warning("Getting all shared entries without an active squad/session. Data might be from an unexpected context or empty.")
            return self._shared_knowledge.copy() # Return potentially stale in-memory copy
            
        lock_path = self._get_lock_path() # Uses internal squad/session IDs
        lock = FileLock(str(lock_path), timeout=self.lock_timeout)
        try:
            with lock.acquire(timeout=0.1):
                # Similar to access, current model relies on load_shared at session set.
                return self._shared_knowledge.copy()
        except Timeout:
            memory_logger.warning(f"Timeout acquiring lock for get_all_shared_entries for Squad '{self._current_identifier}', Session '{self._current_session_id}'. Serving from (potentially stale) in-memory data.")
            return self._shared_knowledge.copy()
        except ValueError as ve:
            memory_logger.error(f"Error getting all shared entries (likely session not set): {ve}")
            return {}
        except Exception as e:
            memory_logger.exception(f"An unexpected error occurred during get_all_shared_entries for Squad '{self._current_identifier}', Session '{self._current_session_id}': {e}")
            return {}

    def clear_all_shared_knowledge(self) -> None:
        if not self._current_identifier or not self._current_session_id:
            memory_logger.error("Cannot clear_all_shared_knowledge: Squad ID or Session ID not set.")
            return
        self._shared_knowledge = {}
        self.save_shared() # Save the cleared state
        memory_logger.info(f"All shared knowledge cleared for Squad '{self._current_identifier}', Session '{self._current_session_id}'.")

# Final imports, ensure they are at the top if not already present by linters.
# import os
# import json
# from datetime import datetime
# from pathlib import Path
# from abc import ABC, abstractmethod
# from typing import Any, Dict, Optional, List
# from filelock import FileLock, Timeout
# import logging
