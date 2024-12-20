from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
import re
from django.http import HttpResponseRedirect
from .models import *
from pprint import pprint

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

class grLBA_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grLBA'

class grAdmin_GroupRequiredMixin(GroupRequiredMixin):
    group_required = 'grAdmin'

class FormValidMixin_IL:
    """
    Mixin to handle the common form_valid logic for CreateView and UpdateView.
    """

    def form_invalid(self, form):
        form.add_error(None, "Es gibt einen oder mehreren Fehler im Formular.")
        return super().form_invalid(form)

    def form_valid(self, form):
        item = form.save(commit=False)

        # Hersteller
        item.hersteller = self.request.user.username
        print("item.hersteller = " + item.hersteller)

        # Gewichtseinheit
        item.gewichtseinheit = "KG"
        print("item.gewichtseinheit = " + item.gewichtseinheit)

        # NSN Gruppe / Klasse
        pattern = r'^\d{4}-\d{2}-\d{3}-\d{4}$'
        if item.nato_stock_number is not None:
            if not re.match(pattern, item.nato_stock_number):
                form.add_error('nato_stock_number', "Der Feld 'Nato Stock Number' muss die folgende Formatierung haben: 'XXXX-XX-XXX-XXXX'.")
        pattern = r'^(\d{4})-\d{2}-\d{3}-\d{4}$'
        match = re.match(pattern, item.nato_stock_number)
        if match:
            item.nsn_gruppe_klasse = match.group(1)

        # Nato Versorgungs-Nr.
        pattern = r'^\d{4}-(\d{2}-\d{3}-\d{4})$'
        match = re.match(pattern, item.nato_stock_number)
        if match:
            item.nato_versorgungs_nr = match.group(1).replace('-', '')

        # Einheit L / B / H
        item.einheit_l_b_h = "MM"
        print("item.einheit_l_b_h = " + item.einheit_l_b_h)

        # Währung
        item.waehrung = "CHF"
        print("item.waehrung = " + item.waehrung)

        if form.errors:
            return self.form_invalid(form)

        item.save()

        return super().form_valid(form)

class FormValidMixin_GD:
    """
    Mixin to handle the common form_valid logic for CreateView and UpdateView.
    """

    def form_invalid(self, form):
        form.add_error(None, "Es gibt einen oder mehreren Fehler im Formular.")
        return super().form_invalid(form)

    def form_valid(self, form):
        item = form.save(commit=False)

        # Geschäftspartner
        if item.geschaeftspartner is None:
            key = form.cleaned_data['cage_code']
            print("key = " + str(key))
            try:
                lookup_record = G_Partner.objects.get(cage_code=key)
                lookup_value = lookup_record.gp_nummer
                print("lookup_value = " + lookup_value)
            except G_Partner.DoesNotExist:
                lookup_value = ""
                print("No lookup")
            item.geschaeftspartner = lookup_value
        print("item.geschaeftspartner = " + item.geschaeftspartner)

        # Revision Fremd
        item.revision_fremd = form.cleaned_data['revision']
        print("item.revision_fremd = " + str(item.revision_fremd))

        # Materialzustandsverwaltung
        print("item.chargenpflicht = " + str(item.chargenpflicht))
        if item.chargenpflicht:
            item.materialzustandsverwaltung = 2
        else:
            item.materialzustandsverwaltung = 2
        print("item.materialzustandsverwaltung = " + str(item.materialzustandsverwaltung))

        if form.errors:
            return self.form_invalid(form)

        item.save()
        return super().form_valid(form)

class FormValidMixin_SMDA:
    """
    Mixin to handle the common form_valid logic for CreateView and UpdateView.
    """

    def form_invalid(self, form):
        form.add_error(None, "Es gibt einen oder mehreren Fehler im Formular.")
        return super().form_invalid(form)

    def form_valid(self, form):
        item = form.save(commit=False)

        # Verkaufsorg.
        if item.werkzuordnung_1 == "0800":
            item.verkaufsorg = "A100"
        else:
            item.verkaufsorg = "M100"
        print("item.verkaufsorg = " + item.verkaufsorg)

        # Vertriebsweg
        item.vertriebsweg = "V0"
        print("item.vertriebsweg = " + item.vertriebsweg)

        # Auszeichnungsfeld
        if item.verteilung_apm_kerda == True:
            item.auszeichnungsfeld = "R"
        print("item.auszeichnungsfeld = " + str(item.auszeichnungsfeld))

        print("item.materialart_grunddaten_id = " + str(item.materialart_grunddaten_id))
        mat_art = Materialart.objects.filter(id=item.id).first()
        print("mat_art.text = " + str(mat_art.text))
        print("<<< APPLY THE RULE HERE >>>")

#        base_obj = Material.objects.filter(id=item.id)
#        print("base_obj = " + str(base_obj))
#
#        field_names = [field.name for field in Material._meta.get_fields()]
#        materials_data = []
#        for obj in base_obj:
#            field_value_dict = {}
#            for field in field_names:
#                # Use getattr to get the value of the field from the object
#                value = getattr(obj, field, None)
#                field_value_dict[field] = value
#            materials_data.append(field_value_dict)
#
#        pprint(materials_data)
#
#        print("base_obj.materialart_grunddaten = " + str(base_obj.materialart_grunddaten))

        # Preissteuerung
        item.preissteuerung = "<< TBD >>"
        print("item.preissteuerung = " + item.preissteuerung)

        # Preisermittlung
        if item.preissteuerung is not None:
            item.preisermittlung = "2"
        print("item.preisermittlung = " + item.preisermittlung)

        # Ausprägung
        print("item.zuteilung_id = " + str(item.zuteilung_id))
        zuteilung = Zuteilung.objects.filter(id=item.zuteilung_id).first()
        print("zuteilung = " + str(zuteilung))
        print("item.auspraegung_id = " + str(item.auspraegung_id))
        auspraegung = Auspraegung.objects.filter(id=item.auspraegung_id).first()
        print("auspraegung = " + str(auspraegung))
        if zuteilung.text == "MKZ" and auspraegung.text == "04":
            form.add_error('auspraegung', "Die Ausprägung mit 'MKZ' muss '01', '02' oder '03' sein.")
        if zuteilung.text == "PRD" and auspraegung.text == "04":
            form.add_error('auspraegung', "Die Ausprägung mit 'PRD' muss '01', '02' oder '03' sein.")

        if form.errors:
            return self.form_invalid(form)

        item.save()
        return super().form_valid(form)

class FormValidMixin_RUAG:
    """
    Mixin to handle the common form_valid logic for CreateView and UpdateView.
    """

    def form_valid(self, form):
        item.save()
        return super().form_valid(form)

