from django.urls import path

from .views import BuyStockAPIView, AsyncBuyStockAPIView


urlpatterns = [
     path('buy-stock/', BuyStockAPIView.as_view()),
     path('buy-stock-v2/', AsyncBuyStockAPIView.as_view()),
]
