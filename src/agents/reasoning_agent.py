# src/agents/reasoning_agent.py

from typing import Dict
from src.llm.llm_client import LLMClient


class ReasoningAgent:
    """
    LLM-powered reasoning agent.

    Purpose:
    - Translate deterministic behavior signals into
      human-readable insights.
    - Explain WHY a customer falls into a segment.
    - Highlight BUSINESS RISK if no action is taken.

    IMPORTANT:
    - This agent does NOT make decisions.
    - It only explains decisions made upstream.
    """

    def __init__(self):
        self.llm = LLMClient()

    def reason(
        self,
        segment: str,
        signals: Dict,
        domain_name: str,
    ) -> Dict:
        """
        Generate reasoning and business context using Groq.
        """

        prompt = f"""
You are a senior marketing intelligence analyst working on a loyalty platform.

Domain: {domain_name}

Customer Segment: {segment}

Observed behavioral signals:
{signals}

Your task:
1. Clearly explain WHY the customer is classified into this segment.
2. Describe the BUSINESS RISK if no action is taken.
3. Do NOT infer sensitive personal attributes.
4. Keep the explanation concise, professional, and suitable
   for a Marketing Manager dashboard.
"""

        llm_explanation = self.llm.run(prompt, task="reasoning")

        return {
            "llm_explanation": llm_explanation,
            "confidence": self._confidence(segment),
            "business_risk": self._business_risk(segment),
        }

    # --------------------------------------------------
    # Deterministic helpers (NO LLM)
    # --------------------------------------------------

    def _confidence(self, segment: str) -> str:
        """
        Confidence reflects signal strength, not model certainty.
        """

        if segment in [
            "Dormant / At-Risk",
            "Price-Sensitive Disengagers",
        ]:
            return "High"

        if segment == "Re-Engaging Customers":
            return "Medium"

        return "Low"

    def _business_risk(self, segment: str) -> str:
        """
        Deterministic business framing for dashboards.
        """

        if segment == "Dormant / At-Risk":
            return "High churn risk if re-engagement is delayed."

        if segment == "Price-Sensitive Disengagers":
            return "Revenue erosion risk if value perception is not addressed."

        if segment == "Re-Engaging Customers":
            return "Missed opportunity to reinforce renewed engagement."

        if segment == "Stable Core Customers":
            return "Low immediate risk, but loyalty erosion if ignored."

        return "Low immediate business risk."
