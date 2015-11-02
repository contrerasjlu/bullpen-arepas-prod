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

	#Precio
	price = models.DecimalField(max_digits=19, decimal_places=2)

	#Ordenamiento por la categoria
	order_in_menu = models.IntegerField()

	#Indicador de estado
	Active = models.BooleanField(default=True)

	#TODO: Crear el field para la imagen que se mostrara como producto

	def __unicode__(self):
		return self.name




