from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
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
	if PaymentBatch.objects.BullpenIsOpen() == True:
		return HttpResponseRedirect(reverse('website:menu'))

	context = {'text': WebText.objects.get_text('closed_text')}

	return render(request, 'website/closed.html', context)

def cart(cartList):

	def SumItems(items):
		sub = 0
		for price in items:
			sub += price['price']
		return sub

	def AppendItems(listA):
		thisList = [] if isinstance(listA,list) else None		
		for itemA in listA:
			item = product.objects.get(pk=itemA)
			thisList.append({'description':item.name+ ' (' + item.description + ')','price':item.price})
		return thisList

	context = {}
	context['status'] = PaymentBatch.objects.BullpenIsOpen()
	subtotal = 0
	if cartList:
		the_cart = []
		for item in cartList:
			a = product.objects.get(pk=item['product_id'])

			price = a.price
			
			qtty = item.get('qtty',1)
			
			extras = AppendItems(item['extras']) \
					 if item['extras'] and a.allow_extras else None

			vegetables = AppendItems(item['vegetables']) \
						 if item['vegetables'] and a.allow_vegetables == True else None

			paid_extras = AppendItems(item['paid_extras']) \
						  if item['paid_extras'] and a.allow_paid_extras else None

			sauces = AppendItems(item['sauces']) \
					 if item['sauces'] and a.allow_sauces else None

			subtotal_extras = SumItems(extras) if not extras == None else 0
			subtotal_vegetables = SumItems(vegetables) if not vegetables == None else 0
			subtotal_paid_extras = SumItems(paid_extras) if not paid_extras == None else 0
			subtotal_sauces = SumItems(sauces) if not sauces == None else 0

			the_cart.append({
				'product': a,'type': item['type'],'extras' : extras,
				'vegetables': vegetables,'paid_extras': paid_extras,
				'sauces': sauces, 'drink': item['soft_drinks'],
				'qtty': qtty,
				'price': int(qtty)*(subtotal_extras + subtotal_vegetables + subtotal_paid_extras + subtotal_sauces + price),
				'unit_price':subtotal_extras + subtotal_vegetables + subtotal_paid_extras + subtotal_sauces + price
			})

			subtotal += (subtotal_extras + subtotal_vegetables + subtotal_paid_extras + subtotal_sauces + price)*int(qtty)

		amounts = {
			'subtotal': subtotal,
			'delivery' : GenericVariable.objects.val('delivery.cost'),
		}

		context['amounts'] = amounts
		context['cart'] = the_cart
		context['cart_is_empty'] = False
		print subtotal

	else:
		context['cart_is_empty'] = True

	return context
###############################################################################
# NUEVO #
###############################################################################
class MenuHome(ListView):
	model = category
	template_name = 'website/wizard/step1.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return category.objects.filter(Active=True, show_in_menu=True)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MenuHome, self).get_context_data(**kwargs)
		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None
		return context

class CategoryProductsList(ListView):
	model = category
	template_name = 'website/wizard/step2.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return get_list_or_404(category, Active=True, show_in_menu=True)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CategoryProductsList, self).get_context_data(**kwargs)
		context['products'] = get_list_or_404(product, Active=True, category=self.kwargs['pk'])
		context['selected'] = str(self.kwargs['pk'])
		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None
		return context

