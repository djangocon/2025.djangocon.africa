# 2025.djangocon.africa
Website for DjangoCon Africa 2025

## Installation

To get up and running do the following:


1. Create a virtual environment.

```
python3.12 -m venv venv
```

Of course there are many ways to make a virtual environment. We are following the simplest method. If you like to use a different thing then go for it.

2. Install the requirements

Activate your virtual env

```
source venv/bin/activate
```

Then install the requirements:

```
pip install -r requirements.txt
```

3. Install npm dependencies

```
npm install
```

## Running the application on development

1. set the database locally as you like. using docker is the easiet way.
   those are some configuration sample :

   dev_db/docker-compose.yaml
    services:
        postgres:
        image: postgres:12
        environment:
        - POSTGRES_USER=""
        - POSTGRES_PASSWORD=""
        - POSTGRES_DB=db
        volumes:
        - ./gitignore/postgresql:/var/lib/postgresql/data
        - ./docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
        ports:
        - "5432:5432"%

    docker-entrypoint-initdb.d/create-db-test.sql :
        CREATE DATABASE test_db;
        grant all privileges on database test_db to pguser;
        -- ALTER USER user WITH SUPERUSER;%

2. Run the server

    Before using the runserver command, you need to load up some environmental variables. `.env_example` has some sensible defaults that just work in a dev environment:

    ```
    source .env_example
    python manage.py runserver
    ```


## Working with tailwind

You can learn about tailwind [here](https://tailwindcss.com/docs/installation). It is installed in this project using the standard "Tailwind CLI" installation.

The Tailwind CLI is used to build a css file. The build process takes in a few inputs:

1. HTML files: It will look at what tailwind classes you are referencing inside your html files. The final built css file will contain only those css classes that are actually being used.

2. An input CSS file. In our case we are using `website/static/src/tailwind_input.css`. This file contains any extra classes or default styles.

3. `tailwind.config.js`. This file contains exra configuration. For example if you want to create new colours or define a primary colour or anything like that it will go in there.

The output of the tailwind build is: `website/static/dist/tailwind_final.css`. You can see that we reference this file in our base template, `website/templates/website/_base.html`

### Building the tailwind css file

There are 2 commands you can use:

This builds the final CSS file:

```
npm run tailwind
```

Sometimes if you are doing a lot of editing of multiple files (html files as well as the other build inputs), then it is useful to watch for file changes and rerun the build automatically.

In this case use:

```
npm run tailwind_watch
```

## Translations for the website
Django internationalisation has been enabled for this website and we support English and French for now. To ensure that every page supports translations please follow the following guidelines in the templates:
1. Include `{% load i18n %}` at the top of the file to support translations.
2. For one line sentences use the `{% translate "Some one line sentence or heading" %}` tag and put the text in the double qoutes.
3. For paragraphs, use the `{% blocktranslate %} A paragraph of text {% endblocktranslate %}`. The `{% blocktranslate %}` tag does not support other tags such as `{% static %}` inside it so make sure to close it before other template tags and then open another one. However is supports variable tags such as `{{ number }}` inside it.
4. To generate messages for translations, use the `django-admin makemessages -l fr` and all the files with translate tags will be added to `locale/fr/LC_MESSAGES/django.po`. This is the file translators should edit to support translation into French.
5. To compile messages use the `django-admin compilemessages` command. For more information on Django translations read the Django documentation
https://docs.djangoproject.com/en/5.1/topics/i18n/translation/.

## wagtail configuration
We use wagtail for to manage articles :
1. Local Configuration : ... (to be added)

## Steps for charging grant application  from csv file
1.  After exporting the google sheets grants application as a csv, rename the header with following names:
    Timestamp,Column1,FullName,Email,Profession,CountryOrigin,CityTravelingFrom,YourNeed,AboutYourself,TypeofGrant,Budget

2.  Upload the csv file in /media/
3.  Use the command `python manage.py preprocess /media/grants.csv  media/grants_treated.csv`
4.  After  content verification, use the command `python manage.py  import_file_grants   media/grants_treated.csv` to record data to the databases
5.  To revert in case of error . use the command `python manage.py import_file_grants media/grants_treated --revert`
