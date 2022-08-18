# LMX
This is the django development version of LMX Software.



## Initials

If you don't have the repo, open a shell and run

```
git clone https://github.com/TSAI-Labs/LMX.git
cd LMX
```

If you already have the repo in your home directory. Go inside it and make sure you have the latest.

```
cd LMX
git pull origin main
```

For required environment run (python3)

```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```



## Run Django App Locally:

Please create your .env file or collect it from Admin
Static and Media files are gitignored. Please add it locally.

```
- cd LMX
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py collectstatic
- python manage.py runserver
```
