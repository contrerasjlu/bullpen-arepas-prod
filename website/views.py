from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from random import randint
from datetime import *
from decimal import Decimal
from ordertogo.models import *
from .forms import *


def load_vars(code):
	code = GenericVariable.objects.get(code=code)
	return code.value

#Funcion para saber si esta abierto el punto de venta.
def is_open():
	#Si esta Abierto y correctamente (No existen mas de un lote abierto)...
	a = PaymentBatch.objects.filter(status="O")
	if len(a) == 0:
		return False
	else:
		return True

#Generar un numero de orden aleatorio
def get_order_number():
	t = 100000
	sure = False
	while sure == False:
		order = randint(1000, t)
		order = str(datetime.now().year)+str(order)
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

	if 'guest' in request.session:
		context['guest'] = request.session['guest']
		
	if 'cart' in request.session:
		context['item_count'] = len(request.session['cart'])
		the_cart = []
		subtotal = 0
		the_session_cart = request.session['cart']
		for item in the_session_cart:
			a = product.objects.get(pk=item['product_id'])
			price = a.price
			
			the_item_type = item['type']

			if a.allow_extras == True:
				if not a.extras == 0:
					the_extras = []
					for extra in item['extras']:
						b = product.objects.get(pk=extra)
						the_extras.append(b.name+ ' (' + b.description + ')')
				else:
					the_extras = 'No Players Allowed'
			else:
				the_extras = 0


			if a.allow_vegetables == True:
				if not item['vegetables'] == None:
					the_vegetables = []
					for vegetable in item['vegetables']:
						v = product.objects.get(pk=vegetable)
						the_vegetables.append(v.name + ' (' + v.description + ')')
						price += v.price

				else:
					the_vegetables = 'No Vegetables'
			else:
				the_vegetables = 0

			if a.allow_paid_extras == True:
				if not item['paid_extras'] == None:
					the_paid_extras = []
					for paid_extra in item['paid_extras']:
						c = product.objects.get(pk=paid_extra)
						the_paid_extras.append(c.name+ ' (' + c.description + ')')
						price += c.price

				else:
					the_paid_extras = 'No Bench Players'
			else:
				the_paid_extras = 0

			if a.allow_sauces == True:
				if not item['sauces'] == None:
					the_sauces = []
					for sauce in item['sauces']:
						d = product.objects.get(pk=sauce)
						the_sauces.append(d.name + ' (' + d.description + ')')

				else:
					the_sauces = 'No Sauces'
			else:
				the_sauces = 0

			if a.allow_drinks == True:
				if not item['soft_drinks'] == '':
					try:
						e = product.objects.get(pk=item['soft_drinks'])
					
					except product.DoesNotExist:
						the_drink = 0
					
					else:						
						the_drink = e.name
						price += e.price

				else:
					the_drink = 'No Drink'
			else:
				the_drink = 0

			this_item = {
						'product': a.name + ' (' + a.description + ')',
						'product_code': a.code,
						'image' : a.image,
						'type': the_item_type,
						'extras' : the_extras,
						'vegetables': the_vegetables,
						'paid_extras' : the_paid_extras,
						'sauces':the_sauces,
						'soft_drinks':the_drink,
						'price' : price
						}

			subtotal += price
			the_cart.append(this_item)

		

		amounts = {
			'subtotal': subtotal,
			'delivery' : load_vars('delivery.cost'),
		}

		context['amounts'] = amounts
		context['cart'] = the_cart
		context['cart_is_empty'] = False

	else:
		context['item_count'] = 0
		context['cart_is_empty'] = True

	return context


def menu(request):
	# Load the Cart to show the products already in cart
	context = cart(request)

	# If the pay was already did it, delete the var
	if 'finish' in request.session:
		del request.session['finish']

	# If there any Batch open
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	context['show_in'] = category.objects.filter(Active=True, show_in_menu=True).order_by('order')

	try:
		return render(request, 'website/plain_page.html', context)
	except ValueError:
		return HttpResponseRedirect(reverse('website:closed'))

