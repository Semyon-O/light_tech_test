from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import UserAccountBalance, Transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import (
    UserBalanceSerializer,
    DepositSerializer,
    TransferSerializer,
    TransactionSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenSerializer,
)

User = get_user_model()


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        balance = request.user.balance
        serializer = UserBalanceSerializer(balance)
        return Response(serializer.data)


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance = request.user.balance

        # Обновляем баланс
        balance.amount += amount
        balance.save()

        # Создаем запись о транзакции
        Transaction.objects.create(
            user=request.user,
            transaction_type='deposit',
            amount=amount,
            desc=f"Пополнение баланса на {amount / 100:.2f} руб."
        )

        return Response(
            {'message': f'Баланс успешно пополнен на {amount / 100:.2f} руб.'},
            status=status.HTTP_200_OK
        )


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        recipient = serializer.validated_data['user_id']
        sender_balance = request.user.balance


        if sender_balance.amount < amount:
            return Response(
                {'error': 'Недостаточно средств на балансе'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recipient_balance, created = UserAccountBalance.objects.get_or_create(user=recipient)


        sender_balance.amount -= amount
        recipient_balance.amount += amount

        sender_balance.save()
        recipient_balance.save()

        Transaction.objects.create(
            user=request.user,
            transaction_type='transfer',
            amount=amount,
            related_user=recipient,
            desc=f"Перевод пользователю {recipient.username} на {amount / 100:.2f} руб."
        )

        Transaction.objects.create(
            user=recipient,
            transaction_type='receive',
            amount=amount,
            related_user=request.user,
            desc=f"Получение от пользователя {request.user.username} {amount / 100:.2f} руб."
        )

        return Response(
            {'message': f'Успешно переведено {amount / 100:.2f} руб. пользователю {recipient.username}'},
            status=status.HTTP_200_OK
        )


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = request.user.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)



class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user_id': user.pk,
                    'username': user.username
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        'token': token.key,
                        'user_id': user.pk,
                        'username': user.username
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {'message': 'Вы успешно вышли из системы'},
            status=status.HTTP_200_OK
        )