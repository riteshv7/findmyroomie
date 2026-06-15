from django import forms
from .models import RoomieUser, Listing

class LoginForm(forms.Form):
    phone = forms.CharField(
        max_length=15, 
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 10-digit mobile number (e.g. 9876543210)',
            'class': 'form-input',
            'pattern': '[0-9]{10}',
            'required': True
        })
    )

class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6, 
        min_length=6,
        label="OTP Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit OTP (123456)',
            'class': 'form-input text-center',
            'pattern': '[0-9]{6}',
            'required': True
        })
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = RoomieUser
        fields = ['first_name', 'last_name', 'age', 'gender', 'occupation']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Occupation (e.g. Software Engineer)'}),
        }

    languages = forms.MultipleChoiceField(
        choices=[
            ('English', 'English'),
            ('Kannada', 'Kannada'),
            ('Hindi', 'Hindi'),
            ('Telugu', 'Telugu'),
            ('Tamil', 'Tamil'),
            ('Malayalam', 'Malayalam'),
            ('Bengali', 'Bengali'),
            ('Marathi', 'Marathi'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False
    )

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'type', 'area', 'nearest_metro', 'rent', 'deposit', 
            'setup_cost', 'monthly_expense_estimate', 'available_from', 
            'house_rules'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-input'}),
            'area': forms.Select(attrs={'class': 'form-input'}),
            'nearest_metro': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nearest Metro Station (e.g. Indiranagar, 500m)'}),
            'rent': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Monthly Rent in ₹'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Security Deposit in ₹'}),
            'setup_cost': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'One-time setup cost in ₹'}),
            'monthly_expense_estimate': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Approx. monthly bills (wifi, maid, power)'}),
            'available_from': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'house_rules': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'E.g., quiet hours after 11 PM, clean up immediately...'}),
        }

    # Choice fields for lifestyle profile
    food_policy = forms.ChoiceField(
        choices=[('veg', 'Veg'), ('non-veg', 'Non-veg'), ('eggetarian', 'Eggetarian')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Food Policy"
    )
    share_kitchen_non_veg = forms.BooleanField(
        required=False,
        label="OK sharing kitchen with non-veg cooking?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    tenant_type = forms.ChoiceField(
        choices=[
            ('bachelors', 'Bachelors'), 
            ('family', 'Family'), 
            ('students', 'Students'), 
            ('working_professionals', 'Working Professionals')
        ],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Who lives there / Target Tenant"
    )
    smoking_allowed = forms.BooleanField(
        required=False,
        label="Smoking Allowed?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    drinking_allowed = forms.BooleanField(
        required=False,
        label="Drinking Allowed?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    partner_stays_over = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('restricted', 'Restricted')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Partner stays over policy"
    )
    guests_policy = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('restricted', 'Restricted')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Guests policy"
    )
    noise_level = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'radio-group-horizontal'}),
        label="Noise Level (1 = quietest, 5 = loudest)"
    )
    cleanliness_level = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'radio-group-horizontal'}),
        label="Cleanliness/Hygiene (1 = messy, 5 = spotless)"
    )
    languages = forms.MultipleChoiceField(
        choices=[
            ('English', 'English'),
            ('Kannada', 'Kannada'),
            ('Hindi', 'Hindi'),
            ('Telugu', 'Telugu'),
            ('Tamil', 'Tamil'),
            ('Malayalam', 'Malayalam'),
            ('Bengali', 'Bengali'),
            ('Marathi', 'Marathi'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        label="Languages spoken by household"
    )
    cook_maid = forms.ChoiceField(
        choices=[('present', 'Present'), ('wanted', 'Wanted'), ('none', 'None')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Cook/Maid Status"
    )
    pets_allowed = forms.BooleanField(
        required=False,
        label="Pets Allowed?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    parking_available = forms.BooleanField(
        required=False,
        label="Parking Available?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    photo_choice = forms.ChoiceField(
        choices=[
            ('/static/images/room1.png', 'Modern Light Room'),
            ('/static/images/room2.png', 'Cosy Shared Room'),
            ('/static/images/room3.png', 'Luxury Living Room/BHK'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'radio-group-images'}),
        label="Select a Photo to Display",
        required=False,
        initial='/static/images/room1.png'
    )
    
    image = forms.ImageField(
        required=False,
        label="Or Upload a Custom Photo",
        widget=forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'})
    )


class SeekerPreferenceForm(forms.Form):
    # Food Preference
    food_preference = forms.ChoiceField(
        choices=[('veg', 'Veg'), ('non-veg', 'Non-veg'), ('eggetarian', 'Eggetarian'), ('any', 'Any')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Food Preference"
    )
    share_kitchen_non_veg = forms.BooleanField(
        required=False,
        label="OK sharing kitchen with non-veg cooking?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    # Target flatmates
    preferred_types = forms.MultipleChoiceField(
        choices=[
            ('bachelors', 'Bachelors'), 
            ('family', 'Family'), 
            ('students', 'Students'), 
            ('working_professionals', 'Working Professionals')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        label="Preferred Household Type"
    )
    
    # Lifestyle preferences
    smoking_ok = forms.BooleanField(
        required=False,
        label="OK with smoking flatmates?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    drinking_ok = forms.BooleanField(
        required=False,
        label="OK with drinking flatmates?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    partner_stays_over = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('restricted', 'Restricted'), ('any', 'Any')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Partner stays over policy"
    )
    guests_policy = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('restricted', 'Restricted'), ('any', 'Any')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Guests policy"
    )
    noise_tolerance = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'radio-group-horizontal'}),
        label="Noise Tolerance (1 = quiet only, 5 = any volume)"
    )
    cleanliness = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'radio-group-horizontal'}),
        label="Minimum Cleanliness Standards (1 = relaxed, 5 = immaculate)"
    )
    
    # Languages preferred
    languages = forms.MultipleChoiceField(
        choices=[
            ('English', 'English'),
            ('Kannada', 'Kannada'),
            ('Hindi', 'Hindi'),
            ('Telugu', 'Telugu'),
            ('Tamil', 'Tamil'),
            ('Malayalam', 'Malayalam'),
            ('Bengali', 'Bengali'),
            ('Marathi', 'Marathi'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        label="Languages preferred"
    )
    
    # Cook/Maid Status
    cook_maid = forms.ChoiceField(
        choices=[('present', 'Present'), ('wanted', 'Wanted'), ('none', 'None'), ('any', 'Any')],
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label="Cook/Maid Preferences"
    )
    pets_ok = forms.BooleanField(
        required=False,
        label="OK with pets?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    parking_needed = forms.BooleanField(
        required=False,
        label="Parking needed?",
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
    # Budget ranges
    rent_min = forms.IntegerField(
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Min Rent (₹)'})
    )
    rent_max = forms.IntegerField(
        initial=50000,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Rent (₹)'})
    )
    deposit_max = forms.IntegerField(
        initial=150000,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Deposit (₹)'})
    )
    setup_cost_max = forms.IntegerField(
        initial=20000,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Setup Cost (₹)'})
    )
    monthly_expense_max = forms.IntegerField(
        initial=10000,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Bills (₹)'})
    )
    
    # Areas preferred
    preferred_areas = forms.MultipleChoiceField(
        choices=[
            ('Koramangala', 'Koramangala'),
            ('HSR Layout', 'HSR Layout'),
            ('Indiranagar', 'Indiranagar'),
            ('BTM Layout', 'BTM Layout'),
            ('Bellandur', 'Bellandur'),
            ('Marathahalli', 'Marathahalli'),
            ('Whitefield', 'Whitefield'),
            ('Electronic City', 'Electronic City'),
            ('Other', 'Other')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        label="Preferred Areas"
    )
    distance_max_km = forms.IntegerField(
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max distance from office/college (km)'})
    )

