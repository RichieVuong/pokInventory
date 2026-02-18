from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("binders/", views.binder_shelf, name="binder_shelf"),
    path("create-binder/", views.create_binder, name="create_binder"),
    path('binder/<int:binder_id>/delete/', views.delete_binder, name='delete_binder'),
    path('card/<int:card_id>/delete/', views.delete_card, name='delete_card'),
    path("binder/<int:binder_id>/", views.binder, {'page': 1}, name="binder"),
    path("binder/<int:binder_id>/0/", views.binder, {'page': 0}, name="binder_cover"), # Explicit cover route
    path("binder/<int:binder_id>/<int:page>/", views.binder, name="binder_page"),
    path("search/", views.search_cards, name="search_cards"),
    path("add/<int:binder_id>/", views.add_card, name="add_card"),
]
