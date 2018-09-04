from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Grade


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['dem1', 'dem2', 'dem3', 'dem4', 'comment', 'img']
        labels = {
            'dem1': _('清晰度'),
            'dem2': _('对比'),
            'dem3': _('维度'),
            'dem4': _('定制'),
        }
    img = forms.IntegerField(required=False, widget=forms.HiddenInput())
