# forms_material_management.py

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

class MaterialAssignmentInlineForm(forms.Form):
    """
    Changed from ModelForm to regular Form to avoid Django's automatic queryset filtering
    """
    
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='grIL').order_by('email'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assigned Users"
    )
    
    primary_user = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='grIL').order_by('email'),
        required=False,
        empty_label="No primary user",
        label="Primary User",
        widget=forms.Select(attrs={
            'class': 'assignment-primary-select form-select',
            'id': 'id_primary_user'
        })
    )
    
    def __init__(self, *args, **kwargs):
        # Extract the instance (material) from kwargs
        self.instance = kwargs.pop('instance', None)
        
        super().__init__(*args, **kwargs)
        
        # Get ALL IL users
        all_il_users = User.objects.filter(groups__name='grIL').order_by('email')
        
        print(f"DEBUG CLEAN: Found {all_il_users.count()} total IL users")
        
        # Explicitly set querysets to ALL IL users
        self.fields['assigned_users'].queryset = all_il_users
        self.fields['primary_user'].queryset = all_il_users
        
        # Set initial values if we have a material instance
        if self.instance and hasattr(self.instance, 'pk') and self.instance.pk:
            try:
                # Get currently assigned users and primary user
                currently_assigned = self.instance.get_assigned_users()
                current_primary = self.instance.get_primary_user()
                
                print(f"DEBUG CLEAN: Currently assigned: {[u.email for u in currently_assigned]}")
                print(f"DEBUG CLEAN: Current primary: {current_primary.email if current_primary else 'None'}")
                
                # Set initial values
                self.fields['assigned_users'].initial = currently_assigned
                if current_primary:
                    self.fields['primary_user'].initial = current_primary.pk
                
            except Exception as e:
                print(f"DEBUG CLEAN: Error setting initial values: {e}")
        
        print(f"DEBUG CLEAN: Final queryset count: {self.fields['primary_user'].queryset.count()}")
    
    def save(self, material, request_user):
        """
        Custom save method since we're not using ModelForm
        """
        assigned_users = self.cleaned_data['assigned_users']
        primary_user = self.cleaned_data['primary_user']
        
        # Remove all existing assignments
        MaterialUserAssociation.objects.filter(material=material).delete()
        
        # Ensure primary user is included in assigned users if specified
        users_to_assign = set(assigned_users)
        if primary_user:
            users_to_assign.add(primary_user)
        
        # Create new assignments
        for user in users_to_assign:
            is_primary = (user == primary_user)
            MaterialUserAssociation.objects.create(
                material=material,
                user=user,
                assigned_by=request_user,
                is_primary=is_primary
            )
        
        return material
