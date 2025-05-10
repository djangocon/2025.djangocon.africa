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

## Running the application

1. Get the development database up and running:

See: dev_db/README.md

Remember to run the migrations!

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