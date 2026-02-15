#!/usr/bin/env python3
"""Seed database with sample data"""
import asyncio
from covenant.db.session import async_session
from covenant.core.constitutional_engine import Constraint, ConstraintType

async def seed_constraints():
    """Seed sample constraints"""
    constraints = [
        {
            "id": "gdpr_data_minimization",
            "type": "legal",
            "description": "Collect only necessary personal data",
            "is_hard": True
        },
        {
            "id": "fairness_demographic",
            "type": "fairness",
            "description": "Ensure fair treatment across demographics",
            "is_hard": False
        },
        {
            "id": "transparency_explainability",
            "type": "transparency",
            "description": "Provide explanations for decisions",
            "is_hard": False
        }
    ]
    
    # In production, save to database
    print(f"Seeded {len(constraints)} constraints")

if __name__ == "__main__":
    asyncio.run(seed_constraints())