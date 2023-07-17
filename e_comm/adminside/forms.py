# from django import forms
# from products.models import *
# from django.forms import formset_factory

# from multiupload.fields import MultiFileField
# class ImageForm(forms.Form):
#     image = forms.ImageField()

# ImageFormSet = formset_factory(ImageForm, extra=1)
# class catogeryform(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields =['name','image','slug']



# class productform(forms.ModelForm):
#     images = MultiFileField(min_num=0, max_num=10, max_file_size=1024*1024*5)
 
#     class Meta:
#         model = Products
#         fields = ('name', 'descriptions', 'price', 'catogery', 'images')
