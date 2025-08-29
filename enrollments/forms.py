from django import forms
from .models import EnrollmentRequest

class EnrollmentRequestForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRequest
        fields = ['phone_number', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you want to join this course...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['phone_number'].required = True
        self.fields['email'].required = True
