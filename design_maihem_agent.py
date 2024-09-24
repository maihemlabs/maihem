from maihem.agents import MaihemAgent


maihem_agent = MaihemAgent(
    identifier="test-agent",
    workflow_prompt="", # Guide the behavior of the Maihem Agent with a prompt describing the workflow of the user
    workflow_dict="", # Optional, provide a dictionary of the workflow to guide the behavior of the Maihem Agent, use our tool to help you generate this
    metric_to_test="helpfulness",
    static_responses=True, # Optional, return the same static responses every time
    turns_static=5, # Optional, to set the first number of turns to be static (repeat the same messages)
    turns_max=10, # Optional, to set maximum number of turns
    add_personality=True, # Optional, add personality to the agent
    target_agent_identifier="target_agent_unique_identifier",
    target_agent_role="mental health assistant",
    target_agent_description="A chatbot for emotional support",
)

# For RAG evaluations
# Load documents that the agent can use to generate responses
maihem_agent.add_documents(paths=["./data/journaling.txt", "./data/habit-building.txt", "./data/emotional-support.txt"])

maihem_agent_message = maihem_agent.chat(
    target_agent_message="Hi, how can I help you today?", # Message from the Target Agent
    contexts=["<Context 1>", "<Context 2>"], # Optional, to provide context for the agent for RAG
)

# Get message content and evals
maihem_agent_message.content
maihem_agent_message.eval

# Get conversation and evals
maihem_agent.conversation
maihem_agent.evals