# Memory Management in SecureAgents

A robust memory system is the cornerstone of any advanced agentic framework. It allows agents to learn, recall information, collaborate effectively, and maintain context across complex, multi-step operations. The SecureAgents framework provides a sophisticated, two-tiered memory system designed for both individual expert autonomy and squad-level collaboration.

This guide provides a comprehensive overview of the memory features and how to leverage them in your projects.

## The Two Tiers of Memory

SecureAgents implements two distinct levels of memory:

1.  **Expert-Level Memory**: Each `Expert` agent has its own private memory, enabling it to maintain its own state, learn from its tasks, and build a persistent knowledge base over time.
2.  **Squad-Level Memory**: Each `Squad` has a shared memory space, allowing all member experts to contribute to and draw from a common pool of information, facilitating seamless collaboration on shared objectives.

---

## 1. Expert-Level Memory

An Expert's memory is further divided into two types, which can be used separately or together. This is controlled by the `memory_mode` parameter during `Expert` initialization.

### Short-Term (Working) Memory

-   **Purpose**: To hold ephemeral, in-the-moment information related to the current task. It acts as the expert's "consciousness."
-   **Behavior**: It logs crucial events, such as the inputs for a task, the tools used, and the outcome—including failures. This provides a detailed trace of the expert's actions, which is invaluable for debugging and observability.
-   **Persistence**: In-memory only; it is reset when the expert object is destroyed.
-   **Configuration**:
    ```python
    # Initialize an expert with only short-term memory
    expert = Expert(
        specialty="Data Analyst",
        objective="Analyze market trends.",
        memory_mode="short_term" 
    )
    ```

### Long-Term (Persistent) Knowledge

-   **Purpose**: To store facts, learned information, and conclusions that need to persist across different sessions and script runs. This forms the expert's long-term knowledge base.
-   **Behavior**: The knowledge is stored in a session-specific JSON file on disk. This ensures that an expert can be stopped and restarted without losing what it has learned. The system uses atomic writes and file locking to ensure data integrity, even in multi-threaded or crash-prone environments.
-   **Persistence**: Saved to disk.
-   **Configuration**:
    ```python
    # Define a path for the expert's knowledge base
    EXPERT_KB_PATH = "./outputs/my_expert_kb"
    EXPERT_SESSION_ID = "project_alpha_research"

    # Initialize an expert with only long-term memory
    expert = Expert(
        specialty="Researcher",
        objective="Gather and store information.",
        memory_mode="long_term",
        persistent_knowledge_base_path=EXPERT_KB_PATH,
        initial_session_id=EXPERT_SESSION_ID
    )
    ```

### Using Both Memory Types

To get the full benefit of both immediate task context and long-term learning, you can enable both memory modes.

-   **Configuration**:
    ```python
    # Initialize an expert with both short-term and long-term memory
    expert = Expert(
        specialty="Lead Researcher",
        objective="Conduct research and maintain a knowledge base.",
        memory_mode="both", # Default mode
        persistent_knowledge_base_path="./outputs/lead_researcher_kb",
        initial_session_id="main_session"
    )
    ```

---

## 2. Squad-Level Shared Memory

Collaboration is key to solving complex problems. The squad's persistent shared knowledge base allows multiple experts to work together, sharing facts and findings in a common context.

-   **Purpose**: To provide a centralized, session-aware repository of information for a squad.
-   **Behavior**: Similar to the expert's long-term knowledge, the squad's shared memory is stored in a session-specific JSON file, ensuring data integrity with atomic writes and file locking.
-   **Session-Awareness**: This is a critical feature. By using different `session_id`s, a single squad can work on multiple distinct projects without the knowledge from one bleeding into the other.

### Configuration and Usage

Configuring and using squad-level memory is done during `Squad` initialization and through dedicated methods.

```python
# From examples/user_friendly/memory_examples/6_squad_memory_deep_dive.py

import os
from tbh_secure_agents import Expert, Operation, Squad

# 1. Define paths and IDs for the squad memory
OUTPUT_DIR = "./outputs/squad_demo"
SHARED_KB_PATH = os.path.join(OUTPUT_DIR, "squad_kb")
SQUAD_ID = "financial_analysis_squad"
SESSION_ID = "q3_earnings_report"

# 2. Initialize the Squad with memory parameters
my_squad = Squad(
    experts=[...], # Your list of experts
    persistent_shared_knowledge_base_path=SHARED_KB_PATH,
    squad_id=SQUAD_ID,
    initial_session_id=SESSION_ID
)

# 3. Deploy the squad to run its operations
my_squad.deploy(operations=[...])

# 4. Interact with the shared memory
# Store a fact in the current session
fact_key = "q3_revenue_preliminary"
fact_value = {"amount": 1.2, "currency": "USD", "unit": "million"}
my_squad.store_shared_fact(fact_key, fact_value)
print(f"Stored fact: {fact_key}")

# Retrieve the fact
retrieved_fact = my_squad.retrieve_shared_fact(fact_key)
print(f"Retrieved fact: {retrieved_fact}")

# Retrieve all facts from the current session
all_session_facts = my_squad.get_all_shared_facts()
print(f"All facts in session '{SESSION_ID}': {all_session_facts}")
```

## Summary of Best Practices

-   **Use `memory_mode="both"`** for most experts to get the best of both worlds.
-   **Always provide explicit paths** for `persistent_knowledge_base_path` and `persistent_shared_knowledge_base_path` to avoid cluttering your root directory and to ensure outputs are organized.
-   **Leverage `session_id`s** extensively to keep contexts clean, especially when a single group of agents might be tasked with different, unrelated objectives over time.
-   **Check the expert's working memory** (`expert.working_memory.get_all_entries()`) when debugging to get a clear trace of its actions.

By understanding and utilizing these memory features, you can build more intelligent, resilient, and collaborative multi-agent systems with SecureAgents.
