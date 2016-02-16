from django.db import models
from django.core.mail import send_mail, BadHeaderError
from ordertogo.models import category, product, GenericVariable

class WebTextManager(models.Manager):
	"""
	Table-level functionality for the WebText Model
	"""
	def get_text(self, code):
		"""
		Return the value of text from a given code
		"""
		try:
			text = WebText.objects.get(code=code)
		except WebText.DoesNotExist:
			return "404 Not Found"
		else:
			return text.text

class WebText(models.Model):

	code = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	text = models.TextField(max_length=3000)
	active = models.BooleanField(default=True)
	objects = WebTextManager()

	class Meta:
		verbose_name = "Text"
		verbose_name_plural = "Texts"

	def __unicode__(self):
		return self.code

class WebCategory(models.Model):

	Style_Options = (
		("L", "List Product"),
		("I", "Image View - Stripped R&B "),
		("C", "Image View - Stripped R&Y "),
	)

	category = models.ForeignKey(category)
	override_desc = models.BooleanField(verbose_name='Override Name?',default=False)
	description = models.TextField(max_length=3000, blank=True)
	show_price = models.BooleanField(
		default=False, 
		help_text="Only For Image View and Image View - Centered"
	)
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
	foot_image_check = models.BooleanField(verbose_name="Aditional Image?", default=False)
	foot_image = models.ImageField(
		verbose_name="Image for Footer", 
		help_text="This Image will be on the Footer od the Modal Window Content",
		upload_to='website/product/images/footer/',
		blank=True
	)
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
	batter = models.BooleanField(
		verbose_name="Show Batter?", 
		default=False, 
		help_text="Only for Image View"
	)
	batter_num = models.PositiveIntegerField(
		verbose_name="How Many Batters?", 
		default="0",
		help_text="Only for Image View"
	)
	override_desc = models.BooleanField(verbose_name="Override Description?", default=False)
	description = models.TextField(verbose_name="Description", blank=True)
	aditional_text = models.CharField(
		verbose_name="Aditional Text to Show", 
		max_length=10, 
		blank=True,
		help_text="Only for Image View - Centered"
	)

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

	def save(self, *args, **kwargs):
		super(WebInfo, self).save(*args, **kwargs)
		send_info_email(self.name,self.email,self.info)

def send_info_email(name,email,info):
	text = "Name:\n"+name+"\nemail:\n"+email+"\ninfo:\n"+info
	html = """\
	<html>
	  <head></head>
	  <body>
	"""

	html += "<p>Name:<br />"+name+"</p>"
	html += "<p>Email:<br />"+email+"</p>"
	html += "<p>Info:<br />"+info+"</p>"

	html +="""\
	  </body>
	</html>
	"""
	try:
		send_mail(
			'Info Request From bullpenarepas.com', 
			text,
			'Website Support <support@bullpenarepas.com>', #From Email
			[GenericVariable.objects.val('info.email')], #To Email
			fail_silently=False,
			html_message=html
		)
	except BadHeaderError:
		return HttpResponse('Invalid header found.')


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