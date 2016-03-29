# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator, ValidationError
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from decimal import Decimal

#Modelo para almacenar las categorias de las comidas ofrecidas
class category(models.Model):
	#Codigo --  Esta en veremos si tengo chance de catchar el ID adios al codigo
	#           pudiera necesitar esto para algun parametro a tomar en cuenta
	code = models.CharField(max_length=50, unique=True)

	#Nombre de la categoria Ej Suggested Plays, Baked or Fries Arepas, etc
	#Este es el string que se muestra al publico
	name = models.CharField(max_length=50)

	#Descripcion de la categoria -- Tal vez no se necesite
	description = models.TextField(max_length=500)

	#Indicador de estado
	Active = models.BooleanField(default=True)

	#Indica si se muestra en el menu o no
	show_in_menu = models.BooleanField(default=True)

	#Indica el orden en el menu
	order = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

	@classmethod
	def GetMenu(self, Batch):
		Categories = category.objects.filter(Active=True,show_in_menu=True)
		CategoryMatrix = []
		for Category in Categories:
			Products = len(product.GetProducts(Category,Batch))
			if Products > 0:
				CategoryMatrix.append(Category)

		return CategoryMatrix

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
		ordering = ['order']

#Modelo para almacenar los productos asociados a una categoria
class product(models.Model):
	#Clave foranea de la categoria -- Obligada
	category = models.ForeignKey(category)

	#Codigo --  Esta en veremos si tengo chance de catchar el ID adios al codigo
	#           pudiera necesitar esto para algun parametro a tomar en cuenta
	code = models.CharField(max_length=50, unique=True)

	#Nombre del Producto Ej Home Run, DOuble, Coke, etc
	#Este string es el que se muestra al publico
	name = models.CharField(max_length=80)

	#Descripcion, creado para almacenar el contenido del producto
	description = models.TextField(max_length=500)

	#Extras, cantidad de extras permitidos por cada producto
	#Cada extra debe estar en la capacidad de seleccionarse y no mas
	extras = models.IntegerField(default=1, 
								 help_text='This item will not count if allow \
								 extras is not checked')

	#Puede Seleccionar Tipo? True or False
	allow_type = models.BooleanField(default=True, verbose_name='Baked or Fries')

	allow_vegetables = models.BooleanField(default=True)

	# Puede Tener Extras? True or False
	allow_extras = models.BooleanField(default=True, 
									   verbose_name='Allow Players?',
									   help_text='This indicates that the item \
									              will display the Players \
									              Category')

	#Puede tener extras pagos? True or False
	allow_paid_extras = models.BooleanField(default=True,
											verbose_name='Allow "On the Bench"?',
											help_text='This indicates that the \
											item will display the "On The Bench \
											Category')

	#Puede Tener Salsas? True or False
	allow_sauces = models.BooleanField(default=True, 
									   help_text='This indicates \
									   that the item will display the "Sauces" \
									   category')

	# Puede tener Bebidas? True or False
	allow_drinks = models.BooleanField(default=True, 
									   help_text='This indicates that the item \
									              will be a Meal with Soft Drinks\
									              (Category "Soft Drinks")')

	#Puede tener Quantty
	allow_qtty = models.BooleanField(default=False, 
									 verbose_name='Allow Quantty?', 
									 help_text='This indicates that the item \
									            will have a quantity field')

	#Precio
	price = models.DecimalField(max_digits=19, decimal_places=2,
								help_text='Accepts only 19 digits including \
								2 decimals')

	#Ordenamiento por la categoria
	order_in_menu = models.IntegerField(help_text='This is the order to present \
										the item in the menu')

	#Imagen de Referencia para el Producto.
	image = models.ImageField(blank=True, upload_to='images')

	#Indicador de estado
	Active = models.BooleanField(default=True, verbose_name='Active?')

	def __unicode__(self):
		return self.name + ' (' + self.description + ')'
	'''
	Este metodo esta deprecado por que fue creado para los wizard de productos.
	@classmethod
	def NeedWizard(self, pk):
		this = product.objects.get(pk=pk)
		wizard = []
		i = 0
		def AppendWizard(misc, section_name, i):
			i += 1
			wizard.append({'section_number':i,
						  'section_name':section_name,
						  str(misc):True})
			return i

		i = AppendWizard('type','Baked or Fry',i) if this.allow_type == True else i
		i = AppendWizard('vegetables','Vegetables',i) if this.allow_vegetables == True else i
		i = AppendWizard('players','Players',i) if this.allow_extras == True else i
		i = AppendWizard('extras','Extras',i) if this.allow_paid_extras == True else i
		i = AppendWizard('sauces','Sauces',i) if this.allow_sauces == True else i
		i = AppendWizard('drinks','Drinks',i) if this.allow_drinks == True else i
		i = AppendWizard('qtty','Quantity',i) if this.allow_qtty == True else i

		if i == 0 or i<= 3:
			return False
		else:
			return wizard
	'''
	class Meta:
		verbose_name = "Product"
		verbose_name_plural = "Products"
		ordering = ['order_in_menu']

	@classmethod
	def GetProducts(self, Category, Batch):
		Location = PaymentBatch.objects.get(pk=Batch)
		Products = product.objects.filter(Active=True, category_id=Category)
		ProductsMatrix = ()
		for Product in Products:
			Restrictions = ProductRestriction.GetProductRestriction(Product)
			if len(Restrictions) == 0:
				ProductsMatrix += (Product, )
			else:
				if len(Restrictions.filter(location=Location.location)) == 1:
					ProductsMatrix += (Product, )

		return ProductsMatrix

