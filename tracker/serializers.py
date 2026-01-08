from rest_framework import serializers
from  .models import Earned,Spent,User,Investments

class EarnedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Earned
        fields=['tid','amt','category','date']
        read_only_fields=['tid','date']
class SpentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Spent
        fields=['tid','amt','category','date']
        read_only_fields=['tid','date']
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Investments
        fields=['tid','amt','category','date']
        read_only_fields=['tid','date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','balance']

class UserDetailsSerializer(serializers.ModelSerializer):
    earned=EarnedSerializer(many=True,read_only=True)
    spent=SpentSerializer(many=True,read_only=True)
    investments=InvestmentSerializer(many=True,read_only=True)
    class Meta:
        model=User
        fields=['email','balance','earned','spent','investments']
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        min_length=6
    )
    class Meta:
        model=User
        fields=['email','password']
    def create(self, validated_data):
        # Extract password
        password = validated_data.pop('password')
        
        # Create user with proper password hashing
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password  # Django automatically hashes this
        )
        
        return user