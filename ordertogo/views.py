from ordertogo.models import category, product
from ordertogo.serializers import CategorySerializer, ProductSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

class Category(generics.ListAPIView):
	"""
	List all Categories
	"""
	queryset = category.objects.filter(Active=True)
	serializer_class = CategorySerializer

class Product(generics.ListAPIView):
	"""
	List all Product by Category
	"""
	queryset = product.objects.filter(Active=True).order_by('order_in_menu')
	serializer_class = ProductSerializer


@api_view(['GET'])
def Product_By_Category(request, CatId):
	"""
	List all product for a given category
	"""
	queryset = product.objects.filter(Active=True,category=CatId).order_by('order_in_menu')
	serializer = ProductSerializer(queryset, many=True)
	
	if queryset.count()>0:
		return Response(serializer.data)
	
	return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def Product_Detail(request, CatId, ProdId):
	"""
	List a single product for a given category and a given product ID
	"""
	queryset = product.objects.filter(Active=True,category=CatId, pk=ProdId)
	serializer = ProductSerializer(queryset, many=True)
	
	if queryset.count()>0:
		return Response(serializer.data)
	
	return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


		