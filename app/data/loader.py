"""
Mock Data Loader

This module loads JSON files containing mock insurance data into memory.
The data is used by LangGraph tools to demonstrate realistic insurance
coverage queries without requiring real APIs or databases.

Data files:
- user_profiles.json: Contains user information and insurance details
- insurance_plans.json: Contains plan types and coverage information
- claims_data.json: Contains historical claims records

Usage:
    from app.data.loader import load_all_data, get_user_by_id

    # Load all data at application startup
    data = load_all_data()

    # Access specific user
    user = get_user_by_id("user_001", data)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


# Get the directory where this file is located
DATA_DIR = Path(__file__).parent


def load_json_file(filename: str) -> Dict[str, Any]:
    """
    Load a JSON file from the data directory.

    Args:
        filename: Name of the JSON file to load

    Returns:
        dict: Parsed JSON data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_all_data() -> Dict[str, Any]:
    """
    Load all mock data files into memory.

    Returns:
        dict: Dictionary containing all loaded data with keys:
            - 'users': List of user profiles
            - 'plans': List of insurance plans
            - 'claims': List of claims records

    Example:
        >>> data = load_all_data()
        >>> print(f"Loaded {len(data['users'])} users")
        Loaded 3 users
    """
    print("📂 Loading mock data...")

    try:
        user_data = load_json_file("user_profiles.json")
        plan_data = load_json_file("insurance_plans.json")
        claims_data = load_json_file("claims_data.json")

        data = {
            'users': user_data.get('users', []),
            'plans': plan_data.get('plans', []),
            'claims': claims_data.get('claims', [])
        }

        print(f"  ✓ Loaded {len(data['users'])} user profiles")
        print(f"  ✓ Loaded {len(data['plans'])} insurance plans")
        print(f"  ✓ Loaded {len(data['claims'])} claims records")

        return data

    except Exception as e:
        print(f"  ✗ Error loading data: {e}")
        raise


def get_user_by_id(user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Find a user by their user_id.

    Args:
        user_id: The unique user identifier (e.g., "user_001")
        data: The loaded data dictionary from load_all_data()

    Returns:
        dict: User profile if found, None otherwise

    Example:
        >>> data = load_all_data()
        >>> user = get_user_by_id("user_001", data)
        >>> print(user['name'])
        Sarah Johnson
    """
    for user in data.get('users', []):
        if user.get('user_id') == user_id:
            return user
    return None


def get_plan_by_id(plan_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Find an insurance plan by its plan_id.

    Args:
        plan_id: The unique plan identifier (e.g., "ppo_gold")
        data: The loaded data dictionary from load_all_data()

    Returns:
        dict: Insurance plan if found, None otherwise

    Example:
        >>> data = load_all_data()
        >>> plan = get_plan_by_id("ppo_gold", data)
        >>> print(plan['plan_name'])
        PPO Gold
    """
    for plan in data.get('plans', []):
        if plan.get('plan_id') == plan_id:
            return plan
    return None


def get_claims_for_user(user_id: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get all claims for a specific user.

    Args:
        user_id: The unique user identifier
        data: The loaded data dictionary from load_all_data()

    Returns:
        list: List of claims for the user (empty list if none found)

    Example:
        >>> data = load_all_data()
        >>> claims = get_claims_for_user("user_001", data)
        >>> print(f"User has {len(claims)} claims")
        User has 3 claims
    """
    return [
        claim for claim in data.get('claims', [])
        if claim.get('user_id') == user_id
    ]


def get_user_with_plan(user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Get a user profile with their full insurance plan details included.

    Args:
        user_id: The unique user identifier
        data: The loaded data dictionary from load_all_data()

    Returns:
        dict: User profile with embedded plan details, None if user not found

    Example:
        >>> data = load_all_data()
        >>> user = get_user_with_plan("user_001", data)
        >>> print(user['plan_details']['plan_name'])
        PPO Gold
    """
    user = get_user_by_id(user_id, data)
    if not user:
        return None

    plan = get_plan_by_id(user.get('plan_id'), data)

    # Create a copy of user with plan details embedded
    user_with_plan = user.copy()
    user_with_plan['plan_details'] = plan

    return user_with_plan


# Module-level storage for loaded data (set at application startup)
_LOADED_DATA: Optional[Dict[str, Any]] = None


def initialize_data():
    """
    Initialize the module-level data storage.
    Call this once at application startup.
    """
    global _LOADED_DATA
    _LOADED_DATA = load_all_data()


def get_data() -> Dict[str, Any]:
    """
    Get the loaded data from module-level storage.

    Returns:
        dict: The loaded data

    Raises:
        RuntimeError: If data hasn't been initialized yet
    """
    if _LOADED_DATA is None:
        raise RuntimeError(
            "Data not initialized. Call initialize_data() first."
        )
    return _LOADED_DATA
