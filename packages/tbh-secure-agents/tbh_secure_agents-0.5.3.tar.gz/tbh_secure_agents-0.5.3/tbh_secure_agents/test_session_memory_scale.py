import os
import sys
import json
import time
import random
import string
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from tbh_secure_agents.memory import FileBasedPersistentSharedKnowledge, memory_logger
import logging

# Configure memory_logger for more detailed output during tests
# memory_logger.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
# memory_logger.addHandler(console_handler)

TEST_BASE_PATH = "./.squad_knowledge_scale_test"
DEFAULT_SQUAD_ID = "scale_test_squad_1"

def generate_random_string(length: int = 100) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_kv_pairs(num_pairs: int, key_prefix: str = "key", value_length: int = 256) -> Dict[str, Any]:
    data = {}
    for i in range(num_pairs):
        data[f"{key_prefix}_{i}"] = generate_random_string(value_length)
    return data

def setup_test_environment():
    if os.path.exists(TEST_BASE_PATH):
        shutil.rmtree(TEST_BASE_PATH)
    os.makedirs(TEST_BASE_PATH, exist_ok=True)
    memory_logger.info(f"Test environment setup at {TEST_BASE_PATH}")

def cleanup_test_environment():
    if os.path.exists(TEST_BASE_PATH):
        shutil.rmtree(TEST_BASE_PATH)
    memory_logger.info(f"Test environment cleaned up from {TEST_BASE_PATH}")

def test_large_data_volume_single_session(num_entries: int = 10000, value_size: int = 512):
    memory_logger.info(f"\n--- Starting Test: Large Data Volume (Single Session) ---")
    memory_logger.info(f"Entries: {num_entries}, Value Size: {value_size} bytes")
    
    shared_kb = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
    session_id = "large_data_session"

    shared_kb.set_active_session(DEFAULT_SQUAD_ID, session_id)
    
    # Contribution phase
    start_time = time.time()
    test_data = generate_kv_pairs(num_entries, "large_vol", value_size)
    for key, value in test_data.items():
        shared_kb.contribute(key, value, contributor_id="test_script")
    end_time = time.time()
    contribution_time = end_time - start_time
    memory_logger.info(f"Contribution of {num_entries} entries took: {contribution_time:.4f} seconds.")

    file_path = shared_kb._get_file_path()
    file_size = os.path.getsize(file_path) / (1024 * 1024) # Size in MB
    memory_logger.info(f"Session file size: {file_size:.2f} MB at {file_path}")

    # Clear KB instance and reload to test load time
    del shared_kb
    shared_kb_reloaded = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
    
    start_time = time.time()
    shared_kb_reloaded.set_active_session(DEFAULT_SQUAD_ID, session_id) # This will trigger load
    end_time = time.time()
    load_time = end_time - start_time
    memory_logger.info(f"Loading {num_entries} entries took: {load_time:.4f} seconds.")

    # Verification
    random_key_to_check = f"large_vol_{num_entries // 2}"
    retrieved_value = shared_kb_reloaded.access(random_key_to_check)
    if retrieved_value == test_data[random_key_to_check]:
        memory_logger.info(f"Data verification successful for key '{random_key_to_check}'.")
    else:
        memory_logger.error(f"Data verification FAILED for key '{random_key_to_check}'.")

    memory_logger.info(f"--- Finished Test: Large Data Volume (Single Session) ---")
    return {
        "contribution_time_seconds": contribution_time,
        "load_time_seconds": load_time,
        "file_size_mb": file_size
    }


