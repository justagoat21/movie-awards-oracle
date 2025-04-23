
import re
from typing import Dict, List, Any, Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> bool:
    """Check if password meets minimum security requirements"""
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def format_user_nomination(nomination: Dict[str, Any]) -> str:
    """Format user nomination for display"""
    return f"{nomination.get('staff_name', 'Unknown')} - {nomination.get('movie_title', 'Unknown')} ({nomination.get('category', 'Unknown')})"

def format_staff_stats(stats: Dict[str, Any]) -> str:
    """Format staff statistics for display"""
    name = stats.get('name', 'Unknown')
    role = stats.get('role', 'Staff')
    nominations = stats.get('nomination_count', 0)
    oscars = stats.get('oscar_count', 0)
    return f"{name} ({role}): {nominations} nomination(s), {oscars} Oscar(s)"

def format_dream_team(team: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """Format dream team for display"""
    formatted = {}
    for role, person in team.items():
        formatted[role] = f"{person.get('name', 'Unknown')}: {person.get('oscar_count', 0)} Oscar(s)"
    return formatted

def format_top_items(items: List[Dict[str, Any]], title_key: str, count_key: str) -> List[str]:
    """Format top items (movies, countries, companies) for display"""
    return [f"{item.get(title_key, 'Unknown')}: {item.get(count_key, 0)}" for item in items]