class RelatedImages(models.Model):
    product = models.ForeignKey(product)
    description = models.CharField(verbose_name='Image Description', max_length=50)
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = "Related Image (For Products)"
        verbose_name_plural = "Related Images (For Products)"

    def __unicode__(self):
        return self.description

class LocationsAvailable(models.Model):
	#Descripcion Huminizada
	description = models.CharField(
		verbose_name="Description",
		max_length = 100
	)
	#Direccion del local o truck
	location = models.CharField(
		verbose_name="Address", 
		max_length=1000,
		help_text="Type the address without the zip code")

	#Código zip de la ubicación del truck
	zip_code = models.CharField(
		verbose_name="Zip Code",
		max_length=5,
		help_text="Type the 4 digits zip code"
		)

	#Coordenadas generadas por Google de Latitud
	x_coord = models.CharField(verbose_name="Latitud", max_length=50, blank=True)

	#Coordenadas generadas por Google de Longitud
	y_coord = models.CharField(verbose_name="Longitud", max_length=50, blank=True)

	merchant_ref = models.CharField(
		verbose_name='Merchant Reference', 
		max_length=50, 
		help_text='This number is provided by Payeezy',
		default='MyPOS'
		)

	def __unicode__(self):
		return self.description

	class Meta:
		verbose_name = "Location Available"
		verbose_name_plural = "Locations Available"

class ProductRestriction(models.Model):

	product = models.ForeignKey(product)
	location = models.ForeignKey(LocationsAvailable)

	class Meta:
		verbose_name = "Product Restriction"
		verbose_name_plural = "Products Restrictions"

	def __unicode__(self):
		return self.product.name + " Only for " + self.location.description

	@classmethod
	def GetProductRestriction(self, Product):
		try:
			Restrictions = ProductRestriction.objects.filter(product=Product)
		except ProductRestriction.DoesNotExist:
			return None
		else:
			return Restrictions

	@classmethod
	def GetCartRestrictions(self, Cart):
		'''
		Se espera el Cart del contexto donde se reciben previamente
		los restrcitions de los productos.

		Se Realiza una depuracion eliminando duplicados para entregar solo
		los que se debe buscar en ValidateAddress.
		'''
		'''
		ValidLocations = []
		for item in Cart['cart']:
			for Restriction in item['restrictions']:
				if not Restriction.location in ValidLocations:
					ValidLocations.append(Restriction.location)
		
		return ValidLocations
		'''

		OpenLocations = PaymentBatch.objects.filter(status='O', open_for_delivery=True)

		NotValidLocations = []
		for Location in OpenLocations:
			for item in Cart['cart']:
				if item['restrictions'] ==  None:
					continue
					
				else:				
					NextItem = False
					for Restriction in item['restrictions']:
						if NextItem == True:
							continue

						if Restriction.location == Location.location:
							NextItem = True
							continue

						if not Restriction.location in NotValidLocations:
							NextItem = False
							NotValidLocations.append(Location.location)

		return NotValidLocations

