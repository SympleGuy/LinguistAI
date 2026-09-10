import logging
import json
from django.http import JsonResponse
from django.conf import settings
from django.urls import resolve
from django.shortcuts import redirect
from django.contrib.sessions.exceptions import SessionInterrupted

logger = logging.getLogger(__name__)

# Public API routes that do not require authentication
PUBLIC_API_ROUTES = [
    "/api/auth/register/",
    "/api/auth/login/",
    "/api/auth/logout/",
    "/api/auth/me/",
    "/api/auth/oauth-sync/",
    "/api/scenarios/",
    "/api/tts/",
    "/api/admin/auth/login/",
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
            is_admin_api = path.startswith("/api/admin/") and not is_public

            if is_admin_api:
                # Admin APIs strictly require staff/admin user or authenticated admin role
                user_id = request.session.get("supabase_user_id")
                is_authorized = (
                    (hasattr(request, "user") and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)) or
                    request.session.get("role") == "admin" or
                    request.session.get("is_admin")
                )
                if not is_authorized and user_id:
                    try:
                        from .models import User as AppUser
                        if AppUser.objects.filter(id=user_id, role="admin").exists():
                            is_authorized = True
                    except Exception:
                        pass

                if not is_authorized:
                    return JsonResponse({
                        "error": "Admin access required.",
                        "code": 403
                    }, status=403)
            elif not is_public:
                user_id = request.session.get("supabase_user_id")
                auth_header = request.headers.get("Authorization", "")
                has_bearer = auth_header.startswith("Bearer ") and len(auth_header.split(" ")) > 1

                # Authenticate Supabase JWT bearer token if session not present
                if not user_id and has_bearer:
                    token = auth_header.split(" ")[1].strip()
                    try:
                        from .supabase_client import supabase
                        if supabase:
                            auth_user_resp = supabase.auth.get_user(token)
                            if auth_user_resp and hasattr(auth_user_resp, 'user') and auth_user_resp.user:
                                user_id = str(auth_user_resp.user.id)
                                request.session["supabase_user_id"] = user_id
                    except Exception:
                        pass

                is_authenticated = bool(user_id) or (hasattr(request, "user") and request.user.is_authenticated)

                if not is_authenticated:
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
        try:
            return self.get_response(request)
        except SessionInterrupted as e:
            logger.info(f"[SessionInterrupted] Gracefully handled concurrent session deletion on {request.method} {request.path}: {e}")
            if request.path.startswith("/api/"):
                return JsonResponse({
                    "error": "Session ended or user logged out.",
                    "code": 401
                }, status=401)
            return redirect("home")
        except Exception as e:
            resp = self.process_exception(request, e)
            if resp is not None:
                return resp
            raise e

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