def ProductDetail(request,id_for_prod):
	context = cart(request);
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	context['product'] = get_object_or_404(product, pk=id_for_prod)

	if request.POST:

		this_product = ArepaForm(request.POST)
		if this_product.is_valid():
			
			# Si el producto permite Type
			if context['product'].allow_type == True:
				if 'arepa_type' in request.POST:
					product_type = request.POST['arepa_type']
				else:
					product_type = None
			else:
				product_type = context['product'].category.name

			# Si el producto permite Vegetales
			if context['product'].allow_vegetables == True:
				if 'vegetables' in request.POST:
					vegetables = []
					for i in request.POST.getlist('vegetables'):
						vegetables.append(i)
				else:
					vegetables = None
			else:
				vegetables = None

			# Si el producto permite Players
			if context['product'].allow_extras == True:
				if 'extras' in request.POST:
					extras = []
					for i in request.POST.getlist('extras'):
						extras.append(i)
				else:
					extras = None
			else:
				extras = None

			# Si el producto permite Bench Players
			if context['product'].allow_paid_extras == True:
				if 'paid_extras' in request.POST:
					paid_extras = []
					for i in request.POST.getlist('paid_extras'):
						paid_extras.append(i)
				else:
					paid_extras = None
			else:
				paid_extras = None

			
			# Si el producto permite Sauces
			if context['product'].allow_sauces == True:
				if 'sauces' in request.POST:
					sauces = []
					for i in request.POST.getlist('sauces'):
						sauces.append(i)
				else:
					sauces = None
			else:
				sauces = None

			# Si el producto permite Drinks
			if context['product'].allow_drinks == True:
				if 'soft_drinks' in request.POST:
					drinks = request.POST['soft_drinks']
				else:
					drinks = None
			else:
				drinks = None
			
			if context['product'].category.show_in_menu == True:
				main_product = True
			else:
				main_product = False

			a = {
				'type' : product_type,
				'product_id':request.POST['id_for_product'],
				'arepa_type':product_type,
				'vegetables':vegetables,
				'extras':extras,
				'paid_extras': paid_extras,
				'sauces':sauces,
				'soft_drinks':drinks,
				'main_product':main_product
				}

			if 'cart' in request.session:
				local_cart = request.session['cart']
				if context['product'].allow_qtty == True:
					for x in range(0,int(request.POST['qtty'])):
						local_cart.append(a)
				else:
					local_cart.append(a)
				request.session['cart'] = local_cart

			else:
				local_cart = []
				if context['product'].allow_qtty == True:
					for x in range(0,int(request.POST['qtty'])):
						local_cart.append(a)
				else:
					local_cart.append(a)
				request.session['cart'] = local_cart

			return HttpResponseRedirect(reverse('website:menu'))
		else:

			html = 'website/arepa_wizard.html'
			context['form'] = ArepaForm(request.POST)
	else:
		html = 'website/arepa_wizard.html'
		context['form'] = ArepaForm(initial={ 'id_for_product': id_for_prod })
	return render(request, html, context)

def empty_cart(request):
	if 'cart' in request.session:
		del request.session['cart']
	if 'order_number' in request.session:
		del request.session['order_number']
	return HttpResponseRedirect(reverse('website:menu'))

