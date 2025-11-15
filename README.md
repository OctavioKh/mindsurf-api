# MindSurf API

A Django REST API that analyzes conversation transcripts and generates structured reports with session detection, key moments identification, and emotion analysis.

## Quick Start

```bash
# 1. Install PostgreSQL 
./install_postgres.sh  
# OR
docker run -d --name mindsurf-postgres -e POSTGRES_DB=mindsurf_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine

# 2. Setup project
./quickstart.sh

# 3. Start server
uv run python manage.py runserver

# 4. Test API
uv run python test_api.py
```

## Tech Stack

- Python 3.14
- Django 5.2.8
- Django REST Framework
- PostgreSQL
- uv (package manager)

## API Endpoint

### POST /api/analyze/

**Request Body:**
```json
{
  "transcript": [
    {
      "timestamp": "2025-10-27T10:00:00Z",
      "role": "assistant",
      "text": "Hola! Me gustaría saber cómo te sientes hoy o si hay algo en particular que te gustaria platicar?",
    },
    {
      "timestamp": "2025-10-27T10:00:05Z",
      "role": "user",
      "text": "Claro me gustaría contarte sobre..."
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "analysis_summary": {
    "session_count": 1,
    "key_moments": {
      "questions_asked": 1,
      "actions_identified": 0
    },
    "emotion_analysis_results": [
         {"emotion": "positive"},
         {"emotion":"negative"}
    ]
  }
}
```

## Analysis Features

- **Session Detection**: Identifies conversation sessions based on >10 minute silence gaps
- **Question Counting**: Counts messages containing "?"
- **Action Detection**: Identifies keywords: necesito, podrias, ayudame, tarea, hacer
- **Emotion Analysis**: Simulates AI emotion detection on text blocks >100 characters

## Installation

### PostgreSQL Setup

**Option 1: Postgres.app**
1. Download from https://postgresapp.com/downloads.html
2. Drag to Applications, open, click "Initialize"
3. Run: `createdb mindsurf_db`

**Option 2: Docker**
```bash
docker run -d --name mindsurf-postgres \
  -e POSTGRES_DB=mindsurf_db \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 postgres:15-alpine
```


### Project Setup

1. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your db credentials
```

For Postgres.app:
```env
DB_USER=your_mac_username 
DB_PASSWORD=
```

For Docker:
```env
DB_USER=postgres
DB_PASSWORD=postgres
```

2. **Install dependencies:**
```bash
uv sync
```

3. **Run migrations:**
```bash
uv run python manage.py migrate
```

4. **Start server:**
```bash
uv run python manage.py runserver
```

## Testing

```bash
# Test database connection
uv run python test_connection.py

# Test API
uv run python test_api.py

# Test with curl
curl -X POST http://localhost:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"transcript":[{"timestamp":"2025-10-27T10:00:00Z","role":"user","text":"Hello!"}]}'
```

## Admin Panel

```bash
# Create superuser
uv run python manage.py createsuperuser

# Access at http://localhost:8000/admin/
```

## Database Access

### Connect to Database

```bash
# PostgreSQL shell
psql mindsurf_db

# Django shell
uv run python manage.py dbshell
```

### Useful Queries

```sql
-- View all tables
\dt

-- See all conversations (latest first)
SELECT id, created_at FROM analyzer_conversation ORDER BY created_at DESC LIMIT 5;

-- See messages from the latest conversation
SELECT role, text, timestamp 
FROM analyzer_message 
WHERE conversation_id = (SELECT MAX(id) FROM analyzer_conversation)
ORDER BY timestamp;

-- See analysis report for the latest conversation
SELECT 
  conversation_id,
  session_count,
  questions_asked,
  actions_identified,
  emotion_results
FROM analyzer_analysisreport 
WHERE conversation_id = (SELECT MAX(id) FROM analyzer_conversation);

-- Count total conversations
SELECT COUNT(*) FROM analyzer_conversation;

-- See all analysis summaries
SELECT 
  c.id,
  c.created_at,
  ar.session_count,
  ar.questions_asked,
  ar.actions_identified
FROM analyzer_conversation c
JOIN analyzer_analysisreport ar ON c.id = ar.conversation_id
ORDER BY c.created_at DESC;

-- Exit psql
\q
```

## Customization

Edit `analyzer/analysis.py`:

```python
class TranscriptAnalyzer:
    SESSION_TIMEOUT_MINUTES = 10  # Session timeout
    ACTION_KEYWORDS = [...]        # Action keywords
    EMOTION_BLOCK_MIN_LENGTH = 100 # Analysis threshold
```

## Project Structure

```
mindsurf-api/
├── analyzer/             # Main application
│   ├── models.py         # Database models
│   ├── views.py          # API endpoint
│   ├── analysis.py       # Analysis logic
│   ├── serializers.py    # Request/response validation
│   └── admin.py          # Admin panel config
├── config/               # Django settings
│   ├── settings.py       # Configuration
│   └── urls.py           # URL routing
├── .env                  # Environment variables
├── manage.py             # Django management
├── test_api.py           # API test script
└── test_connection.py    # Database test script
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Start PostgreSQL (open Postgres.app or `docker start mindsurf-postgres`) |
| psql not found | Add Postgres.app to PATH: `export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"` |

## Commands Reference

