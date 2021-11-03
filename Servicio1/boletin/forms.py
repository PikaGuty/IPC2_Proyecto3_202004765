from django import forms
from .models import IVA, NITE, NITR, FECHA, MyModel
from datetime import datetime


class RegForm(forms.Form):
    ruta = forms.FileField()

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
        fields=['fecha']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['fecha'].widget.attrs.update({
            'class': 'form-control'
        })
        '''self.fields['f'].widget.attrs.update({
            'class': 'form-control'
        })'''


class DateInput(forms.DateInput):
    input_type = 'date'

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = '__all__'
        widgets = {
            'my_date': DateInput()
        }



class rangoForm(forms.Form):
    now = datetime.now()
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  
    fecha_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    iva=forms.IntegerField(widget=forms.Select(choices=[(1,'Con IVA'),(2,'Sin IVA')]))
    

        
        