class MealForm(FormView):
	template_name = 'website/wizard/step3_new2.html'
	form_class = ArepaForm
	success_url = reverse_lazy('website:menu')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MealForm, self).get_context_data(**kwargs)
		
		context['product'] = get_object_or_404(product, Active=True, 
											   category=self.kwargs['pk_cat'], 
											   pk=self.kwargs['pk_prod'])
		
		context['categories'] = get_list_or_404(category, Active=True, 
											    show_in_menu=True)
		
		context['selected'] = str(self.kwargs['pk_cat'])
		context['wizard'] = product.NeedWizard(self.kwargs['pk_prod'])
		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None
		return context

	def form_valid(self, form, **kwargs):
		'''
		Se obtienen los valores del POST, si no son encontrados
		o no existen el valor por defecto es None.

		Para el caso de los Check de Vegetales y Salsas se validan si
		estan checked para no tomar en cuenta cualquier valor que venga
		en el POST.

		Al final se obtiene el valor de qtty, si viene se asigna el valor
		de lo contrario se asigna 1. Luego se repite tantan veces se
		encuentre (o no) y se suma el item en el carrito local.

		El carrito local se asigna de nuevo al de la sesion y finaliza la
		funcion.
		'''
		thisProduct = get_object_or_404(product, Active=True, 
										category=self.kwargs['pk_cat'], 
										pk=self.kwargs['pk_prod'])

		NoVegetables = self.request.POST.get('NoVegetablesCheck', None)
		vegetables = self.request.POST.getlist('vegetables', None) \
					 if not NoVegetables == 'on' else None
		
		NoSauce = self.request.POST.get('NoSaucesCheck', False)
		sauces = self.request.POST.getlist('sauces', None) \
				 if not NoSauce == 'on' else None

		NoExtras = self.request.POST.get('NoExtrasCheck', False)
		extras = self.request.POST.getlist('paid_extras', None) \
				 if not NoExtras == 'on' else None
		
		main_product =  True if thisProduct.category.show_in_menu == True else False

		item = {
			'type': self.request.POST.get('arepa_type', thisProduct.category.name),
			'product_id':self.request.POST['id_for_product'],
			'arepa_type':self.request.POST.get('arepa_type', thisProduct.category.name),
			'vegetables':vegetables,
			'extras':self.request.POST.getlist('extras', None),
			'paid_extras':extras,
			'sauces':sauces,
			'soft_drinks':self.request.POST.get('soft_drinks', None),
			'main_product':main_product,
			'qtty': self.request.POST.get('qtty',1)
			}

		local_cart = self.request.session.get('cart', [])
		
		local_cart.append(item)

		self.request.session['cart'] = local_cart

		return super(MealForm, self).form_valid(form)
		
@login_required(login_url='website:login-auth')
def pre_checkout(request):
	context = {}
	context['categories'] = get_list_or_404(category, Active=True,
			                                show_in_menu=True)

	context['cart'] = cart(request.session['cart']) \
						  if 'cart' in request.session else None

	if context['cart'] == None:
		return HttpResponseRedirect(reverse('website:menu'))

	if PaymentBatch.objects.BullpenIsOpen() == False:
		return HttpResponseRedirect(reverse('website:closed'))

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
				return render(request, 'website/wizard/pre_checkout.html', context)

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
				return render(request, 'website/wizard/pre_checkout.html', context)
		
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
				return render(request, 'website/wizard/pre_checkout.html', context)
		else:
			return Http404("Wrong Way, Bad Request")
	else:
		context['form_delivery'] = PreCheckoutForm_Delivery(initial={ 'type_of_sale': 'D' })
		context['form_pickitup'] = PreCheckoutForm_PickItUp(initial={ 'type_of_sale': 'P' })
		context['form_parkinglot'] = PreCheckoutForm_ParkingLot(initial={ 'type_of_sale': 'PL' })
		context['default_type_of_sale'] = 'D'
		return render(request, 'website/wizard/pre_checkout.html', context)

