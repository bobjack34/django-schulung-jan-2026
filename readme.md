# Django Kurs 1 Woche

## Installationshinweis 

.env Datei anlegen auf Basis von env_example.


## Tag 1

### Themen:
- Projekt aufsetzen
- Models anlegen
- Datenbank Migrationen
- Einführung Model-Manager

### Websites

- https://docs.djangoproject.com/en/6.0/
- https://djangopackages.org
- https://django-news.com/
- https://djangoheroes.friendlybytes.net


## Tag 2

### Themen:
- Views (Detail und Liste, generisch-klassenbasiert und funktionsbasiert)
- Queryset 
- Templates Einführung, Variablen, Tags
- Factory für Events
- Management Commando für das ERstellen von Events
- eigenes User-Model

### Websites
- https://djangoheroes.friendlybytes.net/create_project/user_model.html
- https://djangoheroes.friendlybytes.net/testdaten/create_testdata.html
- https://factoryboy.readthedocs.io/en/stable/orms.html
- https://faker.readthedocs.io/en/stable/providers.html 


## Tag 3

### Themen
- Django Extensions (show_urls, graph_models)
- statische Dateien
- Templates
- Django-Debug-Toolbar
- Django Forms, Crispy Forms
- CreateView, UpdateView, DeleteView
- Validierung
- Logging

### Websites
- https://dreampuf.github.io/GraphvizOnline/
- https://django-extensions.readthedocs.io
- https://djangoheroes.friendlybytes.net/working_with_forms/debug_toolbar.html
- https://djangoheroes.friendlybytes.net/working_with_forms/static_files.html
- https://djangoheroes.friendlybytes.net/working_with_forms/create_categories.html
- https://djangoheroes.friendlybytes.net/working_with_forms/working_with_forms.html
- https://djangoheroes.friendlybytes.net/working_with_forms/crispy_forms.html
- https://django-crispy-forms.readthedocs.io/en/latest/index.html

### Show Urls und graph_models
Django Extensions installieren. 

#### Alle Urls auflisten:

    python manage.py show_urls

#### Projekt als Graph anzeigen

    python manage.py graph_models -a

und hier rein pasten:

    https://dreampuf.github.io/GraphvizOnline/


## Tag 5

### Websites
- https://djangoheroes.friendlybytes.net/organisation/organize_settings.html#django-environ
- https://django-environ.readthedocs.io/en/latest/install.html
- https://djangoheroes.friendlybytes.net/profiwissen/whitenoise.html#index-0
- https://djangoheroes.friendlybytes.net/working_with_forms/static_files.html#statische-dateien-deployen
- https://www.django-rest-framework.org
- ein besserer Token für Django Restframework:
- https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Aus Gründen der bessseren Verständlichkeit wurde die .env-Datei und das per collectstatic generierte Verzeichnis "staticfiles"
nicht in die .gitignore übernommen.