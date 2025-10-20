from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile,MeritList,Announcement,FAApplication,BSApplication,FSCApplication
from django.forms.widgets import SelectDateWidget
from datetime import datetime



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

from django import forms

class FAApplicationForm(forms.ModelForm):
    QUOTA_CHOICES = [
        ('', 'No Quota'),  
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
    ]
    
    quota = forms.ChoiceField(
        choices=QUOTA_CHOICES, 
        required=False,  
        label="Quota",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    roll_no = forms.IntegerField(
        label="Roll Number",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Roll Number'}),
        required=False  
    )

    class Meta:
        model = FAApplication
        fields = [
            'college_selection', 'program_selection', 'employment_status', 'cnic', 'domicile', 
            'religion', 'ssc_registration_number', 'last_school_attended', 'year_of_passing', 
            'roll_no', 'marks_obtained', 'max_marks', 'div_grade', 'board', 'quota', 
            'attested_photocopy_hssc', 'attested_photocopy_father_mother_cnic', 
            'attested_photocopy_candidate_cnic', 'provisional_character_certificate', 
            'original_migration_certificate', 'passport_photographs', 
            'proof_employment_status_parents', 'affidavit_district_court', 
            'payment_screenshot'
        ]

        widgets = {
            'ssc_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SSC Registration Number'}),
            'last_school_attended': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last school attended'}),
            'cnic': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter your CNIC with dashes'}),
            'domicile': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter your Domicile'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter your Religion'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year of Passing'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Marks Obtained'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Maximum Marks'}),
            'div_grade': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Division/Grade'}),
            'board': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Enter Board Name'}),
            'payment_screenshot': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'required', 'placeholder': 'Upload Payment Screenshot'}),
            'college_selection': forms.TextInput(attrs={'class': 'form-control', 'value': 'FG College', 'readonly': 'readonly'}),  # Display as non-editable text
            'proof_employment_status_parents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'proof_employment_status_parents': "(optional)",
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_screenshot'].label = "Upload Payment Screenshot"
        self.fields['payment_screenshot'].help_text = (
        "Please transfer the form fee of RS 200 to one of the following accounts: "
        "Easypaisa: 0345-XXXXXXX, JazzCash: 0300-XXXXXXX. "
        "After completing the transfer, upload the payment screenshot here."
    )

    
        for field in self.fields:
            if field not in ['quota', 'proof_employment_status_parents']:
                self.fields[field].required = True
            
            self.fields[field].error_messages['required'] = (
                f'{self.fields[field].label} is required. Please provide this information.'
            )

    
        self.fields['proof_employment_status_parents'].required = False

        
        
class FSCApplicationForm(forms.ModelForm):
    QUOTA_CHOICES = [
        ('', 'No Quota'),  
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
    ]
    
    quota = forms.ChoiceField(
        choices=QUOTA_CHOICES, 
        required=False,  
        label="Quota",
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select if applicable'})
    )

    class Meta:
        model = FSCApplication
        fields = [
            'college_selection', 'program_selection', 'employment_status', 'cnic', 'domicile', 'religion',
            'ssc_registration_number', 'last_school_attended', 'year_of_passing_ssc', 'ssc_roll_no', 
            'marks_obtained', 'max_marks', 'ssc_div_grade', 'ssc_board', 'quota', 
            'attested_photocopy_hssc', 'attested_photocopy_father_mother_cnic', 
            'attested_photocopy_candidate_cnic', 'provisional_character_certificate', 
            'original_migration_certificate', 'passport_photographs', 
            'proof_employment_status_parents', 'affidavit_district_court', 'payment_screenshot'
        ]
        widgets = {
            'cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your CNIC with dashes'}),
            'domicile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Domicile'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Religion'}),
            'ssc_registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SSC Registration Number'}),
            'last_school_attended': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last school attended'}),
            'year_of_passing_ssc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year of Passing SSC'}),
            'ssc_roll_no': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Enter SSC Roll Number'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marks Obtained'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Maximum Marks'}),
            'ssc_div_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Division/Grade'}),
            'ssc_board': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SSC Board'}),
            'payment_screenshot': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Payment Screenshot'}),
            'college_selection': forms.TextInput(attrs={'class': 'form-control', 'value': 'FG College', 'readonly': 'readonly'}),  # Display as non-editable text
            'proof_employment_status_parents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'proof_employment_status_parents': "(optional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_screenshot'].label = "Upload Payment Screenshot"
        self.fields['payment_screenshot'].help_text = (
            "Please transfer the form fee RS 200 to one of the following accounts: "
            "Easypaisa: 0345-XXXXXXX, JazzCash: 0300-XXXXXXX. "
            "After completing the transfer, upload the payment transaction screenshot here."
        )

        
        for field in self.fields:
            if field == 'employment_status' or field == 'proof_employment_status_parents':
                self.fields[field].required = False  
            elif field != 'quota':
                self.fields[field].required = True
                self.fields[field].error_messages = {
                    'required': f'{self.fields[field].label} is required. Please provide this information.'
                }

    def clean(self):
        cleaned_data = super().clean()

        
        marks_obtained = cleaned_data.get('ssc_marks_obtained')
        max_marks = cleaned_data.get('ssc_max_marks')

        if marks_obtained is not None and max_marks is not None:
            if marks_obtained > max_marks:
                raise ValidationError("Marks obtained cannot exceed maximum marks.")
        
        return cleaned_data

        
        
        
