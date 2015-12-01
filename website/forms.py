# -*- encoding: utf-8 -*-
# Powered by: Ing. Jorge Contreras
# Fecha: 05/11/2015

from django.forms import ModelForm, widgets, NumberInput
from django import forms
from ordertogo.models import *


class ArepaForm(forms.Form):

    id_for_product = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    arepa_type = forms.ChoiceField(
        label="Baked or Fried?",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=(('Baked','Baked'),('Fried','Fried'),),
        initial='Baked'
    )

    extras = forms.ModelMultipleChoiceField(
        label="Choose the Players with your Arepa...",
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat'}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='extras')).order_by('order_in_menu')
    )

    paid_extras = forms.ModelMultipleChoiceField(
        label="On The Bench",
        help_text="Choose as much players as you want for $0.99 each",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat'}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='paid.extras')).order_by('order_in_menu')
    )

    sauces = forms.ModelMultipleChoiceField(
        label="Sauces",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat'}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='sauces')).order_by('order_in_menu')
    )

    soft_drinks = forms.ModelChoiceField(
        label="Soft Drinks",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='drinks')).order_by('order_in_menu'),
        empty_label="I don't want any Dirnk"
    )
    '''
    def clean_extras(self):
        extras = self.cleaned_data.get('extras')
        pk = self.cleaned_data.get('id_for_product')

        info = product.objects.get(pk=pk)

        if not len(extras)==info.extras:
            raise forms.ValidationError("return an error")

        return extras
    '''

class KidForm(forms.Form):

    id_for_product = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    soft_drinks = forms.ModelChoiceField(
        label="Soft Drinks",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=product.objects.filter(Active=True,category=category.objects.get(code='drinks')).order_by('order_in_menu'),
        empty_label="I don't want any Dirnk"
    )

class CreateAccountForm(forms.Form):
    firstname = forms.CharField(
        max_length=80,
        label=" First Name",
        help_text="Ex: Jhon Doe",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Fisrt Name'})
    )

    lastname = forms.CharField(
        max_length=80,
        label="Last Name",
        help_text="Ex: Jhon Doe",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'})
    )

    username = forms.CharField(
        max_length=80,
        label="Username",
        help_text="Ex: jlopez",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'})
    )

    email = forms.EmailField(
        label="Email", 
        help_text="Ex: somebody@mysite.com", 
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'})
    )

    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'})
    )

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

    address = forms.CharField(
        label="Address to deliver the order",
        help_text="We can only makes delivery in a certain range",
        widget=forms.TextInput(attrs={'class': 'form-control has-feedback-left','placeholder':'Address'})
    )
    # 750 South Perry Street, Suite 400. Lawrenceville, GA 30046
    def clean_address(self):
        address = self.cleaned_data.get('address')
        key = GenericVariable.objects.get(code='google.API.KEY')
        
        origins = PaymentBatch.objects.filter(status='O', open_for_delivery=True)
        if len(origins) > 1:
            i = 0
            for location in origins:
                print location.address_for_truck
                print address
                valid_address = ValidateAddress(
                    key.value,
                    location.address_for_truck,
                    address,
                    location.max_miles)
                if valid_address == True:
                    i+=1
        else:
            raise forms.ValidationError("Sorry, we couldn't verify your address. Try it later")

        if i == 0:
            raise forms.ValidationError("You must enter an address in the range")

        print i
        return address

class PreCheckoutForm_PickItUp(forms.Form):
    type_of_sale = forms.CharField(widget=forms.HiddenInput())

    location = forms.ModelChoiceField(
        label="Location",
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=PaymentBatch.objects.filter(status='O'),
        to_field_name="location",
        empty_label="Select the Location..."
    )

    time = forms.ChoiceField(
        label="Time to Pick it Up",
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=(('15','15 Minutes'),('20','20 Minutes'),('25','25 Minutes'),),
        initial='15',
    )

def ValidateAddress(key,origin,destination,max_miles):
    import googlemaps
    from decimal import Decimal
    import json, pprint

    gmaps = googlemaps.Client(key=key)
    dest = gmaps.geocode(destination)
    directions_result = gmaps.directions(
        origin,
        dest[0]['formatted_address']
    )
    
    
    miles = directions_result[0]['legs'][0]['distance']['text'].split(' ')
    
    if  max_miles > Decimal(miles[0]):
        result = True
    else:
        result = False

    return result

