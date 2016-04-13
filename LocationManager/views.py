from django.shortcuts import render, get_list_or_404, get_object_or_404
from ordertogo.models import *
from LocationManager.models import *
from django.db.models import Count, Case, When, Value, Sum, Max, Min
from django.http import Http404,HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.core.urlresolvers import reverse, reverse_lazy
from random import randint
from datetime import *
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from decimal import Decimal

################# Funciones Genericas #######################
# 1. load_menu: Funcion generica para cargar el menu del sitio 
#               de LocationManager
##############################################################

# 
def load_menu():
	menu = location_admin_menu.objects.all().order_by('order')
	return menu

################## Autenticacion #############################
# 1. Auth: Funcion para la autenticacion del usuario en 
#          LocationManager
#
# 2. logout_user: Salir de la sesion
#############################################################

# TODO: Buscar la forma generica de estas funciones no se necesita nada especial, adicionalemente
#       se puede manipular para que funcione como un TemplateView

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

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('LocationManager:index'))

# Pagina Principal
@login_required(redirect_field_name='', login_url='LocationManager:auth')
def index(request):
	context = {}
	context['menu'] = load_menu()
	context['locations'] = LocationsAvailable.objects.all()[:5]
	context['batches'] = PaymentBatch.objects.filter(status='O', open_for_delivery=True).order_by('date').order_by('status')[:5]
	return render(request, 'LocationManager/index.html', context)

###################### Modelo Locations Available #######################
# 1. LocationList: Vista de Lista de los Locationsavailable
#
# 2. LocationAvailableCreateView: Vista del formulario de creacion 
#    de registros del modelo LocationsAvailable
#
# 3. LocationsAvailableUpdateView: Vista del formulario de 
#    actualizacion de registros del modelo LocationsAvailable
########################################################################
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

