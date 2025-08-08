from django.urls import path
from .views import BalanceView, DepositView, TransferView, TransactionHistoryView, UserRegistrationView, UserLoginView, \
    UserLogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('balance/', BalanceView.as_view(), name='balance'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
]