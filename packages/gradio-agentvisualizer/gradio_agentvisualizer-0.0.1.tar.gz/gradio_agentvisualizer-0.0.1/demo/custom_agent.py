from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, OpenAIServerModel

model = InferenceClientModel()
tools = [DuckDuckGoSearchTool()]

detection_agent = CodeAgent(
    name="detection_agent",
    description="Analyzes logs and identifies intrusions using fast AI classification.",
    tools=tools,
    model=model,
)

containment_agent = CodeAgent(
    name="containment_agent",
    description="Executes emergency actions like blocking IPs, killing processes, or isolating the system.",
    tools=tools,
    model=model,
)

forensics_agent = CodeAgent(
    name="forensics_agent",
    description="Inspects filesystem and logs to identify attack vectors and changes.",
    tools=tools,
    model=model,
)

recovery_agent = CodeAgent(
    name="recovery_agent",
    description="Restores system stability by creating new users, restarting services, and cleaning up.",
    tools=tools,
    model=model,
)

audit_agent = CodeAgent(
    name="audit_agent",
    description="Generates a full post-incident report with recommendations and timelines.",
    tools=tools,
    model=model,
)


manager_agent = CodeAgent(
    model=model,
    name="manager_agent",
    description="You ara a manager for an escilation sutation, you need to help the user detect arnomalies in a system and provide information on how to prevent more damage, remove the intruder, recovery and auditing. currently do it as a simulation " \
    ", create a random detection and provide steps on how to remove the thread.",
    tools=tools,
    planning_interval=4,
    max_steps=15,
    managed_agents=[
        detection_agent,
        containment_agent, 
        forensics_agent, 
        recovery_agent, 
        audit_agent, 
    ]
)