class LocationsAvailableCreateView(CreateView):
    model = LocationsAvailable
    template_name = "LocationManager/location_form.html"
    fields = ['description','location','zip_code','merchant_ref']
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
    fields = ['description','location','zip_code','merchant_ref']
    success_url = reverse_lazy('LocationManager:locations-list')

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(LocationsAvailableUpdateView, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()		
		return context

###################### Modelo Payment Batches #######################
# 1. BatchesList: Vista de Lista de los Payment Batches abiertos y cerrados
#
# 2. BatchesCreate: Vista del formulario de creacion de registros 
#    del modelo Payment Batches
#
# 3. BatchesUpdate: Vista del formulario de actualizacion de registros 
#    del modelo LocationsAvailable
########################################################################
class BatchesList(ListView):
	template_name = 'LocationManager/batches.html'
	context_object_name = 'PaymentBatch_Open'
	queryset = PaymentBatch.objects.filter(status='O').order_by('date')

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BatchesList, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		context['PaymentBatch_Closed'] = PaymentBatch.objects.filter(status='C').order_by('-close_date')[:30]
		return context

class BatchesCreate(CreateView):
	model = PaymentBatch
	fields = ['location', 'address_for_truck', 'zip_code_for_truck', 'tax_percent', 'max_miles', 'batch_code', 'notifier', 'open_for_delivery']
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
	fields = ['status', 'location', 'address_for_truck', 'zip_code_for_truck', 'tax_percent', 'max_miles', 'batch_code', 'notifier', 'open_for_delivery', 'Group', 'status']
	success_url = reverse_lazy('LocationManager:batches-list')
	template_name = 'LocationManager/paymentbatch_form.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(BatchesUpdate, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		return context

###################### Modelo Payment Batches #######################
# 1. BatchesList: Vista de Lista de los Payment Batches abiertos y cerrados
#
# 2. BatchesCreate: Vista del formulario de creacion de registros 
#    del modelo Payment Batches
#
# 3. BatchesUpdate: Vista del formulario de actualizacion de registros 
#    del modelo LocationsAvailable
########################################################################
class orders(ListView):
	template_name = 'LocationManager/orders.html'
	context_object_name = 'batches'
	model = PaymentBatch

	def get_queryset(self):
		return PaymentBatch.objects.filter(status='O').annotate(
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
		try:
			detail = OrderDetail.objects.filter(order_number_id=self.kwargs['pk'])
		
		except OrderDetail.DoesNotExist:
			return Http404('Wrong way')

		return detail

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(HandleOrderDetail, self).get_context_data(**kwargs)
		# Add Menu
		context['menu'] = load_menu()
		context['Order'] = get_object_or_404(Order, pk=self.kwargs['pk'])
		context['delivery_cost'] = Decimal(GenericVariable.objects.val('delivery.cost'))

		cart = OrderDetail.objects.filter(
				order_number_id=self.kwargs['pk'], main_product=True
				).order_by('-order_number','item','-main_product')

		if context['Order'].user.username == GenericVariable.objects.val('guest.user'):
			context['guest'] = get_object_or_404(GuestDetail, order=context['Order'])

		
		def MakeDescription(Separator, Item):
			ThisSeparatorQuery = Item.filter(arepa_type=Separator)
			SeparatorList = ()
			if ThisSeparatorQuery.count() == 0:
				return ' | %s: No %s' % (Separator.upper(), Separator)
			for ThisSeparator in ThisSeparatorQuery:
				SeparatorList += ThisSeparator.product_selected.name,
			return ' | %s: %s' % (Separator.upper(),(', ').join(SeparatorList))

		cart_for_context = []

		for item in cart:
			ItemDescription = ''
			Subtotal = OrderDetail.objects.filter(order_number_id=item.order_number_id, item=item.item).aggregate(total=Sum('product_selected__price'))
			ThisItem = OrderDetail.objects.filter(item=item.item, order_number_id=item.order_number_id)

			# Select Meats
			if item.product_selected.allow_extras:
				ItemDescription += '%s ' % MakeDescription('With',ThisItem)

			# Select Additionals
			if item.product_selected.allow_additionals:
				ItemDescription += '%s ' % MakeDescription('Additionals', ThisItem)

			# Select Vegetables
			if item.product_selected.allow_vegetables:
				ItemDescription += '%s ' % MakeDescription('Vegetables', ThisItem)

			# Select Paid Extras
			if item.product_selected.allow_paid_extras:
				ItemDescription += '%s ' % MakeDescription('Extras', ThisItem)

			# Select Sauces
			if item.product_selected.allow_sauces:
				ItemDescription += '%s ' % MakeDescription('Sauces', ThisItem)

			if item.product_selected.allow_drinks:
				ItemDescription += '%s ' % MakeDescription('Drink', ThisItem)

			this_item = {
			'item': item.item,
			'product':item.product_selected.name,
			'code': item.product_selected.code,
			'description': '%s %s' % (item.arepa_type, ItemDescription),
			'subtotal' : Subtotal['total']
			}
			cart_for_context.append(this_item)

		context['invoice'] = cart_for_context
		
		return context

@login_required(redirect_field_name='', login_url='LocationManager:auth')
def OrderUpdate(request, pk):
	order = get_object_or_404(Order, pk=pk)

	# Si la orden esta en incommig va para la concina
	if order.order_status=='P':
		order.order_status = 'K'
		order.save()
		return HttpResponseRedirect(reverse('LocationManager:orders'))
	
	# Si la orden es Pick it Up
	if order.order_type == 'P' and order.order_status == 'K':
		order.order_status = 'D'
		order.save()
		return HttpResponseRedirect(reverse('LocationManager:orders'))

	# Si la orden es Delivered
	elif order.order_type == 'D' and order.order_status == 'K':
		order.order_status='O'
		order.save()
		return HttpResponseRedirect(reverse('LocationManager:orders'))

	# Si la orden estan en Out For Delivery para Delivery
	if order.order_status=='O':
		order.order_status='D'
		order.save()
		return HttpResponseRedirect(reverse('LocationManager:orders'))

	# Si la orden ya fue entregada, 404
	if order.order_status=='D':
		return HttpResponseRedirect(reverse('LocationManager:orders'))

@login_required(redirect_field_name='', login_url='LocationManager:auth')
def CloseBatch(request, batch):
	batch = get_object_or_404(PaymentBatch, pk=batch)
	batch.status = 'C'
	batch.save()
	return HttpResponseRedirect(reverse('LocationManager:batches-list'))

@login_required(redirect_field_name='', login_url='LocationManager:auth')
def CloseBatchDelivery(request, batch):
	batch = get_object_or_404(PaymentBatch, pk=batch)
	batch.open_for_delivery = False
	batch.save()
	return HttpResponseRedirect(reverse('LocationManager:batches-list'))

@login_required(redirect_field_name='', login_url='LocationManager:auth')
def BatchesReport(request, pk):
	from datetime import datetime, date, timedelta
	context = {}
	context['menu'] = load_menu()
	order = get_object_or_404(PaymentBatch, pk=pk)
	context['batch'] = order
	context['hours'] = order.close_date - order.date
	context['calc_orders'] = Order.objects.filter(batch_id=pk).aggregate(
		total=Count('id'),
		revenue=Sum('total_amt'),
		tax=Sum('tax_amt'),
		delivery_amt=Sum('delivery_amt'),
		delivery_order=Count(Case(When(order_type='D', then='order_type'))),
		pickitup=Count(Case(When(order_type='P', then='order_type'))))

	return render(request, 'LocationManager/report.html', context)

@login_required(login_url='LocationManager:auth')
def csv(request, pk):
	from django.http import HttpResponse
	import csv
	batch = get_object_or_404(PaymentBatch, pk=pk)
	orders = Order.objects.filter(batch_id=pk)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Report-for-'+batch.batch_code+'.csv"'
	writer = csv.writer(response)
	writer.writerow(['Bullpen Arepas LLC.', 'Report for Batch:', batch.batch_code ])
	writer.writerow(['Open Date',batch.date,'Close Date',batch.close_date ])
	writer.writerow(['=========','========','==========','==============='])
	writer.writerow(['Orders'])
	writer.writerow(['Date','Type','Client','Order Number','Subtotal','Delivery','Tax','Total'])
	for order in orders:
		writer.writerow([order.date,
						 order.order_type,
						 order.user,
						 order.order_number,
						 order.sub_amt,
						 order.delivery_amt,
						 order.tax_amt,
						 order.total_amt])

	return response