def create_account(request):
	if request.POST:
		a = CreateAccountForm(request.POST)

		if a.is_valid():
			from django.contrib.auth.models import User
			user = User.objects.create_user(
				username = request.POST['username'],
				password = request.POST['password'],
				email = request.POST['email'],
				first_name = request.POST['firstname'],
				last_name = request.POST['lastname']
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


@login_required(login_url='website:login-auth')
def ViewCart(request):
	context = cart(request)
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	return render(request, 'website/cart-view.html', context)

@login_required(login_url='website:login-auth')
def DeleteItem(request, item):
	context = cart(request)
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	the_session_cart = request.session['cart']
	item = int(item) - 1
	del the_session_cart[item]
	request.session['cart'] = the_session_cart

	if len(the_session_cart) == 0:
		return HttpResponseRedirect(reverse('website:menu'))
	else:
		return HttpResponseRedirect(reverse('website:view-cart'))


@login_required(login_url='website:login-auth')
def OrderHistory(request):
	context = cart(request)
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	if 'guest' in request.session:
		return HttpResponseRedirect(reverse('website:menu'))

	context['orders'] = Order.objects.filter(user=request.user).order_by('-id')

	return render(request, 'website/order-history.html', context)


@login_required(login_url='website:login-auth')
def userLogout(request):
    logout(request)
    del request.session

    return HttpResponseRedirect(reverse('website:menu'))

@login_required(login_url='website:login-auth')
def pre_checkout(request):
	context = cart(request)
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	if 'data_client' in request.session:
		del request.session['data_client']

	if request.POST:
		if request.POST['type_of_sale'] == 'D':
			data_client = PreCheckoutForm_Delivery(request.POST)
			if data_client.is_valid():
				origins = PaymentBatch.objects.filter(status='O', open_for_delivery=True)
				near = 0
				for location in origins:
					valid = ValidateAddress(
											load_vars('google.API.KEY'),
											location.address_for_truck,
											request.POST['address'],
											location.max_miles
											)
					if not valid == False:
						if near == 0:
							near = valid
							near_batch = location.id
						elif near > valid:
							near =  valid
							near_batch = location.id
					else:
						return HttpResponseRedirect(reverse('website:pre_checkout'))	

				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'Delivery',
					'batch': near_batch,
					'tax_percent':near_batch.tax_percent,
					'address': RewriteAddress(
											  request.POST['address'],
											  load_vars('google.API.KEY')
											  )
				}
				return HttpResponseRedirect(reverse('website:checkout'))
			else:
				context['form_delivery'] = PreCheckoutForm_Delivery(request.POST)
				context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
				context['default_type_of_sale'] = 'D'
				return render(request, 'website/pre_checkout.html', context)

		elif request.POST['type_of_sale'] == 'P':
			data_client = PreCheckoutForm_PickItUp(request.POST)
			if data_client.is_valid():
				location_desc =  PaymentBatch.objects.get(location_id=request.POST['location'], status='O')

				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'Pick it Up',
					'location': request.POST['location'],
					'location_desc' : location_desc.address_for_truck,
					'tax_percent': location_desc.tax_percent,
					'time': request.POST['time']
				}
				return HttpResponseRedirect(reverse('website:checkout'))
			else:
				context['form_pickitup'] = PreCheckoutForm_PickItUp(request.POST)
				context['form_delivery'] = PreCheckoutForm_Delivery(initial={ 'type_of_sale': 'D' })
				context['default_type_of_sale'] = 'P'
				return render(request, 'website/pre_checkout.html', context)
		else:
			return Http404("Wrong Way, Bad Request")
	else:
		context['form_delivery'] = PreCheckoutForm_Delivery(initial={ 'type_of_sale': 'D' })
		context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
		context['default_type_of_sale'] = 'D'
		return render(request, 'website/pre_checkout.html', context)

