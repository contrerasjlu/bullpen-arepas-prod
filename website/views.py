from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import FormView
from django.views.generic import CreateView, ListView, TemplateView
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

class AboutUsView(TemplateView):
	template_name = 'website/aboutus.html'

	def get_context_data(self, **kwargs):
	    context = super(AboutUsView, self).get_context_data(**kwargs)
	    context['status'] = PaymentBatch.objects.BullpenIsOpen()
	    return context

class OurProductsView(TemplateView):
	template_name = 'website/ourproducts.html'

	def get_context_data(self, **kwargs):
	    context = super(OurProductsView, self).get_context_data(**kwargs)
	    context['status'] = PaymentBatch.objects.BullpenIsOpen()
	    return context

def index(request):
	context = {}

	# Validate if there are stores open
	context['status'] = PaymentBatch.objects.BullpenIsOpen()

	# Initiates the Information Form
	context['form'] = WebInfoForm()
	
	# Collecting Texts
	texts = WebText.objects.filter(active=True)

	#Collect the Opens Locations
	context['locations'] = PaymentBatch.GetLocationsOpen()
	
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

	return render(request, 'website/wizard/closed.html', context)

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

		context['amounts'] = {'subtotal': subtotal,
							  'delivery' : GenericVariable.objects.val('delivery.cost'),
							  }

		context['cart'] = the_cart
		context['cart_is_empty'] = False

	else:
		context['cart_is_empty'] = True

	return context
###############################################################################
# NUEVO #
###############################################################################
class PreCheckoutView(TemplateView):
	template_name = 'website/wizard/PreCheckout.html'

	def get_context_data(self, **kwargs):
		context = super(PreCheckoutView, self).get_context_data(**kwargs)

		context['locations'] = PaymentBatch.GetLocationsOpen()

		if context['locations'] is None:
			return HttpResponseRedirect(reverse('website:closed'))

		return context

class PreCheckoutDelivery(FormView):
	template_name = 'website/wizard/PreCheckoutDelivery.html'
	form_class = PreCheckoutForm_Delivery
	success_url = reverse_lazy('website:menu')

	def get_initial(self):
		initial = super(PreCheckoutDelivery, self).get_initial()
		initial['type_of_sale'] = 'D'
		return initial

	def get_context_data(self, **kwargs):
		context = super(PreCheckoutDelivery, self).get_context_data(**kwargs)

		if PaymentBatch.objects.BullpenIsOpen() == False:
			return HttpResponseRedirect(reverse('website:closed'))

		return context

	def form_valid(self, form, **kwargs):
		'''
		Return the Form Valid with the Batch that is nearest.
		All the values are saved in session:
		1. Batch: The Batch Selected as nearest
		2. TypeOfSale: with the code and the text to show.
		3. Dict for TypeOfSale: With values returned by the form.

		*** Al the logic is in the form.py file ***
		'''
		self.request.session['Batch'] = form.cleaned_data.get('NearestLocation')
		self.request.session['TypeOfSale'] = {'code':'D','text':'Delivery','icon':'fa fa-home'}
		self.request.session['D'] = {'Address':form.cleaned_data.get('address'),
									 'Address2': form.cleaned_data.get('address2',' '),
									 'City': form.cleaned_data.get('city'),
									 'ZipCode': form.cleaned_data.get('zip_code')}

		return super(PreCheckoutDelivery, self).form_valid(form)

class PreCheckoutPickItUp(FormView):
	template_name = 'website/wizard/PreCheckoutPickItUp.html'
	form_class = PreCheckoutForm_PickItUp
	success_url = reverse_lazy('website:menu')

	def get_initial(self):
		initial = super(PreCheckoutPickItUp, self).get_initial()
		initial['type_of_sale'] = 'P'
		return initial

	def get_context_data(self, **kwargs):
		context = super(PreCheckoutPickItUp, self).get_context_data(**kwargs)

		if PaymentBatch.objects.BullpenIsOpen() == False:
			return HttpResponseRedirect(reverse('website:closed'))

		return context

	def form_valid(self, form, **kwargs):
		'''
		Return the Form Valid with the Batch that is nearest.
		All the values are saved in session:
		1. Batch: The Batch Selected by user
		2. TypeOfSale: with the code and the text to show.
		3. Dict for TypeOfSale: With values returned by the form.

		*** Al the logic is in the form.py file ***
		'''
		Location = form.cleaned_data.get('location')
		self.request.session['Batch'] = Location.id
		self.request.session['TypeOfSale'] = {'code':'P','text':'Pick it Up','icon':'fa fa-bicycle'}
		self.request.session['P'] = {'Time': form.cleaned_data.get('time')}

		return super(PreCheckoutPickItUp, self).form_valid(form)

