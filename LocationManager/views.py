from django.shortcuts import render, get_list_or_404, get_object_or_404
from ordertogo.models import *
from LocationManager.models import *
from django.db.models import Count, Case, When, Value, Sum, Max, Min
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from random import randint
from datetime import *
#from .forms import *
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView
from decimal import Decimal

def load_vars(code):
	code = GenericVariable.objects.get(code=code)
	return code.value

def auth(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('LocationManager:index'))
		else:
			msg = loadMsj("invalid.credential")
			return render(request, 'LocationManager/login.html', {'msg': msg})

	return render(request, 'LocationManager/login.html')

def load_menu():
	menu = location_admin_menu.objects.all().order_by('order')
	return menu

@login_required(redirect_field_name='', login_url='/location/login')
def index(request):
	context = {}
	context['menu'] = load_menu()
	context['locations'] = LocationsAvailable.objects.all()[:5]
	context['batches'] = PaymentBatch.objects.filter(status='O', open_for_delivery=True).order_by('date').order_by('status')[:5]
	return render(request, 'LocationManager/index.html', context)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('LocationManager:index'))

class LocationsList(ListView):
	model = LocationsAvailable
	template_name = 'LocationManager/locations.html'
	context_object_name = 'locations'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LocationsList, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		return context

class BatchesList(ListView):
	template_name = 'LocationManager/batches.html'
	context_object_name = 'PaymentBatch_Open'
	queryset = PaymentBatch.objects.filter(status='O').order_by('date')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BatchesList, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		context['PaymentBatch_Closed'] = PaymentBatch.objects.filter(status='C').order_by('date')[:30]
		return context

class BatchesCreate(CreateView):
	model = PaymentBatch
	fields = ['location', 'address_for_truck', 'zip_code_for_truck', 'max_miles', 'batch_code', 'open_for_delivery']
	success_url = reverse_lazy('LocationManager:batches-list')
	template_name = 'LocationManager/paymentbatch_form.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BatchesCreate, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context

class BatchesUpdate(UpdateView):
	model = PaymentBatch
	fields = ['status', 'location', 'address_for_truck', 'zip_code_for_truck', 'max_miles', 'batch_code', 'open_for_delivery', 'status']
	success_url = reverse_lazy('LocationManager:batches-list')
	template_name = 'LocationManager/paymentbatch_form.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BatchesUpdate, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context

