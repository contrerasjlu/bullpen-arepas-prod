from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView, ListView
from django.core.mail import send_mail, BadHeaderError
from random import randint
from datetime import *
from decimal import Decimal
from ordertogo.models import *
from website.models import *
from .forms import *

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

	# Validate if there are stores open
	context['status'] = PaymentBatch.objects.BullpenIsOpen()

	# Initiates the Information Form
	context['form'] = WebInfoForm()
	
	# Collecting Texts
	texts = WebText.objects.filter(active=True)
	
	# Wrapping the text out
	for text in texts:
		context[text.code] = text.text

	# Collecting Menu
	context['categories'] = WebCategory.objects.filter(active=True).order_by('order')
	
	# Collecting Data for the carrousel
	context['WebImages'] = WebCarrousel.objects.filter(active=True).order_by('order')

	if request.POST:
		info = WebInfoForm(request.POST)
		if info.is_valid():
			info.save()

			# Indicator for the success of the Information Form
			context['success'] = True

			# Restore the Form, keeping the re-submitting out of bussiness
			context['form'] = WebInfoForm()
		else:
			context['WebInfoForm'] = WebInfoForm(request.POST)

	return render(request, 'website/index.html', context)

def closed(request):
	context = {}
	if PaymentBatch.objects.BullpenIsOpen() == True:
		return HttpResponseRedirect(reverse('website:menu'))

	context['text'] = WebText.objects.get_text('closed_text')
	return render(request, 'website/closed.html', context)

def cart(request):
	context = {}
	context['status'] = PaymentBatch.objects.BullpenIsOpen()

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
					the_vegetables = None
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
					the_paid_extras = None
			else:
				the_paid_extras = 0

			if a.allow_sauces == True:
				if not item['sauces'] == None:
					the_sauces = []
					for sauce in item['sauces']:
						d = product.objects.get(pk=sauce)
						the_sauces.append(d.name + ' (' + d.description + ')')

				else:
					the_sauces = None
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
			'delivery' : GenericVariable.objects.val('delivery.cost'),
		}

		context['amounts'] = amounts
		context['cart'] = the_cart
		context['cart_is_empty'] = False

	else:
		context['item_count'] = 0
		context['cart_is_empty'] = True

	return context
###############################################################################
# NUEVO #
###############################################################################
class MenuHome(ListView):
	model = category
	template_name = 'website/menu.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return category.objects.filter(Active=True, show_in_menu=True).order_by('order')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MenuHome, self).get_context_data(**kwargs)
		return context

def CategoryProductsList2(request, pk):
	context = {}
	context['categories'] = get_list_or_404(category, Active=True, show_in_menu=True)
	context['products'] = get_list_or_404(product, Active=True, category=pk)
	context['selected'] = pk
	context['form'] = ArepaForm()
	return render(request, 'website/category.html', context)

class CategoryProductsList(ListView):
	model = category
	template_name = 'website/category.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return category.objects.filter(Active=True, show_in_menu=True).order_by('order')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CategoryProductsList, self).get_context_data(**kwargs)
		context['products'] = get_list_or_404(product, Active=True, category=self.kwargs['pk'])
		context['selected'] = str(self.kwargs['pk'])
		context['form'] = ArepaForm()
		return context

	def get_form(self):
		return HttpResponseRedirect(reverse('website:menu'))