@login_required(redirect_field_name='', login_url='website:login-auth')
def checkout(request):
	context = cart(request)
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	if context['cart_is_empty'] == True:
		return HttpResponseRedirect(reverse('website:menu'))

	if 'data_client' in request.session:
		context['data_client'] = request.session['data_client']
		if context['data_client']['type_of_sale'] == 'D':
			context['amounts']['total'] += int(load_vars('delivery.cost'))
	else:
		return HttpResponseRedirect(reverse('website:pre_checkout'))

	context['tax'] = context['data_client']['tax_percent']
	context['amounts']['tax'] = Decimal(context['tax']*context['amounts']['subtotal']) / 100 
	context['amounts']['total'] = context['amounts']['subtotal'] + context['amounts']['tax']

	if not 'order_number' in request.session:
		request.session['order_number'] = get_order_number()
	
	context['order_number'] = request.session['order_number']
	context['pay_form'] = PaymentForm()

	if request.POST:
		payment = PaymentForm(request.POST)

		if payment.is_valid():
			exp = request.POST['expiry'].replace('/', '')
			value = str(float("{0:.2f}".format(context['amounts']['total'])))
			value = value.replace('.','')
			location_ref = LocationsAvailable.objects.get(pk=context['data_client']['location'])
			ref = location_ref.merchant_ref

			pay = PaymentRaw(
							 request.POST['name_on_card'],
							 request.POST['card_number'],
							 exp,
							 value,
							 request.POST['cvv'],
							 ref
							)

			if pay['status'] == False:
				context['pay_form'] = PaymentForm(request.POST)
				context['FailTrx'] = "Transaction Fail:"
				context['FailMsj'] = pay['object']
				return render(request, 'website/invoice.html', context)
			else:
				PayEgg = {
					'cardholder_name' : pay['object'].json()['card']['cardholder_name'],
					'card_type' : pay['object'].json()['card']['type'],
					'card_number' : pay['object'].json()['card']['card_number'],
					'exp_date' : pay['object'].json()['card']['exp_date'],
					'gateway_message' : pay['object'].json()['gateway_message'],
					'bank_message' : pay['object'].json()['bank_message'],
					'bank_resp_code' : pay['object'].json()['bank_resp_code'],
					'gateway_resp_code' : pay['object'].json()['gateway_resp_code'],
					'cvv2' : pay['object'].json()['cvv2'],
					'amount' : pay['object'].json()['amount'],
					'transaction_tag' : pay['object'].json()['transaction_tag'],
					'transaction_type' : pay['object'].json()['transaction_type'],
					'currency' : pay['object'].json()['currency'],
					'correlation_id' : pay['object'].json()['correlation_id'],
					'token_type' : pay['object'].json()['token']['token_type'],
					'token_value' : pay['object'].json()['token']['token_data']['value'],
					'transaction_status' : pay['object'].json()['transaction_status'],
					'validation_status' : pay['object'].json()['validation_status'],
					'method' : pay['object'].json()['method'],
					'transaction_id' : pay['object'].json()['transaction_id']
				}

				if context['data_client']['type_of_sale'] == 'P':
					this_order = Order(
						order_number=context['order_number'],
						order_type=context['data_client']['type_of_sale'],
						user=request.user,
						batch=PaymentBatch.objects.get(location=context['data_client']['location'], status='O'),
						address='--',
						time=context['data_client']['time'],
						sub_amt=context['amounts']['subtotal'],
						tax_amt=context['amounts']['tax'],
						delivery_amt=0,
						total_amt=context['amounts']['total']
					)

				elif context['data_client']['type_of_sale'] == 'D':
					
					this_order = Order(
						order_number=context['order_number'],
						order_type=context['data_client']['type_of_sale'],
						user=request.user,
						batch=PaymentBatch.objects.get(pk=context['data_client']['batch']),
						address=context['data_client']['address'],
						time='--',
						sub_amt=context['amounts']['subtotal'],
						tax_amt=context['amounts']['tax'],
						delivery_amt=Decimal(load_vars('delivery.cost')),
						total_amt=context['amounts']['total']
					)
				else:
					return HttpResponseRedirect(reverse('website:pre_checkout'))

				this_order.save()
				if request.user.username == load_vars('guest.user'):
					guest = request.session['guest']
					this_guest = GuestDetail(
						firstname=guest['firstname'],
						lastname=guest['lastname'],
						email=guest['email'],
						phone=guest['phone'],
						order=this_order
						)
					this_guest.save()

				# Almacenar el detalle de la orden
				the_session_cart = request.session['cart']
				item_number=1
				for item in the_session_cart:			
					if item['type'] == 'Arepa':
						arepa_type = item['arepa_type'] + ' ' + item['type']
					else:
						arepa_type = item['type']
					a = product.objects.get(pk=item['product_id'])
					this_detail = OrderDetail(
						item=item_number,
						arepa_type=arepa_type,
						product_selected=a,
						order_number=this_order,
						main_product=True,
					)
					this_detail.save()
					
					if not a.extras == 0:
						for extra in item['extras']:
							extras_detail = OrderDetail(
														item=this_detail.item,
														arepa_type='With',
														product_selected=product.objects.get(pk=extra),
														order_number=Order.objects.get(pk=this_order.id)
														)
							extras_detail.save()
					
					try:
						if not item['vegetables'] == None:
							for vegetable in item['vegetables']:
								vegetables_detail = OrderDetail(
																item=this_detail.item,
																arepa_type='Vegetables',
																product_selected=product.objects.get(pk=vegetable),
																order_number=Order.objects.get(pk=this_order.id)
																)
								vegetables_detail.save()

					except KeyError:
						pass


					try:
						if not item['paid_extras'] == None:
							for paid_extra in item['paid_extras']:
								paid_extras_detail = OrderDetail(
																 item=this_detail.item,
																 arepa_type='Paid Extra',
																 product_selected=product.objects.get(pk=paid_extra),
																 order_number=Order.objects.get(pk=this_order.id)
																)
								paid_extras_detail.save()

					except KeyError:
						pass

					try:
						if not item['sauces'] == None:
							for sauce in item['sauces']:
								sauce_detail = OrderDetail(
														   item=this_detail.item,
														   arepa_type='Sauces',
														   product_selected=product.objects.get(pk=sauce),
														   order_number=Order.objects.get(pk=this_order.id)
														   )
								sauce_detail.save()
					except KeyError:
						pass

					if a.allow_drinks == True:
						if not item['soft_drinks'] == '':
							drink = OrderDetail(
												item=this_detail.item,
												arepa_type='Drink',
												product_selected=product.objects.get(pk=item['soft_drinks']),
												order_number=Order.objects.get(pk=this_order.id)
												)
							drink.save()
					
					item_number+=1

				# Almacenar el detalle del pago

				PayEgg_model = OrderPaymentDetail(
					order_number = this_order,
					cardholder_name = PayEgg['cardholder_name'],
					card_type = PayEgg['card_type'],
					card_number = PayEgg['card_number'],
					exp_date = PayEgg['exp_date'],
					gateway_message = PayEgg['gateway_message'],
					bank_message = PayEgg['bank_message'],
					bank_resp_code = PayEgg['bank_resp_code'],
					gateway_resp_code = PayEgg['gateway_resp_code'],
					cvv2 = PayEgg['cvv2'],
					amount = PayEgg['amount'],
					transaction_tag = PayEgg['transaction_tag'],
					transaction_type = PayEgg['transaction_type'],
					currency = PayEgg['currency'],
					correlation_id = PayEgg['correlation_id'],
					token_type = PayEgg['token_type'],
					token_value = PayEgg['token_value'],
					transaction_status = PayEgg['transaction_status'],
					validation_status = PayEgg['validation_status'],
					method = PayEgg['method'],
					transaction_id = PayEgg['transaction_id']
				)
				PayEgg_model.save()
				del request.session['data_client']
				del request.session['order_number']
				del request.session['cart']
				request.session['finish'] = True
				#send_invoice_email()
				return HttpResponseRedirect(reverse('website:thankyou'))
		else:
			context['pay_form'] = PaymentForm(request.POST)

	return render(request, 'website/invoice.html', context)

