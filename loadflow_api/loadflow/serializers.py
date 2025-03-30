from rest_framework import serializers
from .models import Bus, Generator, Load

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class GeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generator
        fields = '__all__'

class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'
