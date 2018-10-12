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


NEW_CHOICES_1 = (
    (5, '5-没有虚焦'),
    (4, '4-轻微虚焦'),
    (3, '3-中度虚焦'),
    (2, '2-较多虚焦'),
    (1, '1-严重虚焦'),
)

NEW_CHOICES_2 = (
    (5, '5-没有模糊'),
    (4, '4-轻微模糊'),
    (3, '3-中度模糊'),
    (2, '2-较多模糊'),
    (1, '1-严重模糊'),
)

NEW_CHOICES_3 = (
    (5, '5-没有曝光'),
    (4, '4-轻微曝光'),
    (3, '3-中度曝光'),
    (2, '2-较多曝光'),
    (1, '1-过曝'),
)

GAIJIN_CHOICES_1 = (
    (3, '3-没有改进空间'),
    (2, '2-改进空间一般'),
    (1, '1-改进空间很大'),
)


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['dem1', 'dem2', 'dem3', 'dem4', 'dem5', 'img']
    img = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dem1 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='色调', initial=3)
    dem2 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='亮度', initial=3)
    dem3 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='内容', initial=3)
    dem4 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='噪声', initial=3)
    dem5 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='纹理', initial=3)


class GradeForm2(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['dem1', 'dem2', 'dem3', 'dem4', 'img']
    img = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dem1 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='对焦', initial=3)
    dem2 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='清晰', initial=3)
    dem3 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='曝光', initial=3)
    dem4 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), ]), label='颜值', initial=3)


class GradeForm3(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['dem1', 'img']
    img = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dem1 = forms.IntegerField(required=True, widget=forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), ]), label='改进空间', initial=2)