def test_multiple_sessions(num_sessions: int = 50, entries_per_session: int = 100):
    memory_logger.info(f"\n--- Starting Test: Multiple Sessions ---")
    memory_logger.info(f"Sessions: {num_sessions}, Entries per session: {entries_per_session}")

    shared_kb = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
    session_data_map: Dict[str, Dict[str, Any]] = {}

    # Creation phase
    start_time = time.time()
    for i in range(num_sessions):
        session_id = f"multi_session_{i}"
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, session_id)
        session_data = generate_kv_pairs(entries_per_session, f"s{i}_")
        session_data_map[session_id] = session_data
        for key, value in session_data.items():
            shared_kb.contribute(key, value, contributor_id="multi_test")
    creation_time = time.time() - start_time
    memory_logger.info(f"Creation of {num_sessions} sessions with {entries_per_session} entries each took: {creation_time:.4f} seconds.")

    # Verification phase
    start_time = time.time()
    all_verified = True
    for i in range(num_sessions):
        session_id = f"multi_session_{i}"
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, session_id)
        original_data = session_data_map[session_id]
        # Check a random key from this session
        random_key = list(original_data.keys())[entries_per_session // 2]
        retrieved_value = shared_kb.access(random_key)
        if retrieved_value != original_data[random_key]:
            memory_logger.error(f"Verification FAILED for session '{session_id}', key '{random_key}'.")
            all_verified = False
            break
    verification_time = time.time() - start_time
    memory_logger.info(f"Initial verification of {num_sessions} sessions took: {verification_time:.4f} seconds.")

    # Additional tests for access_all and clear for one session
    if all_verified and num_sessions > 0:
        chosen_session_index = num_sessions // 2
        chosen_session_id = f"multi_session_{chosen_session_index}"
        original_data_for_chosen_session = session_data_map[chosen_session_id]

        memory_logger.info(f"\n--- Testing access_all_shared_knowledge for session '{chosen_session_id}' --- ") 
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, chosen_session_id)
        all_retrieved_data = shared_kb._shared_knowledge # Access internal dict for testing
        if all_retrieved_data == original_data_for_chosen_session:
            memory_logger.info(f"SUCCESS: access_all_shared_knowledge for session '{chosen_session_id}' verified.")
        else:
            memory_logger.error(f"FAILURE: access_all_shared_knowledge for session '{chosen_session_id}' FAILED verification.")
            all_verified = False

        memory_logger.info(f"\n--- Testing clear_shared_knowledge for session '{chosen_session_id}' --- ")
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, chosen_session_id) # Ensure it's active
        shared_kb._shared_knowledge = {} # Clear internal dict
        shared_kb.save_shared() # Save the cleared state
        memory_logger.info(f"Cleared and saved session '{chosen_session_id}'. Verifying...")

        # Verify by reloading
        shared_kb_reloaded_for_clear_test = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
        shared_kb_reloaded_for_clear_test.set_active_session(DEFAULT_SQUAD_ID, chosen_session_id)
        if not shared_kb_reloaded_for_clear_test._shared_knowledge: # Check if it's empty
            memory_logger.info(f"SUCCESS: clear_shared_knowledge for session '{chosen_session_id}' verified (session is empty after reload).")
        else:
            memory_logger.error(f"FAILURE: clear_shared_knowledge for session '{chosen_session_id}' FAILED. Expected empty, got: {shared_kb_reloaded_for_clear_test._shared_knowledge}")
            all_verified = False
        
        # Restore original data for the chosen session for subsequent tests if any, or just for consistency of session_data_map
        # This is important if other tests might rely on the full session_data_map integrity
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, chosen_session_id)
        shared_kb._shared_knowledge = original_data_for_chosen_session
        shared_kb.save_shared()
        memory_logger.info(f"Restored original data for session '{chosen_session_id}'.")

    if all_verified:
        memory_logger.info("All multiple session verifications (including access_all and clear) PASSED.")
    else:
        memory_logger.error("One or more multiple session verifications (including access_all and clear) FAILED.")

    memory_logger.info(f"--- Finished Test: Multiple Sessions ---")
    return {
        "creation_time_seconds": creation_time,
        "verification_time_seconds": verification_time, # This is initial verification time
        "all_verified": all_verified
    }

