from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
import re
from django.http import HttpResponseRedirect
from .models import *
from pprint import pprint
from django.views.generic import TemplateView
from django.urls import resolve

class GroupRequiredMixin(LoginRequiredMixin):
    allowed_groups = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if user belongs to any of the allowed groups
        if not any(group in self.allowed_groups for group in request.user.groups.values_list('name', flat=True)):
            raise PermissionDenied  # Raise an error if the user is not in the required groups
        return super().dispatch(request, *args, **kwargs)

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

        # Bruttogewicht
        if item.bruttogewicht <= 0:
            form.add_error('bruttogewicht', "Das Bruttogewicht muss positiv sein.")

        # Nettogewicht
        if item.nettogewicht is not None and item.nettogewicht <= 0:
            form.add_error('nettogewicht', "Das Nettogewicht muss positiv sein.")

        # Bestellmengeneinheit
        if item.bestellmengeneinheit is not None and item.bestellmengeneinheit <= 0:
            form.add_error('bestellmengeneinheit', "Die Bestellmengeneinheit muss positiv sein.")

        # Mindestbestellmenge
        if item.mindestbestellmenge is not None and item.mindestbestellmenge <= 0:
            form.add_error('mindestbestellmenge', "Die Mindestbestellmenge muss positiv sein.")

        # Lieferzeit
        if item.lieferzeit is not None and item.lieferzeit <= 0:
            form.add_error('lieferzeit', "Die Lieferzeit muss positiv sein.")

        # Länge
        if item.laenge is not None and item.laenge <= 0:
            form.add_error('laenge', "Die Länge muss positiv sein.")

        # Breite
        if item.breite is not None and item.breite <= 0:
            form.add_error('breite', "Die Breite muss positiv sein.")

        # Höhe
        if item.hoehe is not None and item.hoehe <= 0:
            form.add_error('hoehe', "Die Höhe muss positiv sein.")

        # Preis
        if item.preis is not None and item.preis <= 0:
            form.add_error('preis', "Der Preis muss positiv sein.")

        # Preiseinheit
        if item.preiseinheit is not None and item.preiseinheit <= 0:
            form.add_error('preiseinheit', "Die Preiseinheit muss positiv sein.")

        # Lagerfähigkeit
        if item.lagerfaehigkeit is not None and item.lagerfaehigkeit <= 0:
            form.add_error('lagerfaehigkeit', "Die Lagerfähigkeit muss positiv sein.")

        # NSN Gruppe / Klasse
        if item.nato_stock_number is not None:
            pattern = r'^\d{4}-\d{2}-\d{3}-\d{4}$'
            if not re.match(pattern, item.nato_stock_number):
                form.add_error('nato_stock_number', "Der Feld 'Nato Stock Number' muss die folgende Formatierung haben: 'XXXX-XX-XXX-XXXX'.")
            pattern = r'^(\d{4})-\d{2}-\d{3}-\d{4}$'
            match = re.match(pattern, item.nato_stock_number)
            if match:
                item.nsn_gruppe_klasse = match.group(1)

        # Nato Versorgungs-Nr.
        if item.nato_stock_number is not None:
            pattern = r'^\d{4}-(\d{2}-\d{3}-\d{4})$'
            match = re.match(pattern, item.nato_stock_number)
            if match:
                item.nato_versorgungs_nr = match.group(1).replace('-', '')

        # Hersteller
        item.hersteller = self.request.user.username
        print("item.hersteller = " + item.hersteller)

        # Gewichtseinheit
        item.gewichtseinheit = "KG"
        print("item.gewichtseinheit = " + item.gewichtseinheit)

        # Einheit L / B / H
        item.einheit_l_b_h = "MM"
        print("item.einheit_l_b_h = " + item.einheit_l_b_h)

        # Währung
        item.waehrung = "CHF"
        print("item.waehrung = " + item.waehrung)

        # Instandsetzbar
        expected_value = "6" if item.instandsetzbar else "0"
        try:
            spare_part_class = SparePartClassCode.objects.get(text=expected_value)
            # Set the spare_part_class_code field to the found object
            item.spare_part_class_code = spare_part_class
            print(f"item.spare_part_class_code set to {spare_part_class.text} (idx={spare_part_class.idx})")

        except SparePartClassCode.DoesNotExist:
            # Add a non-field error instead of a field-specific error
            error_msg = f"Die Wert '{expected_value}' für Spare Part Class Code wurde nicht gefunden."
            form.add_error(None, error_msg)
            print(f"Error: {error_msg}")

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

        # Produkthierarchie
        if item.produkthierarchie is not None and len(item.produkthierarchie) != 4:
            form.add_error('produkthierarchie', "Die Produkthierarchie muss eine 4-Stellen Nummer ('0' left-padded).")

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

        # Preissteuerung
        item.preissteuerung = "<< TBD >>"
        print("item.preissteuerung = " + item.preissteuerung)

        # Preisermittlung
        if item.preissteuerung is not None:
            item.preisermittlung = "2"
        print("item.preisermittlung = " + item.preisermittlung)

        # Ausprägung
        print("item.zuteilung_id = " + str(item.zuteilung_id))
        zuteilung = item.zuteilung
        print("zuteilung = " + str(zuteilung))
        print("item.auspraegung_id = " + str(item.auspraegung_id))
        auspraegung = item.auspraegung
        print("auspraegung = " + str(auspraegung))
        if zuteilung.text == "MKZ" and (auspraegung.text == "02" or auspraegung.text == "03" or auspraegung.text == "04"):
            form.add_error('auspraegung', "Die Ausprägung mit 'MKZ' muss '01' sein.")
        if zuteilung.text == "PRD" and (auspraegung.text == "03" or auspraegung.text == "04"):
            form.add_error('auspraegung', "Die Ausprägung mit 'PRD' muss '01' oder '02' sein.")

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

from django.views.generic import TemplateView

class ComputedContextMixin:

    def convert_url(self, url):
        pattern_gd = r'gd'
        pattern_smda = r'smda'
        match_gd = re.search(pattern_gd, url.strip())
        match_smda = re.search(pattern_smda, url.strip())
        ret = '?????????'
        if match_gd:
            replacement = "smda"
            ret = re.sub(pattern_gd, replacement, url.strip())
        if match_smda:
            replacement = "gd"
            ret = re.sub(pattern_smda, replacement, url.strip())
        return ret

    def extract_other_view(self, url):
        pattern_gd = r'gd'
        pattern_smda = r'smda'
        match_gd = re.search(pattern_gd, url.strip())
        match_smda = re.search(pattern_smda, url.strip())
        if match_gd:
            return "Systemmanager / Datenassistent"
        if match_smda:
            return "Grunddaten"

    def extract_current_view(self, url):
        pattern_gd = r'gd'
        pattern_smda = r'smda'
        match_gd = re.search(pattern_gd, url.strip())
        match_smda = re.search(pattern_smda, url.strip())
        if match_gd:
            return "Grunddaten"
        if match_smda:
            return "Systemmanager / Datenassistent"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_url = resolve(self.request.path_info).url_name
        context['current_view'] = self.extract_current_view(self.request.path_info)
        context['other_view'] = self.extract_other_view(self.request.path_info)
        context['other_url'] = self.convert_url(self.request.path_info)
        return context
