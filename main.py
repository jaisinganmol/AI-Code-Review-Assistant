from fastapi import FastAPI, UploadFile, HTTPException
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from langchain_core.prompts import PromptTemplate
from typing import List
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY — set it in your .env file.")

review_prompt = PromptTemplate(
    input_variables=["code"],
    template="Perform an AI-driven static and security review on the following code:\n{code}",
)

static_agent = Agent(
    name="StaticAnalyzer",
    role="Analyze code logic, structure, and maintainability.",
    model=OpenAIChat(id="gpt-4o-mini"),
)

security_agent = Agent(
    name="SecurityScanner",
    role="Check for vulnerabilities, unsafe functions, or secrets leakage.",
    model=OpenAIChat(id="gpt-4o-mini"),
)

agent_os = AgentOS(description="AI Code Review Orchestrator", agents=[static_agent, security_agent])

app = FastAPI(title="AI Code Review Assistant")


@app.post("/review/")
async def review_code(files: List[UploadFile]):
    try:
        results = []
        for file in files:
            content = (await file.read()).decode("utf-8")
            prompt = review_prompt.format(code=content)

            loop = asyncio.get_event_loop()
            static_result = await loop.run_in_executor(None, lambda: static_agent.run(prompt))
            security_result = await loop.run_in_executor(None, lambda: security_agent.run(prompt))

            # Extract plain text from RunOutput
            static_text = static_result.content if hasattr(static_result, "content") else str(static_result)
            security_text = security_result.content if hasattr(security_result, "content") else str(security_result)

            combined_review = f"### Static Analysis\n{static_text}\n\n### Security Analysis\n{security_text}"


            results.append({"filename": file.filename, "review": combined_review})
        return {"reviews": results}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
