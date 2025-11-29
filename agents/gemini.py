from . import agent
from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini25FlashSecurityReviewerAgent(agent.BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def ask(self, diff: str) -> str:
        prompt = "Please review the following pull request diff for security vulnerabilities and provide feedback."
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        response = await llm.ainvoke(f"{prompt}\n\n{diff}")
        return str(response.content)

class Gemini25FlashTidynessReviewerAgent(agent.BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def ask(self, diff: str) -> str:
        prompt = "Please review the following pull request diff for code tidiness, style, and best practices, and provide feedback."
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        response = await llm.ainvoke(f"{prompt}\n\n{diff}")
        return str(response.content)
