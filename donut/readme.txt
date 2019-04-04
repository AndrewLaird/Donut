Database entries are made in the models.py file
when you change that file and want to update the database to accomodate for them you have to:
python3 manage.py makemigrations donut
python3 manage.py migrate donut

#donut is the name of the app
