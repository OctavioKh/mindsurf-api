#!/usr/bin/env python3
"""
Test PostgreSQL database connection
Run this after setting up PostgreSQL and configuring .env
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection"""
    print("🔍 Testing PostgreSQL connection...\n")
    
    # Get connection details
    db_name = os.getenv('DB_NAME', 'mindsurf_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    print(f"Database: {db_name}")
    print(f"User: {db_user}")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Password: {'(set)' if db_password else '(empty)'}\n")
    
    try:
        import psycopg2
        
        print("Attempting connection...")
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print("\n✅ Connection successful!\n")
        print(f"PostgreSQL version:\n{version}\n")
        
        cursor.close()
        conn.close()
        
        print("Next steps:")
        print("  1. Run migrations: uv run python manage.py migrate")
        print("  2. Start server: uv run python manage.py runserver")
        print("  3. Test API: uv run python test_api.py")
        
        return True
        
    except ImportError:
        print("\n❌ psycopg2 not installed")
        print("Run: uv sync")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}\n")
        print("Troubleshooting:")
        print("  1. Is PostgreSQL running?")
        print("     - Postgres.app: Open the app")
        print("     - Docker: docker start mindsurf-postgres")
        print("     - Check: ps aux | grep postgres")
        print()
        print("  2. Does the database exist?")
        print("     - Create it: createdb mindsurf_db")
        print()
        print("  3. Are credentials correct?")
        print("     - Check .env file")
        print("     - Postgres.app: use your Mac username, no password")
        print()
        print("  4. Check connection details:")
        print(f"     psql -U {db_user} -d {db_name} -h {db_host} -p {db_port}")
        print()
        print("See POSTGRESQL_SETUP.md for detailed instructions")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