class PaymentBatchManager(models.Manager):
	'''
	Table-level functionality to manage Payment Batch Model
	'''
	def BullpenIsOpen(self):
		count = PaymentBatch.objects.filter(status='O')
		if len(count) > 0:
			return True
		else:
			return False

#Modelo para el Lote de Pago a crear
class PaymentBatch(models.Model):
	#Matriz de status del lote de pago
	batch_status = (("O", "Open"),("C", "Closed"),)

	#Fecha de la apertura del lote de pago
	date = models.DateTimeField(
		verbose_name="Fecha de Lote",
		auto_now_add=True, 
		help_text="Fecha en la que se Aperturó el Truck"
		)

	close_date = models.DateTimeField(
		verbose_name="Fecha y Hora de Cierre", 
		auto_now=True
	)

	#Relacionado con una locacion
	location = models.ForeignKey(LocationsAvailable)

	#Direccion del truck
	address_for_truck = models.CharField(
		verbose_name="Address for Truck", 
		max_length=1000,
		help_text="Must be a Valid Address",
		blank=True
	)

	zip_code_for_truck = models.CharField(
		verbose_name="Zip Code",
		max_length=5,
		help_text="If the Location selected is NOT mobile, please leave blank this field",
		blank=True
	)

	tax_percent = models.IntegerField(
		verbose_name='Tax Percent Value for Batch',
		default=7,
		help_text="You must enter the exac value, ex: 7 mean 7%"
		)

	#Maximo de millas a recorres por el delivery
	max_miles = models.IntegerField(
		verbose_name="Max miles for Delivery", 
		help_text="Please insert a value for the coverage round area"
	)

	#Codigo de Lote para el dia
	batch_code = models.CharField(
		verbose_name="Batch Code", 
		max_length=10, 
		help_text="This code will be used to identify the batch",
		unique=True
		)

	#Hora de cierre en hora militar
	time_to_close = models.TimeField(
		verbose_name="Hora de Cierre",
		help_text="Ingrese la Hora de cierre del lote en hora militar, Ej: 23000",
		auto_now_add=True
		)

	#Indicador para saber si el Lote esta abierto para Delivery
	open_for_delivery = models.BooleanField(
		verbose_name="Open for Delivery?",
		default=True,
		help_text='Indicates if the Location accept Delivery Orders'
		)

	#Estado del Lote de Pago
	status = models.CharField(
		verbose_name="Estado",
		help_text="Indica el Estado Actual del Lote, Debe estar Abierto para Aceptar Pedidos", 
		max_length=1,
		default="O",
		choices=batch_status
		)

	#Mail de Notificacion de Orden
	notifier = models.EmailField(default='do-not-reply@bullpenarepas.com')

	objects = PaymentBatchManager()

	class Meta:
		verbose_name = "Batch"
		verbose_name_plural = "Batches"

	def __unicode__(self):
		return self.location.description + ' @ ' + self.address_for_truck

	def clean(self, *args, **kwargs):
		try:
			valid = PaymentBatch.objects.get(location=self.location, status='O')
		except PaymentBatch.DoesNotExist:
			pass
		else:
			if not valid.id == self.id:
				raise ValidationError({'location': "You can't save a Batch for this Location, already Open"})

	@classmethod
	def GetLocationsOpen(self):
		'''
		Get the locations that are open and return in an object
		the count for delivery and the ones that are open for delivery

		Output: Object
		Locations: Collections of objects Batch with status Open ('O')
		ForDelivery: Count of Locations Open for delivery
		ForCountQry: Collections of objects Batch that are open for delivery (open_for_delivery=True)
		'''
		try:
			Locations = PaymentBatch.objects.filter(status='O')
		
		except PaymentBatch.DoesNotExist:
			return None
		
		else:
			ForDelivery = Locations.filter(open_for_delivery=True)
			Object = { 'Locations': Locations, 
						'LocationsCount': len(Locations),
					   'ForDelivery': len(ForDelivery), 
					   'ForDeliveryQry': ForDelivery }
			return Object

