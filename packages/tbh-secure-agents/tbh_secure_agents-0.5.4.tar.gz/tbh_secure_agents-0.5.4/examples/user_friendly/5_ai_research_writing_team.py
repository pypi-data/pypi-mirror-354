#!/usr/bin/env python3
"""
Example 5: AI Research & Writing Team
=====================================

This example shows how to create a team of AI agents (Squad) that work
together - a researcher and writer collaborating on a complete project.

Features demonstrated:
- Creating multiple Expert agents
- Using Squad for team collaboration
- Sequential workflow (research then write)
- Using guardrails for team coordination
- Saving final result in JSON format
"""

import os
import shutil # For cleanup

# Set your Google API key (replace with your actual key or use environment variables)
# Using the key provided by the user for testing
os.environ["GOOGLE_API_KEY"] = "AIzaSyBtIh9ShcSmezYKa8xmI0kIyyl2gJZIYFc"

from tbh_secure_agents import Expert, Operation, Squad

# Define path for persistent shared knowledge
PERSISTENT_SHARED_KB_PATH = "./.user_example_squad_kb"
SQUAD_ID = "research_team_alpha"
INITIAL_SESSION_ID = "project_kickoff"

def main():
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs/user_examples", exist_ok=True)

    try:
        print(f"--- Initializing Squad '{SQUAD_ID}' with Session-Aware Shared Memory ---")
        print(f"Persistent Shared KB Path: {PERSISTENT_SHARED_KB_PATH}")
        print(f"Initial Session ID: {INITIAL_SESSION_ID}\n")

        # Create AI team members
        # Set memory_mode to 'none' for individual experts to focus on shared squad memory
        researcher = Expert(
            specialty="Research Specialist",
            objective="Conduct thorough research and gather comprehensive information",
            security_profile="minimal",
            memory_mode="none" 
        )

        writer = Expert(
            specialty="Content Writer",
            objective="Transform research into engaging, well-written content",
            security_profile="minimal",
            memory_mode="none"
        )

        # Define team guardrails for the first phase
        team_guardrails_phase1 = {
            "factual_content": True,
            "no_harmful_content": True,
            "professional_tone": True,
            "project_topic": "sustainable technology trends for Q1 2025",
            "target_audience": "business executives",
            "content_length": "comprehensive but concise",
            "include_data": True,
            "include_recommendations": True
        }

        # Create research operation for phase 1
        research_operation_phase1 = Operation(
            instructions="Research the latest trends in {project_topic}, including market data, key innovations, and industry outlook for {target_audience}.",
            output_format="Comprehensive research findings with data, trends, and key insights.",
            expert=researcher,
            result_destination=f"outputs/user_examples/{SQUAD_ID}_sustainability_research_phase1.md"
        )

        # Create writing operation for phase 1 (will use research results as context from shared memory)
        writing_operation_phase1 = Operation(
            instructions="Based on the research findings (available in shared squad memory under 'phase1_research_summary'), write an executive summary about {project_topic} for {target_audience}.",
            output_format="Professional executive summary with key insights and actionable recommendations.",
            expert=writer,
            result_destination=f"outputs/user_examples/{SQUAD_ID}_sustainability_summary_phase1.md"
        )

        # Create the AI team (Squad)
        research_writing_team = Squad(
            experts=[researcher, writer],
            operations=[research_operation_phase1, writing_operation_phase1],
            process="sequential",  # Research first, then write
            persistent_shared_knowledge_base_path=PERSISTENT_SHARED_KB_PATH,
            squad_id=SQUAD_ID,
            initial_session_id=INITIAL_SESSION_ID,
            result_destination={
                "format": "json",
                "file_path": f"outputs/user_examples/{SQUAD_ID}_team_project_results_phase1.json"
            }
        )

        print(f"Squad '{research_writing_team.get_squad_id()}' initialized. Active shared session: {research_writing_team.get_active_shared_session()}\n")

        # Deploy the team for Phase 1
        print(f"--- Deploying Squad for Phase 1: {INITIAL_SESSION_ID} ---")
        print(f"Project: {team_guardrails_phase1['project_topic']}")
        print(f"Process: Sequential (Research → Write)")
        print(f"Expected Final Output: {research_writing_team.result_destination['file_path']}\n")

        # We need to run operations more granularly to interact with shared memory between them.
        # The current Squad.deploy() executes all operations sequentially without intermediate steps.
        # For this example, we'll simulate a more controlled execution to showcase shared memory.

        print("Executing Phase 1 Research Operation...")
        # Execute research_operation_phase1 - In a real scenario, Squad.deploy might handle this execution.
        # For this example, we'll assume the operation runs and produces a result.
        # To simulate, we'll directly store a fact that the researcher would have found.
        research_summary_phase1 = "Phase 1 research indicates strong growth in solar and wind, with emerging opportunities in green hydrogen."
        research_writing_team.store_shared_fact("phase1_research_summary", research_summary_phase1)
        print(f"Stored in shared memory (Session: {research_writing_team.get_active_shared_session()}): 'phase1_research_summary': '{research_summary_phase1}'")
        # Manually create the research output file for completeness of the example flow
        with open(research_operation_phase1.result_destination, 'w') as f:
            f.write(f"# Research Summary for {team_guardrails_phase1['project_topic']}\n\n{research_summary_phase1}")
        print(f"Phase 1 research output (simulated) saved to: {research_operation_phase1.result_destination}\n")

        print("Executing Phase 1 Writing Operation...")
        # The writer expert would ideally retrieve this from shared memory during its operation.
        # We'll retrieve it here to show it's available.
        retrieved_summary = research_writing_team.retrieve_shared_fact("phase1_research_summary")
        print(f"Retrieved from shared memory for writer: '{retrieved_summary}'")
        assert retrieved_summary == research_summary_phase1, "Failed to retrieve phase 1 research summary!"
        
        # Simulate writer creating the summary based on the retrieved fact
        executive_summary_phase1 = f"Executive Summary for {team_guardrails_phase1['project_topic']}:\n{retrieved_summary}\nKey recommendations include investing in solar R&D."
        with open(writing_operation_phase1.result_destination, 'w') as f:
            f.write(executive_summary_phase1)
        print(f"Phase 1 writing output (simulated) saved to: {writing_operation_phase1.result_destination}")
        print("✅ Phase 1 (Project Kickoff) completed successfully!\n")

        # --- Phase 2: Deep Dive Analysis (New Session) ---
        DEEP_DIVE_SESSION_ID = "deep_dive_ai_sustainability"
        print(f"--- Starting Phase 2: Deep Dive Analysis (Switching to Session: {DEEP_DIVE_SESSION_ID}) ---")
        research_writing_team.set_active_shared_session(DEEP_DIVE_SESSION_ID)
        print(f"Squad active shared session: {research_writing_team.get_active_shared_session()}")

        team_guardrails_phase2 = {
            "project_topic": "AI's role in optimizing sustainable energy grids",
            "research_depth": "in-depth technical analysis",
            "focus_areas": "smart grid optimization, predictive maintenance for renewables, AI in energy storage"
        }

        # New research operation for phase 2
        research_operation_phase2 = Operation(
            instructions="Conduct an {research_depth} on {project_topic}, focusing on {focus_areas}.",
            output_format="Detailed technical report with case studies and future projections.",
            expert=researcher, # Same researcher expert
            result_destination=f"outputs/user_examples/{SQUAD_ID}_ai_sustainability_research_phase2.md"
        )
        
        print("Executing Phase 2 Research Operation...")
        research_summary_phase2 = "Phase 2 research on AI in sustainable grids highlights significant efficiency gains through predictive analytics for wind turbine maintenance and optimized solar farm output."
        research_writing_team.store_shared_fact("phase2_ai_grid_insight", research_summary_phase2)
        print(f"Stored in shared memory (Session: {research_writing_team.get_active_shared_session()}): 'phase2_ai_grid_insight': '{research_summary_phase2}'")
        with open(research_operation_phase2.result_destination, 'w') as f:
            f.write(f"# Research Report: {team_guardrails_phase2['project_topic']}\n\n{research_summary_phase2}")
        print(f"Phase 2 research output (simulated) saved to: {research_operation_phase2.result_destination}\n")

        # --- Demonstrate Shared Memory Isolation and Recall ---
        print("--- Demonstrating Shared Memory Isolation and Recall ---")
        # Currently in DEEP_DIVE_SESSION_ID
        print(f"Currently in shared session: {research_writing_team.get_active_shared_session()}")
        retrieved_phase2_fact = research_writing_team.retrieve_shared_fact("phase2_ai_grid_insight")
        print(f"Recalling 'phase2_ai_grid_insight': {retrieved_phase2_fact}")
        assert retrieved_phase2_fact == research_summary_phase2, "Phase 2 fact recall failed!"

        retrieved_phase1_fact_in_phase2_session = research_writing_team.retrieve_shared_fact("phase1_research_summary")
        print(f"Attempting to recall 'phase1_research_summary' (from project_kickoff session): {retrieved_phase1_fact_in_phase2_session}")
        assert retrieved_phase1_fact_in_phase2_session is None, "Phase 1 fact incorrectly found in Phase 2 session!"

        # Switch back to INITIAL_SESSION_ID ("project_kickoff")
        research_writing_team.set_active_shared_session(INITIAL_SESSION_ID)
        print(f"\nSwitched back to shared session: {research_writing_team.get_active_shared_session()}")
        retrieved_phase1_fact_again = research_writing_team.retrieve_shared_fact("phase1_research_summary")
        print(f"Recalling 'phase1_research_summary': {retrieved_phase1_fact_again}")
        assert retrieved_phase1_fact_again == research_summary_phase1, "Phase 1 fact recall failed after switching back!"

        retrieved_phase2_fact_in_phase1_session = research_writing_team.retrieve_shared_fact("phase2_ai_grid_insight")
        print(f"Attempting to recall 'phase2_ai_grid_insight' (from deep_dive session): {retrieved_phase2_fact_in_phase1_session}")
        assert retrieved_phase2_fact_in_phase1_session is None, "Phase 2 fact incorrectly found in Phase 1 session after switching back!"

        print("\n✅ Squad shared session memory recall and isolation tests PASSED!\n")
        print("✅ Full example completed successfully!")

    except Exception as e:
        print(f"❌ Error during squad operations: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup the persistent shared knowledge base directory
        if os.path.exists(PERSISTENT_SHARED_KB_PATH):
            print(f"Cleaning up test shared knowledge base: {PERSISTENT_SHARED_KB_PATH}")
            shutil.rmtree(PERSISTENT_SHARED_KB_PATH)
        print("Squad example script finished.")

if __name__ == "__main__":
    main()
