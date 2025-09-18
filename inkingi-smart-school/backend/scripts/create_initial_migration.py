#!/usr/bin/env python3
"""
Create initial database migration
"""
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alembic.config import Config
from alembic import command

def create_initial_migration():
    """Create initial migration"""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message="Initial migration")

if __name__ == "__main__":
    create_initial_migration()