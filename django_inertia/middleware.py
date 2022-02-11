from django.http import HttpResponseRedirect

from .core import Inertia


class InertiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # -> Code to be executed for each request before other middlewares and view are called.
        if not Inertia.get_version():
            Inertia.version(self.version(request))
        Inertia.share(self.share(request))

        response = self.get_response(request)

        # -> Code to be executed for each request/response after the view is called.
        response = self.check_version(request, response)
        # handle PUT, PATCH, DELETE redirections
        if (
            request.method in ["PUT", "PATCH", "DELETE"]
            and isinstance(response, HttpResponseRedirect)
            and response.status_code == 302
        ):
            response.status_code = 303
        return response

    def is_inertia(self, request):
        return request.headers.get("X-Inertia", False)

    def check_version(self, request, response):
        """In the event that the assets change, initiate a client-side location visit
        to force an update."""
        if (
            self.is_inertia(request)
            and request.method == "GET"
            and request.headers.get("X-Inertia-Version", "") != Inertia.get_version()
        ):
            # TODO: reflash session ?
            return Inertia.location(request.get_full_path_info())

        return response

    def version(self, request):
        """Determines the current asset version. Can be overriden."""
        # assets_url = config("inertia.public_path")
        # if assets_url:
        #     return hashlib.md5(assets_url.encode()).hexdigest()

        # manifest_file_path = public_path("mix-manifest.json")
        # if os.path.exists(manifest_file_path):
        #     hasher = hashlib.md5()
        #     with open(manifest_file_path, "rb") as manifest_file:
        #         buf = manifest_file.read()
        #         hasher.update(buf)
        #     return hasher.hexdigest()
        return 1

    def share(self, request):
        """Defines the props that are shared by default. Can be overriden."""
        errors = request.session.get("errors", False)
        success = request.session.get("success", False)
        # remove flash data for next request
        request.session["errors"] = False
        request.session["success"] = False
        return {"errors": Inertia.static(errors), "success": Inertia.static(success)}
