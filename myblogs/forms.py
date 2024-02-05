from.models import blog_category, Comment, blog_post
from django.forms import ModelForm
from django import forms
 
class Blog_Form(ModelForm):
    class Meta:
         model = blog_category
         fields = "__all__"

class blog_post_form(ModelForm):
     class Meta:
          model = blog_post
          fields="__all__"
          exclude =["like_count","views_count"]
         
class CommentForm(ModelForm):
     class Meta:
          model=Comment
          fields="__all__"
          exclude = ['post', 'created_date', 'author']
          widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add Comments', 'rows': 3}),  # Adjust rows as per your requirement
        }