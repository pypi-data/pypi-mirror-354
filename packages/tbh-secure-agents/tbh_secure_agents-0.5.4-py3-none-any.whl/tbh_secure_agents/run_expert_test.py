import os
import uuid
import nltk
import logging
import glob
import traceback
import sys # For sys.stderr in fallback

# Configure logging for the test script
# Aggressively configure root logger for DEBUG output
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Ensure there's a handler and it's set to DEBUG
if not root_logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)
else:
    for handler in root_logger.handlers:
        handler.setLevel(logging.DEBUG)
        # Optionally re-set formatter if needed
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

logger = logging.getLogger(__name__) # Get a specific logger for this module if needed, will inherit root's level

# Attempt to import the Expert class and other necessary components
try:
    from tbh_secure_agents.agent import Expert
    # If SecurityProfile enum or other specific constants are needed directly by the test harness logic,
    # they would need to be imported as well, e.g.:
    # from tbh_secure_agents.security_profiles import SecurityProfile 
except ImportError as e:
    logger.error(f"Failed to import Expert or related components: {e}")
    logger.error("Ensure that you are running this script from a directory where 'tbh_secure_agents' package is accessible,")
    logger.error("or that the package is installed in your Python environment.")
    logger.error("PYTHONPATH might need to be set, e.g., export PYTHONPATH=/path/to/parent_of_tbh_secure_agents:$PYTHONPATH")
    exit(1)

