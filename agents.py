from agno.agent import Agent
from langchain_core.prompts import PromptTemplate

static_agent = Agent(
    name="StaticAnalyzer",
    system_prompt="Analyze code for logical errors, complexity, and maintainability."
)

security_agent = Agent(
    name="SecurityScanner",
    system_prompt="Identify vulnerabilities, insecure patterns, and secrets in code."
)

review_template = PromptTemplate(
    input_variables=["code"],
    template="Perform a holistic review of the following code:\n{code}"
)
