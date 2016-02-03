from ordertogo.models import category, product
from website.models import WebText, WebCategory, WebProduct
from ordertogo.serializers import WebCategorySerializer, WebProductSerializer, WebTextSerializer, ProductSerializer
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response

class api_WebCategories(generics.ListAPIView):
	"""
	List all Categories
	"""
	queryset = WebCategory.objects.filter(active=True).order_by('order')
	serializer_class = WebCategorySerializer

class api_WebCategoryDetails(APIView):
	"""
	Return a single Category from an ID
	"""
	def get_object(self, CatId):
		try:
			return WebCategory.objects.get(id=CatId)
		except WebCategory.DoesNotExist:
			raise Http404

	def get(self, request, CatId, format=None):
		cat = self.get_object(CatId)
		serializer = WebCategorySerializer(cat)
		return Response(serializer.data)

class api_WebProducts(APIView):
	"""
	List all product for a given category
	"""
	def get(self, request, CatId, format=None):
		queryset = WebProduct.objects.filter(webCat=CatId)
		serializer = WebProductSerializer(queryset, many=True)
		return Response(serializer.data)

class api_WebProductsDetails(APIView):
	"""
	Return a single Category from an ID
	"""
	def get_object(self, ProdId):
		try:
			return product.objects.get(id=ProdId)
		except product.DoesNotExist:
			raise Http404

	def get(self, request, CatId, ProdId, format=None):
		prod = self.get_object(ProdId)
		serializer = ProductSerializer(prod)
		return Response(serializer.data)

class Texts(generics.ListAPIView):
	"""
	List all the texts for the App
	"""
	queryset = WebText.objects.filter(active=True)
	serializer_class = WebTextSerializer

class TextDetail(APIView):
	"""
	Return a Text from a given code
	"""
	def get_object(self, code):
		try:
			return WebText.objects.get(code=code)
		except WebText.DoesNotExist:
			raise Http404

	def get(self, request, code, format=None):
		text = self.get_object(code)
		serializer = WebTextSerializer(text)
		return Response(serializer.data)


		