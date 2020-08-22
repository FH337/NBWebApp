import django_filters 
from .models import Emiten, TbpTable2

#filter for emiten
class EmitenFilter(django_filters.FilterSet):
    class Meta:
        model = Emiten
        fields = ['emiten_code', 'emiten_name']


#filter for sentencesplit
class TbpTable2Filter(django_filters.FilterSet):
    class Meta:
        model = TbpTable2
        fields = ['emiten']
