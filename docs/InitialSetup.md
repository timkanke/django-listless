# New Project setup

Initial repo setup

## Create directory

```
cd {project_name}
git init
```

## Set python version

```
pyenv local {major.minor}
```

## Create virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

## Add packages

```
pip install pycodestyle pytest
pip freeze > requirements.txt
```

## Setup gitignore

```
echo .venv >> .gitignore
git add .python-version .gitignore requirements.txt
```

## Commit

```
git commit -m "Initialize {project_name}"
```

## Create Django project

```
pip install django
pip freeze > requirements.txt

mkdir src
cd src

django-admin startproject {projectname} . # Note the dot at the end

python manage.py startapp {appname}
```

Note: projectname should be the same as the repo name

Add "appname" to your INSTALLED_APPS, also set static and media paths in projectname/settings.py

```
INSTALLED_APPS = [
    ...
    'appname',
]

...

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Run in src directory

```
python manage.py collectstatic
python manage.py migrate
```

Create admin

```
python manage.py createsuperuser
```

Create templates directory for HTML files

```
mkdir {appname}/templates
```

In project root, add to .gitignore

```
printf ".env\n.coverage\nstatic/*\n__pycache__\n*.sqlite3" >> .gitignore
```
