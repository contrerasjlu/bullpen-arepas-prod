from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
	product = serializers.PrimaryKeyRelatedField(many=True,queryset=product.objects.filter(Active=True))
	
	class Meta:
		model = category
		fields = ('id','code','name','description','product' )

class ProductSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = product
		exclude = ['Active','category']