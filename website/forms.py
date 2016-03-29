# -*- encoding: utf-8 -*-
# Powered by: Ing. Jorge Contreras
# Fecha: 05/11/2015

from django.forms import ModelForm, widgets, NumberInput, TextInput, EmailInput
from django.contrib.auth.models import User
from requests import ConnectionError
from django import forms
from ordertogo.models import *
from website.models import WebInfo, WebText

attr  = 'form-control has-feedback-left agencia-regular'
attr2 = 'form-control agencia-regular'
attr3 = 'flat'

class ArepaForm(forms.Form):

    id_for_product = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    arepa_type = forms.ChoiceField(label="Baked or Fried?",
                                   required=False,
                                   widget=forms.Select(attrs={'class': attr2}),
                                   choices=(('Baked','Baked'),('Fried','Fried'),),
                                   initial='Baked',
                                   help_text="We can Fry your Arepa or make it in the Oven"
    )
    NoVegetablesCheck = forms.BooleanField(initial=False, 
                                           widget=forms.CheckboxInput(attrs={'class':attr3 + ' vgch'}),
                                           required=False, 
                                           label="No, I don't want Vegetables")

    vegetables = forms.ModelMultipleChoiceField(label='Vegetables',
                                                required=False,
                                                widget=forms.CheckboxSelectMultiple(
                                                    attrs={'class': attr3}
                                                    ),
                                                queryset=product.objects.filter(
                                                    Active=True,category=category.objects.get(
                                                        code='vegetables'
                                                        )
                                                    ).order_by('order_in_menu'),
                                                help_text="Wich vegetables do you want on your item"
        )
    NoExtrasCheck = forms.BooleanField(initial=False, 
                                       widget=forms.CheckboxInput(attrs={'class':attr3 + ' extras-id'}),
                                       required=False, 
                                       label="No, I don't want Extras")

    extras = forms.ModelMultipleChoiceField(
        label="Choose the Players with your Arepa...",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': attr3}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='extras')).order_by('order_in_menu')
    )

    paid_extras = forms.ModelMultipleChoiceField(
        label="Additional Players",
        help_text="Choose as much as 4 additional players for your item ($1.00 each)",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': attr3}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='paid.extras')).order_by('order_in_menu')
    )

    NoSaucesCheck = forms.BooleanField(initial=False, 
                                       widget=forms.CheckboxInput(attrs={'class':attr3 + ' sach'}),
                                       required=False, 
                                       label="No, I don't want Sauces")

    sauces = forms.ModelMultipleChoiceField(
        label="Sauces",
        help_text="Select the sauces thet you want.",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': attr3}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='sauces')).order_by('order_in_menu')
    )

    soft_drinks = forms.ModelChoiceField(
        label="Soft Drinks",
        required=False,
        widget=forms.Select(attrs={'class': attr2}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='drinks')).order_by('order_in_menu'),
        empty_label="I don't want any Drink"
    )

    qtty = forms.IntegerField(
        label='Quantty',
        required=False,
        help_text='How many do you Want?',
        initial=1,
        widget=forms.NumberInput(attrs={'class':attr2})
        )

    def clean(self):
        cleaned_data = super(ArepaForm, self).clean()
        id_for_product = cleaned_data.get("id_for_product")
        extras = cleaned_data.get('extras')
        paid_extras = cleaned_data.get("paid_extras")
        qtty = cleaned_data.get("qtty")
        MaxExtras = GenericVariable.objects.val('max_extras')

        this_product = product.objects.get(pk=id_for_product)

        if (not this_product.extras == len(extras)) and this_product.allow_extras == True:
            msg = "You must select %d Players for this product" % this_product.extras
            self.add_error('extras', msg)

        if this_product.allow_qtty == True and (qtty < 1):
            msg = "You must enter a valid Quantty"
            self.add_error('qtty', msg)

        if (len(paid_extras) > int(MaxExtras)) and this_product.allow_paid_extras == True:
            msg = "You can't select more the %s Extras for your item" % MaxExtras
            self.add_error('paid_extras', msg)

class CreateAccountForm(forms.Form):
    firstname = forms.CharField(
        max_length=80,
        label=" First Name",
        help_text="Ex: Jhon Doe",
        widget=forms.TextInput(attrs={'class': attr2, 'placeholder':'Fisrt Name'})
    )

    lastname = forms.CharField(
        max_length=80,
        label="Last Name",
        help_text="Ex: Jhon Doe",
        widget=forms.TextInput(attrs={'class': attr2, 'placeholder':'Last Name'})
    )

    username = forms.CharField(
        max_length=80,
        label="Username",
        help_text="Ex: jlopez",
        widget=forms.TextInput(attrs={'class': attr2, 'placeholder':'Username'})
    )

    email = forms.EmailField(
        label="Email", 
        help_text="Ex: somebody@mysite.com", 
        widget=forms.TextInput(attrs={'class': attr2,'placeholder':'Email'})
    )

    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': attr2,'placeholder':'Password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError("User Taken")

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("Email Taken")

