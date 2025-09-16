from django.contrib import admin
from django.urls import path, include
from academic_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("academic_app.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # 🌟 Add this line to include the new AI agent app's URLs
    path("agent/", include("gemini_agent_app.urls")),
]
