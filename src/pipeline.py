# src/pipeline.py

import os

from src.agents.behavior_agent import BehaviorAgent
from src.agents.reasoning_agent import ReasoningAgent
from src.agents.campaign_agent import CampaignAgent

from src.domains.supermarket import SUPERMARKET_DOMAIN
from src.domains.oil import OIL_DOMAIN
from src.domains.banking import BANKING_DOMAIN

from src.utils import load_json, pretty_print


# --------------------------------------------------
# BASE DIRECTORY (FINAL FIX)
# --------------------------------------------------
# Use current working directory (project root)
BASE_DIR = os.getcwd()


# --------------------------------------------------
# DOMAIN CONFIGURATION
# --------------------------------------------------

DOMAIN_CONFIGS = {
    "supermarket": SUPERMARKET_DOMAIN,
    "oil": OIL_DOMAIN,
    "banking": BANKING_DOMAIN,
}


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

def run_pipeline(domain_name: str):

    if domain_name not in DOMAIN_CONFIGS:
        raise ValueError(f"Unsupported domain: {domain_name}")

    domain = DOMAIN_CONFIGS[domain_name]

    # ----------------------------
    # Load DOMAIN-SCOPED data
    # ----------------------------
    customers = load_json(
        os.path.join(BASE_DIR, "data", domain_name, "customers.json")
    )

    transactions = load_json(
        os.path.join(BASE_DIR, "data", domain_name, "transactions.json")
    )

    # ----------------------------
    # Initialize agents
    # ----------------------------
    behavior_agent = BehaviorAgent()
    reasoning_agent = ReasoningAgent()
    campaign_agent = CampaignAgent()

    results = []

    # ----------------------------
    # CUSTOMER LOOP (DOMAIN SAFE)
    # ----------------------------
    for customer in customers:
        customer_id = customer["customer_id"]

        # 1. Behavior analysis (deterministic)
        behavior = behavior_agent.analyze_customer(
            customer_id=customer_id,
            transactions=transactions,
            domain_config=domain,
        )

        segment = behavior["segment"]
        signals = behavior["signals"]

        # 2. LLM reasoning (Groq)
        reasoning = reasoning_agent.reason(
            segment=segment,
            signals=signals,
            domain_name=domain.name,
        )

        # 3. Campaign recommendation + ROI
        campaign = campaign_agent.recommend_campaign(
            segment=segment,
            signals=signals,
            domain_config=domain,
            segment_size=1000,  # POC assumption
        )

        results.append({
            "customer_id": customer_id,
            "segment": segment,
            "signals": signals,
            "reasoning": reasoning,
            "campaign": campaign,
        })

    return results


def run_pipeline_with_data(
    domain: str,
    customers: list,
    transactions: list,
    past_campaigns: list,
):
    """
    Same logic as run_pipeline(), but uses in-memory data.
    """

    from src.agents.behavior_agent import BehaviorAgent
    from src.agents.reasoning_agent import ReasoningAgent
    from src.agents.campaign_agent import CampaignAgent
    from src.domains.registry import DOMAIN_REGISTRY

    domain_config = DOMAIN_REGISTRY[domain]

    behavior_agent = BehaviorAgent()
    reasoning_agent = ReasoningAgent()
    campaign_agent = CampaignAgent(past_campaigns)

    output = []

    for customer in customers:
        customer_id = customer["customer_id"]

        behavior = behavior_agent.analyze_customer(
            customer_id=customer_id,
            transactions=transactions,
            domain_config=domain_config,
        )

        reasoning = reasoning_agent.reason(
            customer_id=customer_id,
            segment=behavior["segment"],
            signals=behavior["signals"],
            domain=domain,
        )

        campaign = campaign_agent.recommend_campaign(
            segment=behavior["segment"]
        )

        output.append({
            "customer_id": customer_id,
            "segment": behavior["segment"],
            "signals": behavior["signals"],
            "reasoning": reasoning,
            "campaign": campaign,
        })

    return output

def run_pipeline_with_ingestion(
    domain: str,
    customers: list,
    transactions: list,
    past_campaigns: list,
):
    """
    Run pipeline using live-ingested data (API / Streamlit)
    """

    from src.agents.behavior_agent import BehaviorAgent
    from src.agents.reasoning_agent import ReasoningAgent
    from src.agents.campaign_agent import CampaignAgent
    from src.domains.registry import DOMAIN_REGISTRY

    domain_config = DOMAIN_REGISTRY[domain]

    behavior_agent = BehaviorAgent()
    reasoning_agent = ReasoningAgent()
    campaign_agent = CampaignAgent()

    results = []

    for customer in customers:
        customer_id = customer["customer_id"]

        behavior_output = behavior_agent.analyze_customer(
            customer_id=customer_id,
            transactions=transactions,
            domain_config=domain_config,
        )

        reasoning = reasoning_agent.reason(
            customer_id=customer_id,
            segment=behavior_output["segment"],
            signals=behavior_output["signals"],
            domain=domain,
        )

        campaign = campaign_agent.recommend_campaign(
            segment=behavior_output["segment"],
            past_campaigns=past_campaigns,
        )

        results.append(
            {
                "customer_id": customer_id,
                "segment": behavior_output["segment"],
                "signals": behavior_output["signals"],
                "reasoning": reasoning,
                "campaign": campaign,
            }
        )

    return {
        "domain": domain,
        "results": results,
    }

# --------------------------------------------------
# CLI ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    for domain_name in ["supermarket", "oil", "banking"]:
        print("\n" + "#" * 80)
        print(f"RUNNING PIPELINE FOR DOMAIN: {domain_name.upper()}")
        print("#" * 80)

        output = run_pipeline(domain_name)
        pretty_print("FINAL OUTPUT", output)