class PaymentForm(forms.Form):
    name_on_card = forms.CharField(
        required=True,
        max_length=80,
        label="Name on Card",
        help_text="Ex: Jhon D Lopez"
    )

    card_number = forms.CharField(
        required=True,
        max_length=16,
        min_length=15,
        label="Card Number",
        help_text="Please Insert your card number"
    )

    expiry = forms.CharField(
        required=True,
        label="Expiricy Date",
        max_length=5,
        help_text="Ex: 06/16" )

    cvv = forms.CharField(
        required=True,
        max_length=4,
        min_length=3,
        label="CVV",
        help_text="This code is in the front side of your American Express Card, and in the back side of your Visa or Master Card"
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.cart = kwargs.pop('cart')
        self.user = kwargs.pop('user')
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean_name_on_card(self):
        name_on_card = self.cleaned_data.get('name_on_card')

        wname_on_card = name_on_card.replace(' ', '')

        if not wname_on_card.isalpha():
            raise forms.ValidationError("Please Intert a Valid Name")

        return name_on_card

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')

        if not card_number.isdigit():
            raise forms.ValidationError("Only numeric digits are accepted")

        if card_number.startswith('3'):
            if not len(card_number) == 15:
                raise forms.ValidationError("Please inter a valid American Express card number")

        elif card_number.startswith('4') or card_number.startswith('5'):
            if not len(card_number) == 16:
                raise forms.ValidationError("Please inter a valid card number")

        else:
            raise forms.ValidationError("Please inter a valid card number")

        return card_number

    def clean_cvv(self):
        card_number = self.cleaned_data.get('card_number')
        cvv = self.cleaned_data.get('cvv')

        if not cvv.isdigit():
            raise forms.ValidationError("Only numeric digits are accepted")

        if card_number.startswith('3'):
            if not len(cvv) == 4:
                raise forms.ValidationError("Please insert a valid American Express CVV")

        elif card_number.startswith('4') or card_number.startswith('5'):
            if not len(cvv) == 3:
                raise forms.ValidationError("Please insert a valid CVV")

        else:
            raise forms.ValidationError("Please insert a valid CVV")

        return cvv

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry')

        if '/' in expiry:
            nexpiry = expiry.split('/')
            month = nexpiry[0]
            year = '20'+nexpiry[1]

            from datetime import date

            d = date.timetuple(date.today())


            if int(year) < (d[0]):
                raise forms.ValidationError("The Expiricy Date is not Valid")

            if int(year) == int(d[0]) and int(month) < d[1]:
                raise forms.ValidationError("The Expiricy Date is not Valid")

        else:
            raise forms.ValidationError("The Expiricy Date is not Valid")

        return expiry.replace('/', '')

    def clean(self, **kwargs):
        cleaned_data = super(PaymentForm, self).clean()
        name_on_card = cleaned_data.get("name_on_card")
        card_number = cleaned_data.get("card_number")
        expiry = cleaned_data.get("expiry")
        cvv = cleaned_data.get("cvv")

        ############################################
        OrderNumber = self.request['order_number']
        ref = 'Order #'+str(OrderNumber)
        DataClient = {'Location': PaymentBatch.objects.get(pk=self.request['Batch']),
                      'TypeOfSale': self.request['TypeOfSale']['code'],
                      'Object':self.request[self.request['TypeOfSale']['code']]}
        Amounts = Order.GetAmts(self.cart['amounts']['subtotal'], DataClient['Location'].tax_percent, self.request['TypeOfSale']['code'])
        TotalAmt = Amounts['TotalAmt']
        TaxAmt = Amounts['TaxAmt']
        Subtotal = self.cart['amounts']['subtotal']

        value = round(TotalAmt,2)
        value = str(value)
        valueTry = str(value).split(".")
        if len(valueTry[1]) == 1:
            value += "0"
        value = value.replace('.','')
        try:
            pay = Order.Payment(name_on_card,card_number,expiry,value,cvv,ref)

        except ConnectionError:
            msj = "Something went wrong with the Payment Gateway, Try Again Later"
            self.add_error('card_number',msj)
        else:
            if pay['status'] == False:
                for error in pay['object']:
                    msj = "%s - %s" % (error['code'],error['description'])
                    self.add_error('card_number',msj)
            else:
                ThisOrder = Order.SaveOrder(DataClient,OrderNumber,Subtotal,TaxAmt,TotalAmt, self.user)
                
                OrderPaymentDetail.SaveOrderPaymentDetail(pay, ThisOrder)

                AddressForEmail = ThisOrder.user.email

                if self.user.username == GenericVariable.objects.val('guest.user'):
                    guest = self.request['guest']
                    this_guest = GuestDetail(
                        firstname=guest['firstname'],
                        lastname=guest['lastname'],
                        email=guest['email'],
                        phone=guest['phone'],
                        order=this_order
                        )
                    this_guest.save()
                    AddressForEmail = guest['email']

                OrderDetail.SaveOrderDetail(self.request,ThisOrder)
                Order.SendInvoice(ThisOrder, AddressForEmail, self.cart)

class PreCheckoutForm_Delivery(forms.Form):

    type_of_sale = forms.CharField(widget=forms.HiddenInput())

    address = forms.CharField(label="Address to deliver the order",
                              help_text="We can only makes delivery \
                                         in a certain range",
                              widget=forms.TextInput(attrs={'class': attr,
                                                            'placeholder':'Address'}))

    address2 = forms.CharField(label="Suite and Floor",
                               required=False,
                               help_text="If you are in a Building",
                               widget=forms.TextInput(attrs={'class': attr,
                                                             'placeholder':'Suite and Floor'}))

    city = forms.CharField(label='City', 
                           required=True, 
                           help_text='Ex: Roswell',
                           widget=forms.TextInput(attrs={'class': attr,
                                                         'placeholder':'City'}))

    zip_code = forms.CharField(label='Zip Code', 
                               required=True, 
                               help_text='Ex: 30076',
                               widget=forms.TextInput(attrs={'class': attr,
                                                             'placeholder':'Zip Code'}))

    NearestLocation = forms.CharField(widget=forms.HiddenInput(),required=False)

    def clean(self):
        cleaned_data = super(PreCheckoutForm_Delivery, self).clean()
        address = cleaned_data.get('address')
        city = cleaned_data.get('city')
        zip_code = cleaned_data.get('zip_code')

        CustomerAddress = "%s, %s, GA, %s" % (address, city, str(zip_code))

        NearestLocation = Order.ValidateAddress(CustomerAddress)
        Near = 0
        for Batch in NearestLocation:
            if Batch['inRange'] == True:
                if Near == 0:
                    Near = Decimal(Batch['Distance'][0])
                    ValidBatch = Batch
                elif Near < Decimal(Batch['Distance'][0]):
                    Near = Decimal(Batch['Distance'][0])
                    ValidBatch = Batch

        if Near == 0:
            self.add_error('address',"We couldn't find a Location in the range for this Address")
        else:
            cleaned_data['NearestLocation'] = ValidBatch['Location'].id

        return cleaned_data

class PreCheckoutForm_PickItUp(forms.Form):
    
    type_of_sale = forms.CharField(widget=forms.HiddenInput())

    location = forms.ModelChoiceField(label="Where are you going to pick the order up?",
        widget=forms.Select(attrs={'class': attr2}),
        queryset=PaymentBatch.objects.filter(status='O'),
        to_field_name="location",
        empty_label="Select the Location..."
    )

    time = forms.ChoiceField(
        label="Time to Pick it Up",
        widget=forms.Select(attrs={'class': attr2}),
        choices=(('15','15 Minutes'),('20','20 Minutes'),('25','25 Minutes'),),
        initial='15',
    )

class PreCheckoutForm_ParkingLot(forms.Form):

    type_of_sale = forms.CharField(widget=forms.HiddenInput())

    location = forms.ModelChoiceField(label="Wich Parking lot Location are you?",
                                      widget=forms.Select(attrs={'class': attr2}),
                                      queryset=PaymentBatch.objects.filter(status='O'),
                                      to_field_name="location",
                                      empty_label="Select the Location...")

    car_model = forms.CharField(label='Car Model', 
                                max_length=50,
                                help_text='Ex: Mustang, Malibu',
                                widget=forms.TextInput(attrs={'class': attr,
                                                              'placeholder':'Car Model'})
    )

    car_brand = forms.CharField(label='Car Brand', 
                                 max_length=50, 
                                 help_text='Ex: Ford, Chevrolet',
                                 widget=forms.TextInput(attrs={'class': attr,
                                                               'placeholder':'Car Brand'}))

    car_color = forms.CharField(label='Car Color', 
                                 max_length=50, 
                                 help_text='Ex: White, Black, Silver',
                                 widget=forms.TextInput(attrs={'class': attr,
                                                               'placeholder':'Car Color'}))

    car_license = forms.CharField(label='Car License', 
                                 max_length=50, 
                                 help_text='Ex: ...',
                                 widget=forms.TextInput(attrs={'class': attr,
                                                               'placeholder':'Car License'}))

class WebInfoForm(forms.ModelForm):
    class Meta:
        model = WebInfo
        fields = '__all__'
        widgets = \
        {
            'name': TextInput(attrs={
                'class':attr2,
                'placeholder':'Name'}
            ),

            'email': EmailInput(attrs={
                'class':attr2,
                'placeholder':'Email'}
            ),

            'info': forms.Textarea(attrs={
                'class':attr2,
                'placeholder': WebText.objects.get_text('info_info'), 
                'rows':8}
            )
        }
    