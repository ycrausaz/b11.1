# myapp/admin.py

from django.contrib import admin
from .models import *
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('positions_nr', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile')


@admin.register(HelpTooltip)
class HelpTooltipAdmin(admin.ModelAdmin):
    list_display = ('field_name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(G_Partner)
class G_PartnerAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BEGRU)
class BEGRUAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Basismengeneinheit)
class BasismengeneinheitAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Materialart)
class MaterialartAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Sparte)
class SparteAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Rueckfuehrungscode)
class RueckfuehrungscodeAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Serialnummerprofil)
class SerialnummerprofilAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(SparePartClassCode)
class SparePartClassCodeAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Uebersetzungsstatus)
class UebersetzungsstatusAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Gefahrgutkennzeichen)
class GefahrgutkennzeichenAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Werkzuordnung_1)
class Werkzuordnung_1Admin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Werkzuordnung_2)
class Werkzuordnung_2Admin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Werkzuordnung_3)
class Werkzuordnung_3Admin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Werkzuordnung_4)
class Werkzuordnung_4Admin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(AllgemeinePositionstypengruppe)
class AllgemeinePositionstypengruppeAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Vertriebsweg)
class VertriebswegAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Auszeichnungsfeld)
class AuszeichnungsfeldAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Fertigungssteuerer)
class FertigungssteuererAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Sonderablauf)
class SonderablaufAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Temperaturbedingung)
class TemperaturbedingungAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Bewertungsklasse)
class BewertungsklasseAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Zuteilung)
class ZuteilungAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Auspraegung)
class AuspraegungAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Preissteuerung)
class PreissteuerungAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(MaterialeinstufungNachZUVA)
class MaterialeinstufungNachZUVAAdmin(admin.ModelAdmin):
    list_display = ('text',)
