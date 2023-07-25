from django.urls import path, include
from . import views

app_name = 'mail'

path_patterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

api_routes = [
    # API Routes
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
]

urlpatterns = [
    path('mailbox/',  views.index, name='index'),
    path('mailbox/', include(path_patterns)),
    path('mailbox/', include(api_routes)),
]
