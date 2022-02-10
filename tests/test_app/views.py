from django_inertia import Inertia


def home(request):
    return Inertia.render(request, "Index", {"message": "Hello World"})


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
