"""
Economics API — FastAPI router.
Mount on the main PrivateVault API with prefix /economics.
"""
from fastapi import APIRouter, Query, HTTPException
from pv_economics.storage.economics_store import EconomicsStore

router = APIRouter(prefix="/economics", tags=["economics"])
_store = EconomicsStore()


@router.get("/agent/{agent_name}")
def agent_summary(
    agent_name: str,
    days: int = Query(7, ge=1, le=90),
):
    """7-day economics summary for a single agent."""
    data = _store.get_agent_summary(agent_name, days=days)
    if data.get("runs", 0) == 0:
        raise HTTPException(404, f"No data for agent '{agent_name}'")
    return data


@router.get("/workflow/{workflow_id}")
def workflow_summary(
    workflow_id: str,
    days: int = Query(7, ge=1, le=90),
):
    """Cost and waste breakdown across agents in a workflow."""
    return _store.get_workflow_summary(workflow_id, days=days)


@router.get("/recent")
def recent_executions(
    limit: int = Query(50, ge=1, le=500),
):
    """Latest N execution records."""
    return _store.get_recent(limit=limit)


@router.get("/health")
def health():
    return {"status": "ok", "module": "pv_economics"}
