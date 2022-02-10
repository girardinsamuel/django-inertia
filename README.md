# django-inertia

Django server-side new adapter for [Inertia.js](https://inertiajs.com).


## Getting Started

### Install the package

`pip install django-inertia`

### Configure your project

1. Add the package `django_inertia` to your applications (if you want to use the template tag else
it's not necessary).

2. Add `InertiaMiddleware` to your project middlewares:

```python
MIDDLEWARES = [
  #...,
  "django_inertia.middleware.InertiaMiddleware",
]
```

### Creating responses

To create and inertia response you need to use `Inertia.render()` method:

```python
from django_inertia import Inertia

def event_detail(request, id):
    event = Event.objects.get(pk=id)
    props = {
        'event': {
            'id':event.id,
            'title': event.title,
            'start_date': event.start_date,
            'description': event.description
        }
    }
    return Inertia.render(request, "Event/Show", props)
```

### Loading data into your template

```html+django
{% load inertia_tags %}
<!DOCTYPE html>
<html  class="h-full bg-gray-200">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
    <script src="{{ STATIC_URL}}dist/app.js" defer></script>
    <link href="{{ STATIC_URL}}dist/app.css" rel="stylesheet" />
  </head>
  <body>
    {% inertia %}
  </body>
</html>
```


## Credits

Thanks to [Andres Vargas](https://github.com/zodman) for the inspiration on this package. Here is
the link to its legacy package which seems not be actively maintained anymore:
[inertia-django](https://github.com/zodman/inertia-django)

## Contributing

<!-- Please read the [Contributing Documentation](CONTRIBUTING.md) here. -->
TODO

## Maintainers

- [Samuel Girardin](https://www.github.com/girardinsamuel)

## License

django-inertia is open-sourced software licensed under the [MIT license](LICENSE).
