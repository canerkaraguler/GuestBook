from rest_framework import serializers
from .models import User, Entry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'created_date']
        read_only_fields = ['created_date']

class EntrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Entry
        fields = ['subject', 'message', 'created_date', 'name']
        read_only_fields = ['created_date']

    def create(self, validated_data):
        name = validated_data.pop('name')
        user, _ = User.objects.get_or_create(name=name)
        validated_data['user'] = user
        return super().create(validated_data)
    

