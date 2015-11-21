from django.shortcuts import render, get_list_or_404
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
	a = PaymentBatch.objects.filter(status="O")
	if len(a) == 0:
		return False
	else:
		return True

#Generar un numero de orden aleatorio
def get_order_number():
	t = 10000
	sure = False
	while sure == False:
		order = randint(5000, t)
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
			'total': subtotal+(subtotal* Decimal(load_vars('tax.percent')))
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
	if 'finish' in request.session:
		del request.session['finish']

	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

	arepas = product.objects.filter(Active=True,category=category.objects.get(code='arepas')).order_by('order_in_menu')
	kids = product.objects.filter(Active=True,category=category.objects.get(code='kids')).order_by('order_in_menu')
	
	context['arepas'] = arepas
	context['kids'] = kids
	try:
		return render(request, 'website/plain_page.html', context)
	except ValueError:
		return HttpResponseRedirect(reverse('website:closed'))

def ProductDetail(request,id_for_prod):
	context = cart(request);
	if context['status']==False:
		return HttpResponseRedirect(reverse('website:closed'))

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
					valid = ValidateAddress(load_vars('google.API.KEY'),location.address_for_truck,request.POST['address'],location.max_miles)
					print valid
					if not valid == False:
						if near == 0:
							near = valid
							near_batch = location.id
						elif near > valid:
							near =  valid
							near_batch = location.id

				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'Delivery',
					'batch': near_batch,
					'address': RewriteAddress(request.POST['address'], load_vars('google.API.KEY'))
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

				location_desc =  PaymentBatch.objects.get(location=request.POST['location'])

				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'Pick it Up',
					'location': request.POST['location'],
					'location_desc' : location_desc.address_for_truck,
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

@login_required(redirect_field_name='', login_url='/website/login')
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

	context['tax'] = float(load_vars('tax.percent'))*100

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
			desc = "Bullpen Arepas Order-"+str(context['order_number'])

			pay = payment_try(
				request.POST['name_on_card'],
				request.POST['card_number'], 
				exp, 
				desc, 
				value, 
				request.POST['cvv']
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
						batch=PaymentBatch.objects.get(location=context['data_client']['location']),
						address='--',
						time=context['data_client']['time'],
						sub_amt=context['amounts']['subtotal'],
						tax_amt=context['amounts']['tax'],
						delivery_amt=0,
						total_amt=context['amounts']['total']
					)
				elif context['data_client']['type_of_sale'] == 'D':
					from decimal import Decimal
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

				# Almacenar el detalle de la orden
				the_session_cart = request.session['cart']
				i=1
				for item in the_session_cart:			
					if item['type'] == 'Arepa':
						arepa_type = item['arepa_type'] + ' ' + item['type']
					else:
						arepa_type = item['type']
					a = product.objects.get(pk=item['product_id'])
					this_detail = OrderDetail(
						item=i,
						arepa_type=arepa_type,
						product_selected=a,
						order_number=this_order
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

					if not item['soft_drinks'] == '':
						drink = OrderDetail(
							item=this_detail.item,
							arepa_type='Drink',
							product_selected=product.objects.get(pk=item['soft_drinks']),
							order_number=Order.objects.get(pk=this_order.id)
						)
						drink.save()
					i+=1

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
				#send_email()
				return HttpResponseRedirect(reverse('website:thankyou'))

	return render(request, 'website/invoice.html', context)

@login_required(redirect_field_name='', login_url='website/login/')
def thankyou(request):
    try:
    	if request.session['finish'] == True:
    		return render(request, 'website/thankyou.html')
    except KeyError:
    	return HttpResponseRedirect(reverse('website:menu'))


def RewriteAddress(address, key):
	import googlemaps
	gmaps = googlemaps.Client(key=key)
	dest = gmaps.geocode(address)
	return dest[0]['formatted_address']


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
    if Decimal(miles[0]) < max_miles:
        result = Decimal(miles[0])
    else:
        result = False

    return result

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

    payeezy.apikey = str(load_vars('pay.apikey'))

    payeezy.apisecret = str(load_vars('pay.secret'))

    payeezy.token = str(load_vars('pay.token'))

    payeezy.url = load_vars('pay.url')

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

def send_email():
	import smtplib

	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	# me == my email address
	# you == recipient's email address
	me = "my@email.com"
	you = "ingjorgecontreras@gmail.com"

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Link"
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
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

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('smpt.gmail.com')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()