def test_rapid_switching_and_ops(num_sessions: int = 5, num_operations: int = 1000, entries_per_session_init: int = 10):
    memory_logger.info(f"\n--- Starting Test: Rapid Switching and Operations ---")
    memory_logger.info(f"Sessions: {num_sessions}, Operations: {num_operations}")

    shared_kb = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
    session_ids = [f"rapid_session_{i}" for i in range(num_sessions)]
    
    # Initial population
    # Keep track of expected state of each session's data
    expected_session_states: Dict[str, Dict[str, Any]] = {sid: {} for sid in session_ids}

    for sid in session_ids:
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, sid)
        initial_data = generate_kv_pairs(entries_per_session_init, f"{sid}_init_")
        for k, v in initial_data.items():
            shared_kb.contribute(k, v)
            expected_session_states[sid][k] = v
    memory_logger.info(f"Initial population of {num_sessions} sessions complete.")

    # Rapid operations phase
    start_time = time.time()
    for op_count in range(num_operations):
        chosen_session_id = random.choice(session_ids)
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, chosen_session_id)
        
        operation_type = random.choice(["contribute", "access", "retract"])
        
        if operation_type == "contribute":
            key = f"{chosen_session_id}_op_{op_count}"
            value = generate_random_string(50)
            shared_kb.contribute(key, value)
            expected_session_states[chosen_session_id][key] = value
        elif operation_type == "access":
            if expected_session_states[chosen_session_id]:
                key_to_access = random.choice(list(expected_session_states[chosen_session_id].keys()))
                shared_kb.access(key_to_access) # Actual value check will be done at the end
        elif operation_type == "retract":
            if expected_session_states[chosen_session_id]:
                key_to_retract = random.choice(list(expected_session_states[chosen_session_id].keys()))
                shared_kb.retract(key_to_retract)
                del expected_session_states[chosen_session_id][key_to_retract]

        if op_count % (num_operations // 10) == 0 and op_count > 0:
            memory_logger.debug(f"Completed {op_count}/{num_operations} rapid operations...")

    ops_time = time.time() - start_time
    memory_logger.info(f"Execution of {num_operations} rapid operations took: {ops_time:.4f} seconds.")

    # Final verification
    all_verified_final = True
    for sid in session_ids:
        shared_kb.set_active_session(DEFAULT_SQUAD_ID, sid)
        current_kb_state = shared_kb.get_all_shared_entries()
        # We need to compare the 'value' field of the items in current_kb_state
        # with the direct values in expected_session_states
        simplified_current_state = {k: v['value'] for k, v in current_kb_state.items() if isinstance(v, dict) and 'value' in v}

        if simplified_current_state != expected_session_states[sid]:
            memory_logger.error(f"Final verification FAILED for session '{sid}'. Mismatch detected.")
            # For detailed debugging, one might print the differences here
            # memory_logger.error(f"Expected: {expected_session_states[sid]}")
            # memory_logger.error(f"Actual: {simplified_current_state}")
            all_verified_final = False
            # break # Stop on first error or check all
    
    if all_verified_final:
        memory_logger.info(f"Final verification of all sessions after rapid ops: All OK.")
    else:
        memory_logger.error(f"Final verification FAILED for one or more sessions after rapid ops.")

    memory_logger.info(f"--- Finished Test: Rapid Switching and Operations ---")
    return {
        "ops_time_seconds": ops_time,
        "all_verified_final": all_verified_final
    }


def test_multiple_squad_ids_same_session():
    memory_logger.info(f"\n--- Starting Test: Multiple Squad IDs, Same Session ID ---")
    squad_id_alpha = "squad_alpha_test"
    squad_id_beta = "squad_beta_test"
    common_session_id = "common_session_for_squad_isolation"

    data_alpha = {"fact_alpha": "This is data from Alpha squad", "shared_fact": "Alpha's version"}
    data_beta = {"fact_beta": "This is data from Beta squad", "shared_fact": "Beta's version"}

    shared_kb = FileBasedPersistentSharedKnowledge(base_path=TEST_BASE_PATH)
    all_squad_id_test_verified = True

    # Squad Alpha contributes
    memory_logger.info(f"Squad Alpha ({squad_id_alpha}) contributing to session '{common_session_id}'")
    shared_kb.set_active_session(squad_id_alpha, common_session_id)
    for key, value in data_alpha.items():
        shared_kb.contribute(key, value, "squad_alpha_contributor")
    shared_kb.save_shared()

    # Squad Beta contributes
    memory_logger.info(f"Squad Beta ({squad_id_beta}) contributing to session '{common_session_id}'")
    shared_kb.set_active_session(squad_id_beta, common_session_id)
    for key, value in data_beta.items():
        shared_kb.contribute(key, value, "squad_beta_contributor")
    shared_kb.save_shared()

    # Verify Squad Alpha's data isolation
    memory_logger.info(f"Verifying data for Squad Alpha ({squad_id_alpha}), session '{common_session_id}'")
    shared_kb.set_active_session(squad_id_alpha, common_session_id) # Reloads data for alpha
    retrieved_alpha_data = shared_kb._shared_knowledge
    if retrieved_alpha_data == data_alpha:
        memory_logger.info(f"SUCCESS: Data for Squad Alpha verified.")
    else:
        memory_logger.error(f"FAILURE: Data mismatch for Squad Alpha. Expected: {data_alpha}, Got: {retrieved_alpha_data}")
        all_squad_id_test_verified = False
    
    if "fact_beta" in retrieved_alpha_data:
        memory_logger.error(f"FAILURE: Squad Alpha's KB contains data from Squad Beta ('fact_beta')!")
        all_squad_id_test_verified = False

    # Verify Squad Beta's data isolation
    memory_logger.info(f"Verifying data for Squad Beta ({squad_id_beta}), session '{common_session_id}'")
    shared_kb.set_active_session(squad_id_beta, common_session_id) # Reloads data for beta
    retrieved_beta_data = shared_kb._shared_knowledge
    if retrieved_beta_data == data_beta:
        memory_logger.info(f"SUCCESS: Data for Squad Beta verified.")
    else:
        memory_logger.error(f"FAILURE: Data mismatch for Squad Beta. Expected: {data_beta}, Got: {retrieved_beta_data}")
        all_squad_id_test_verified = False

    if "fact_alpha" in retrieved_beta_data:
        memory_logger.error(f"FAILURE: Squad Beta's KB contains data from Squad Alpha ('fact_alpha')!")
        all_squad_id_test_verified = False

    if all_squad_id_test_verified:
        memory_logger.info("SUCCESS: Multiple Squad ID isolation test PASSED.")
    else:
        memory_logger.error("FAILURE: Multiple Squad ID isolation test FAILED.")

    memory_logger.info(f"--- Finished Test: Multiple Squad IDs, Same Session ID ---")
    return {"squad_id_isolation_verified": all_squad_id_test_verified}


if __name__ == "__main__":
    # Ensure TEST_BASE_PATH is ready for log files first
    # This call also configures the memory_logger if it's the first time
    setup_test_environment()

    stdout_log_path = Path(TEST_BASE_PATH) / "script_stdout.log"
    stderr_log_path = Path(TEST_BASE_PATH) / "script_stderr.log"

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    stdout_log_file = None  # Initialize to None
    stderr_log_file = None  # Initialize to None

    # Outer try/finally to ensure stdout/stderr are restored
    try:
        with open(stdout_log_path, 'w') as f_stdout, open(stderr_log_path, 'w') as f_stderr:
            stdout_log_file = f_stdout  # Assign to higher-scoped variable
            stderr_log_file = f_stderr  # Assign to higher-scoped variable
            sys.stdout = stdout_log_file
            sys.stderr = stderr_log_file

            memory_logger.info(f"Script output is being redirected. STDOUT: {stdout_log_path}, STDERR: {stderr_log_path}")
            print(f"INFO: Script output is being redirected. STDOUT: {stdout_log_path}, STDERR: {stderr_log_path}") # Also to redirected stdout

            results = {}
            # Inner try/except/finally for the actual test logic and summary saving
            try:
                # Adjust parameters here for different scales
                results["large_data_single_session"] = test_large_data_volume_single_session(num_entries=5000, value_size=256)
                # results["large_data_single_session_bigger"] = test_large_data_volume_single_session(num_entries=20000, value_size=512)
                
                results["multiple_sessions"] = test_multiple_sessions(num_sessions=20, entries_per_session=50)
                # results["multiple_sessions_more"] = test_multiple_sessions(num_sessions=100, entries_per_session=100)

                results["rapid_switching"] = test_rapid_switching_and_ops(num_sessions=5, num_operations=500, entries_per_session_init=20)
                # results["rapid_switching_more_ops"] = test_rapid_switching_and_ops(num_sessions=10, num_operations=2000, entries_per_session_init=50)

                results["squad_id_isolation"] = test_multiple_squad_ids_same_session()
                memory_logger.info("\n\n--- Overall Test Summary (logged to file) ---")
                for test_name, res_data in results.items():
                    memory_logger.info(f"Test: {test_name}")
                    for k, v in res_data.items():
                        memory_logger.info(f"  {k}: {v}")
                    memory_logger.info("---")

            except Exception as e:
                memory_logger.exception(f"An error occurred during scale testing: {e}")
                # Also print to new stderr to ensure it's in the file
                print(f"EXCEPTION IN SCRIPT LOGIC: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
            finally:
                memory_logger.info(f"Entering inner finally block. Attempting to save summary. Results dictionary: {results}")
                # Ensure the base path for the summary file exists, just in case it was removed externally
                Path(TEST_BASE_PATH).mkdir(parents=True, exist_ok=True)

                summary_file_path = Path(TEST_BASE_PATH) / "scale_test_summary.json"
                memory_logger.info(f"Attempting to write summary to: {summary_file_path.resolve()}")
                try:
                    with open(summary_file_path, 'w') as f_summary_writer:
                        json.dump(results, f_summary_writer, indent=4)
                    memory_logger.info(f"Scale test summary saved successfully to: {summary_file_path.resolve()}")
                except Exception as e_summary:
                    memory_logger.error(f"Failed to save scale test summary: {e_summary}", exc_info=True)
                    print(f"ERROR SAVING SUMMARY JSON: {e_summary}", file=sys.stderr)
                    import traceback
                    traceback.print_exc(file=sys.stderr)

                # cleanup_test_environment() # Uncomment to auto-clean, or leave for inspection
                memory_logger.info("Inner finally block finished. Review redirected logs for details.")
                if Path(TEST_BASE_PATH).exists():
                    memory_logger.info(f"Test artifacts (if not cleaned) are in: {Path(TEST_BASE_PATH).resolve()}")
                else:
                    memory_logger.warning(f"Test base path {TEST_BASE_PATH} does not exist at script completion (from inner finally).")
    finally:
        # Create a flag file to check if this block is reached and TEST_BASE_PATH is writable
        flag_file_path = Path(TEST_BASE_PATH) / "finally_block_flag.txt"
        try:
            with open(flag_file_path, 'w') as f_flag:
                f_flag.write(f"Reached outer finally block at {datetime.now()}\n")
            print(f"INFO: Created flag file {flag_file_path.resolve()}", file=original_stdout)
        except Exception as e_flag:
            print(f"ERROR: Failed to create flag file {flag_file_path}: {e_flag}", file=original_stderr)

        # This block ensures stdout/stderr are restored.
        # Point sys.stdout/stderr back to their original streams first.
        if sys.stdout != original_stdout:
            sys.stdout = original_stdout
        if sys.stderr != original_stderr:
            sys.stderr = original_stderr

        # Now, close the file objects we had redirected to, if they were opened.
        if stdout_log_file:
            try:
                stdout_log_file.flush()
                stdout_log_file.close()
            except ValueError: # Handle 'I/O operation on closed file' if already closed
                print("Note: stdout_log_file was already closed.", file=original_stderr)
            except Exception as e_close_stdout:
                print(f"Error closing stdout_log_file: {e_close_stdout}", file=original_stderr)
            
        if stderr_log_file:
            try:
                stderr_log_file.flush()
                stderr_log_file.close()
            except ValueError: # Handle 'I/O operation on closed file' if already closed
                print("Note: stderr_log_file was already closed.", file=original_stderr)
            except Exception as e_close_stderr:
                print(f"Error closing stderr_log_file: {e_close_stderr}", file=original_stderr)

        # --- Final Script Self-Check Report --- 
        report_file_path = Path(TEST_BASE_PATH).parent / 'final_script_self_check_report.txt'
        # This message will go to the actual console (original_stdout)
        print(f"\nAttempting to write Final Script Self-Check Report to: {report_file_path.resolve()}", file=original_stdout)
        try:
            with open(report_file_path, 'w') as report_f:
                report_f.write(f"--- Final Script Self-Check Report (from {report_file_path.name}) ---\n")
                report_f.write(f"Timestamp: {datetime.now()}\n")
                report_f.write(f"Test Base Path: {Path(TEST_BASE_PATH).resolve()}\n\n")

                files_to_check = {
                    "Stdout Log": stdout_log_path,
                    "Stderr Log": stderr_log_path,
                    "Flag File": flag_file_path,
                    "Summary JSON": Path(TEST_BASE_PATH) / 'scale_test_summary.json'
                }

                if Path(TEST_BASE_PATH).exists() and Path(TEST_BASE_PATH).is_dir():
                    report_f.write(f"Directory {TEST_BASE_PATH} exists.\n")
                    report_f.write(f"Contents of {TEST_BASE_PATH}:\n")
                    try:
                        for item in os.listdir(TEST_BASE_PATH):
                            report_f.write(f"  - {item}\n")
                    except Exception as e_ls:
                        report_f.write(f"  Error listing directory contents: {e_ls}\n")
                else:
                    report_f.write(f"Directory {TEST_BASE_PATH} does NOT exist or is not a directory.\n")
                report_f.write("\n")

                for name, path_obj in files_to_check.items():
                    if path_obj.exists() and path_obj.is_file():
                        report_f.write(f"File '{name}' ({path_obj.name}): EXISTS.\n")
                        try:
                            with open(path_obj, 'r') as f_check:
                                content_preview = f_check.read(200).replace('\n', '\\n') # First 200 chars
                            report_f.write(f"  Preview: '{content_preview}...\n")
                        except Exception as e_read:
                            report_f.write(f"  Error reading file: {e_read}\n")
                    else:
                        report_f.write(f"File '{name}' ({path_obj.name}): NOT FOUND or not a file.\n")
                report_f.write("--- End of Self-Check Report ---\n")
            print(f"Successfully wrote Final Script Self-Check Report to: {report_file_path.resolve()}", file=original_stdout)
        except Exception as e_report_write:
            print(f"ERROR: Failed to write Final Script Self-Check Report to {report_file_path.resolve()}: {e_report_write}", file=original_stderr)
