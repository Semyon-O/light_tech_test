from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAccountBalance, Transaction
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserBalanceSerializer(serializers.ModelSerializer):
    amount_rub = serializers.SerializerMethodField()

    class Meta:
        model = UserAccountBalance
        fields = ['amount', 'amount_rub']

    def get_amount_rub(self, obj):
        return obj.amount / 100


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class TransferSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(pk=value)
            if user == self.context['request'].user:
                raise serializers.ValidationError("Нельзя перевести деньги самому себе")
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type_display = serializers.CharField(source='get_transaction_type_display')
    amount_rub = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'transaction_type_display', 'amount', 'amount_rub', 'timestamp', 'related_user',
                  'desc']

    def get_amount_rub(self, obj):
        return obj.amount / 100



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_check = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']