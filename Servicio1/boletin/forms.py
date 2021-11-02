from django import forms
from .models import NITE, NITR, FECHA


class RegForm(forms.Form):
    ruta = forms.CharField()
    

class teForm(forms.Form):
    xml = forms.CharField(widget=forms.Textarea)

class nitForm(forms.ModelForm):
    class Meta:
        model=NITE
        fields=['nit']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nit'].widget.attrs.update({
            'class': 'form-control'
        })

class nitrForm(forms.ModelForm):
    class Meta:
        model=NITR
        fields=['nit']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nit'].widget.attrs.update({
            'class': 'form-control'
        })

class fForm(forms.ModelForm):
    class Meta:
        model=FECHA
        fields=['nit']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['nit'].widget.attrs.update({
            'class': 'form-control'
        })