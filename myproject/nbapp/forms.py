from django import forms  
from .models import Emiten, TbpTable2
from bootstrap_datepicker_plus import DatePickerInput

class EmitenForm(forms.ModelForm):  
    class Meta:  
        model = Emiten  
        fields = "__all__"  

class TbpTable2Form(forms.ModelForm):
    class Meta:
        model=TbpTable2
        fields = "__all__"  
        #fields = ['date']
        widgets = {
            'date': DatePickerInput(),
        }

