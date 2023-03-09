from django import forms
from account.models import UserProfile, Blogs, Comments

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

        widgets = {
            'age' :forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your age'}),
            'gender' : forms.Select(attrs={'class':'form-control',}),
            'phone' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter your phone number'}),
            'profile_pic' : forms.FileInput()

        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=20,label="Old Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Old Password'}))
    new_password = forms.CharField(max_length=20,label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter New Password'}))
    c_password = forms.CharField(max_length=20,label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Re-enter Password'}))

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['title','description','image']
        widgets = {
            'title' :forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your title'}),
            'description' : forms.Textarea(attrs={'class':'form-control','placeholder':'Enter your description'}),
            'image' : forms.FileInput()

        }

class CommentForm(forms.ModelForm):
     class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment' : forms.Textarea(attrs={'class':'form-control','placeholder':'Type your comment...'}),
        }
