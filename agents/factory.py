from enum import Enum
from .gemini import Gemini25FlashSecurityReviewerAgent, Gemini25FlashTidynessReviewerAgent

class AgentType(Enum):
    SECURITY_REVIEWER = "security_reviewer"
    TIDYNESS_REVIEWER = "tidyness_reviewer"

class AgentFactory:
    @staticmethod
    def create_agent(agent_type: AgentType, llm_model, **kwargs):
        if agent_type == AgentType.SECURITY_REVIEWER:
            if llm_model == "gemini-2.5-flash":
                return Gemini25FlashSecurityReviewerAgent(**kwargs)
        elif agent_type == AgentType.TIDYNESS_REVIEWER:
            if llm_model == "gemini-2.5-flash":
                return Gemini25FlashTidynessReviewerAgent(**kwargs)
        
        return None
