# myapp/admin.py

from django.contrib import admin
from .models import Material, BEGRU, Basismengeneinheit, Materialart, Sparte, Rueckfuehrungscode, Serialnummerprofil, SparePartClassCode, Uebersetzungsstatus

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('positions_nr', 'kurztext_de', 'kurztext_fr', 'kurztext_en', 'grunddatentext_de_1_zeile')


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



