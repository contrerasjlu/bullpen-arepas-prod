from rest_framework import serializers
from .models import *
from website.models import WebText, WebCategory, WebProduct

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = category
		fields = '__all__'

class WebCategorySerializer(serializers.ModelSerializer):
	category = CategorySerializer(category)

	class Meta:
		model = WebCategory
		fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = product
		fields = '__all__'

class WebProductSerializer(serializers.ModelSerializer):
	product = ProductSerializer(product)

	class Meta:
		model = WebProduct
		fields = '__all__'

class WebTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = WebText
		fields = ('code','name','text','active')