#Modelo de Ordenes Recibidas
class Order(models.Model):
	#Matriz de Tipos de Ordenes
	ORDER_TYPE = (('D','Delivery'),
				  ('P','Pick it Up'),
				  ('PL','Parking Lot'),)

	#Matriz de tiempos de pick it up
	MAX_TIME = (('15','15 Minutes'),
				('20','20 Minutes'),
				('25','25 Minutes'),)

	ORDER_STATUS = (('P','Paid'),
					('K','Kitchen'),
					('O','Out for Delivery'),
					('D','Delivered'),)

	#Fecha y Hora de la Orden
	date = models.DateTimeField(verbose_name="Order Date and Time", auto_now_add=True)

	#Numero de Orden - Calculado
	order_number = models.IntegerField(verbose_name="Order Number", unique=True)

	#Tipo de Ordenes
	order_type = models.CharField(
								  verbose_name="Order Type",
								  max_length=2,
								  choices=ORDER_TYPE,
								  help_text="Please Choose if you're going to \
								  pick it up o we're going to deliver the order")

	#Relacionado con el Usuario
	user = models.ForeignKey(User)

	#Relacionado con el PaymentBatch
	batch = models.ForeignKey(PaymentBatch)
	
	#Direccion del Delivery, puede estar vacio si es tipo "P" la orden
	address = models.CharField(verbose_name="Adress",
							   max_length=1000,
							   help_text="Please enter the delivery adress",
							   blank=True)

	adress2 = models.CharField(verbose_name='Adress Line 2', 
							   max_length=200,
							   help_text='Ex: Suite 23, Floor 2',
							   blank=True)

	car_brand = models.CharField(verbose_name='Car Brand', 
								 max_length=50, 
								 blank=True)

	car_model = models.CharField(verbose_name='Car Model', 
								 max_length=50, 
								 blank=True)

	car_color = models.CharField(verbose_name='Car Color', 
								 max_length=50, 
								 blank=True)

	car_license = models.CharField(verbose_name='Car License', 
								   max_length=50, 
								   blank=True)

	#Tiempo en que el cliente buscara la comida en el truck
	time = models.CharField(verbose_name="Time to Pick the order Up",
							max_length=2,
							blank=True,
							choices=MAX_TIME,
							help_text="Please select how many minutes you're \
									   going to pick the order up")

	#Monto del Pedido Sin Tax
	sub_amt = models.DecimalField(verbose_name='Subtotal',
        						  max_digits=10,
        						  decimal_places=2,
        						  validators=[MinValueValidator(0.00)])

	#Monto del Tax del pedido
	tax_amt = models.DecimalField(verbose_name='Tax',
						          max_digits=10,
						          decimal_places=2,
						          validators=[MinValueValidator(0.00)])

	delivery_amt = models.DecimalField(verbose_name='Delivery',
									   max_digits=10,
									   decimal_places=2,
									   default=0)

	#Monto total del pedido (Tax + Delivery + Subtotal)
	total_amt = models.DecimalField(verbose_name='Total',
        							max_digits=10,
							        decimal_places=2,
							        validators=[MinValueValidator(0.00)])

	order_status = models.CharField(verbose_name="Status",
									max_length=1,
									choices=ORDER_STATUS,
									default='P')

	def __unicode__(self):
		return str(self.order_number)

	@classmethod
	def RewriteAddress(self, address, key):
		import googlemaps
		gmaps = googlemaps.Client(key=key)
		dest = gmaps.geocode(address)
		return dest[0]['formatted_address']

	@classmethod
	def ValidateAddress(self,CustomerAddress):
		'''
		Search one by one for the Batches Open for Delivery
		Using the Google Maps API Client for Python.

		Input: 
		CustomerAddress: Address of the client

		Output:
		LocationMatrix: List with Dict, two parameters
		                in the dict the Batch Id and the Distnace calculated
		'''
		import googlemaps

		# Get the Open Batches with the ClassMethod
		OpenBatches = PaymentBatch.GetLocationsOpen()

		# Instanciates the Google Object for the Python API
		GoogleObject = googlemaps.Client(key=GenericVariable.objects.val(code='google.API.KEY'))

		LocationMatrix = []
		for Origin in OpenBatches['ForDeliveryQry']:
			Result = GoogleObject.directions(Origin.address_for_truck,CustomerAddress)

			Distance = Result[0]['legs'][0]['distance']['text'].split(' ')

			if Distance[1] == 'ft':
				inRange = True
			elif Distance[1] == 'mi' and Decimal(Distance[0]) < Decimal(Origin.max_miles):
				inRange = True
			else:
				inRange = False

			LocationMatrix.append({'Location':Origin,
								   'Distance':Distance,
								   'inRange': inRange})
		return LocationMatrix

	@classmethod
	def SaveOrder(self, DataClient, OrderNumber, Subtotal, TaxAmt, TotalAmt, Customer):

		TypeOfSale = DataClient['TypeOfSale']
		Batch = DataClient['Location']
		Address = "%s, %s, GA, %s" % (DataClient['Object'].get('Address',''),
									  DataClient['Object'].get('City',''),
									  str(DataClient['Object'].get('ZipCode','')))
		ThisOrder = Order(
					order_number = OrderNumber,
					order_type = TypeOfSale,
					user = Customer,
					batch = Batch,
					address = Batch.address_for_truck \
							  if not TypeOfSale == 'D' else Address,
					adress2 = DataClient['Object'].get('Address2',''),
					car_brand = DataClient['Object'].get('CarBrand',''),
					car_color = DataClient['Object'].get('CarColor',''),
					car_model = DataClient['Object'].get('CarModel',''),
					car_license = DataClient['Object'].get('CarLicense',''),
					time = DataClient['Object'].get('Time','--'),
					sub_amt = Subtotal,
					delivery_amt = Decimal(GenericVariable.objects.val('delivery.cost')) \
								   if TypeOfSale == 'D' else 0,
					tax_amt = TaxAmt,
					total_amt = TotalAmt
				    )

		ThisOrder.save()

		return ThisOrder

	@classmethod
	def GetAmts(self, Subtotal,TaxPercent,TypeOfSale):
		delivery = int(GenericVariable.objects.val('delivery.cost'))

		Amounts = {}
		Amounts['TaxAmt'] = Decimal(TaxPercent*(Subtotal + delivery))/100 \
							if TypeOfSale == 'D' else Decimal(TaxPercent*Subtotal)/100
		
		Amounts['TotalAmt'] = Subtotal + Amounts['TaxAmt'] + delivery \
							  if TypeOfSale == 'D' else Subtotal + Amounts['TaxAmt']

		return Amounts

	@classmethod
	def Payment(self,name,card,exp,amt,cvv,ref):
		'''
		Funcion para realizar un pago a la pasarela payeezy
		Datos de entrada validos: 	# VISA: 4788250000028291
		con cualquier nombre, cualquier cualquier fecha de 
		vencimiento que sea mayor a la actual y cualquier cvv.
		'''

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

	@classmethod
	def SendInvoice(self, Order, Email, Cart):
		text = "Your Order "+Order.order_number+" have been recived\nThank you...\nAny Questions?\nWrite us at support@bullpenarepas.com\nCall us at (404) 643 2568"
		html = render_to_string('website/wizard/email_template.html',{'cart':Cart,'order':Order})
		subject = 'Your Order #'+ Order.order_number +' From bullpenarepas.com'
		from_email = 'Bullpen Arepas <do-not-reply@bullpenarepas.com>'
		cc_email = Order.batch.notifier

		try:
			send_mail(subject,text, from_email, [Email], fail_silently=True, html_message=html)
			send_mail(subject,text, from_email, [cc_email], fail_silently=True, html_message=html)

		except BadHeaderError:
			return HttpResponse('Invalid header found.')

