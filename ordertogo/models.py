# -*- encoding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

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

	#Pudieramos necesitar una imagen para representar la categoria

	def __unicode__(self):
		return self.name

#Modelo para almacenar los productos asociados a una categoria
class product(models.Model):
	#Clave foranea de la categoria -- Obligada
	category = models.ForeignKey(category, related_name='product')

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
	extras = models.IntegerField(default=1)

	#Puede tener extras pagos? True or False
	allow_paid_extras = models.BooleanField(default=True)

	#Puede Tener Salsas? True or False
	allow_sauces = models.BooleanField(default=True)

	#Precio
	price = models.DecimalField(max_digits=19, decimal_places=2)

	#Ordenamiento por la categoria
	order_in_menu = models.IntegerField()

	#Imagen de Referencia para el Producto.
	image = models.ImageField(blank=True)

	#Indicador de estado
	Active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

#Modelo para el Lote de Pago a crear
class PaymentBatch(models.Model):
	#Matriz de status del lote de pago
	batch_status = (("O", "Abierto"),("C", "Cerrado"),)

	#Fecha de la apertura del lote de pago
	date = models.DateField(
		verbose_name="Fecha de Lote",
		auto_now_add=True, 
		help_text="Fecha en la que se Aperturó el Truck"
		)

	#Direccion del Truck
	location = models.CharField(
		verbose_name="Dirección de la Locación", 
		max_length=1000,
		help_text="Ingrese la Dirección donde se ubica el Truck")

	#Código zip de la ubicación del truck
	zip_code = models.CharField(
		verbose_name="Código Zip",
		max_length=4,
		help_text="Ingrese el código postal de la ubicacion del truck"
		)

	#Coordenadas generadas por Google de Latitud
	x_coord = models.CharField(verbose_name="Latitud", max_length=50)

	#Coordenadas generadas por Google de Longitud
	y_coord = models.CharField(verbose_name="Longitud", max_length=50)

	#Maximo de millas a recorres por el delivery
	max_miles = models.IntegerField(
		verbose_name="Millas Máximas", 
		help_text="Ingrese la Cantidad de millas máximas para el Delivery"
		)

	#Codigo de Lote para el dia
	batch_code = models.CharField(
		verbose_name="Código de Lote", 
		max_length=10, 
		help_text="Ingrese el código que se asignará al Lote",
		unique=True
		)

	#Hora de cierre en hora militar
	time_to_close = models.TimeField(
		verbose_name="Hora de Cierre",
		help_text="Ingrese la Hora de cierre del lote en hora militar, Ej: 23000"
		)

	#Indicador para saber si el Lote esta abierto para Delivery
	open_for_delivery = models.BooleanField(
		verbose_name="Abierto para Delivery?",
		default=True
		)

	#Estado del Lote de Pago
	status = models.CharField(
		verbose_name="Estado",
		help_text="Indica el Estado Actual del Lote, No pueden existir mas de un Lote Abierto", 
		max_length=1,
		default="O",
		choices=batch_status
		)

#Modelo de Ordenes Recibidas
class Order(models.Model):
	#Matriz de Tipos de Ordenes
	ORDER_TYPE = (('D','Delivery'),('P','Pick it Up'),)

	#Matriz de tiempos de pick it up
	MAX_TIME = (('15','15 Minutes'),('20','20 Minutes'),('25','25 Minutes'),)

	#Fecha y Hora de la Orden
	date = models.DateTimeField(verbose_name="Order Date and Time", auto_now_add=True)

	#Numero de Orden - Calculado
	order_number = models.IntegerField(verbose_name="Order Number")

	#Tipo de Ordenes
	order_type = models.CharField(
		verbose_name="Order Type",
		max_length=1,
		choices=ORDER_TYPE,
		help_text="Please Choose if you're going to pick it up o we're going to deliver the order"
		)

	#Correo Electronico del Cliente
	email = models.EmailField(
		verbose_name="Email",
		help_text="Please enter your email address"
		)

	
	#Direccion del Delivery, puede estar vacio si es tipo "P" la orden
	address = models.CharField(
		verbose_name="Adress",
		max_length=100,
		help_text="Please enter the delivery adress",
		blank=True
		)

	#Tiempo en que el cliente buscara la comida en el truck
	time = models.CharField(
		verbose_name="Time to Pick the order Up",
		max_length=2,
		blank=True,
		choices=MAX_TIME,
		help_text="Please select how many minutes you're going to pick the order up"
		)

	#Monto del Pedido Sin Tax
	sub_amt = models.DecimalField(
		verbose_name='Subtotal',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
        )

	#Monto del Tax del pedido
	tax_amt = models.DecimalField(
		verbose_name='Tax',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
        )

	#Monto total del pedido (Tax + Subtotal)
	total_amt = models.DecimalField(
		verbose_name='Total',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
        )

	def __unicode__(self):
		return self.order_number

#Modelo de Detalle del la Orden (Productos seleccionados por el cliente)
class OrderDetail(models.Model):
	#Numero de Item a Mostrar
	item = models.IntegerField(verbose_name="Item")

	#Baked or Fried
	arepa_type = models.CharField(verbose_name="Baked or Fried", default="Baked", max_length=5, blank=True)

	#Producto que solicito
	product_selected = models.ForeignKey(product)

	#Pedido
	order_number = models.ForeignKey(Order)

#Modelo de Detalle del pago de la orden (Tarjeta, etc)
class OrderPaymentDetail(models.Model):
	order_number = models.ForeignKey(Order)
	cardholder_name = models.CharField(max_length=50)
	card_type = models.CharField(max_length=20)
	card_number = models.CharField(max_length=4)
	exp_date = models.CharField(max_length=4)
	gateway_message = models.CharField(max_length=15)
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