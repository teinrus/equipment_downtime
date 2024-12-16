from rest_framework import serializers
from .models import ProductOutput

class ProductOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOutput
        fields = ['line', 'quantity', 'date', 'time']  # Все необходимые поля
