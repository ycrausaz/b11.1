from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
import re
from django.http import HttpResponseRedirect

class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None

    def test_func(self):
        if self.group_required and self.request.user.is_authenticated:
            if self.request.user.groups.filter(name=self.group_required).exists() or self.request.user.is_superuser:
                return True
        raise PermissionDenied

class grIL_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grIL'

class grGD_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grGD'

class grSMDA_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grSMDA'

class FormValidMixin:
    """
    Mixin to handle the common form_valid logic for CreateView and UpdateView.
    """

    def form_valid(self, form):
        # Add the name of the 'hersteller'
        item = form.save(commit=False)
        item.hersteller = self.request.user.username
        print("item.hersteller = " + item.hersteller)
        item.gewichtseinheit = "KG"
        print("item.gewichtseinheit = " + item.gewichtseinheit)
        item.nsn_gruppe_klasse = "XXXXXXXXXX"
        print("item.nsn_gruppe_klasse = " + item.nsn_gruppe_klasse)
        item.nato_versorgungs_nr = "XXXXXXXXXX"
        print("item.nato_versorgungs_nr = " + item.nato_versorgungs_nr)
        item.einheit_l_b_h = "MM"
        print("item.einheit_l_b_h = " + item.einheit_l_b_h)
        item.waehrung = "CHF"
        print("item.waehrung = " + item.waehrung)

        pattern = r'^\d{4}-\d{2}-\d{3}-\d{4}$'
        if len(item.nato_stock_number) > 0:
            if not re.match(pattern, item.nato_stock_number):
                form.add_error('nato_stock_number', "Der Feld 'Nato Stock Number' muss die folgende Formatierung haben: 'XXXX-XX-XXX-XXXX'.")

        if form.errors:
            return self.form_invalid(form)

        pattern = r'^(\d{4})-\d{2}-\d{3}-\d{4}$'
        match = re.match(pattern, item.nato_stock_number)
        if match:
            item.nsn_gruppe_klasse = match.group(1)

        pattern = r'^\d{4}-(\d{2}-\d{3}-\d{4})$'
        match = re.match(pattern, item.nato_stock_number)
        if match:
            item.nato_versorgungs_nr = match.group(1).replace('-', '')

        item.save()
        return super().form_valid(form)