@login_required(redirect_field_name='', login_url='website:login-auth')
def thankyou(request):
    try:
    	if request.session['finish'] == True:
    		logout(request)
    		del request.session
    		return render(request, 'website/thankyou.html')
    except KeyError:
    	return HttpResponseRedirect(reverse('website:userlogout'))

class GuestLogin(CreateView):
	model = GuestDetail
	fields = ('firstname','lastname','email','phone')
	success_url = reverse_lazy('website:menu')
	template_name = 'website/guest_login.html'
	context_object_name = 'form'

	def form_valid(self, form):
		if 'phone' in self.request.POST:
			phone = self.request.POST['phone']
		else:
			phone = ''

		self.request.session['guest'] = {
			'firstname' : self.request.POST['firstname'],
			'lastname' : self.request.POST['lastname'],
			'email' : self.request.POST['email'],
			'phone' : phone
		}

		username = load_vars('guest.user')
		password = load_vars('guest.password')

		user = authenticate(username=username, password=password)
		login(self.request, user)

		return HttpResponseRedirect(reverse('website:menu'))


def RewriteAddress(address, key):
	import googlemaps
	gmaps = googlemaps.Client(key=key)
	dest = gmaps.geocode(address)
	return dest[0]['formatted_address']


def ValidateAddress(key,origin,destination,max_miles):
    import googlemaps
    
    gmaps = googlemaps.Client(key=key)
    dest = gmaps.geocode(destination)
    directions_result = gmaps.directions(
        origin,
        dest[0]['formatted_address']
    )
    
    
    miles = directions_result[0]['legs'][0]['distance']['text'].split(' ')
    
    if  max_miles > Decimal(miles[0]):
        result = Decimal(miles[0])
    else:
        result = False

    return result

