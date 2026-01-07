from rest_framework import serializers
from  .models import Earned,Spent,User

class EarnedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Earned
        fields=['tid','amt','category','date']
class SpentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Spent
        fields=['tid','amt','category','date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','balance']
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        min_length=6
    )
    class Meta:
        model=User
        firlds=['email','password']