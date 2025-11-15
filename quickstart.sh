#!/bin/bash

echo "🚀 MindSurf API Quick Start"
echo "============================"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL not found!"
    echo ""
    echo "Please install PostgreSQL first. Lightest options:"
    echo ""
    echo "1. Postgres.app (Recommended - ~50MB, no dependencies)"
    echo "   Download: https://postgresapp.com/downloads.html"
    echo "   Or run: curl -L -o ~/Downloads/Postgres.dmg https://github.com/PostgresApp/PostgresApp/releases/download/v2.8.1/Postgres-2.8.1-16.dmg"
    echo ""
    echo "2. Docker (if already installed)"
    echo "   docker run -d --name mindsurf-postgres -e POSTGRES_DB=mindsurf_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine"
    echo ""
    echo "See POSTGRESQL_SETUP.md for detailed instructions"
    exit 1
fi

# Install dependencies first
echo "📚 Installing dependencies..."
source $HOME/.local/bin/env
uv sync

# Test database connection
echo ""
echo "🔍 Testing database connection..."
if uv run python test_connection.py; then
    echo ""
    echo "🔄 Running migrations..."
    uv run python manage.py migrate
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "To start the server:"
    echo "  uv run python manage.py runserver"
    echo ""
    echo "To test the API:"
    echo "  uv run python test_api.py"
else
    echo ""
    echo "⚠️  Database connection failed"
    echo ""
    echo "Please:"
    echo "  1. Make sure PostgreSQL is running"
    echo "  2. Create the database: createdb mindsurf_db"
    echo "  3. Update .env with correct credentials"
    echo "  4. Run: uv run python test_connection.py"
    echo ""
    echo "See POSTGRESQL_SETUP.md for help"
    exit 1
fi
echo ""