class PreCheckoutParkingLot(FormView):
	template_name = 'website/wizard/PreCheckoutParkingLot.html'
	form_class = PreCheckoutForm_ParkingLot
	success_url = reverse_lazy('website:menu')

	def get_initial(self):
		initial = super(PreCheckoutParkingLot, self).get_initial()
		initial['type_of_sale'] = 'PL'
		return initial

	def get_context_data(self, **kwargs):
		context = super(PreCheckoutParkingLot, self).get_context_data(**kwargs)

		if PaymentBatch.objects.BullpenIsOpen() == False:
			return HttpResponseRedirect(reverse('website:closed'))

		return context

	def form_valid(self, form, **kwargs):
		'''
		Return the Form Valid with the Batch that is nearest.
		All the values are saved in session:
		1. Batch: The Batch Selected by user
		2. TypeOfSale: with the code and the text to show.
		3. Dict for TypeOfSale: With values returned by the form.

		*** Al the logic is in the form.py file ***
		'''
		Location = form.cleaned_data.get('location')
		self.request.session['Batch'] = Location.id
		self.request.session['TypeOfSale'] = {'code':'PL','text':'Parking Lot','icon':'fa fa-car'}
		self.request.session['PL'] = {'CarModel':form.cleaned_data.get('car_model'),
									  'CarBrand':form.cleaned_data.get('car_brand'),
									  'CarColor':form.cleaned_data.get('car_color'),
									  'CarLicense': form.cleaned_data.get('car_license')}
		return super(PreCheckoutParkingLot, self).form_valid(form)

class MenuHome(ListView):
	model = category
	template_name = 'website/wizard/step1.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return category.GetMenu(self.request.session['Batch'])

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(MenuHome, self).get_context_data(**kwargs)
		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None

		context['Batch'] = PaymentBatch.objects.get(pk=self.request.session['Batch']) \
						   if 'Batch' in self.request.session else None

		if context['Batch'] == None:
			return HttpResponseRedirect(reverse('website:PreCheckout'))
		else:
			context['TypeOfSale'] = self.request.session['TypeOfSale']
			TypeOfSale = self.request.session['TypeOfSale']['code']
			context[TypeOfSale] = self.request.session[TypeOfSale]

		return context

class CategoryProductsList(ListView):
	model = category
	template_name = 'website/wizard/step2.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return category.GetMenu(self.request.session['Batch'])

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(CategoryProductsList, self).get_context_data(**kwargs)
		context['products'] = product.GetProducts(str(self.kwargs['pk']),self.request.session['Batch'])
		
		# If there is no Product to Show
		if context['products'] == None:
			return HttpResponseRedirect(reverse('website:menu'))


		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None

		context['Batch'] = PaymentBatch.objects.get(pk=self.request.session['Batch']) \
						   if 'Batch' in self.request.session else None
		
		if context['Batch'] == None:
			return HttpResponseRedirect(reverse('website:PreCheckout'))
		else:
			context['TypeOfSale'] = self.request.session['TypeOfSale']
			TypeOfSale = self.request.session['TypeOfSale']['code']
			context[TypeOfSale] = self.request.session[TypeOfSale]
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
		
		context['categories'] = category.GetMenu(self.request.session['Batch'])
		
		context['cart'] = cart(self.request.session['cart']) \
						  if 'cart' in self.request.session else None

		context['Batch'] = PaymentBatch.objects.get(pk=self.request.session['Batch']) \
						   if 'Batch' in self.request.session else None

		if context['Batch'] == None:
			return HttpResponseRedirect(reverse('website:PreCheckout'))
		else:
			context['TypeOfSale'] = self.request.session['TypeOfSale']
			TypeOfSale = self.request.session['TypeOfSale']['code']
			context[TypeOfSale] = self.request.session[TypeOfSale]

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

		Restriction = ProductRestriction.GetProductRestriction(thisProduct.id)

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