@login_required(login_url='website:login-auth')
def checkout(request):
	context = {}
	context['categories'] = get_list_or_404(category, Active=True,
			                                show_in_menu=True)

	context['cart'] = cart(request.session['cart']) \
					  if 'cart' in request.session else None

	if context['cart'] == None:
		return HttpResponseRedirect(reverse('website:menu'))

	if PaymentBatch.objects.BullpenIsOpen() == False:
		return HttpResponseRedirect(reverse('website:closed'))

	if 'data_client' in request.session:
		context['data_client'] = request.session['data_client']
	else:
		return HttpResponseRedirect(reverse('website:pre_checkout'))

	if 'guest' in request.session:
		context['guest'] = request.session['guest']

	context['tax'] = context['data_client']['tax_percent']

	subtotal = Decimal(context['cart']['amounts']['subtotal'])
	tax = context['data_client']['tax_percent']
	delivery = int(GenericVariable.objects.val('delivery.cost'))

	context['taxAmt'] = Decimal(tax*(subtotal + delivery))/100 \
						if context['data_client']['type_of_sale'] == 'D' \
						else Decimal(tax*subtotal)/100
	
	context['totalAmt'] = subtotal + context['taxAmt'] + delivery \
						  if context['data_client']['type_of_sale'] == 'D' \
						  else subtotal + context['taxAmt']

	if not 'order_number' in request.session:
		request.session['order_number'] = get_order_number()
	
	context['order_number'] = request.session['order_number']
	context['pay_form'] = PaymentForm()

	if request.POST:
		payment = PaymentForm(request.POST)

		if payment.is_valid():
			exp = request.POST['expiry'].replace('/', '')
			value = round(context['totalAmt'],2)
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
						sub_amt=subtotal,
						tax_amt=context['taxAmt'],
						delivery_amt=0,
						total_amt=context['totalAmt']
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
						sub_amt=subtotal,
						tax_amt=context['taxAmt'],
						delivery_amt=0,
						total_amt=context['totalAmt']
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
						sub_amt=subtotal,
						tax_amt=context['taxAmt'],
						delivery_amt=Decimal(GenericVariable.objects.val('delivery.cost')),
						total_amt=context['totalAmt']
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
				send_invoice_email(this_order,AddressForEmail,context['cart'])
				return HttpResponseRedirect(reverse('website:thankyou'))
		else:
			context['pay_form'] = PaymentForm(request.POST)

	return render(request, 'website/wizard/invoice.html', context)

class GuestLogin(CreateView):
	model = GuestDetail
	fields = ('firstname','lastname','email','phone')
	template_name = 'website/wizard/guest_login.html'
	context_object_name = 'form'

	def get_context_data(self, **kwargs):
	    context = super(GuestLogin, self).get_context_data(**kwargs)
	    context['next'] = self.request.GET.get('next','')
	    return context

	def form_valid(self, form):
		username = GenericVariable.objects.val('guest.user')
		password = GenericVariable.objects.val('guest.password')

		user = authenticate(username=username, password=password)
		login(self.request, user)

		phone = self.request.POST.get('phone','')
		self.request.session['guest'] = {
			'firstname' : self.request.POST['firstname'],
			'lastname' : self.request.POST['lastname'],
			'email' : self.request.POST['email'],
			'phone' : phone
		}

		return HttpResponseRedirect(self.request.POST.get('next',reverse('website:pre_checkout')))

class CreateAcct(FormView):
	template_name = 'website/wizard/create-acct.html'
	form_class = CreateAccountForm

	def get_context_data(self, **kwargs):
	    context = super(CreateAcct, self).get_context_data(**kwargs)
	    context['next'] = self.request.GET.get('next','')
	    return context

	def form_valid(self, form, **kwargs):
		from django.contrib.auth.models import User
		user = User.objects.create_user(
			username = self.request.POST['username'],
			password = self.request.POST['password'],
			email = self.request.POST['email'],
			first_name = self.request.POST['firstname'],
			last_name = self.request.POST['lastname']
			)
		user.save()
		username = self.request.POST['username']
		password = self.request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		return HttpResponseRedirect(self.request.POST.get('next',reverse('website:pre_checkout')))

###############################################################################
def empty_cart(request):
	if 'cart' in request.session:
		del request.session['cart']
	if 'order_number' in request.session:
		del request.session['order_number']
	return HttpResponseRedirect(reverse('website:menu'))

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
		del request.session['cart']
		return HttpResponseRedirect(reverse('website:menu'))
	else:
		return HttpResponseRedirect(reverse('website:menu'))


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
def thankyou(request):
    return render(request,'website/thankyou.html')

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

def send_invoice_email(order,email,cart):
	text = "Your Order "+order.order_number+" have been recived\nThank you...\nAny Questions?\nWrite us at support@bullpenarepas.com\nCall us at (404) 643 2568"
	html = render_to_string('website/wizard/email_template.html',{'cart':cart,'order':order})
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