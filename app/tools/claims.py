"""
Claims Status Tool for CARE Assistant.

This tool retrieves user claims history and current claim statuses
from mock insurance data. It can show pending, approved, and denied claims
along with payment details.
"""

from typing import Dict, Any, List
from langchain_core.tools import tool
from app.data.loader import get_data, get_claims_for_user, get_user_by_id


@tool
def claims_status(user_id: str, status_filter: str = "all") -> Dict[str, Any]:
    """
    Retrieve claims history and status for a user.

    This tool queries claims records to show:
    - Claim ID and service date
    - Service type and provider
    - Claim status (Pending, Approved, Denied)
    - Billing and payment details
    - Patient responsibility amounts

    Args:
        user_id: The unique user identifier (e.g., "user_001")
        status_filter: Optional filter for claim status. Options:
                      - "all" (default): Show all claims
                      - "pending": Show only pending claims
                      - "approved": Show only approved claims
                      - "denied": Show only denied claims

    Returns:
        dict: A structured response containing:
            - status: "success" or "error"
            - claims_count: Total number of claims found
            - claims: List of claim records
            - summary: Aggregate information (total billed, total paid, etc.)
            - message: Human-readable status message

    Example:
        >>> result = claims_status("user_001", "pending")
        >>> print(result['claims_count'])
        1
        >>> print(result['claims'][0]['claim_status'])
        Pending

    Note:
        Claims are returned in reverse chronological order (most recent first).
        The summary includes totals that can help users understand their
        out-of-pocket spending and insurance coverage.
    """
    try:
        # Get the loaded mock data
        data = get_data()

        # Verify user exists
        user = get_user_by_id(user_id, data)
        if not user:
            return {
                "status": "error",
                "message": f"User {user_id} not found in system",
                "claims_count": 0,
                "claims": []
            }

        # Get all claims for the user
        all_claims = get_claims_for_user(user_id, data)

        # Apply status filter if specified
        status_filter = status_filter.lower()
        if status_filter != "all":
            filtered_claims = [
                claim for claim in all_claims
                if claim.get('claim_status', '').lower() == status_filter
            ]
        else:
            filtered_claims = all_claims

        # Sort claims by service date (most recent first)
        filtered_claims.sort(
            key=lambda x: x.get('service_date', ''),
            reverse=True
        )

        # Calculate summary statistics
        total_billed = sum(claim.get('billed_amount', 0) for claim in filtered_claims)
        total_insurance_paid = sum(claim.get('insurance_paid', 0) for claim in filtered_claims)
        total_patient_responsibility = sum(
            claim.get('patient_responsibility', 0) for claim in filtered_claims
        )
        total_applied_to_deductible = sum(
            claim.get('applied_to_deductible', 0) for claim in filtered_claims
        )

        # Count claims by status
        status_counts = {}
        for claim in all_claims:
            status = claim.get('claim_status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "status": "success",
            "message": f"Retrieved {len(filtered_claims)} claim(s) for {user.get('name')}",
            "claims_count": len(filtered_claims),
            "claims": filtered_claims,
            "summary": {
                "total_billed": total_billed,
                "total_insurance_paid": total_insurance_paid,
                "total_patient_responsibility": total_patient_responsibility,
                "total_applied_to_deductible": total_applied_to_deductible,
                "status_breakdown": status_counts
            },
            "user_info": {
                "name": user.get('name'),
                "deductible_met": user.get('deductible_met'),
                "out_of_pocket_spent": user.get('out_of_pocket_spent')
            },
            "filter_applied": status_filter
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving claims: {str(e)}",
            "claims_count": 0,
            "claims": []
        }
