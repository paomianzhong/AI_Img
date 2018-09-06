from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Grade

CHOICES_1 = (
    (5, '5-大都更鲜明'),
    (4, '4-部分更鲜明'),
    (3, '3-不变'),
    (2, '2-轻微失真'),
    (1, '1-严重失真'),
)

CHOICES_2 = (
    (5, '5-大都更合适'),
    (4, '4-部分更合适'),
    (3, '3-不变'),
    (2, '2-轻微失真'),
    (1, '1-严重失真'),
)

CHOICES_3 = (
    (5, '5-大都更清晰'),
    (4, '4-部分更清晰'),
    (3, '3-不变'),
    (2, '2-轻微失真'),
    (1, '1-严重失真'),
)

CHOICES_4 = (
    (5, '5-被消除'),
    (4, '4-被减弱'),
    (3, '3-不变'),
    (2, '2-轻微增强'),
    (1, '1-显著增强'),
)

CHOICES_5 = (
    (5, '5-大都更清晰'),
    (4, '4-部分更清晰'),
    (3, '3-不变'),
    (2, '2-轻微被模糊或锐化过度'),
    (1, '1-显著被模糊或锐化过度'),
)


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['dem1', 'dem2', 'dem3', 'dem4', 'dem5', 'img']
    img = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dem1 = forms.IntegerField(required=True, widget=forms.Select(choices=CHOICES_1), label='色调')
    dem2 = forms.IntegerField(required=True, widget=forms.Select(choices=CHOICES_2), label='亮度')
    dem3 = forms.IntegerField(required=True, widget=forms.Select(choices=CHOICES_3), label='内容')
    dem4 = forms.IntegerField(required=True, widget=forms.Select(choices=CHOICES_4), label='噪声')
    dem5 = forms.IntegerField(required=True, widget=forms.Select(choices=CHOICES_5), label='纹理')