class orders(ListView):
	template_name = 'LocationManager/orders.html'
	context_object_name = 'batches'
	model = PaymentBatch

	def get_queryset(self):
		return PaymentBatch.objects.filter(status='O', open_for_delivery=True).annotate(
			paid=Count(Case(When(order__order_status='P', then='order__order_status'))),
			kitchen=Count(Case(When(order__order_status='K', then='order__order_status'))),
			out_for_delivery=Count(Case(When(order__order_status='O', then='order__order_status'))),
			delivered=Count(Case(When(order__order_status='D', then='order__order_status'))),
		)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(orders, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context

class HandleOrders(ListView):
	template_name = 'LocationManager/orders_filtered.html'
	context_object_name = 'Orders'
	model = Order

	def get_queryset(self):
		return Order.objects.filter(
			order_status=self.kwargs['order_status'], 
			batch=PaymentBatch.objects.get(pk=self.kwargs['batch'])
		).order_by('-id','date')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(HandleOrders, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		context['type_view'] = self.kwargs['order_status']
		
		return context

class HandleOrderDetail(ListView):
	template_name = 'LocationManager/order_detail.html'
	context_object_name = 'OrderDetail'
	model = OrderDetail

	def get_queryset(self):
		return OrderDetail.objects.filter(order_number_id=self.kwargs['id_order']).aggregate(
			subtotal=Sum('product_selected__price'),
			tax=Sum('product_selected__price')*Decimal(load_vars('tax.percent')),
			total=Case(
					When(order_number__order_type='P', then=Sum('product_selected__price')+
															(Sum('product_selected__price')*Decimal(load_vars('tax.percent')))),
					When(order_number__order_type='D', then=Sum('product_selected__price')+
															(Sum('product_selected__price')*Decimal(load_vars('tax.percent')))+
															(Decimal(load_vars('delivery.cost')))))
			)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(HandleOrderDetail, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		context['Order'] = get_object_or_404(Order, pk=self.kwargs['id_order'])
		context['tax_value'] = Decimal(load_vars('tax.percent')) * 100
		context['delivery_cost'] = Decimal(load_vars('delivery.cost'))

		# Para deslodar el querydict del OrderDetail se tiene que ir de item en item
		# Vamos a buscar el maximo item del query y se almacena en una variable

		cart = OrderDetail.objects.filter(
				order_number_id=self.kwargs['id_order'], main_product=True).order_by('-order_number','item','-main_product')

		cart_for_context = []

		for item in cart:
			this_extras = OrderDetail.objects.filter(
				order_number_id=item.order_number_id,
				item=item.item,
				main_product=False,
				arepa_type='With'
			)
			if len(this_extras) > 0:
				EXTRAS = ''
				for extras in this_extras:
					EXTRAS = EXTRAS + extras.product_selected.name + ', '
			else:
				EXTRAS = 'Nothing'

			this_paid_extras = OrderDetail.objects.filter(
				order_number_id=item.order_number_id,
				item=item.item,
				main_product=False,
				arepa_type='Paid Extra'
			)

			subtotal = OrderDetail.objects.filter(
				order_number_id=item.order_number_id,
				item=item.item,
				main_product=False,
				arepa_type='Paid Extra'
			).aggregate(total=Sum('product_selected__price'))

			PAID_EXTRAS = ''
			if len(this_paid_extras) > 0:
				for paid in this_paid_extras:
					PAID_EXTRAS = PAID_EXTRAS + paid.product_selected.name + ', '

			this_sauces = OrderDetail.objects.filter(
				order_number_id=item.order_number_id,
				item=item.item,
				main_product=False,
				arepa_type='Sauces'
			)
			if len(this_sauces) > 0:
				SAUCES = ''
				for sauce in this_sauces:
					SAUCES = SAUCES + sauce.product_selected.name + ', '
			else:
				SAUCES = 'No Sauce'

			try:
				this_drinks = OrderDetail.objects.get(
					order_number_id=item.order_number_id,
					item=item.item,
					main_product=False,
					arepa_type='Drink'
				)
			except OrderDetail.DoesNotExist:
				DRINK = 'No Drink'
				drink_price = 0
			else:
				DRINK = this_drinks.product_selected.name
				drink_price = Decimal(this_drinks.product_selected.price)

			sub = Decimal(item.product_selected.price) + drink_price
			if subtotal['total']:
				sub += Decimal(subtotal['total'])
			this_item = {
			'item': item.item,
			'product':item.product_selected.name,
			'code': item.product_selected.code,
			'description': item.arepa_type + ' WITH: ' + EXTRAS + ' EXTRAS: ' + PAID_EXTRAS + ' SAUCES: ' + SAUCES + ' DRINK: ' + DRINK,
			'subtotal' : sub
			}
			cart_for_context.append(this_item)

		context['invoice'] = cart_for_context
		
		return 

@login_required(redirect_field_name='', login_url='/location/login')
def CloseBatch(request, batch):
	batch = PaymentBatch.objects.get(pk=batch)
	batch.status = 'C'
	batch.save()
	return HttpResponseRedirect(reverse('LocationManager:batches-list'))

@login_required(redirect_field_name='', login_url='/location/login')
def CloseBatchDelivery(request, batch):
	batch = PaymentBatch.objects.get(pk=batch)
	batch.open_for_delivery = False
	batch.save()
	return HttpResponseRedirect(reverse('LocationManager:batches-list'))

class LocationsAvailableCreateView(CreateView):
    model = LocationsAvailable
    template_name = "LocationManager/location_form.html"
    fields = ['description','location','zip_code']
    success_url = reverse_lazy('LocationManager:locations-list')

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LocationsAvailableCreateView, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context

class LocationsAvailableUpdateView(UpdateView):
    model = LocationsAvailable
    template_name = "LocationManager/location_form.html"
    fields = ['description','location','zip_code']
    success_url = reverse_lazy('LocationManager:locations-list')

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LocationsAvailableUpdateView, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context