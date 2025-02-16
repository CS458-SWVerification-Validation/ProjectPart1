# ProjectPart1

This is the Flask App for CS458 Project.

# Getting Started

## Windows

> [!WARNING]
> If Visual Studio Code is the used IDE, it\
> is advised to use CMD instead of PowerShell\
> since if the required permissions are not given\
> to PowerShell it will not run the scripts that are \
> needed for the next steps.\

### Cloning Repository

```bash
git clone https://github.com/CS458-SWVerification-Validation/ProjectPart1.git
```

### Flask Environment Setup

```bash
cd ProjectPart1
python -m venv env
.\env\Scripts\activate
```

If '(env)' is seen at the start of the command line\
the first part of the setup is complete.\

```bash
pip install -r requirements.txt
```

This command installs all the necessary dependencies\
for the project to run. After the installation only\
database setup remains.\

### Database Setup

```bash
flask db init
flask db migrate
flask db upgrade
```

This command block will initialize the migration repository,\
detect the changes made on the SQLAlchemy models and run the\
latest migration scripts onto the database.

### Running the Flask App

```bash
python app.py
```

Now the Flask application would run on [http://127.0.0.1:8003](http://127.0.0.1:8003)
