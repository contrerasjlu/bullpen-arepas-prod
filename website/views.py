from django.shortcuts import render
from ordertogo.models import *
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse
from random import randint
from datetime import *
from .forms import *
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test

def load_vars(code):
	code = GenericVariable.objects.get(code=code)
	return code.value

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
		the_session_cart = request.session['cart']
		for item in the_session_cart:
			a = product.objects.get(pk=item['product_id'])
			price = a.price
			
			if item['type'] == 'Arepa':
				the_item_type = item['arepa_type'] + ' ' + item['type']
				if not a.extras == 0:
					the_extras = []
					for extra in item['extras']:
						b = product.objects.get(pk=extra)
						the_extras.append(b.name+ ' (' + b.description + ')')
				else:
					the_extras = 0

				if not item['paid_extras'] == None:
					the_paid_extras = []
					for paid_extra in item['paid_extras']:
						c = product.objects.get(pk=paid_extra)
						the_paid_extras.append(c.name+ ' (' + c.description + ')')
						price += c.price

				else:
					the_paid_extras = 0

				if not item['sauces'] == None:
					the_sauces = []
					for sauce in item['sauces']:
						d = product.objects.get(pk=sauce)
						the_sauces.append(d.name + ' (' + d.description + ')')

				else:
					the_sauces = 0

			else:
				the_item_type = item['type']
				the_extras = 0
				the_paid_extras = 0
				the_sauces = 0

			if not item['soft_drinks'] == '':
				e = product.objects.get(pk=item['soft_drinks'])
				the_drink = e.name
				price += e.price

			else:
				the_drink = 'No Drink'

			this_item = {
						'product': a.name + ' (' + a.description + ')',
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

		from decimal import Decimal

		amounts = {
			'subtotal': subtotal,
			'delivery' : load_vars('delivery.cost'),
			'tax': subtotal * Decimal(load_vars('tax.percent')),
			'total': subtotal+(subtotal* Decimal(load_vars('tax.percent')))+int(load_vars('delivery.cost'))
		}
		context['amounts'] = amounts
		context['cart'] = the_cart
		context['cart_is_empty'] = False

	else:
		context['item_count'] = 0
		context['cart_is_empty'] = True

	return context


def menu(request):
	context = cart(request)
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

				return HttpResponseRedirect(reverse('website:menu'))
			else:

				html = 'website/arepa_wizard.html'
				context['form'] = ArepaForm(request.POST)
				print context['form']
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
			if Product.extras == 0:
				context['pabellon'] = product.objects.get(code='RF')
			context['form'] = ArepaForm(initial={ 'id_for_product': id_for_prod })
		else:
			html = 'website/kid_wizard.html'
			context['form'] = KidForm(initial={'id_for_product': id_for_prod})

	return render(request, html, context)

def empty_cart(request):
	if 'cart' in request.session:
		del request.session['cart']
	return HttpResponseRedirect(reverse('website:menu'))

def create_account(request):
	if request.POST:
		a = CreateAccountForm(request.POST)

		if a.is_valid():
			from django.contrib.auth.models import User
			user = User.objects.create_user(
				username = request.POST['username'],
				password = request.POST['password'],
				email = request.POST['email']
				)
			user.save()
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if 'next' in request.GET:
					return HttpResponseRedirect(request.GET['next'])
				else:
					return HttpResponseRedirect(reverse('website:menu'))
		else:
			context = {}
			context['new_user'] = CreateAccountForm(request.POST)
			return render(request, 'website/login.html', context)



@login_required(redirect_field_name='', login_url='website/login/')
def userLogout(request):
    logout(request)
    if 'cart' in request.session:
		del request.session['cart']
    return HttpResponseRedirect(reverse('website:menu'))

@login_required(redirect_field_name='', login_url='website/login/')
def pre_checkout(request):
	context = cart(request)
	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	if request.POST:
		data_client = PreCheckoutForm(request.POST)
		if data_client.is_valid():
			request.session['data_client'] = {
				'type_of_sale': request.POST['type_of_sale'],
				'delivery': request.POST['address'],
				'location': request.POST['location'],
				'time': request.POST['time']
			}
			return HttpResponseRedirect(reverse('website:checkout'))
		else:
			context['form'] = PreCheckoutForm(request.POST)
			return render(request, 'website/pre_checkout.html', context)
	else:
		context['form'] = PreCheckoutForm()
		return render(request, 'website/pre_checkout.html', context)



@login_required(redirect_field_name='', login_url='/website/login')
def checkout(request):
	context = cart(request)
	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	context['tax'] = float(load_vars('tax.percent'))*100
	context['pay_form'] = PaymentForm()
	context['data_client'] = request.session['data_client']
	return render(request, 'website/invoice.html', context)

def ValidateAddress(key,origin,destination,max_miles):
    import googlemaps
    from decimal import Decimal
    gmaps = googlemaps.Client(key=key)
    dest = gmaps.geocode(destination)
    directions_result = gmaps.directions(
        origin,
        dest[0]['formatted_address'],
        mode="transit"
    )
    miles = directions_result[0]['legs'][0]['distance']['text'].split(' ')

    if Decimal(miles[0]) > max_miles:
        return False
    else:
        return True


#Master: 5424180279791732
def payment_try(name,card,exp,desc, amt, cvv):
    import payeezy
    import json

    if card.startswith('3'):
        cardT = 'American Express'
    elif card.startswith('4'):
        cardT = 'Visa'
    elif card.startswith('5'):
        cardT = 'Mastercard'

    payeezy.apikey = str(loadVars('pay.apikey'))

    payeezy.apisecret = str(loadVars('pay.secret'))

    payeezy.token = str(loadVars('pay.token'))

    payeezy.url = loadVars('pay.url')

    responseAuthorize =  payeezy.transactions.authorize(amount=amt,
                                                        currency_code='usd',
                                                        card_type=cardT,
                                                        cardholder_name=name,
                                                        card_number=card,
                                                        card_expiry=exp,
                                                        card_cvv=cvv,
                                                        description=desc
                                                        )
    response = {}
    try:
        responseAuthorize.json()['Error']['messages']

    except KeyError:
        response['status'] = True
        response['object'] = responseAuthorize

    else:
        Error = responseAuthorize.json()['Error']['messages']
        response['status'] = False
        response['object'] = Error

    return response