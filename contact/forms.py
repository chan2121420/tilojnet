from django import forms
from .models import ContactMessage, QuoteRequest, Newsletter
from services.models import ServiceCategory, CategoryItem


class ContactForm(forms.ModelForm):
    """Form for contact messages with validation"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+263 771 234 567',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Your message here...',
                'required': True
            }),
        }
    
    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces and common separators
            phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if len(phone) < 10:
                raise forms.ValidationError("Please enter a valid phone number with at least 10 digits.")
        return phone
    
    def clean_message(self):
        """Ensure message has minimum length"""
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError("Please provide a more detailed message (at least 10 characters).")
        return message


class QuoteRequestForm(forms.ModelForm):
    """Form for quote requests with category items support"""
    
    class Meta:
        model = QuoteRequest
        fields = [
            'name', 'email', 'phone', 'service_category', 
            'category_items', 'location', 'budget', 
            'project_description', 'timeline'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'service_category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'category_items': forms.CheckboxSelectMultiple(),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country',
                'required': True
            }),
            'budget': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us about your vision, space requirements, style preferences...',
                'required': True
            }),
            'timeline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2-3 months',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category_items optional
        self.fields['category_items'].required = False
        self.fields['service_category'].empty_label = "Select Category"
    
    def clean_project_description(self):
        """Validate project description length"""
        description = self.cleaned_data.get('project_description')
        if description and len(description.strip()) < 20:
            raise forms.ValidationError(
                "Please provide more details about your project (at least 20 characters)."
            )
        return description
    
    def clean(self):
        """Additional cross-field validation"""
        cleaned_data = super().clean()
        service_category = cleaned_data.get('service_category')
        category_items = cleaned_data.get('category_items')
        
        # If category items are selected, ensure they belong to the selected category
        if service_category and category_items:
            for item in category_items:
                if item.category != service_category:
                    raise forms.ValidationError(
                        f"Selected item '{item.name}' does not belong to category '{service_category.name}'."
                    )
        
        return cleaned_data


class NewsletterForm(forms.ModelForm):
    """Simple newsletter subscription form"""
    
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
                'required': True
            })
        }
    
    def clean_email(self):
        """Check if email already exists"""
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed to our newsletter.")
        return email