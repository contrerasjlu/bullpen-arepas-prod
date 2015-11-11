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
            raise forms.ValidationError(loadMsj('Return an Error'))

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