class GuestDetail(models.Model):
    firstname = models.CharField(verbose_name='First Name', max_length=50)
    
    lastname = models.CharField(verbose_name='Last Name', max_length=50)
    
    email = models.EmailField(verbose_name='E-mail')
    
    phone = models.CharField(verbose_name='Telephone Number', 
    						 max_length=50, blank=True)
    
    order = models.ForeignKey(Order)

    class Meta:
        verbose_name = "Guest Detail"
        verbose_name_plural = "Guest Details"

    def __unicode__(self):
        return self.firstname + ' ' + self.lastname

#Modelo de Detalle del la Orden (Productos seleccionados por el cliente)
class OrderDetail(models.Model):
	#Numero de Item a Mostrar
	item = models.IntegerField(verbose_name="Item")

	#Baked or Fried
	arepa_type = models.CharField(verbose_name="Baked or Fried", 
								  default="Baked", 
								  max_length=15, 
								  blank=True)

	#Producto que solicito
	product_selected = models.ForeignKey(product)

	#Pedido
	order_number = models.ForeignKey(Order)

	# Producto Principal (Bool)
	main_product = models.BooleanField(verbose_name='is the Main Product of the \
									                 Order?',
									   help_text='Indicates if the product is the \
									              main Product',
									   default=False)

	def __unicode__(self):
		return str(self.order_number.order_number)

	@classmethod
	def SaveExtraDetail(self, DetaillList, Item, ThisOrder, ArepaType):
		for Extra in DetaillList:
			ThisExtra = product.objects.get(pk=Extra)
			Detail = OrderDetail(item=Item, arepa_type=ArepaType, 
								 product_selected=ThisExtra, order_number=ThisOrder)
			Detail.save()

	@classmethod
	def SaveOrderDetail(self, Cart, ThisOrder):
		item_number=1
		for item in Cart['cart']:
			for i in range(int(item['qtty'])):
				ThisProduct = product.objects.get(pk=item['product_id'])
				Vegetables = item['vegetables']
				PaidExtras = item['paid_extras']
				Sauces = item['sauces']
				Drink = [item['soft_drinks'],]

				ThisItem = OrderDetail(
					item=item_number,
					arepa_type=ThisProduct.category.name,
					product_selected=ThisProduct,
					order_number=ThisOrder,
					main_product=True,
				)
				ThisItem.save()

				if ThisProduct.allow_extras == True:
					OrderDetail.SaveExtraDetail(item['extras'],ThisItem.item,ThisOrder, 'With')
				
				if ThisProduct.allow_vegetables == True and not Vegetables == None:
					OrderDetail.SaveExtraDetail(Vegetables, ThisItem.item, ThisOrder, 'Vegetables')

				if ThisProduct.allow_paid_extras == True and not PaidExtras == None:
					OrderDetail.SaveExtraDetail(PaidExtras, ThisItem.item, ThisOrder, 'Extras')

				if ThisProduct.allow_sauces == True and not Sauces == None:
					OrderDetail.SaveExtraDetail(Sauces, ThisItem.item, ThisOrder, 'Sauces')

				if ThisProduct.allow_drinks == True and not Drink == '':
					OrderDetail.SaveExtraDetail(Drink, ThisItem.item, ThisOrder, 'Drink')
				
				item_number+=1

