from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("api/scenarios/", views.scenarios_list, name="scenarios_list"),
    path("api/scenarios/<int:scenario_id>/", views.ScenarioDetailView.as_view(), name="scenario_detail"),
    path("api/sessions/start/", views.StartSessionView.as_view(), name="start_session"),
    path("api/debug-session/", views.DebugSessionView.as_view(), name="debug_session"),
    path("api/sessions/<uuid:session_id>/respond/", views.SubmitResponseView.as_view(), name="submit_response"),
    path("api/dashboard/<uuid:user_id>/", views.DashboardView.as_view(), name="user_dashboard"),
    path("api/sessions/history/<uuid:user_id>/", views.SessionHistoryView.as_view(), name="session_history"),
]