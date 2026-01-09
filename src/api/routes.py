from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from src.pipeline import run_pipeline, run_pipeline_with_ingestion

router = APIRouter()

# =====================================================
# REQUEST MODELS
# =====================================================

class DomainPayload(BaseModel):
    domain: str


class IngestionPayload(BaseModel):
    domain: str
    customers: List[Dict[str, Any]]
    transactions: List[Dict[str, Any]]
    past_campaigns: List[Dict[str, Any]]


# =====================================================
# ROUTES
# =====================================================

@router.post("/run")
def run_pipeline_api(payload: DomainPayload):
    """
    Runs pipeline using stored dataset
    """
    results = run_pipeline(payload.domain)
    return {"results": results}


@router.post("/ingest-and-analyze")
def ingest_and_analyze(payload: IngestionPayload):
    """
    Runs pipeline using live ingested data
    """
    results = run_pipeline_with_ingestion(
        domain=payload.domain,
        customers=payload.customers,
        transactions=payload.transactions,
        past_campaigns=payload.past_campaigns,
    )
    return results