#Modelo de Detalle del pago de la orden (Tarjeta, etc)
class OrderPaymentDetail(models.Model):
	order_number = models.ForeignKey(Order)
	cardholder_name = models.CharField(max_length=50)
	card_type = models.CharField(max_length=20)
	card_number = models.CharField(max_length=4)
	exp_date = models.CharField(max_length=4)
	gateway_message = models.CharField(max_length=50)
	bank_message = models.CharField(max_length=50)
	bank_resp_code = models.CharField(max_length=50)
	gateway_resp_code = models.CharField(max_length=50)
	cvv2 = models.CharField(max_length=5)
	amount = models.CharField(max_length=19)
	transaction_tag = models.CharField(max_length=50)
	transaction_type = models.CharField(max_length=50)
	currency = models.CharField(max_length=4)
	correlation_id = models.CharField(max_length=50)
	token_type = models.CharField(max_length=50)
	token_value = models.CharField(max_length=50)
	transaction_status = models.CharField(max_length=50)
	validation_status = models.CharField(max_length=50)
	method = models.CharField(max_length=50)
	transaction_id = models.CharField(max_length=100)

	def __unicode__(self):
		return str(self.order_number.order_number)

	@classmethod
	def SaveOrderPaymentDetail(self, pay, Order):
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

		PayEgg_model = OrderPaymentDetail(
					order_number = Order,
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

class GenericVariableManager(models.Manager):
	"""
	Table-level functionality for Generic Vars Model
	"""
	def val(self, code):
		"""
		Return the Value of the generic variable for a code given
		"""
		try:
			GenVar = GenericVariable.objects.get(code=code)
		except GenericVariable.DoesNotExist:
			return "404 Not Found"
		else:
			return GenVar.value

# Modelo Clasico de Variables Genericas
class GenericVariable(models.Model):
	code = models.CharField(verbose_name='Code', max_length=45, unique=True)
	value = models.CharField(verbose_name='Value', max_length=500)
	description = models.TextField(verbose_name='Descripcion', max_length=45)
	objects = GenericVariableManager()

#Modelo de Obtencion de Album
class Album(models.Model):
	name = models.CharField(verbose_name='Given Name', max_length=150)
	email = models.EmailField(unique=True)
	
	class Meta:
		verbose_name = "Album"
		verbose_name_plural = "Albums"
