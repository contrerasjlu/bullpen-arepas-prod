from django.db import models
from ordertogo.models import category, product

class WebText(models.Model):

	code = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	text = models.TextField(max_length=3000)
	active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Text"
		verbose_name_plural = "Texts"

	def __unicode__(self):
		return self.code

class WebCategory(models.Model):

	Style_Options = (("L", "List Product"),("I", "Image View"),)

	category = models.ForeignKey(category)
	override_desc = models.BooleanField(verbose_name='Override Name?',default=False)
	description = models.TextField(max_length=3000, blank=True)
	show_price = models.BooleanField(default=False)
	webImage = models.ImageField(
		verbose_name='Image to Show for Category',
		upload_to='website/category/images/'
	)
	type_cat = models.CharField(
		verbose_name='Category Style', 
		max_length=1, 
		choices=Style_Options, 
		default='I'
	)
	order = models.PositiveIntegerField(verbose_name='Order To Show in Page', default=0)
	active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Web Category"
		verbose_name_plural = "Web Categories"

	def __unicode__(self):
		return self.category.name

class WebProduct(models.Model):

	webCat = models.ForeignKey(WebCategory)
	product = models.ForeignKey(product)
	webImage = models.ImageField(
		verbose_name='Image to Show for Product', 
		upload_to='website/product/images/'
	)
	batter = models.BooleanField(verbose_name="Show Batter?", default=False)
	batter_num = models.PositiveIntegerField(verbose_name="How Many Batters?", default="0")


	class Meta:
		verbose_name = "Web Product"
		verbose_name_plural = "Web Products"

	def __unicode__(self):
		return self.product.name

class WebInfo(models.Model):

	name = models.CharField(verbose_name='Name', max_length=50)
	email = models.EmailField(verbose_name='Email')
	info = models.TextField(verbose_name='Tell us, What do you need?')

	class Meta:
		verbose_name = "Web Info"
		verbose_name_plural = "Email"

	def __unicode__(self):
		return self.name + self.email

class WebCarrousel(models.Model):

	image = models.ImageField(upload_to='website/carrousel/')
	alt = models.CharField(verbose_name='Alternative Text', max_length=50, help_text='This text is show if the Image is not Loaded')
	order = models.PositiveIntegerField(verbose_name='Order')
	active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Web Carrousel Image"
		verbose_name_plural = "Web Carrousel Images"

	def __unicode__(self):
		return self.alt