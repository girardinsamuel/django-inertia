from django_inertia import Inertia


def home(request):
    return Inertia.render(request, "Index", {"message": "Hello World"})


def home_extra_data(request):
    return Inertia.render(request, "Index", {"message": "Hello World"}, view_data={
        'app_name': 'Django Inertia',
        'app_version': '1.0'
    })


def view_with_lazy_props(request):
    return Inertia.render(
        request, "Index", {"message": "Hello World", "data": Inertia.lazy(lambda r: "value")}
    )


def view_with_lazy_props_using_request(request):
    return Inertia.render(
        request,
        "Index",
        {"message": "Hello World", "data": Inertia.lazy(lambda r: r.user.first_name)},
    )


def view_with_view_data(request):
    return Inertia.render(
        request,
        "Index",
        {"message": "Hello World", "data": Inertia.lazy(lambda r: r.user.first_name)},
        view_data={'name': Inertia.lazy(lambda r: r.user.first_name)}
    )
