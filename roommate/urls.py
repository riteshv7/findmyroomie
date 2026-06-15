from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.search_view, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('role-select/', views.role_select_view, name='role_select'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('create-listing/', views.create_listing_view, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail_view, name='listing_detail'),
    path('listing/<int:pk>/interest/', views.express_interest_view, name='express_interest'),
    path('interests/', views.interests_view, name='interests'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<str:conversation_id>/', views.chat_view, name='chat_thread'),
    path('profile/', views.profile_view, name='profile'),
    path('sw.js', TemplateView.as_view(template_name="roommate/sw.js", content_type="application/javascript"), name="sw.js"),
]

