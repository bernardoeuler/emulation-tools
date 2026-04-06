#!/bin/bash

set -e

DATABASE_USER="${DATABASE_USER:-postgres}"
DATABASE_NAME="${DATABASE_NAME:-emulation_tools}"

echo "Initializing PostgreSQL database..."

psql -U "$DATABASE_USER" -c "CREATE DATABASE $DATABASE_NAME;"

echo "Database initialization complete"
