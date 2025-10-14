# Mock Data Documentation

This directory contains mock insurance data used to demonstrate LangGraph concepts without requiring real APIs or databases.

## Files

- **user_profiles.json** - User profiles with insurance information
- **insurance_plans.json** - Insurance plan types and coverage details
- **claims_data.json** - Historical claims records
- **loader.py** - Python module for loading and querying the data

## Data Schemas

### User Profile Schema (`user_profiles.json`)

Each user has the following fields:

```json
{
  "user_id": "string",           // Unique identifier (e.g., "user_001")
  "name": "string",              // Full name
  "age": number,                 // Age in years
  "plan_id": "string",           // References insurance_plans.json
  "member_since": "YYYY-MM-DD",  // Enrollment date
  "deductible_annual": number,   // Annual deductible amount ($)
  "deductible_met": number,      // Amount of deductible already met ($)
  "out_of_pocket_max": number,   // Maximum out-of-pocket spending ($)
  "out_of_pocket_spent": number, // Amount spent toward max ($)
  "dependents": number,          // Number of dependents on plan
  "notes": "string"              // Additional context
}
```

**Example:**
- Sarah Johnson (user_001) - PPO Gold plan, family with 2 dependents, partial deductible met
- Michael Chen (user_002) - HMO Silver, individual, new year (no deductible met)
- Emily Rodriguez (user_003) - EPO Bronze, high deductible fully met

### Insurance Plan Schema (`insurance_plans.json`)

Each plan has the following structure:

```json
{
  "plan_id": "string",            // Unique identifier (e.g., "ppo_gold")
  "plan_name": "string",          // Display name (e.g., "PPO Gold")
  "plan_type": "string",          // PPO, HMO, or EPO
  "monthly_premium": number,      // Monthly cost ($)
  "description": "string",        // Plan overview
  "coverage": {
    "primary_care": {             // Coverage for primary care visits
      "in_network": {
        "copay": number,          // Fixed payment amount ($)
        "coverage_percent": number, // Percentage covered after copay
        "notes": "string"
      },
      "out_of_network": {
        // Same structure
      }
    },
    "specialist": { ... },        // Specialist visit coverage
    "emergency_room": { ... },    // ER coverage
    "urgent_care": { ... },       // Urgent care coverage
    "prescription_drugs": {       // Medication coverage by tier
      "generic": { ... },
      "brand_name": { ... },
      "specialty": { ... }
    },
    "preventive_care": { ... },   // Annual physicals, screenings
    "mental_health": { ... }      // Mental health services
  }
}
```

**Plan Types:**
- **PPO (Preferred Provider Organization)**: Broad network, no referrals needed, covers out-of-network
- **HMO (Health Maintenance Organization)**: Requires PCP selection and referrals, in-network only
- **EPO (Exclusive Provider Organization)**: In-network only, no referrals needed

### Claims Schema (`claims_data.json`)

Each claim record includes:

```json
{
  "claim_id": "string",             // Unique identifier (e.g., "CLM-2024-001")
  "user_id": "string",              // References user_profiles.json
  "service_date": "YYYY-MM-DD",     // Date service was provided
  "service_type": "string",         // Type of medical service
  "provider_name": "string",        // Healthcare provider name
  "provider_network": "string",     // "in_network" or "out_of_network"
  "claim_status": "string",         // "Approved", "Pending", or "Denied"
  "billed_amount": number,          // Provider's charge ($)
  "insurance_paid": number,         // Amount insurance covered ($)
  "patient_responsibility": number, // Amount patient owes ($)
  "applied_to_deductible": number,  // Amount applied to deductible ($)
  "notes": "string"                 // Additional details
}
```

**Claim Statuses:**
- **Approved**: Claim processed and paid
- **Pending**: Under review
- **Denied**: Not covered by plan

## Usage Examples

### Loading All Data

```python
from app.data.loader import load_all_data

# Load all data at once
data = load_all_data()

print(f"Users: {len(data['users'])}")
print(f"Plans: {len(data['plans'])}")
print(f"Claims: {len(data['claims'])}")
```

### Querying Specific User

```python
from app.data.loader import get_user_by_id, get_data

data = get_data()
user = get_user_by_id("user_001", data)

print(f"Name: {user['name']}")
print(f"Plan: {user['plan_id']}")
print(f"Deductible met: ${user['deductible_met']} / ${user['deductible_annual']}")
```

### Getting User with Plan Details

```python
from app.data.loader import get_user_with_plan, get_data

data = get_data()
user = get_user_with_plan("user_001", data)

print(f"Plan Name: {user['plan_details']['plan_name']}")
print(f"Plan Type: {user['plan_details']['plan_type']}")
print(f"Monthly Premium: ${user['plan_details']['monthly_premium']}")
```

### Getting Claims for User

```python
from app.data.loader import get_claims_for_user, get_data

data = get_data()
claims = get_claims_for_user("user_001", data)

for claim in claims:
    print(f"{claim['claim_id']}: {claim['service_type']} - {claim['claim_status']}")
```

## Data Design Notes

### Diversity
The mock data includes varied scenarios:
- Different plan types (PPO, HMO, EPO)
- Various deductible statuses (none met, partially met, fully met)
- Mix of claim statuses and types
- Different family structures (individual, couples, families)

### Realism
Data reflects real-world insurance scenarios:
- Realistic dollar amounts
- Common coverage categories
- Typical copay and coinsurance structures
- Real service types and terminology

### Learning Focus
Data is designed for educational purposes:
- Simple enough to understand quickly
- Complex enough to demonstrate real patterns
- Includes edge cases (denied claims, out-of-network)
- Shows how deductibles and out-of-pocket maximums work

## Future Enhancements

For future versions, consider:
- Adding more users with diverse scenarios
- Including dental and vision coverage
- Adding prescription history
- Including provider network directories
- Adding prior authorization status
