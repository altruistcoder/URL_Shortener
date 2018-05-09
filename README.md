# SHORTISH

Shortish is a URL shortening webapp which is used to shorten any url.

## Instructions

1. Get the source code on your pc via git.

```
  git clone https://github.com/altruistcoder/URL_Shortener
```
2. Create a virtual environment.

```
  virtualenv venv
```
3. Move the contents of cloned repository inside virtual environment folder.

4. Activate the virtual environment (You have to activate it everytime you are working on project).

```
  For mac users:

    source venv/bin/activate  

  For windows users:

    .\Scripts\activate
```

5. Now, install python dependencies.

```
  pip install -r requirements.txt
```
6. Now, navigate to the directory containing manage.py file.

7. Run following command:

```
  python manage.py migrate
  python manage.py runserver
```
8. That's it, shortish is ready. You can run it at [127.0.0.1:8000/](127.0.0.1:8000/).
