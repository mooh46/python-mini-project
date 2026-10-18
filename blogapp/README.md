# Personal Blog (Django)

A simple personal blog I built with Django. Anyone can read the articles, and I can log in as the admin to add, edit and delete them. There is no database. Every article is saved as its own JSON file.

## What it does

**Guest side (anyone can open)**
- Home page that lists all the articles
- Article page that shows one article with its date

**Admin side (login needed)**
- Login page with a username and password
- Dashboard that lists every article, with buttons to add, edit and delete
- Add article page
- Edit article page (the form comes pre-filled and saves over the same file)
- Logout

If you are not logged in, the admin pages send you to the login page.

## How it works

- **Storage:** each article is a JSON file in `blogapp/storedFiles/` holding the title, date and content. The file name is the slugified title plus a short random id, like `my-first-post-a3f9c21b.json`.
- **Forms:** the add/edit page and the login page use Django `forms.Form` classes in `forms.py`.
- **Login:** the typed username and password are compared with a username and password written in `views.py` (hardcoded, which the project allows). If they match, a note is saved in the session. An `admin_required` decorator checks for that note before running any admin view.
- **File names from the URL:** the edit and delete views only keep the last part of the name they receive (`Path(name).name`). This stops someone typing something like `..\..\file.py` into the address bar to reach files outside `storedFiles`.
- **Pages:** templates share one base template, and the styling is in `blogapp/static/blogapp/style.css`. No JavaScript.

## Project layout

```
Project1/            Django project settings and main urls
blogapp/
  forms.py           AddArticle and Login forms
  views.py           all the views
  urls.py
  storedFiles/       the article JSON files
  static/blogapp/    style.css
  templates/         the HTML pages
manage.py
```

## Running it

1. Clone the project and open the folder.
2. Install what it needs:
   ```
   pip install django
   ```
3. Make sure the folder `blogapp/storedFiles/` exists. Python does not create folders by itself.
4. Set up the session table:
   ```
   python manage.py migrate
   ```
5. Start the server:
   ```
   python manage.py runserver
   ```
6. Open `http://127.0.0.1:8000/blog/` in your browser.

## Limits

- There is only one admin account, and its username and password are written straight into `views.py` in plain text.
- Articles are files, not database rows. That is fine for a small blog but not for lots of articles or many writers.
- Delete is a normal link, so there is no "are you sure?" step.
- No comments, search or tags.
- It is a learning project and not ready to put on a real server.

## What I practiced

Templating, forms, reading and writing files, JSON, URL routing with path converters, and sessions for login.

For Roadmaps.sh
this is the url: https://roadmap.sh/projects/blogging-platform-api also this: https://roadmap.sh/projects/personal-blog