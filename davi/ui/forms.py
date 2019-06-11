#-*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


class VaultForm(forms.Form):
    password = forms.CharField(max_length=100)
    yaml = forms.CharField(widget=forms.Textarea, required=False)
    vault = forms.CharField(widget=forms.Textarea, required=False)
