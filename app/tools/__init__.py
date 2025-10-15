"""
LangGraph Tools for CARE Assistant.

This module exports all tools that the agent can use to query insurance information.
Tools are functions decorated with @tool that can be called by LangGraph nodes.

Available Tools:
    - coverage_lookup: Query comprehensive coverage details for a user
    - benefit_verify: Check if a specific service is covered
    - claims_status: Retrieve claims history and status

Usage:
    from app.tools import coverage_lookup, benefit_verify, claims_status

    # In a LangGraph node:
    result = coverage_lookup.invoke({"user_id": "user_001", "query": ""})
"""

from app.tools.coverage import coverage_lookup
from app.tools.benefits import benefit_verify
from app.tools.claims import claims_status

# Export all tools
__all__ = [
    "coverage_lookup",
    "benefit_verify",
    "claims_status",
]
