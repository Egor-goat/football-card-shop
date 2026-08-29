from django.urls import path
from . import views

urlpatterns = [
    path("", views.card_shop, name="card_shop"),
    path("buy/<int:card_id>/", views.buy_card, name="buy_card"),
    path("my-cards/", views.my_cards, name="my_cards"),
    path("collect-income/", views.collect_income,name="collect_income"),
    path("add_to_team/<int:card_id>/", views.add_to_team,name="add_to_team"),
    path("open-pack/<int:pack_id>/",views.open_pack,name="open_pack"),
    path("my-team/",views.my_team,name="my_team"),
    path("remove-from-team/<int:team_card_id>/",views.remove_from_team,name="remove_from_team"),
]