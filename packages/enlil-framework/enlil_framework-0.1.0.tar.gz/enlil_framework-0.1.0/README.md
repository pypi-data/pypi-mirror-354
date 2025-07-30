# Enlil

A Python web framework built on FastAPI, designed for modular, maintainable, and production-grade applications.

## Features

- FastAPI-compatible
- Modular app design
- Built-in ORM with Tortoise
- Jinja2 templating
- Dependency Injection
- CLI tools for scaffolding

## Project Setup

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd enlil
poetry install
```

3. Create and activate virtual environment (choose one method):

   a. Using Poetry's default virtual environment:
   ```bash
   poetry shell
   ```

   b. Using a local .venv directory:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   poetry install
   ```

Note: All Poetry commands (`poetry run enlil ...`) will work regardless of which virtual environment method you choose.

## CLI Commands

### Create a New App
```bash
poetry run enlil startapp <app_name>
```
This creates a new app with the following structure:
- models.py
- views/api.py and views/ui.py
- serializers/input.py, output.py, data_objects.py
- services.py, utils.py
- routers.py
- tests/ directory

### Generate CRUD Endpoints
```bash
poetry run enlil makecrud <model_name> <field1>:<type1> <field2>:<type2> --app <app_name>
```
Example:
```bash
poetry run enlil makecrud Post title:str content:str is_published:bool --app blog
```

### Run Development Server
```bash
poetry run enlil runserver
```
Options:
- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to bind to (default: 8000)

## Database Management

### Initial Setup (Run Once)
```bash
# Initialize database and create first migration
poetry run aerich init-db
```

### When Making Model Changes
1. After modifying your models (adding/removing fields, etc.):
```bash
# Create a new migration file
poetry run aerich migrate

# Apply the migration to update database
poetry run aerich upgrade
```

Example workflow:
```python
# 1. You modify your model (e.g., add a new field)
class Post(models.Model):
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    is_published = fields.BooleanField(default=False)
    # New field added:
    author = fields.CharField(max_length=100)  # <-- New field

# 2. Create migration
poetry run aerich migrate

# 3. Apply migration
poetry run aerich upgrade
```

Note: Always create and apply migrations after any model changes to keep your database schema in sync.

## Testing

Run all tests:
```bash
poetry run pytest
```

Run specific test file:
```bash
poetry run pytest src/<app_name>/tests/test_api.py -v
```

## Project Structure

```
src/
├── config.py              # Environment-based settings
├── core/                  # Core framework components
├── enlil/                  # Framework package
│   ├── cli.py             # CLI commands
│   ├── dependencies.py    # Dependency injection
│   ├── models.py         # Base models
│   ├── services.py       # Base services
│   ├── settings.py       # Settings management
│   ├── scaffolds/       # Project templates
│   └── tests/           # Framework tests
├── template_app/          # App template for scaffolding
├── apps/                  # Application modules
│   └── <your_app>/       # Your application code
│       ├── models.py
│       ├── views/
│       ├── serializers/
│       ├── services.py
│       └── tests/
├── main.py               # FastAPI application entry point
├── migrations/           # Database migrations
└── templates/           # Global Jinja2 templates
```

## Environment Variables

Create a `.env` file in the project root:
```
DEBUG=true
DATABASE_URL=sqlite://db.sqlite3
SECRET_KEY=your-secret-key
TEMPLATE_DIR=templates
```

## Development

1. Create a new app using `enlil startapp`
2. Define your models in `models.py`
3. Create views in `views/api.py` and `views/ui.py`
4. Define serializers in `serializers/`
5. Add business logic in `services.py`
6. Write tests in `tests/`
7. Run migrations to create database tables
8. Start the development server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[Your License Here]