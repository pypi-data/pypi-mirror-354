# 6_squad_memory_deep_dive.py

# This example demonstrates the initialization of a SecureAgents Squad 
# with a focus on:
# 1. Session-aware persistent shared memory (Squad-level).
#    - `persistent_shared_knowledge_base_path`: Custom base directory for squad knowledge.
#    - `squad_id`: Static ID for the squad.
#    - `initial_session_id`: Specific session for the squad's memory operations.
# 2. Guardrails integration.
#    - Passing dynamic `guardrails` to the `deploy` method.
# 3. Result destination.
#    - Configuring `result_destination` for the squad's final output.
# 4. Minimal security profile.
#    - `security_profile="minimal"` to allow operations even with potential warnings.
# 5. Expert with short-term memory.
#    - `memory_mode="short_term"` for the expert.
# 6. Explicit test of squad-level shared memory functions.
#
# The script aims for clarity and minimalism, avoiding extra functions or complex logic
# to clearly showcase these initialization parameters and their basic usage.
# Note: This example will show warnings about LLM initialization if an API key 
# (e.g., GOOGLE_API_KEY) is not set in the environment, as the Expert's core
# functionality relies on an LLM. The focus here is on the framework's features.

import os
import shutil
import logging
import sys
import os

# Add the project root to the Python path to resolve modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import uuid # Kept for potential unique run IDs if user wants to re-enable
from datetime import datetime, timezone # Standardized for timezone-aware UTC timestamps
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import SecurityProfile # Corrected import

# --- Configuration Constants ---
# Using a unique run ID for the main output directory to avoid conflicts if needed,
# but keeping internal paths static as requested for simplicity in KB and result file.
RUN_ID = uuid.uuid4().hex[:8] 
BASE_OUTPUT_DIR_NAME = "squad_mem_guard_dest_demo"
# Corrected and consolidated path definitions:
OUTPUT_DIR = f"./outputs/{BASE_OUTPUT_DIR_NAME}_{RUN_ID}" # Added RUN_ID to base output to ensure clean test runs
RESULT_FILE_PATH = os.path.join(OUTPUT_DIR, "operation_output.txt")
SHARED_KB_PATH = os.path.join(OUTPUT_DIR, "squad_kb")
EXPERT_PERSISTENT_KB_BASE_PATH = os.path.join(OUTPUT_DIR, "expert_persistent_kb") # Path for expert's own KB

