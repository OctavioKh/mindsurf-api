#!/bin/bash

echo "📦 PostgreSQL Installation Helper"
echo "=================================="
echo ""
echo "Choose installation method:"
echo ""
echo "1. Postgres.app (Recommended - ~50MB, easiest)"
echo "2. Docker (if you have Docker installed)"
echo "3. Show manual installation instructions"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📥 Downloading Postgres.app..."
        echo ""
        
        # Detect architecture
        if [[ $(uname -m) == 'arm64' ]]; then
            echo "Detected: Apple Silicon (M1/M2)"
            URL="https://github.com/PostgresApp/PostgresApp/releases/download/v2.8.1/Postgres-2.8.1-16-arm64.dmg"
        else
            echo "Detected: Intel Mac"
            URL="https://github.com/PostgresApp/PostgresApp/releases/download/v2.8.1/Postgres-2.8.1-16.dmg"
        fi
        
        curl -L -o ~/Downloads/Postgres.dmg "$URL"
        
        echo ""
        echo "✅ Downloaded to ~/Downloads/Postgres.dmg"
        echo ""
        echo "Next steps:"
        echo "  1. Open ~/Downloads/Postgres.dmg"
        echo "  2. Drag Postgres to Applications"
        echo "  3. Open Postgres.app"
        echo "  4. Click 'Initialize' button"
        echo "  5. Run: createdb mindsurf_db"
        echo ""
        echo "Then update .env file:"
        echo "  DB_USER=$(whoami)"
        echo "  DB_PASSWORD=(leave empty)"
        echo ""
        
        read -p "Open Downloads folder now? (y/n): " open_choice
        if [[ $open_choice == "y" ]]; then
            open ~/Downloads
        fi
        ;;
        
    2)
        echo ""
        echo "🐳 Setting up PostgreSQL with Docker..."
        echo ""
        
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker not found. Please install Docker first:"
            echo "   https://www.docker.com/products/docker-desktop"
            exit 1
        fi
        
        echo "Creating PostgreSQL container..."
        docker run -d \
          --name mindsurf-postgres \
          -e POSTGRES_DB=mindsurf_db \
          -e POSTGRES_USER=postgres \
          -e POSTGRES_PASSWORD=postgres \
          -p 5432:5432 \
          postgres:15-alpine
        
        echo ""
        echo "✅ PostgreSQL container created!"
        echo ""
        echo "Update your .env file:"
        echo "  DB_NAME=mindsurf_db"
        echo "  DB_USER=postgres"
        echo "  DB_PASSWORD=postgres"
        echo "  DB_HOST=localhost"
        echo "  DB_PORT=5432"
        echo ""
        echo "Container commands:"
        echo "  Start:  docker start mindsurf-postgres"
        echo "  Stop:   docker stop mindsurf-postgres"
        echo "  Logs:   docker logs mindsurf-postgres"
        echo "  Remove: docker rm -f mindsurf-postgres"
        echo ""
        ;;
        
    3)
        echo ""
        echo "📖 Manual Installation Options:"
        echo ""
        echo "Option 1: Postgres.app (~50MB)"
        echo "  Download: https://postgresapp.com/downloads.html"
        echo "  1. Drag to Applications"
        echo "  2. Open and click Initialize"
        echo "  3. Add to PATH: echo 'export PATH=\"/Applications/Postgres.app/Contents/Versions/latest/bin:\$PATH\"' >> ~/.zshrc"
        echo "  4. Restart terminal"
        echo "  5. Run: createdb mindsurf_db"
        echo ""
        echo "Option 2: Official Installer (~200MB)"
        echo "  Download: https://www.postgresql.org/download/macosx/"
        echo "  Follow installation wizard"
        echo "  Run: /Library/PostgreSQL/15/bin/createdb -U postgres mindsurf_db"
        echo ""
        echo "Option 3: Homebrew (if you have it)"
        echo "  brew install postgresql@15"
        echo "  brew services start postgresql@15"
        echo "  createdb mindsurf_db"
        echo ""
        echo "See POSTGRESQL_SETUP.md for detailed instructions"
        echo ""
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "After installation, test the connection:"
echo "  uv run python test_connection.py"
echo ""
