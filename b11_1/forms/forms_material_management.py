from django import forms
from django.contrib.auth.models import User
from ..models import Material, MaterialUserAssociation

class MaterialUserAssignmentForm(forms.Form):
    """Form for bulk assignment of users to materials"""
    
    materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'material-checkbox'}),
        required=True,
        label="Select Materials"
    )
    
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='grIL'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'user-checkbox'}),
        required=True,
        label="Select IL Users"
    )
    
    action = forms.ChoiceField(
        choices=[
            ('assign', 'Assign Users to Materials'),
            ('remove', 'Remove Users from Materials'),
            ('replace', 'Replace All Assignments')
        ],
        widget=forms.RadioSelect,
        initial='assign'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order materials by position number
        self.fields['materials'].queryset = Material.objects.filter(
            is_archived=False
        ).order_by('positions_nr')
        
        # Order users by email
        self.fields['users'].queryset = User.objects.filter(
            groups__name='grIL'
        ).order_by('email')

class MaterialAssignmentInlineForm(forms.ModelForm):
    """Inline form for individual material assignments"""
    
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='grIL'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    primary_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='grIL'),
        required=False,
        empty_label="No primary user"
    )
    
    class Meta:
        model = Material
        fields = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Set initial values for existing material
            self.fields['assigned_users'].initial = self.instance.get_assigned_users()
            self.fields['primary_user'].initial = self.instance.get_primary_user()
