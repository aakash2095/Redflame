from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . models import Userdetails

class Registerform(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        label={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
                'first_name':forms.TextInput(attrs={'class':'form-control'}),
                'last_name':forms.TextInput(attrs={'class':'form-control'}),
                'email':forms.TextInput(attrs={'class':'form-control'}),}
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name[0].isdigit():
            raise ValidationError("first_name cannot start with a number")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')      
        if last_name[0].isdigit():
            raise ValidationError("Last name cannot start with a number")
        return last_name
        

class Authenticateform(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class userchange(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        widgets= {'username':forms.TextInput(attrs={'class':'form-control'}),
                  'first_name':forms.TextInput(attrs={'class':'form-control'}),
                  'last_name':forms.TextInput(attrs={'class':'form-control'}),
                  'email':forms.TextInput(attrs={'class':'form-control'}),
                  }
        


class changepasswordform(PasswordChangeForm):
    old_password=forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

class AdminProfileForm(UserChangeForm):
    password =None
    class Meta:
        model = User
        fields = '__all__'
        widgets= {'username':forms.TextInput(attrs={'class':'form-control'}),
                  'email':forms.TextInput(attrs={'class':'form-control'}),
                  'first_name':forms.TextInput(attrs={'class':'form-control'}),
                  'last_name':forms.TextInput(attrs={'class':'form-control'}),
                  }
        
class Userform(forms.ModelForm):
    class Meta:
        model=Userdetails
        fields=['name','address','city','state','pincode']
        labels ={'name':'Full Name'}
        widgets= {'name':forms.TextInput(attrs={'class':'form-control'}),
                  'address':forms.TextInput(attrs={'class':'form-control'}),
                  'city':forms.TextInput(attrs={'class':'form-control'}),
                  'state':forms.Select(attrs={'class':'form-control'}),
                  'pincode':forms.NumberInput(attrs={'class':'form-control'}),
                  }
        
