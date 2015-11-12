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

def cart(request):
	context = {}
	context['status'] = is_open()
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))
	
	if 'cart' in request.session:
		context['item_count'] = len(request.session['cart'])
		the_cart = []
		subtotal = 0
		for item in request.session['cart']:
			a = product.objects.get(pk=item['product_id'])
			price = a.price
			
			if item['type'] == 'Arepa':
				the_item_type = item['arepa_type'] + ' ' + item['type']
				if not a.extras == 0:
					the_extras = []
					for extra in item['extras']:
						b = product.objects.get(pk=extra)
						the_extras.append(b.name)
				else:
					the_extras = 'No Line Up Players'

				if not item['paid_extras'] == None:
					the_paid_extras = []
					for paid_extra in item['paid_extras']:
						c = product.objects.get(pk=paid_extra)
						the_paid_extras.append(c.name)
						price += c.price

				else:
					the_paid_extras = 'No Bench Players'

				if not item['sauces'] == None:
					the_sauces = []
					for sauce in item['sauces']:
						d = product.objects.get(pk=sauce)
						the_sauces.append(d.name)

				else:
					the_sauces = 'No Sauce'

			else:
				the_item_type = item['type']

			if not item['soft_drinks'] == '':
				e = product.objects.get(pk=item['soft_drinks'])
				the_drink = e.name
				price += e.price

			else:
				the_drink = 'No Drink'

			this_item = {
						'product': a.name,
						'product_code': a.code,
						'image' : a.image,
						'type': the_item_type,
						'extras' : the_extras,
						'paid_extras' : the_paid_extras,
						'sauces':the_sauces,
						'soft_drinks':the_drink,
						'price' : price
						}

			subtotal += price
			the_cart.append(this_item)

		amounts = {
			'subtotal': subtotal,
			'tax': subtotal,
			'total': subtotal+(subtotal)
		}
		the_cart.append(amounts)
		context['cart'] = the_cart

	else:
		context['item_count'] = 0

	return context


def menu(request):
	context = cart(request)
	#del request.session['cart']
	#print str(request.session['cart'])
	#Pido todas las categorias y productos
	arepas = product.objects.filter(Active=True,category=category.objects.get(code='arepas')).order_by('order_in_menu')

	kids = product.objects.filter(Active=True,category=category.objects.get(code='kids')).order_by('order_in_menu')
	
	context['arepas'] = arepas
	context['kids'] = kids

	if not 'order_number' in request.session:
		request.session['order_number'] = get_order_number()

	return render(request, 'website/plain_page.html', context)

def ProductDetail(request,id_for_prod):
	context = cart(request);

	try:
		Product = product.objects.get(pk=id_for_prod)

	except product.DoesNotExist:
		return HttpResponseRedirect(reverse('website:menu'))

	else:
		context['product'] = Product

	if request.POST:
		if Product.category.code == 'arepas':
			
			arepa = ArepaForm(request.POST)

			if arepa.is_valid():
				
				if 'paid_extras' in request.POST:
					paid_extras = []
					for i in request.POST.getlist('paid_extras'):
						paid_extras.append(i)
				else:
					paid_extras = None

				if 'sauces' in request.POST:
					sauces = []
					for i in request.POST.getlist('sauces'):
						sauces.append(i)
				else:
					sauces = None

				if Product.extras == 0:
					extras = None
				else:
					extras = []
					for i in request.POST.getlist('extras'):
						extras.append(i)
				
				a = {
					'type' : 'Arepa',
					'product_id':request.POST['id_for_product'],
					'arepa_type':request.POST['arepa_type'],
					'extras':extras,
					'paid_extras': paid_extras,
					'sauces':sauces,
					'soft_drinks':request.POST['soft_drinks']
					}
				if 'cart' in request.session:
					local_cart = request.session['cart']
					local_cart.append(a)
					request.session['cart'] = local_cart
					print local_cart

				else:
					local_cart = []
					local_cart.append(a)
					request.session['cart'] = local_cart
					print local_cart


				return HttpResponseRedirect(reverse('website:menu'))
			else:
				html = 'website/arepa_wizard.html'
				context['form'] = ArepaForm(request.POST)
		else:
			kid_meal = KidForm(request.POST)

			if kid_meal.is_valid():
				a = {
					'type': "Kid's Meal",
					'product_id':request.POST['id_for_product'],
					'soft_drinks':request.POST['soft_drinks']
					}
				if 'cart' in request.session:
					local_cart = request.session['cart']
					local_cart.append(a)
					request.session['cart'] = local_cart

				else:
					local_cart = []
					local_cart.append(a)
					request.session['cart'] = local_cart

				return HttpResponseRedirect(reverse('website:menu'))

			else:
				html = 'website/kid_wizard.html'
				context['form'] = KidForm(request.POST)
	else:
		if Product.category.code == 'arepas':
			html = 'website/arepa_wizard.html'
			context['form'] = ArepaForm(initial={ 'id_for_product': id_for_prod })
		else:
			html = 'website/kid_wizard.html'
			context['form'] = KidForm(initial={'id_for_product': id_for_prod})

	return render(request, html, context)

def checkout(request):
	context = cart(request)
	return render(request, 'website/invoice.html', context)