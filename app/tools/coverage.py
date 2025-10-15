"""
Coverage Lookup Tool for CARE Assistant.

This tool queries user coverage details from mock insurance data.
It demonstrates how to integrate external data sources as LangGraph tools.

The tool uses LangChain's @tool decorator to make it compatible with LangGraph's
tool-calling nodes. Tools are essentially functions that the agent can invoke
to retrieve information or perform actions.
"""

from typing import Dict, Any
from langchain_core.tools import tool
from app.data.loader import get_data, get_user_with_plan


@tool
def coverage_lookup(user_id: str, query: str = "") -> Dict[str, Any]:
    """
    Look up insurance coverage details for a user.

    This tool retrieves comprehensive coverage information including:
    - Insurance plan type and name
    - Deductible information (annual amount, amount met so far)
    - Out-of-pocket maximum and spending
    - Coverage details by category (preventive, specialist, emergency, etc.)
    - Network information

    Args:
        user_id: The unique user identifier (e.g., "user_001")
        query: Optional natural language query about coverage (e.g., "physical therapy")
               Currently not used for filtering, but included for future enhancements

    Returns:
        dict: A structured response containing:
            - status: "success" or "error"
            - data: Coverage information if found
            - message: Human-readable status message
            - user_info: Basic user information

    Example:
        >>> result = coverage_lookup("user_001", "What's covered?")
        >>> print(result['status'])
        success
        >>> print(result['data']['plan_name'])
        PPO Gold

    Note:
        This tool is designed to be called by LangGraph nodes. The @tool decorator
        makes it compatible with LangChain's tool-calling framework.
    """
    try:
        # Get the loaded mock data
        data = get_data()

        # Get user profile with embedded plan details
        user_with_plan = get_user_with_plan(user_id, data)

        if not user_with_plan:
            return {
                "status": "error",
                "message": f"User {user_id} not found in system",
                "data": None
            }

        # Extract relevant coverage information
        plan_details = user_with_plan.get('plan_details', {})

        coverage_info = {
            # Plan information
            "plan_name": plan_details.get('plan_name'),
            "plan_type": plan_details.get('plan_type'),
            "monthly_premium": plan_details.get('monthly_premium'),

            # Deductible info
            "deductible_annual": user_with_plan.get('deductible_annual'),
            "deductible_met": user_with_plan.get('deductible_met'),
            "deductible_remaining": (
                user_with_plan.get('deductible_annual', 0) -
                user_with_plan.get('deductible_met', 0)
            ),

            # Out-of-pocket info
            "out_of_pocket_max": user_with_plan.get('out_of_pocket_max'),
            "out_of_pocket_spent": user_with_plan.get('out_of_pocket_spent'),
            "out_of_pocket_remaining": (
                user_with_plan.get('out_of_pocket_max', 0) -
                user_with_plan.get('out_of_pocket_spent', 0)
            ),

            # Coverage details by category
            "coverage_details": plan_details.get('coverage_details', {}),

            # Network information
            "network_info": plan_details.get('network_info', {}),
        }

        return {
            "status": "success",
            "message": f"Retrieved coverage information for {user_with_plan.get('name')}",
            "data": coverage_info,
            "user_info": {
                "name": user_with_plan.get('name'),
                "user_id": user_id,
                "member_since": user_with_plan.get('member_since'),
                "dependents": user_with_plan.get('dependents')
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving coverage: {str(e)}",
            "data": None
        }
