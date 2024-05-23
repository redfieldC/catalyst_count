## Project Setup Instructions

Follow these instructions to set up the project in your local development environment.

### Step 1: Navigate to the Project Directory

Open your terminal and navigate to the project directory:

```bash
cd path/to/your/project
```

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate project dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS and Linux:

  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Project Dependencies

Install the necessary project dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

Ensure that PostgreSQL is installed and running on your machine. Set up the PostgreSQL database as follows:

1. Create a new PostgreSQL database and user.

2. Update the database settings in your `settings.py` file:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

### Final Steps

Start the development server to verify the setup:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.

---