SQUAD_ID_VAL = "squad_alpha_static"
INITIAL_SESSION_ID_VAL = "session_main_01"
EXPERT_SESSION_ID_VAL = "expert_session_alpha"
# OP_NAME = "DataProcessingOp" # Not strictly needed if name is directly in Operation

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print(f"INFO: Outputs and KB will be in: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True) # Create the base output dir
    os.makedirs(SHARED_KB_PATH, exist_ok=True) # Ensure KB path also exists

    try:
        # 1. Initialize Expert with short-term memory
        core_expert = Expert(
            specialty="Data Processor",
            objective="Process and summarize data based on provided guidelines.",
            memory_mode="both", # Enable short-term and long-term memory
            api_key="", # Explicitly empty to test behavior without functional LLM
            security_profile="minimal", # Expert-level security profile
            persistent_knowledge_base_path=EXPERT_PERSISTENT_KB_BASE_PATH, # Path for its own KB
            initial_session_id=EXPERT_SESSION_ID_VAL # Session for its own KB
        )

        # 2. Define an Operation
        processing_op = Operation(
            name="DataProcessingOp",
            instructions="Generate a summary for {data_type} data about {subject_matter}.",
            expert=core_expert
        )

        # 3. Define Guardrails for the Squad
        squad_guardrails = {
            "data_type": "Financial Reports",
            "subject_matter": "Q3 Earnings"
        }

        # 4. Define result_destination for the Squad's final output
        squad_output_config = {
            "file_path": RESULT_FILE_PATH,
            "format": "txt"
        }

        # 5. Initialize Squad with shared memory, guardrails, and result_destination params
        main_squad = Squad(
            experts=[core_expert],
            operations=[processing_op],
            persistent_shared_knowledge_base_path=SHARED_KB_PATH,
            squad_id=SQUAD_ID_VAL,
            initial_session_id=INITIAL_SESSION_ID_VAL,
            result_destination=squad_output_config,
            security_profile=SecurityProfile.MINIMAL.value
        )

        # 6. Deploy the Squad with guardrails
        print("\nDeploying squad...")
        squad_result = main_squad.deploy(guardrails=squad_guardrails)

        if squad_result:
            # Simplified check for LLM error, as that's expected without API key
            if "Error:" in squad_result and "cannot execute operation" in squad_result:
                print(f"\nSquad deployment resulted in expected LLM error: {squad_result.splitlines()[0]}")
            elif "Squad execution failed:" in squad_result: # Check for security block
                 print(f"\nSquad deployment failed due to security: {squad_result}")
            else:
                print(f"\nSquad deployed successfully. Final output:\n{squad_result}")
            
            if os.path.exists(RESULT_FILE_PATH):
                print(f"INFO: Squad output written to: {RESULT_FILE_PATH}")
                # Optional: print file content if needed for debug, but can be verbose
                # with open(RESULT_FILE_PATH, 'r', encoding='utf-8') as f:
                #     print("--- File Content Start ---")
                #     print(f.read())
                #     print("--- File Content End ---")
            else:
                print(f"INFO: Squad output file NOT found at: {RESULT_FILE_PATH}")
        else:
            print("\nSquad deployment did not produce a result.")

        # 7. Test Squad Shared Memory
        print("\n--- Testing Squad Shared Memory --- ")
        fact_key = "squad_test_fact_alpha"
        fact_value = f"This is a test value stored by the squad '{SQUAD_ID_VAL}' in session '{INITIAL_SESSION_ID_VAL}'. Run: {RUN_ID}"
        
        print(f"Storing fact: {{'{fact_key}': '{fact_value}'}} in squad shared memory...")
        main_squad.store_shared_fact(fact_key, fact_value)
        print("Fact stored.")

        print(f"Retrieving fact '{fact_key}' from squad shared memory...")
        retrieved_value = main_squad.retrieve_shared_fact(fact_key)
        print(f"Retrieved value: {retrieved_value}")
        assert retrieved_value == fact_value, f"Error: Retrieved value '{retrieved_value}' does not match stored value '{fact_value}'"
        print("Assertion for retrieved value PASSED.")

        print("Retrieving all facts from current session in squad shared memory...")
        all_facts_session = main_squad.get_all_shared_facts()
        print(f"All facts in session '{INITIAL_SESSION_ID_VAL}': {all_facts_session}")
        assert fact_key in all_facts_session, f"Error: Fact key '{fact_key}' not found in all_facts_session: {all_facts_session}"
        assert all_facts_session[fact_key] == fact_value, f"Error: Value for '{fact_key}' ({all_facts_session.get(fact_key)}) in all_facts_session does not match '{fact_value}'"
        print("Assertions for all_facts_session PASSED.")
        print("--- Squad Shared Memory Test Completed Successfully ---")

        # 8. Test Expert's Short-Term (Working) Memory
        print("\n--- Testing Expert's Short-Term (Working) Memory --- ")
        if core_expert.working_memory:
            expert_working_memory_content = core_expert.working_memory.get_all_entries()
            print(f"Content of Expert '{core_expert.specialty}' working memory:")
            if expert_working_memory_content:
                for i, item in enumerate(expert_working_memory_content):
                    print(f"  Item {i+1}: {item}")
            else:
                print("  Expert's working memory is empty.")
        else:
            print("  Expert does not have a working memory initialized.")
        print("--- Expert Working Memory Test Completed ---")

        # 9. Test Expert's Long-Term (Persistent) Memory
        print("\n--- Testing Expert's Long-Term (Persistent) Memory --- ")
        if hasattr(core_expert, 'persistent_knowledge') and core_expert.persistent_knowledge:
            expert_kb = core_expert.persistent_knowledge
            test_expert_kb_key = "expert_test_fact_omega"
            test_expert_kb_value_actual = f"This is a persistent fact for expert '{core_expert.specialty}' in session '{EXPERT_SESSION_ID_VAL}'. Run: {RUN_ID}"
            test_expert_kb_entry = {
                "value": test_expert_kb_value_actual,
                "timestamp": datetime.now(timezone.utc).isoformat(), # Standardized timezone-aware UTC
                "source": "6_squad_memory_deep_dive_test"
            }

            print(f"Storing fact in expert's persistent knowledge (session: {EXPERT_SESSION_ID_VAL}): Key='{test_expert_kb_key}', Value='{test_expert_kb_value_actual}'")
            expert_kb._knowledge[test_expert_kb_key] = test_expert_kb_entry # Directly modify _knowledge dict
            expert_kb.save() # Persist changes to file
            print("Fact stored in expert's persistent KB and saved.")

            print(f"Retrieving fact '{test_expert_kb_key}' from expert's persistent KB (session: {EXPERT_SESSION_ID_VAL})...")
            retrieved_expert_value = expert_kb.recall(test_expert_kb_key)
            print(f"Retrieved value from expert KB: {retrieved_expert_value}")

            assert retrieved_expert_value == test_expert_kb_value_actual, \
                f"Assertion failed for expert KB recall! Expected '{test_expert_kb_value_actual}', got '{retrieved_expert_value}'"
            print("Assertion for expert persistent KB retrieved value PASSED.")
            
            # Verify the file exists
            expected_expert_kb_file = expert_kb._get_current_file_path()
            assert expected_expert_kb_file.exists(), f"Expert KB file {expected_expert_kb_file} was not created!"
            print(f"Expert KB file confirmed to exist at: {expected_expert_kb_file}")

        else:
            print("Expert does not have persistent_knowledge initialized or memory_mode is not 'long_term' or 'both'.")
        print("--- Expert Persistent Memory Test Completed ---")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        # Cleanup: Remove the output directory and its contents after the run
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
            print(f"INFO: Cleaned up base output directory: {OUTPUT_DIR}")
        else:
            print(f"INFO: Output directory {OUTPUT_DIR} not found for cleanup.")
    
    print(f"INFO: Script execution finished for run {RUN_ID}.")