```bash
# Development
uv run python manage.py runserver          # Start server
uv run python manage.py migrate            # Run migrations
uv run python manage.py makemigrations     # Create migrations
uv run python manage.py createsuperuser    # Create admin user
uv run python manage.py shell              # Django shell

# Database
createdb mindsurf_db                       # Create database
psql mindsurf_db                           # Connect to database
uv run python test_connection.py           # Test connection

# Testing
uv run python test_api.py                  # Test API
curl -X POST http://localhost:8000/api/analyze/ -H "Content-Type: application/json" -d '{...}'


```

## Design Decisions

### Que compromisos hiciste?

**Simular AI en lugar de analysis real de emociones, debería conectarse a un modelo ya sea local o integrarlo a modelos externos**  

**Procesamiento síncrono, debería ser async para que pueda permitir el flujo adecuado de las operaciones**  

**Relaciona palabras sencillas como necesito, ayudame, y no tiene contexto**  

**Las sesiones deberian de llevar analysis semantico también**  


### Mejoras con mas tiempo

**1. Integraciones reales**  

**2. Procesos internos**  

**3. Mejor detección de acciones con ML**  

**5. Mejores pruebas unitarias**  


### A) Technical Validation (Verify the Code Works)

Check if the analysis is working correctly:

**1. Check the Database**
```sql
-- Connect to database
psql mindsurf_db

-- See the latest analysis
SELECT 
  conversation_id,
  session_count,
  questions_asked,
  actions_identified,
  emotion_results
FROM analyzer_analysisreport 
WHERE conversation_id = (SELECT MAX(id) FROM analyzer_conversation);

-- See the actual messages
SELECT role, text, timestamp 
FROM analyzer_message 
WHERE conversation_id = (SELECT MAX(id) FROM analyzer_conversation)
ORDER BY timestamp;
```

**2. Manual Verification**
- Count the "?" in messages yourself - should match `questions_asked`
- Look for keywords (need, help, could, task, do) - should match `actions_identified`
- Check timestamps - gaps >10 minutes should create new sessions

**3. Use the Admin Panel**
```bash
# Access at http://localhost:8000/admin/
# Login: admin / admin123
```
Browse through conversations, messages, and reports visually.

**4. Compare Multiple Runs**
Send the same transcript twice - results should be consistent (emotions will differ since they're random).

**5. Test Edge Cases**
```bash
# Test with no questions
curl -X POST http://localhost:8000/api/analyze/ -H "Content-Type: application/json" \
  -d '{"transcript":[{"timestamp":"2025-11-14T10:00:00Z","role":"user","text":"Hello there"}]}'
# Should return questions_asked: 0
```

### B) Review and Rate Analysis Results (For Evaluators)

If you want to study the analysis and provide feedback:

**1. View Analysis in Admin Panel**
```bash
# Access at http://localhost:8000/admin/
# Login: admin / admin123
```
- Click on **Analysis Reports** to see all analyses
- Click on a specific report to view details
- Read the conversation messages
- Review the analysis results

**2. Query for Review**
```sql
-- Get conversation with analysis for review
SELECT 
  c.id,
  c.created_at,
  ar.session_count,
  ar.questions_asked,
  ar.actions_identified,
  ar.emotion_results
FROM analyzer_conversation c
JOIN analyzer_analysisreport ar ON c.id = ar.conversation_id
WHERE c.id = 1;  -- Change to the conversation you want to review

-- Read the messages
SELECT role, text, timestamp 
FROM analyzer_message 
WHERE conversation_id = 1  -- Change to the conversation you want to review
ORDER BY timestamp;
```

**3. Add Your Review/Rating (Optional Enhancement)**

You can extend the system to add reviews:

```sql
-- Create a review table
CREATE TABLE IF NOT EXISTS analysis_review (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES analyzer_conversation(id),
    reviewer_name VARCHAR(100),
    accuracy_rating INTEGER CHECK (accuracy_rating >= 1 AND accuracy_rating <= 5),
    comments TEXT,
    reviewed_at TIMESTAMP DEFAULT NOW()
);

-- Add your review
INSERT INTO analysis_review (conversation_id, reviewer_name, accuracy_rating, comments)
VALUES (1, 'Jane Doe', 4, 'Session detection is accurate. Action detection could be improved.');

-- View all reviews
SELECT 
  ar.conversation_id,
  ar.reviewer_name,
  ar.accuracy_rating,
  ar.comments,
  ar.reviewed_at
FROM analysis_review ar
ORDER BY ar.reviewed_at DESC;
```

**4. Export for External Review**
```sql
-- Export conversation with analysis as JSON
SELECT json_build_object(
  'conversation_id', c.id,
  'created_at', c.created_at,
  'messages', (
    SELECT json_agg(json_build_object('role', role, 'text', text, 'timestamp', timestamp))
    FROM analyzer_message WHERE conversation_id = c.id ORDER BY timestamp
  ),
  'analysis', json_build_object(
    'session_count', ar.session_count,
    'questions_asked', ar.questions_asked,
    'actions_identified', ar.actions_identified,
    'emotions', ar.emotion_results
  )
) as review_package
FROM analyzer_conversation c
JOIN analyzer_analysisreport ar ON c.id = ar.conversation_id
WHERE c.id = 1;
```

This gives you a complete package to share with reviewers or save for documentation.

## Support

- Test connection: `uv run python test_connection.py`
- Test API: `uv run python test_api.py`
- Check logs: Server output or `docker logs mindsurf-postgres`


