from django.urls import path

from .views import (
    AddFavouriteCoin,
    ListFavouriteCoins,
    GetAllCoins,
    AddFavouriteCoinV2,
    ListFavouriteCoinsV2
)


urlpatterns = [
    path('v1/add/', AddFavouriteCoin.as_view(), name='add_coin'),
    path('v1/favourites', ListFavouriteCoins.as_view({'get': 'list'}), name='favourites'),
    path('v1/all_coins', GetAllCoins.as_view(), name='all_coins'),
    path('v2/add/<str:coin>', AddFavouriteCoinV2.as_view(), name='add_coin_v2'),
    path('v2/favourites', ListFavouriteCoinsV2.as_view({'get': 'list'}), name='favourites_v2'),
]