if __name__ == "__main__":
    error_log_file = "runtime_error.txt"
    test_kb_path = "./.test_expert_knowledge_runtime"
    # Ensure the base KB path exists for consistent file operations
    os.makedirs(test_kb_path, exist_ok=True)

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        # Fallback to the hardcoded key if env var is not set (as per previous setup)
        google_api_key = "AIzaSyBtIh9ShcSmezYKa8xmI0kIyyl2gJZIYFc"
        logger.info("GOOGLE_API_KEY environment variable not set. Using hardcoded key for testing.")
    else:
        logger.info("Using GOOGLE_API_KEY from environment variable.")

    # Make sure necessary NLTK data is downloaded (e.g., 'punkt')
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        logger.info("NLTK 'punkt' tokenizer not found. Downloading...")
        nltk.download('punkt', quiet=True)
        logger.info("'punkt' tokenizer downloaded.")

    memory_modes_to_test = ["short_term", "long_term", "none", "both"]
    # Store all session IDs created during the tests for cleanup
    all_session_ids_created = ["session_alpha", "session_beta"] # From original tests

    for current_memory_mode in memory_modes_to_test:
        logger.info(f"\n{'='*30} TESTING MEMORY MODE: {current_memory_mode.upper()} {'='*30}")
        test_expert = None # Ensure expert is reset for each mode
        current_session_id = f"session_mode_{current_memory_mode}_{str(uuid.uuid4())[:8]}"
        all_session_ids_created.append(current_session_id)

        try:
            logger.info(f"Initializing Expert for memory_mode='{current_memory_mode}' with session_id='{current_session_id}'...")
            test_expert = Expert(
                specialty=f"Test Analyst ({current_memory_mode})",
                objective=f"Testing memory_mode: {current_memory_mode}",
                background="This expert is for mode-specific memory testing.",
                llm_model_name='gemini-1.5-flash-latest',
                security_profile='minimal',
                api_key=google_api_key,
                persistent_knowledge_base_path=test_kb_path,
                initial_session_id=current_session_id,
                memory_mode=current_memory_mode
            )
            logger.info(f"Expert initialized with ID: {test_expert.expert_id}, session '{current_session_id}', mode '{current_memory_mode}'")

            # Assertions for memory component initialization
            if current_memory_mode == "short_term":
                assert test_expert.working_memory is not None, "Working memory should be active for 'short_term' mode."
                assert test_expert.persistent_knowledge is None, "Persistent knowledge should be None for 'short_term' mode."
                logger.info("Memory components validated for 'short_term' mode.")
            elif current_memory_mode == "long_term":
                assert test_expert.working_memory is None, "Working memory should be None for 'long_term' mode."
                assert test_expert.persistent_knowledge is not None, "Persistent knowledge should be active for 'long_term' mode."
                logger.info("Memory components validated for 'long_term' mode.")
            elif current_memory_mode == "none":
                assert test_expert.working_memory is None, "Working memory should be None for 'none' mode."
                assert test_expert.persistent_knowledge is None, "Persistent knowledge should be None for 'none' mode."
                logger.info("Memory components validated for 'none' mode.")
            elif current_memory_mode == "both":
                assert test_expert.working_memory is not None, "Working memory should be active for 'both' mode."
                assert test_expert.persistent_knowledge is not None, "Persistent knowledge should be active for 'both' mode."
                logger.info("Memory components validated for 'both' mode.")

            # Execute a simple task to remember a fact
            fact_to_remember = f"The color of the sky is blue in {current_memory_mode} mode."
            task_remember_sky = f"Remember this: {fact_to_remember}"
            logger.info(f"\nExecuting task to remember a fact: '{task_remember_sky}'")
            test_expert.execute_task(task_description=task_remember_sky, context=f"Storing a fact for {current_memory_mode} mode test.")
            logger.info(f"Task executed. Verifying fact storage for mode '{current_memory_mode}'...")

            # Verify fact storage based on memory mode
            fact_in_wm = False
            if test_expert.working_memory:
                wm_content = test_expert.working_memory.get_all_entries()
                if any(fact_to_remember in str(entry) for entry in wm_content):
                    fact_in_wm = True
            
            fact_in_pkb = False
            pkb_file_path_current_mode = None
            if test_expert.persistent_knowledge:
                pkb_content = test_expert.persistent_knowledge.get_all_facts()
                if any(fact_to_remember in str(value) for value in pkb_content.values()):
                    fact_in_pkb = True
                # Construct the expected file path for the current expert and session
                pkb_file_path_current_mode = os.path.join(test_kb_path, f"expert_{test_expert.expert_id}_session_{current_session_id}_kb.json")

            if current_memory_mode == "short_term":
                assert fact_in_wm, "Fact NOT found in working memory for 'short_term' mode."
                assert not fact_in_pkb, "Fact FOUND in persistent knowledge for 'short_term' mode (unexpected)."
                if pkb_file_path_current_mode:
                    assert not os.path.exists(pkb_file_path_current_mode), f"PKB file {pkb_file_path_current_mode} SHOULD NOT exist for 'short_term' mode."
                logger.info("Fact storage validated for 'short_term' mode: In WM, not in PKB, no PKB file.")
            elif current_memory_mode == "long_term":
                assert not fact_in_wm, "Fact FOUND in working memory for 'long_term' mode (unexpected, WM should be None)."
                assert fact_in_pkb, "Fact NOT found in persistent knowledge for 'long_term' mode."
                assert os.path.exists(pkb_file_path_current_mode), f"PKB file {pkb_file_path_current_mode} MUST exist for 'long_term' mode."
                logger.info("Fact storage validated for 'long_term' mode: Not in WM, in PKB, PKB file exists.")
            elif current_memory_mode == "none":
                assert not fact_in_wm, "Fact FOUND in working memory for 'none' mode (unexpected)."
                assert not fact_in_pkb, "Fact FOUND in persistent knowledge for 'none' mode (unexpected)."
                if pkb_file_path_current_mode: # pkb_file_path_current_mode will be None if PK is None
                     assert not os.path.exists(pkb_file_path_current_mode), f"PKB file {pkb_file_path_current_mode} SHOULD NOT exist for 'none' mode."
                logger.info("Fact storage validated for 'none' mode: Not in WM, not in PKB, no PKB file.")
            elif current_memory_mode == "both":
                assert fact_in_wm, "Fact NOT found in working memory for 'both' mode."
                assert fact_in_pkb, "Fact NOT found in persistent knowledge for 'both' mode."
                assert os.path.exists(pkb_file_path_current_mode), f"PKB file {pkb_file_path_current_mode} MUST exist for 'both' mode."
                logger.info("Fact storage validated for 'both' mode: In WM, in PKB, PKB file exists.")

            logger.info(f"Test for memory_mode '{current_memory_mode}' completed successfully.")

        except Exception as e_mode_test:
            error_message = f"An exception occurred during memory_mode '{current_memory_mode}' test: {e_mode_test}\n"
            error_message += traceback.format_exc()
            logger.error(error_message)
            # Optionally, write to error_log_file here as well or re-raise to be caught by outer handler
            # For now, just log and continue to test other modes if possible.
            # Depending on severity, might want to sys.exit(1) here.

    # Original multi-session test (can be kept or refactored further)
    # For now, let's run it after the memory mode tests, re-initializing an expert
    logger.info(f"\n{'='*30} RUNNING ORIGINAL MULTI-SESSION TEST {'='*30}")
    try:
        original_session_alpha = "session_alpha_orig"
        original_session_beta = "session_beta_orig"
        all_session_ids_created.extend([original_session_alpha, original_session_beta])

        test_expert_orig = Expert(
            specialty="Test Analyst (Original)",
            objective="To test multi-session memory integration.",
            background="This expert is for multi-session testing.",
            llm_model_name='gemini-1.5-flash-latest',
            security_profile='minimal',
            api_key=google_api_key,
            persistent_knowledge_base_path=test_kb_path,
            initial_session_id=original_session_alpha,
            memory_mode="both" # Original test used 'both'
        )
        logger.info(f"Original Test Expert initialized with ID: {test_expert_orig.expert_id} and initial session '{original_session_alpha}'")

        task_desc_1 = "What is the capital of France? Provide a concise answer."
        logger.info(f"\nExecuting task 1 (Original Test): {task_desc_1}")
        test_expert_orig.execute_task(task_description=task_desc_1, context="Original test context.")

        task_remember_eiffel = "Remember this important fact: The Eiffel Tower is a famous landmark in Paris."
        logger.info(f"\nExecuting task to remember Eiffel Tower (Original Test - {original_session_alpha}): {task_remember_eiffel}")
        test_expert_orig.execute_task(task_description=task_remember_eiffel, context=f"Storing key information for {original_session_alpha}.")

        test_expert_orig.set_active_memory_session(original_session_beta)
        logger.info(f"Active memory session is now '{original_session_beta}'.")

        task_remember_brandenburg = "Keep in mind: The Brandenburg Gate is a well-known landmark in Berlin."
        logger.info(f"\nExecuting task to remember Brandenburg Gate (Original Test - {original_session_beta}): {task_remember_brandenburg}")
        test_expert_orig.execute_task(task_description=task_remember_brandenburg, context=f"Storing key information for {original_session_beta}.")

        test_expert_orig.set_active_memory_session(original_session_alpha)
        logger.info(f"Active memory session is now '{original_session_alpha}'.")

        if test_expert_orig.persistent_knowledge:
            all_facts_alpha_orig = test_expert_orig.persistent_knowledge.get_all_facts()
            assert "The Eiffel Tower is a famous landmark in Paris." in str(all_facts_alpha_orig.values()), "Eiffel Tower fact missing from original_session_alpha!"
            assert "The Brandenburg Gate is a well-known landmark in Berlin." not in str(all_facts_alpha_orig.values()), "Brandenburg Gate fact unexpectedly in original_session_alpha!"
            logger.info("Original multi-session test: session_alpha correctly contains Eiffel Tower fact and not Brandenburg Gate fact.")
        logger.info("Original multi-session test completed successfully.")

    except Exception as top_level_e:
        # This is the main top-level exception handler.
        error_message = f"A top-level unhandled exception occurred in run_expert_test.py: {top_level_e}\n"
        error_message += traceback.format_exc()
        
        try:
            logger.critical(error_message) # Try to log it first
        except Exception as log_err:
            print(f"CRITICAL: Logging failed while reporting top-level error. Error: {log_err}", file=sys.stderr)

        try:
            with open(error_log_file, "w") as f_err:
                f_err.write(error_message)
            print(f"Detailed top-level error traceback written to {error_log_file}", file=sys.stderr)
        except Exception as ef_err:
            print(f"CRITICAL: Failed to write top-level error to {error_log_file}. Error: {ef_err}", file=sys.stderr)
            print(f"Original Top-Level Traceback:\n{error_message}", file=sys.stderr)
        
        sys.exit(1) # Ensure script exits with an error code

    finally:
        logger.info("\nStarting cleanup phase...")
        # Cleanup session-specific files for all known expert IDs and session IDs
        # This requires knowing all expert_ids created. For simplicity, we'll glob for expert IDs.
        # A more robust way would be to collect expert_ids during tests.
        
        # Clean up all *.json files within test_kb_path that match the expert session pattern
        # This is a broader cleanup to catch all generated files regardless of expert_id tracking.
        for session_id_to_clean in set(all_session_ids_created):
            # Construct a pattern that matches any expert_id for a given session_id
            kb_file_pattern = os.path.join(test_kb_path, f"expert_*_session_{session_id_to_clean}_kb.json")
            matching_kb_files = glob.glob(kb_file_pattern)
            for kb_file_path in matching_kb_files:
                if os.path.exists(kb_file_path):
                    try:
                        os.remove(kb_file_path)
                        logger.info(f"Cleaned up test knowledge base file: {kb_file_path}")
                    except Exception as e_clean:
                        logger.warning(f"Could not clean up test knowledge base file {kb_file_path}: {e_clean}")
                else:
                    # This case should ideally not be hit if glob.glob found it, but good for safety
                    logger.info(f"Test knowledge base file {kb_file_path} (from glob) not found during cleanup attempt.")

        # Cleanup stray lock files (session-aware)
        # This pattern will catch all expert session lock files.
        lock_file_pattern_session = os.path.join(test_kb_path, "expert_*_session_*_kb.json.lock")
        stray_lock_files_session = glob.glob(lock_file_pattern_session)
        if stray_lock_files_session:
            logger.info(f"Cleaning up {len(stray_lock_files_session)} stray session lock file(s) from {test_kb_path}...")
            for lock_file in stray_lock_files_session:
                try:
                    os.remove(lock_file)
                    logger.info(f"  - Successfully removed session lock: {lock_file}")
                except OSError as e:
                    logger.error(f"  - Error removing session lock {lock_file}: {e}")
        else:
            logger.info(f"No stray session-specific lock files found in {test_kb_path} matching pattern '{lock_file_pattern_session}'.")

        # Attempt to remove the directory if it's empty
        if os.path.exists(test_kb_path):
            try:
                if not os.listdir(test_kb_path): # Check if directory is empty
                    os.rmdir(test_kb_path)
                    logger.info(f"Cleaned up empty test knowledge base directory: {test_kb_path}")
                else:
                    # Log remaining files if directory is not empty
                    remaining_files = os.listdir(test_kb_path)
                    logger.info(f"Test knowledge base directory {test_kb_path} not empty, leaving as is. Remaining items: {remaining_files}")
            except Exception as e_clean_dir:
                logger.warning(f"Could not clean up test knowledge base directory {test_kb_path}: {e_clean_dir}")
        else:
            logger.info(f"Test knowledge base directory {test_kb_path} does not exist, no need to remove.")
        
        logger.info("Test script execution completed (from finally block).")
