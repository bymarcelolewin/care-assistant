"""
Benefit Verification Tool for CARE Assistant.

This tool checks if specific medical services or procedures are covered
under a user's insurance plan. It looks up coverage details for services
like specialist visits, prescriptions, emergency care, etc.
"""

from typing import Dict, Any
from langchain_core.tools import tool
from app.data.loader import get_data, get_user_with_plan


@tool
def benefit_verify(user_id: str, service_type: str) -> Dict[str, Any]:
    """
    Verify if a specific medical service is covered under the user's insurance plan.

    This tool checks coverage for various types of medical services including:
    - primary_care: Primary care physician visits
    - specialist: Specialist consultations
    - emergency_room: ER visits
    - urgent_care: Urgent care visits
    - prescription_drugs: Medications (generic, brand_name, specialty)
    - preventive_care: Annual physicals, screenings, vaccines
    - mental_health: Mental health services

    Args:
        user_id: The unique user identifier (e.g., "user_001")
        service_type: The type of service to check (e.g., "specialist", "emergency_room")

    Returns:
        dict: A structured response containing:
            - status: "success" or "error"
            - service_type: The service that was queried
            - is_covered: Boolean indicating if service is covered
            - coverage_details: Specific coverage information (copays, coverage %, notes)
            - message: Human-readable status message

    Example:
        >>> result = benefit_verify("user_001", "specialist")
        >>> print(result['is_covered'])
        True
        >>> print(result['coverage_details']['in_network']['copay'])
        50

    Note:
        The service_type should match keys in the insurance plan's coverage dict.
        If the service is not found, the tool returns a helpful error message.
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
                "is_covered": False,
                "coverage_details": None
            }

        # Get the plan's coverage information
        plan_details = user_with_plan.get('plan_details', {})
        coverage = plan_details.get('coverage', {})

        # Normalize service_type (handle variations)
        service_key = service_type.lower().replace(" ", "_")

        # Check if the service is covered
        service_coverage = coverage.get(service_key)

        if service_coverage is None:
            # Service not found in coverage
            available_services = list(coverage.keys())
            return {
                "status": "error",
                "service_type": service_type,
                "is_covered": False,
                "coverage_details": None,
                "message": f"Service '{service_type}' not found in coverage. Available services: {', '.join(available_services)}",
                "available_services": available_services
            }

        # Service is covered, return details
        return {
            "status": "success",
            "service_type": service_type,
            "is_covered": True,
            "coverage_details": service_coverage,
            "plan_info": {
                "plan_name": plan_details.get('plan_name'),
                "plan_type": plan_details.get('plan_type')
            },
            "message": f"Coverage details retrieved for {service_type} under {plan_details.get('plan_name')} plan",
            "user_info": {
                "name": user_with_plan.get('name'),
                "deductible_remaining": (
                    user_with_plan.get('deductible_annual', 0) -
                    user_with_plan.get('deductible_met', 0)
                )
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "service_type": service_type,
            "is_covered": False,
            "coverage_details": None,
            "message": f"Error verifying benefits: {str(e)}"
        }