class BSApplicationForm(forms.ModelForm):
    QUOTA_CHOICES = [
        ('', 'No Quota'),  
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
    ]
    
    quota = forms.ChoiceField(
        choices=QUOTA_CHOICES, 
        required=False,
        label="Quota",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = BSApplication
        fields = [
            'college_selection', 'program_selection', 'employment_status', 'cnic', 'domicile', 'religion', 
            'certificate_degree_level', 'year_of_passing', 'marks_obtained', 'max_marks', 'roll_no', 'board',
            'major_subject', 'father_cnic', 'relationship_to_student', 'father_profession', 'contact_number', 
            'emergency_number', 'father_whatsapp_number', 'quota', 'attested_photocopy_hssc', 
            'attested_photocopy_father_mother_cnic', 'attested_photocopy_candidate_cnic', 
            'provisional_character_certificate', 'original_migration_certificate', 'passport_photographs', 
            'proof_employment_status_parents', 'affidavit_district_court', 'payment_screenshot'
        ]
        widgets = {
            'college_selection': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Select College'}),
            'program_selection': forms.Select(attrs={'class': 'form-control'}),  
            
            'cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CNIC With Dashes '}),
            'domicile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Domicile'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Religion'}),
            'certificate_degree_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Certificate/Degree Level'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Year of Passing'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Marks Obtained'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Maximum Marks'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number'}),
            'board': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Board'}),
            'major_subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Major Subject'}),
            'father_cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father\'s CNIC'}),
            'relationship_to_student': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Relationship to Student'}),
            'father_profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father\'s Profession'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number (11 digits)'}),
            'emergency_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Emergency Contact Number'}),
            'father_whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Father\'s WhatsApp Number'}),
            'attested_photocopy_hssc': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Attested HSSC Copy'}),
            'attested_photocopy_father_mother_cnic': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload CNIC Copy of Parents'}),
            'attested_photocopy_candidate_cnic': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Candidate\'s CNIC Copy'}),
            'provisional_character_certificate': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Character Certificate'}),
            'original_migration_certificate': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Migration Certificate'}),
            'passport_photographs': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Passport Photographs'}),
            'proof_employment_status_parents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        
            'affidavit_district_court': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload District Court Affidavit'}),
            'payment_screenshot': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload Payment Screenshot'}),
            'college_selection': forms.TextInput(attrs={'class': 'form-control', 'value': 'FG College', 'readonly': 'readonly'}),  # Display as non-editable text
        }
        help_texts = {
            'proof_employment_status_parents': "(optional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_screenshot'].label = "Upload Payment Screenshot"
        self.fields['payment_screenshot'].help_text = (
            "Please transfer the form fee RS 200 to one of the following accounts: "
            "Easypaisa: 0345-XXXXXXX, JazzCash: 0300-XXXXXXX. "
            "After completing the transfer, upload the payment transaction screenshot here."
        )

        
        for field in self.fields:
            if field in ['employment_status', 'proof_employment_status_parents', 'quota']:
                self.fields[field].required = False
            else:
                self.fields[field].required = True
                self.fields[field].error_messages = {
                    'required': f'{self.fields[field].label} is required. Please provide this information.'
                }

    def clean(self):
        cleaned_data = super().clean()

        # Validate obtained marks and total marks
        obtained_marks = cleaned_data.get('marks_obtained')
        total_marks = cleaned_data.get('max_marks')
        if obtained_marks is not None and total_marks is not None:
            if obtained_marks > total_marks:
                raise ValidationError("Obtained marks cannot exceed total marks.")

        # Validate phone number fields
        phone_fields = ['contact_number', 'emergency_number', 'father_whatsapp_number']
        for field in phone_fields:
            phone_number = cleaned_data.get(field)
            if phone_number and (len(phone_number) != 11 or not phone_number.isdigit()):
                raise ValidationError(f"{self.fields[field].label} must be exactly 11 digits.")

        return cleaned_data

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = None  # This will be dynamically set in the view

    def __init__(self, *args, **kwargs):
        application_type = kwargs.pop('application_type', None)
        super(ApplicationStatusForm, self).__init__(*args, **kwargs)
        if application_type == 'FA':
            self.Meta.model = FAApplication
        elif application_type == 'FSC':
            self.Meta.model = FSCApplication
        elif application_type == 'BS':
            self.Meta.model = BSApplication

        self.fields['status'] = forms.ChoiceField(
            choices=[
                ('accepted', 'Accepted'),
                ('rejected', 'Rejected')
            ],
            widget=forms.Select(attrs={'class': 'form-control'})
        )



class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['profile_image', 'father_name', 'date_of_birth', 'address', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email  

        # Add CSS classes to fields for styling
        self.fields['father_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        # Check if phone is None or empty
        if not phone:
            raise forms.ValidationError("Phone number is required.")

        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")

        if len(phone) != 11:
            raise forms.ValidationError("Phone number must be exactly 11 digits.")

        return phone

    def clean_father_name(self):
        father_name = self.cleaned_data.get('father_name')
        if not father_name:
            raise forms.ValidationError("Father's name is required.")
        if not father_name.replace(" ", "").isalpha(): # Ensure only alphabets
            raise forms.ValidationError("Father's name must contain only letters.")
        return father_name

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if not profile_image:  # Handle empty profile image
            raise ValidationError("Profile image is required.")
        return profile_image

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if not dob:
            raise ValidationError("Date of birth is required.")
        return dob
    
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise ValidationError("Address is required.")
        return address


    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.save()
            profile.user.save()
        return profile
        
        
class MeritListForm(forms.ModelForm):
    class Meta:
        model = MeritList
        fields = ['program']
        
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        
        
        
class AdminSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        user.is_staff = True  # Mark user as admin
        if commit:
            user.save()
        return user