class ViewCartSummary(TemplateView):
	template_name = 'website/wizard/ViewCartSummary.html'

	def get_context_data(self, **kwargs):
		context = super(ViewCartSummary, self).get_context_data(**kwargs)
		context['categories'] = category.GetMenu(self.request.session['Batch'])

		if 'cart' in self.request.session:
			context['cart'] = cart(self.request.session['cart'])

		if context['cart'] == None:
			return HttpResponseRedirect(reverse('website:menu'))

		context['Batch'] = PaymentBatch.objects.get(pk=self.request.session['Batch']) \
						   if 'Batch' in self.request.session else None

		if context['Batch'] == None:
			return HttpResponseRedirect(reverse('website:PreCheckout'))
		else:
			context['TypeOfSale'] = self.request.session['TypeOfSale']
			TypeOfSale = self.request.session['TypeOfSale']['code']
			context[TypeOfSale] = self.request.session[TypeOfSale]

		return context

class Checkout(FormView):
	template_name = 'website/wizard/invoice.html'
	form_class = PaymentForm
	success_url = reverse_lazy('website:thankyou')

	def get_context_data(self, **kwargs):

		context = super(Checkout, self).get_context_data(**kwargs)

		context['cart'] = self.request.session.get('cart',None)

		if context['cart'] == None:
			return HttpResponseRedirect(reverse('website:menu'))
		else:
			context['cart'] = cart(self.request.session['cart'])

		if PaymentBatch.objects.BullpenIsOpen() == False:
			return HttpResponseRedirect(reverse('website:closed'))

		context['Batch'] = PaymentBatch.objects.get(pk=self.request.session['Batch']) \
						   if 'Batch' in self.request.session else None

		if context['Batch'] == None:
			return HttpResponseRedirect(reverse('website:PreCheckout'))
		else:
			context['TypeOfSale'] = self.request.session['TypeOfSale']
			TypeOfSale = self.request.session['TypeOfSale']['code']
			context[TypeOfSale] = self.request.session[TypeOfSale]
			context['categories'] = category.GetMenu(self.request.session['Batch'])

		context['guest'] = self.request.session['guest'] if 'guest' in self.request.session else False

		subtotal = Decimal(context['cart']['amounts']['subtotal'])
		tax = context['Batch'].tax_percent
		delivery = int(GenericVariable.objects.val('delivery.cost'))

		context['taxAmt'] = Decimal(tax*(subtotal + delivery))/100 \
							if TypeOfSale == 'D' \
							else Decimal(tax*subtotal)/100
		
		context['totalAmt'] = subtotal + context['taxAmt'] + delivery \
							  if TypeOfSale == 'D' \
							  else subtotal + context['taxAmt']

		if not 'order_number' in self.request.session:
			self.request.session['order_number'] = get_order_number()
		
		context['order_number'] = self.request.session['order_number']

		return context

	def get_form_kwargs(self, **kwargs):
		kwargs = super(Checkout, self).get_form_kwargs()
		kwargs['request'] = self.request.session
		kwargs['cart'] = self.request.session.get('cart',None)
		if not kwargs['cart'] is None:
			kwargs['cart'] = cart(self.request.session['cart'])
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form, **kwargs):
		del self.request.session['Batch']
		del self.request.session[self.request.session['TypeOfSale']['code']]
		del self.request.session['TypeOfSale']
		del self.request.session['order_number']
		del self.request.session['cart']
		return super(Checkout, self).form_valid(form)

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
		logout(self.request)
		username = GenericVariable.objects.val('guest.user')
		password = GenericVariable.objects.val('guest.password')

		user = authenticate(username=username, password=password)
		login(self.request,user)

		phone = self.request.POST.get('phone','')
		self.request.session['guest'] = {
			'firstname' : self.request.POST['firstname'],
			'lastname' : self.request.POST['lastname'],
			'email' : self.request.POST['email'],
			'phone' : phone
		}

		return HttpResponseRedirect(self.request.POST.get('next',reverse('website:PreCheckout')))

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
			login(self.request,user)
		return HttpResponseRedirect(self.request.POST.get('next',reverse('website:PreCheckout')))

class ThankYouView(TemplateView):
	"""Thank You View after a Order is complete"""
	template_name = 'website/wizard/thankyou.html'
		

###############################################################################
def empty_cart(request):
	if 'cart' in request.session:
		del request.session['cart']
	if 'order_number' in request.session:
		del request.session['order_number']
	return HttpResponseRedirect(reverse('website:menu'))

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
def userLogout(request):
    logout(request)
    next = request.GET.get('next','')
    return HttpResponseRedirect(reverse('website:login-auth'))