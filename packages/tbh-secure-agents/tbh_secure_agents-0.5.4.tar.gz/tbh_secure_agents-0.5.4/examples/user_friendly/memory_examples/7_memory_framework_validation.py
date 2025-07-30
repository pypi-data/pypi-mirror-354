import os
import sys
import shutil
import logging
import uuid
from datetime import datetime, timezone

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import SecurityProfile

# --- Test Script: 7_memory_framework_validation.py ---
# This script validates the memory system against the latest framework changes.

# --- Configuration ---
RUN_ID = uuid.uuid4().hex[:8]
BASE_OUTPUT_DIR = f'./outputs/framework_validation_{RUN_ID}'
SHARED_KB_PATH = os.path.join(BASE_OUTPUT_DIR, 'squad_kb')
EXPERT_KB_PATH = os.path.join(BASE_OUTPUT_DIR, 'expert_kb')
RESULTS_FILE_PATH = os.path.join(BASE_OUTPUT_DIR, 'results.json')
SQUAD_ID = 'squad_framework_validation'
SESSION_ID = 'session_validation_main'

# --- Logging & Directory Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
os.makedirs(SHARED_KB_PATH, exist_ok=True)
os.makedirs(EXPERT_KB_PATH, exist_ok=True)

def run_validation():
    """Runs the full validation suite."""
    print(f'--- Starting Memory Framework Validation (Run ID: {RUN_ID}) ---')
    print(f'INFO: All outputs will be in: {BASE_OUTPUT_DIR}')

    try:
        # --- Step 1: Initialization ---
        print('\n--- Step 1: Initializing Components ---')
        core_expert = Expert(
            specialty='Framework Validator',
            objective='Validate framework changes.',
            api_key='AIzaSyDg0rnMpJMVaWc3zujTrP8SrMYvu1ObETU',  # Intentionally empty
            memory_mode='both',
            persistent_knowledge_base_path=EXPERT_KB_PATH,
            security_profile='minimal'
        )

        # CORRECTED: Initialize Operation with 'instructions'
        operation = Operation(
            instructions='Analyze the data for {data_type} regarding {subject_matter}.'  # Simplified to pass security check
        )

        # CORRECTED: Pass 'operations' during Squad initialization
        test_squad = Squad(
            experts=[core_expert],
            operations=[operation],
            security_profile='minimal',  # CORRECTED: Pass as a string
            persistent_shared_knowledge_base_path=SHARED_KB_PATH,
            squad_id=SQUAD_ID,
            initial_session_id=SESSION_ID,
            result_destination={'file_path': RESULTS_FILE_PATH}
        )
        print('INFO: Expert, Operation, and Squad initialized successfully.')

        # --- Step 2: Deployment ---
        print('\n--- Step 2: Deploying Squad ---')
        # CORRECTED: Call deploy() with 'guardrails'
        guardrails = {'data_type': 'Financial Reports', 'subject_matter': 'Q4 Projections'}
        test_squad.deploy(guardrails=guardrails)
        print('INFO: Squad deployment finished.')

        # --- Step 3: Squad Shared Memory Test ---
        print('\n--- Step 3: Testing Squad Shared Memory ---')
        fact_key = 'squad_validation_fact'
        fact_value = f'This is a validation value from run {RUN_ID}'
        test_squad.store_shared_fact(fact_key, fact_value)
        retrieved_value = test_squad.retrieve_shared_fact(fact_key)
        assert retrieved_value == fact_value, 'Squad shared memory retrieval FAILED!'
        print('INFO: Squad shared memory store/retrieve PASSED.')

        # --- Step 4: Expert Working Memory Test ---
        print("\n--- Step 4: Testing Expert's Short-Term (Working) Memory ---")
        working_memory = core_expert.working_memory.get_all_entries()
        assert len(working_memory) > 0, 'Working memory is empty!'
        # The framework returns a mock success, so we check for a success log entry.
        first_entry = working_memory[0]
        assert 'operation_id' in first_entry, "Working memory entry is missing 'operation_id' key!"
        assert 'task' in first_entry, "Working memory entry is missing 'task' key!"
        assert 'output_snippet' in first_entry, "Working memory entry is missing 'output_snippet' key!"
        print('INFO: Expert working memory test PASSED.')

        # --- Step 5: Expert Persistent Memory Test ---
        print("\n--- Step 5: Testing Expert's Long-Term (Persistent) Memory ---")
        expert_kb = core_expert.persistent_knowledge
        expert_fact_key = 'expert_persistent_fact'
        expert_fact_value = f'A persistent fact from validation run {RUN_ID}'
        expert_kb._knowledge[expert_fact_key] = {
            'value': expert_fact_value,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        expert_kb.save()
        # Recall the specific fact using its key
        recalled_value = expert_kb.recall(key=expert_fact_key)
        assert recalled_value is not None, "Failed to recall knowledge from persistent memory!"
        assert recalled_value == expert_fact_value, f"Expert persistent memory value mismatch! Expected '{expert_fact_value}', got '{recalled_value}'"
        print('INFO: Expert persistent memory test PASSED.')

        print('\n--- Validation Suite Completed Successfully ---')

    except Exception as e:
        logger.error(f'VALIDATION FAILED: An unexpected error occurred: {e}', exc_info=True)
    finally:
        # --- Cleanup ---
        print('\n--- Cleaning up output directory ---')
        try:
            shutil.rmtree(BASE_OUTPUT_DIR)
            print(f'INFO: Successfully cleaned up directory: {BASE_OUTPUT_DIR}')
        except OSError as e:
            print(f'ERROR: Could not remove directory {BASE_OUTPUT_DIR}: {e.strerror}')

if __name__ == '__main__':
    run_validation()
