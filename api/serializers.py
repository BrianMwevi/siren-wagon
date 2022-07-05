from rest_framework import serializers
from sirenapp.models import  Package,Trip


class PackageSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='package-detail')
    user=serializers.RelatedField(source='users',read_only=True)
    class Meta:
        model=Package
        fields=[
            # 'url',
            'id',
            'package_choice',
            'user'
            ]
    
        

class TripSerializer(serializers.ModelSerializer):
    driver=serializers.RelatedField(source='users',read_only=True)
    fee=serializers.RelatedField(source='transaction',read_only=True)
    
    class Meta:
        model=Trip
        fields= [
            'id',
            'trip_date',
            'driver',
            'fee',
            'destination',
            'pickup'
            ]
       
        
    