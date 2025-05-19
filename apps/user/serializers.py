import re
from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def validate_phone(self, value):
        number = value.replace(' ', '').replace('+977', '')

        pattern = r'^\d{10}$'
        if not re.match(pattern, number):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")

        return f'+977 {number}'
