# -*- encoding: utf-8 -*-
# Powered by: Ing. Jorge Contreras
# Fecha: 05/11/2015

from django.forms import ModelForm, widgets, NumberInput, TextInput, EmailInput
from django.contrib.auth.models import User
from django import forms
from ordertogo.models import *
from website.models import WebInfo, WebText

attr  = 'form-control has-feedback-left agencia-regular'
attr2 = 'form-control agencia-regular'
attr3 = 'flat agencia-regular'

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
                                                help_text="Please select \
                                                           wich vegetables do you \
                                                           want with your selected \
                                                           product"
        )

    extras = forms.ModelMultipleChoiceField(
        label="Choose the Players with your Arepa...",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': attr3}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='extras')).order_by('order_in_menu')
    )

    paid_extras = forms.ModelMultipleChoiceField(
        label="On The Bench",
        help_text="Choose as much players as you want for $0.99 each",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': attr3}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='paid.extras')).order_by('order_in_menu')
    )

    sauces = forms.ModelMultipleChoiceField(
        label="Sauces",
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
        arepa_type = cleaned_data.get("arepa_type")
        vegetables = cleaned_data.get("vegetables")
        extras = cleaned_data.get("extras")
        paid_extras = cleaned_data.get("paid_extras")
        sauces = cleaned_data.get("sauces")
        soft_drinks = cleaned_data.get("soft_drinks")
        qtty = cleaned_data.get("qtty")

        this_product = product.objects.get(pk=id_for_product)

        if (not this_product.extras == len(extras)) and this_product.allow_extras == True:
            msg = "You must select %d Players for this product" % this_product.extras
            self.add_error('extras', msg)

        if this_product.allow_qtty == True and (qtty < 1):
            msg = "You must enter a valid Quantty"
            self.add_error('qtty', msg)

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
        max_length=80,
        label="Name on Card",
        help_text="Ex: Jhon D Lopez"
    )

    card_number = forms.CharField(
        max_length=16,
        min_length=15,
        label="Card Number",
        help_text="Please Insert your card number"
    )

    expiry = forms.CharField(
        label="Expiricy Date",
        max_length=5,
        help_text="Ex: 06/16" )

    cvv = forms.CharField(
        max_length=4,
        min_length=3,
        label="CVV",
        help_text="This code is in the front side of your American Express Card, and in the back side of your Visa or Master Card"
    )

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

        return expiry

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

    # 750 South Perry Street, Suite 400. Lawrenceville, GA 30046
    def clean(self):
        cleaned_data = super(PreCheckoutForm_Delivery, self).clean()
        address = cleaned_data.get('address')
        city = cleaned_data.get('city')
        zip_code = cleaned_data.get('zip_code')

        addr_composed = address +", "+city+", GA, "+str(zip_code)
        
        key = GenericVariable.objects.val(code='google.API.KEY')
        
        origins = PaymentBatch.objects.filter(status='O', open_for_delivery=True)
        if len(origins) > 0:
            i = 0
            for location in origins:
                valid_address = ValidateAddress(key, location.address_for_truck,
                                                addr_composed,location.max_miles)
                if valid_address == True:
                    i+=1
        else:
            self.add_error('address',"Sorry, we couldn't verify your address. Try it later")
        
        if i == 0:
            self.add_error('address',"You must enter an address in the range")

class PreCheckoutForm_PickItUp(forms.Form):
    type_of_sale = forms.CharField(widget=forms.HiddenInput())

    location = forms.ModelChoiceField(label="Location",
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

    location = forms.ModelChoiceField(label="Location",
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

def ValidateAddress(key,origin,destination,max_miles):
    import googlemaps
    from decimal import Decimal
    import json, pprint

    gmaps = googlemaps.Client(key=key)
    print destination
    dest = gmaps.geocode(destination)
    directions_result = gmaps.directions(
        origin,
        dest[0]['formatted_address']
    )
    miles = directions_result[0]['legs'][0]['distance']['text'].split(' ')
    
    if miles[1] == 'ft':
        result = True
    elif  Decimal(miles[0]) < max_miles:
        result = True
    else:
        result = False

    return result
    