###############################################################################
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
				addr_compose = "%s, %s, GA, %s" % (request.POST['address'],request.POST['city'],request.POST['zip_code'])
				near = 0
				for location in origins:
					valid = ValidateAddress(
											GenericVariable.objects.val('google.API.KEY'),
											location.address_for_truck,
											addr_compose,
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

				realOrigin = PaymentBatch.objects.get(pk=near_batch)
				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'Delivery',
					'batch': near_batch,
					'tax_percent':realOrigin.tax_percent,
					'address': RewriteAddress(
											  addr_compose,
											  GenericVariable.objects.val('google.API.KEY')
											  ),
					'address2': request.POST['address2']
				}
				return HttpResponseRedirect(reverse('website:checkout'))
			else:
				context['form_delivery'] = PreCheckoutForm_Delivery(request.POST)
				context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
				context['form_parkinglot'] = PreCheckoutForm_ParkingLot(initial={ 'type_of_sale': 'PL' })
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
				context['form_parkinglot'] = PreCheckoutForm_ParkingLot(initial={ 'type_of_sale': 'PL' })
				context['default_type_of_sale'] = 'P'
				return render(request, 'website/pre_checkout.html', context)
		
		elif request.POST['type_of_sale'] == 'PL':
			data_client = PreCheckoutForm_ParkingLot(request.POST)
			if data_client.is_valid():
				location_desc =  PaymentBatch.objects.get(location_id=request.POST['location'], status='O')

				request.session['data_client'] = {
					'type_of_sale': request.POST['type_of_sale'],
					'label_for_type_of_sale': 'I\'m at the Parking Lot',
					'location': request.POST['location'],
					'location_desc' : location_desc.address_for_truck,
					'tax_percent': location_desc.tax_percent,
					'car_brand' : request.POST['car_brand'],
					'car_model' : request.POST['car_model'],
					'car_color' : request.POST['car_color'],
					'car_license' : request.POST['car_license'],
				}
				return HttpResponseRedirect(reverse('website:checkout'))
			else:
				context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
				context['form_delivery'] = PreCheckoutForm_Delivery(initial={ 'type_of_sale': 'D' })
				context['form_parkinglot'] = PreCheckoutForm_ParkingLot(request.POST)
				context['default_type_of_sale'] = 'PL'
				return render(request, 'website/pre_checkout.html', context)
		else:
			return Http404("Wrong Way, Bad Request")
	else:
		context['form_delivery'] = PreCheckoutForm_Delivery(initial={ 'type_of_sale': 'D' })
		context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
		context['form_parkinglot'] = PreCheckoutForm_ParkingLot(initial={ 'type_of_sale': 'PL' })
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
	else:
		return HttpResponseRedirect(reverse('website:pre_checkout'))

	context['tax'] = context['data_client']['tax_percent']
	context['amounts']['tax'] = Decimal(context['tax']*context['amounts']['subtotal']) / 100 
	context['amounts']['total'] = context['amounts']['subtotal'] + context['amounts']['tax']
	if context['data_client']['type_of_sale'] == 'D':
		context['amounts']['total'] += int(GenericVariable.objects.val('delivery.cost'))

	if not 'order_number' in request.session:
		request.session['order_number'] = get_order_number()
	
	context['order_number'] = request.session['order_number']
	context['pay_form'] = PaymentForm()

	if request.POST:
		payment = PaymentForm(request.POST)

		if payment.is_valid():
			exp = request.POST['expiry'].replace('/', '')
			value = round(context['amounts']['total'],2)
			value = str(value)
			valueTry = str(value).split(".")
			if len(valueTry[1]) == 1:
				value += "0"
			value = value.replace('.','')
			ref = 'Order #'+str(context['order_number'])

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
				PayEgg = {}

				try:
					PayEgg['cardholder_name'] = pay['object'].json()['card']['cardholder_name']
				except KeyError:
					PayEgg['cardholder_name'] = 'Not Available'

				try:
					PayEgg['card_type'] = pay['object'].json()['card']['type']
				except KeyError:
					PayEgg['card_type'] = 'Not Available'

				try:
					PayEgg['card_number'] = pay['object'].json()['card']['card_number']
				except KeyError:
					PayEgg['card_number'] = 'Not Available'

				try:
					PayEgg['exp_date'] = pay['object'].json()['card']['exp_date']
				except KeyError:
					PayEgg['exp_date'] = 'Not Available'

				try:
					PayEgg['gateway_message'] = pay['object'].json()['gateway_message']
				except KeyError:
					PayEgg['gateway_message'] = 'Not Available'

				try:
					PayEgg['bank_message'] = pay['object'].json()['bank_message']
				except KeyError:
					PayEgg['bank_message'] = 'Not Available'

				try:
					PayEgg['bank_resp_code'] = pay['object'].json()['bank_resp_code']
				except KeyError:
					PayEgg['bank_resp_code'] = 'Not Available'

				try:
					PayEgg['gateway_resp_code'] = pay['object'].json()['gateway_resp_code']
				except KeyError:
					PayEgg['gateway_resp_code'] = 'Not Available'

				try:
					PayEgg['cvv2'] = pay['object'].json()['cvv2']
				except KeyError:
					PayEgg['cvv2'] = 'Not Available'

				try:
					PayEgg['amount'] = pay['object'].json()['amount']
				except KeyError:
					PayEgg['amount'] = 'Not Available'
				
				try:
					PayEgg['transaction_tag'] = pay['object'].json()['transaction_tag']
				except KeyError:
					PayEgg['transaction_tag'] = 'Not Available'

				try:
					PayEgg['transaction_type'] = pay['object'].json()['transaction_type']
				except KeyError:
					PayEgg['transaction_type'] = 'Not Available'
				
				try:
					PayEgg['currency'] = pay['object'].json()['currency']
				except KeyError:
					PayEgg['currency'] = 'Not Available'

				try:
					PayEgg['correlation_id'] = pay['object'].json()['correlation_id']
				except KeyError:
					PayEgg['correlation_id'] = pay['object'].json()['correlation_id']

				try:
					PayEgg['token_type'] = pay['object'].json()['token']['token_type']
				except KeyError:
					PayEgg['token_type'] = 'Not Available'

				try:
					PayEgg['token_value'] = pay['object'].json()['token']['token_data']['value']
				except KeyError:
					PayEgg['token_value'] = 'Not Available'

				try:
					PayEgg['transaction_status'] = pay['object'].json()['transaction_status']
				except KeyError:
					PayEgg['transaction_status'] = 'Not Available'

				try:
					PayEgg['validation_status'] = pay['object'].json()['validation_status']
				except KeyError:
					PayEgg['validation_status'] = 'Not Available'

				try:
					PayEgg['method'] = pay['object'].json()['method']
				except KeyError:
					PayEgg['method'] = 'Not Available'

				try:
					PayEgg['transaction_id'] = pay['object'].json()['transaction_id']
				except KeyError:
					PayEgg['transaction_id'] = 'Not Available'

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

				elif context['data_client']['type_of_sale'] == 'PL':
					Batching = PaymentBatch.objects.get(location=context['data_client']['location'], status='O')
					this_order = Order(
						order_number=context['order_number'],
						order_type=context['data_client']['type_of_sale'],
						user=request.user,
						batch=Batching,
						address=Batching.address_for_truck,
						car_brand=context['data_client']['car_brand'],
						car_model=context['data_client']['car_model'],
						car_color=context['data_client']['car_color'],
						car_license=context['data_client']['car_license'],
						time='--',
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
						adress2=context['data_client']['address2'],
						time='--',
						sub_amt=context['amounts']['subtotal'],
						tax_amt=context['amounts']['tax'],
						delivery_amt=Decimal(GenericVariable.objects.val('delivery.cost')),
						total_amt=context['amounts']['total']
					)
				else:
					return HttpResponseRedirect(reverse('website:pre_checkout'))

				this_order.save()
				AddressForEmail = this_order.user.email

				if request.user.username == GenericVariable.objects.val('guest.user'):
					guest = request.session['guest']
					this_guest = GuestDetail(
						firstname=guest['firstname'],
						lastname=guest['lastname'],
						email=guest['email'],
						phone=guest['phone'],
						order=this_order
						)
					this_guest.save()
					AddressForEmail = guest['email']
					request.session['finish'] = True

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
				send_invoice_email(this_order,AddressForEmail)
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
    	else:
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

		username = GenericVariable.objects.val('guest.user')
		password = GenericVariable.objects.val('guest.password')

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
    
    if miles[1] == 'ft':
    	result = Decimal(1)
    elif  Decimal(miles[0]) < max_miles:
        result = Decimal(miles[0])
    else:
        result = False

    return result

