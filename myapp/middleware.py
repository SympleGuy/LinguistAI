import logging
import json
from django.http import JsonResponse
from django.conf import settings
from django.urls import resolve

logger = logging.getLogger(__name__)

# Public API routes that do not require authentication
PUBLIC_API_ROUTES = [
    "/api/auth/register/",
    "/api/auth/login/",
    "/api/auth/logout/",
    "/api/auth/me/",
    "/api/scenarios/",
    "/api/debug-session/",
]


class ApiAuthenticationMiddleware:
    """
    Middleware that enforces authentication on protected API endpoints.
    Returns HTTP 401 Unauthorized with standardized JSON error when unauthenticated.
    Accepts: Django session, Authorization: Bearer token, or X-User-ID header.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Only check requests targeting the /api/ prefix
        if path.startswith("/api/"):
            is_public = any(path.startswith(pub_route) for pub_route in PUBLIC_API_ROUTES)

            if not is_public:
                user_id = request.session.get("supabase_user_id")
                auth_header = request.headers.get("Authorization", "")
                has_bearer = auth_header.startswith("Bearer ") and len(auth_header.split(" ")) > 1
                x_user_id = request.headers.get("X-User-ID", "")

                # Also attach x_user_id to session if not already there (helps keep session alive)
                if x_user_id and not user_id:
                    try:
                        request.session["supabase_user_id"] = x_user_id
                        request.session.modified = True
                    except Exception:
                        pass

                if not user_id and not has_bearer and not x_user_id and not (hasattr(request, "user") and request.user.is_authenticated):
                    return JsonResponse({
                        "error": "Unauthorized access. Authentication required.",
                        "code": 401
                    }, status=401)

        response = self.get_response(request)
        return response


class GlobalExceptionHandlerMiddleware:
    """
    Middleware that captures all uncaught exceptions across the application.
    Prevents leaking internal Python tracebacks to clients and returns structured JSON on API routes.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(
            f"[GlobalExceptionHandler] Unhandled exception on {request.method} {request.path}: {exception}",
            exc_info=True
        )

        is_api = request.path.startswith("/api/") or request.content_type == "application/json" or request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if is_api:
            return JsonResponse({
                "error": "Internal server error. Please try again later.",
                "code": 500
            }, status=500)

        # For non-API views, let Django's default exception handling proceed if DEBUG=True
        if settings.DEBUG:
            return None

        return JsonResponse({
            "error": "An unexpected error occurred. Please try again later.",
            "code": 500
        }, status=500)
