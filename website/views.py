from django.shortcuts import render
from ordertogo.models import *
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from random import randint
from datetime import *
from .forms import *

# Create your views here.

#Funcion para saber si esta abierto el punto de venta.
def is_open():
	#Si esta Abierto y correctamente (No existen mas de un lote abierto)...
	try:
		batch = PaymentBatch.objects.get(status="O")
		#TODO: Buscar la forma de limitar la hora tambien en la consulta
	except PaymentBatch.DoesNotExist:
		return False

	except PaymentBatch.MultipleObjectsReturned:
		return False
	else:
		return True

#Generar un numero de orden aleatorio
def get_order_number():
	t = 10000
	sure = False
	while sure == False:
		order = randint(5000, t)
		order = str(datetime.now().year)+str(t)
		try:
			Order.objects.get(order_number=order)
		except Order.DoesNotExist:
			sure = True
	return order

def index(request):
	context = {}
	context['status'] = is_open()
	return render(request, 'website/index.html', context)

def closed(request):
	context = {}
	context['status'] = is_open()
	if context['status']==True:
		return HttpResponseRedirect(reverse('website:menu'))

	return render(request, 'website/closed.html', context)

def menu(request):
	context = {}
	context['status'] = is_open()
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	#Pido todas las categorias y productos
	arepas = product.objects.filter(Active=True,category=category.objects.get(code='arepas')).order_by('order_in_menu')

	kids = product.objects.filter(Active=True,category=category.objects.get(code='kids')).order_by('order_in_menu')
	
	context['arepas'] = arepas
	context['kids'] = kids

	if not 'order_number' in request.session:
		request.session['order_number'] = get_order_number()

	return render(request, 'website/plain_page.html', context)

def ProductDetail(request,id_for_prod):
	context = {}
	context['status'] = is_open()
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	try:
		Product = product.objects.get(pk=id_for_prod)

	except product.DoesNotExist:
		return HttpResponseRedirect(reverse('website:menu'))

	else:
		context['product'] = Product

	if Product.category.code == 'arepas':
		html = 'website/arepa_wizard.html'
	else:
		context['product_type'] = 'kids'

	context['form'] = ArepaForm(initial={ 'id_for_product': id_for_prod })

	return render(request, html, context)