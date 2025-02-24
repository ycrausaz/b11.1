from django.db import migrations, models
from django.db import connection

# 1
def create_views_makt_beschreibung(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_makt_beschreibung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS makt_beschreibung;')

# 2
def create_views_mara_ausp_merkmale(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_ausp_merkmale(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_ausp_merkmale;')

# 3
def create_views_mara_grunddaten(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_grunddaten;')

# 4
def create_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_kssk_klassenzuordnung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_kssk_klassenzuordnung;')

# 5
def create_views_mara_stxh_grunddaten(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxh_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxh_grunddaten;')

# 6
def create_views_mara_stxl_grunddaten(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mara_stxl_grunddaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mara_stxl_grunddaten;')

# 7
def create_views_marc_werksdaten(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_marc_werksdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS marc_werksdaten;')

# 8
def create_views_mbew_buchhaltung(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mbew_buchhaltung(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mbew_buchhaltung;')

# 9
def create_views_mlan_steuer(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mlan_steuer(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mlan_steuer;')

# 10
def create_views_mvke_verkaufsdaten(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_mvke_verkaufsdaten(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS mvke_verkaufsdaten;')

# 11
def create_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    view_sql = '''
        '''
    schema_editor.execute(view_sql)

def drop_views_ckmlcr_material_ledger_preise(apps, schema_editor):
    schema_editor.execute('DROP VIEW IF EXISTS ckmlcr_material_ledger_preise;')


class Migration(migrations.Migration):

    dependencies = [
        ('symm', '0001_initial'),
    ]

    operations = [
# 1
        migrations.RunPython(create_views_makt_beschreibung, reverse_code=drop_views_makt_beschreibung),
# 2
        migrations.RunPython(create_views_mara_ausp_merkmale, reverse_code=drop_views_mara_ausp_merkmale),
# 3
        migrations.RunPython(create_views_mara_grunddaten, reverse_code=drop_views_mara_grunddaten),
# 4
        migrations.RunPython(create_views_mara_kssk_klassenzuordnung, reverse_code=drop_views_mara_kssk_klassenzuordnung),
# 5
        migrations.RunPython(create_views_mara_stxh_grunddaten, reverse_code=drop_views_mara_stxh_grunddaten),
# 6
        migrations.RunPython(create_views_mara_stxl_grunddaten, reverse_code=drop_views_mara_stxl_grunddaten),
# 7
        migrations.RunPython(create_views_marc_werksdaten, reverse_code=drop_views_marc_werksdaten),
# 8
        migrations.RunPython(create_views_mbew_buchhaltung, reverse_code=drop_views_mbew_buchhaltung),
# 9
        migrations.RunPython(create_views_mlan_steuer, reverse_code=drop_views_mlan_steuer),
# 10
        migrations.RunPython(create_views_mvke_verkaufsdaten, reverse_code=drop_views_mvke_verkaufsdaten),
# 11
        migrations.RunPython(create_views_ckmlcr_material_ledger_preise, reverse_code=drop_views_ckmlcr_material_ledger_preise),
    ]

