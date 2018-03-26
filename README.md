# Django Togo

A management command to convert Django templates to Go templates. This does:

- Remove all the `{% load %}` tags
- Transform all the `{% static "foo/bar" %}` tags in  `/static/foo/bar`
- Remove all the `{% block foo %}{% endblock %}` tags
- Transform all the `{% include "foo.html" %}` into `{{ template  "foo.html"  . }}` 
- Change the `{{ variable }}` to `{{ .variable }}`

## Install

Add `"togo",` to installed apps

## Run

```
python3 manage.py togo destination_folder
```

This will copy and transform all the files in `templates` to the destination directory.

## Options

Support for [Hugo](https://gohugo.io/) static sites generator format:

```
python3 manage.py togo destination_folder -h
```