# VISA: 4788250000028291
def PaymentRaw(name,card,exp,amt,cvv,ref):

	import os,hashlib,hmac,time,base64,json,requests

	apiKey = str(GenericVariable.objects.val('pay.apikey')).strip()

	apiSecret = str(GenericVariable.objects.val('pay.secret')).strip()

	token = str(GenericVariable.objects.val('pay.token')).strip()

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
	payload = json.dumps(payload)

	# Crypographically strong random number
	nonce = str(int(os.urandom(16).encode('hex'),16)) 

	# Epoch timestamp in milli seconds
	timestamp = str(int(round(time.time() * 1000)))

	data = apiKey + nonce + timestamp + token + payload
	
	# Make sure the HMAC hash is in hex 
	hmac = hmac.new(apiSecret, msg=data, digestmod=hashlib.sha256).hexdigest()
	
	# Authorization : base64 of hmac hash 
	authorization = base64.b64encode(hmac);

	url = GenericVariable.objects.val('pay.url')

	headers = {
			   'apikey':apiKey,
			   'Authorization':authorization,
			   'Content-type':'application/json',
			   'nonce':nonce,
			   'timestamp':timestamp,
			   'token':token
			   }

	payment = requests.post(url, data=payload, headers=headers)

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

	return response

def send_invoice_email(order,email):
	text = "Your Order "+order.order_number+" have been recived\nThank you...\nAny Questions?\nWrite us at support@bullpenarepas.com\nCall us at (404) 643 2568"
	html = """\
	<html>
		<head></head>
		<body>
			<p>Your Order #"""+order.order_number+""" have been recived</p>
			<p>Thank you... </p>
			<p>Any Questions?</p> 
			<p>Write us at support@bullpenarepas.com</p>
			<p>Call us at (404) 643 2568</p>
		</body>
	</html>
	"""
	try:
		send_mail(
			'Your Order #'+ order.order_number +' From bullpenarepas.com', 
			text,
			'Bullpen Arepas <do-not-reply@bullpenarepas.com>', #From Email
			[email], #To Email
			fail_silently=False,
			html_message=html
		)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')