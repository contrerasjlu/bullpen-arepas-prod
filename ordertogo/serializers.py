from rest_framework import serializers
from .models import *
from website.models import WebText, WebCategory

class CategorySerializer(serializers.ModelSerializer):
	#product = serializers.PrimaryKeyRelatedField(many=True,queryset=product.objects.filter(Active=True))
	
	class Meta:
		model = WebCategory
		fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = product
		exclude = ['Active','category']

class WebTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = WebText
		fields = ('code','name','text','active')