# VISA: 4788250000028291
def PaymentRaw(name,card,exp,amt,cvv,ref):
	#import required libs to generate HMAC
	import os,hashlib,hmac,time,base64,json,requests

	apiKey = str(load_vars('pay.apikey'))
	apiSecret = str(load_vars('pay.secret'))
	token = str(load_vars('pay.token'))

	if card.startswith('3'):
		cardT = 'American Express'
	elif card.startswith('4'):
		cardT = 'Visa'
	elif card.startswith('5'):
		cardT = 'Mastercard'


	payload = {
			   "merchant_ref": ref,
			   "transaction_type": "purchase",
			   "method": "credit_card",
			   "amount":amt,
			   "partial_redemption":"false",
			   "currency_code":"USD",
			   "credit_card":{"type":cardT,
			   				  "cardholder_name":name,
			   				  "card_number":card,
			   				  "exp_date":exp,
			   				  "cvv":cvv
			   				  }
			   }

	# Crypographically strong random number
	nonce = str(int(os.urandom(16).encode('hex'),16)) 

	# Epoch timestamp in milli seconds
	timestamp = str(int(round(time.time() * 1000)))

	data = apiKey + nonce + timestamp + token + str(payload)
	
	# Make sure the HMAC hash is in hex 
	hmac = hmac.new(apiSecret, msg=data, digestmod=hashlib.sha256).hexdigest()
	
	# Authorization : base64 of hmac hash 
	authorization = base64.b64encode(hmac);

	url = load_vars('pay.url')

	headers = {
			   'apikey':apiKey,
			   'Authorization':authorization,
			   'Content-type':'application/json',
			   'nonce':nonce,
			   'timestamp':timestamp,
			   'token':token
			   }

	print headers

	payment = requests.post(url, data=json.dumps(payload), headers=headers)

	response = {}
	try:
		payment.json()['Error']['messages']

	except KeyError:
		response['status'] = True
		response['object'] = payment

	else:
		Error = payment.json()['Error']['messages']
		response['status'] = False
		response['object'] = Error

	print payment.json()
	return response

def send_invoice_email():
	from django.core.mail import send_mail, BadHeaderError

	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hi!<br>
	       How are you?<br>
	       Here is the <a href="https://www.python.org">link</a> you wanted.
	    </p>
	  </body>
	</html>
	"""
	try:
		send_mail(
			'Order From Bullpen Arepas', 
			text, 
			'ingjorgecontreras@gmail.com',
			['ingjorgecontreras@gmail'], 
			fail_silently=True,
			html_message=html
		)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')