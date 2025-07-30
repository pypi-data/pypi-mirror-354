#!/usr/bin/env python3
"""
Example 1: AI Researcher
========================

This example shows how to create an AI researcher that can research any topic
and save the results to a markdown file.

Features demonstrated:
- Creating an Expert with minimal security
- Creating an Operation with result_destination
- Simple research workflow
"""

import os
import shutil # For cleanup

# Set your Google API key (replace with your actual key or use environment variables)
# Using the key provided by the user for testing
os.environ["GOOGLE_API_KEY"] = "AIzaSyBOtAoCrhKbrEvSNajJ9C6bEOfsKSAUQMI"

from tbh_secure_agents import Expert, Operation

# Define path for persistent knowledge
PERSISTENT_KB_PATH = "./.user_example_researcher_kb"

def main():
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs/user_examples", exist_ok=True)

    try:
        # --- Initial Expert Setup with Session-Aware Memory ---
        print("--- Initializing Expert with Session-Aware Persistent Memory ---")
        researcher = Expert(
            specialty="AI Researcher specializing in {research_topic}",
            objective="Research {research_topic} and provide {research_depth} information",
            security_profile="minimal",
            persistent_knowledge_base_path=PERSISTENT_KB_PATH,
            initial_session_id="solar_power_deep_dive" # Session 1
        )
        print(f"Expert initialized. Active session: {researcher.get_active_memory_session()}\n")

        # --- Task 1: Research Solar Power (Session 1) ---
        print("--- Starting Task 1: Research Solar Power (Session: solar_power_deep_dive) ---")
        solar_guardrails = {
            "research_topic": "Solar Power Innovations",
            "research_depth": "detailed",
            "focus_areas": "perovskite cells, transparent solar panels, space-based solar",
            "tone": "academic",
            "include_sources": True
        }
        solar_research_op = Operation(
            instructions="Research the latest developments in {research_topic}. Focus on {focus_areas}. Use a {tone} tone and provide {research_depth} analysis.",
            output_format="A {research_depth} research report on {research_topic}.",
            expert=researcher,
            result_destination="outputs/user_examples/solar_power_research_session1.md"
        )
        solar_result = solar_research_op.execute(guardrails=solar_guardrails)
        print(f"Solar power research completed. Results: {solar_research_op.result_destination}")
        
        # Remember a fact in Session 1
        solar_fact_key = "solar_efficiency_note"
        solar_fact_value = "Recent advancements in perovskite solar cells show promise for higher efficiency."
        if researcher.persistent_knowledge:
            researcher.persistent_knowledge.remember(solar_fact_key, solar_fact_value)
            print(f"In session '{researcher.get_active_memory_session()}', remembered: '{solar_fact_key}'\n")
        else:
            print("Warning: Persistent knowledge not initialized. Cannot remember fact.")

        # --- Task 2: Research Wind Energy (Session 2) ---
        print("--- Starting Task 2: Research Wind Energy (Switching to Session: wind_energy_potentials) ---")
        researcher.set_active_memory_session("wind_energy_potentials") # Switch to Session 2
        print(f"Expert switched. Active session: {researcher.get_active_memory_session()}")
        
        wind_guardrails = {
            "research_topic": "Wind Energy Advancements",
            "research_depth": "thorough",
            "focus_areas": "floating offshore turbines, AI in wind farm optimization, bladeless designs",
            "tone": "technical",
            "include_sources": True
        }
        wind_research_op = Operation(
            instructions="Investigate {research_topic}. Detail {focus_areas}. Maintain a {tone} tone and provide a {research_depth} overview.",
            output_format="A {research_depth} technical overview on {research_topic}.",
            expert=researcher,
            result_destination="outputs/user_examples/wind_energy_research_session2.md"
        )
        wind_result = wind_research_op.execute(guardrails=wind_guardrails)
        print(f"Wind energy research completed. Results: {wind_research_op.result_destination}")

        # Remember a fact in Session 2
        wind_fact_key = "wind_turbine_design_note"
        wind_fact_value = "Floating offshore wind turbines are expanding deployment possibilities."
        if researcher.persistent_knowledge:
            researcher.persistent_knowledge.remember(wind_fact_key, wind_fact_value)
            print(f"In session '{researcher.get_active_memory_session()}', remembered: '{wind_fact_key}'\n")
        else:
            print("Warning: Persistent knowledge not initialized. Cannot remember fact.")

        # --- Demonstrate Memory Isolation and Recall ---
        print("--- Demonstrating Memory Isolation and Recall ---")
        # Currently in Session 2 ("wind_energy_potentials")
        print(f"Currently in session: {researcher.get_active_memory_session()}")
        if researcher.persistent_knowledge:
            recalled_wind_fact = researcher.persistent_knowledge.recall(wind_fact_key)
            print(f"Recalling '{wind_fact_key}': {recalled_wind_fact}")
            assert recalled_wind_fact == wind_fact_value, "Wind fact recall failed in its session!"
            
            recalled_solar_fact_in_wind_session = researcher.persistent_knowledge.recall(solar_fact_key)
            print(f"Attempting to recall '{solar_fact_key}' (from solar session): {recalled_solar_fact_in_wind_session}")
            assert recalled_solar_fact_in_wind_session is None, "Solar fact incorrectly found in wind session!"
        else:
            print("Warning: Persistent knowledge not initialized. Cannot test recall.")

        # Switch back to Session 1 ("solar_power_deep_dive")
        researcher.set_active_memory_session("solar_power_deep_dive")
        print(f"\nSwitched back to session: {researcher.get_active_memory_session()}")
        if researcher.persistent_knowledge:
            recalled_solar_fact = researcher.persistent_knowledge.recall(solar_fact_key)
            print(f"Recalling '{solar_fact_key}': {recalled_solar_fact}")
            assert recalled_solar_fact == solar_fact_value, "Solar fact recall failed in its session!"

            recalled_wind_fact_in_solar_session = researcher.persistent_knowledge.recall(wind_fact_key)
            print(f"Attempting to recall '{wind_fact_key}' (from wind session): {recalled_wind_fact_in_solar_session}")
            assert recalled_wind_fact_in_solar_session is None, "Wind fact incorrectly found in solar session!"
        
        print("\nSession-aware memory recall and isolation tests PASSED!\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup the persistent knowledge base directory
        if os.path.exists(PERSISTENT_KB_PATH):
            print(f"Cleaning up test knowledge base: {PERSISTENT_KB_PATH}")
            shutil.rmtree(PERSISTENT_KB_PATH)
        print("Example script finished.")

if __name__ == "__main__":
    main()
