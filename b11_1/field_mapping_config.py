from .models import *

FIELD_MAPPING = {
# Start IL
    'positions_nr': {
        'tab': 'Input_Lieferant',
        'column': 'B',
        'type': 'simple'
    },
    'referenznummer_leiferant': {
        'tab': 'Input_Lieferant',
        'column': 'C',
        'type': 'simple'
    },
    'kurztext_de': {
        'tab': 'Input_Lieferant',
        'column': 'D',
        'type': 'simple'
    },
    'kurztext_fr': {
        'tab': 'Input_Lieferant',
        'column': 'E',
        'type': 'simple'
    },
    'kurztext_en': {
        'tab': 'Input_Lieferant',
        'column': 'F',
        'type': 'simple'
    },
    'grunddatentext_de_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'G',
        'type': 'simple'
    },
    'grunddatentext_de_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'H',
        'type': 'simple'
    },
    'grunddatentext_fr_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'I',
        'type': 'simple'
    },
    'grunddatentext_fr_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'J',
        'type': 'simple'
    },
    'grunddatentext_en_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'K',
        'type': 'simple'
    },
    'grunddatentext_en_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'L',
        'type': 'simple'
    },
    'basismengeneinheit': {
        'tab': 'Input_Lieferant',
        'column': 'M',
        'type': 'fk',
        'model': Basismengeneinheit,
        'lookup_field': 'text'
    },
    'bruttogewicht': {
        'tab': 'Input_Lieferant',
        'column': 'N',
        'type': 'simple'
    },
    'gewichtseinheit': {
        'tab': 'Input_Lieferant',
        'column': 'O',
        'type': 'simple'
    },
    'nettogewicht': {
        'tab': 'Input_Lieferant',
        'column': 'P',
        'type': 'simple'
    },
    'groesse_abmessung': {
        'tab': 'Input_Lieferant',
        'column': 'Q',
        'type': 'simple'
    },
    'ean_upc_code': {
        'tab': 'Input_Lieferant',
        'column': 'R',
        'type': 'simple'
    },
    'nato_stock_number': {
        'tab': 'Input_Lieferant',
        'column': 'S',
        'type': 'simple'
    },
    'nsn_gruppe_klasse': {
        'tab': 'Input_Lieferant',
        'column': 'T',
        'type': 'simple'
    },
    'nato_versorgungs_nr': {
        'tab': 'Input_Lieferant',
        'column': 'U',
        'type': 'simple'
    },
    'herstellerteilenummer': {
        'tab': 'Input_Lieferant',
        'column': 'V',
        'type': 'simple'
    },
    'normbezeichnung': {
        'tab': 'Input_Lieferant',
        'column': 'W',
        'type': 'simple'
    },
    'gefahrgutkennzeichen': {
        'tab': 'Input_Lieferant',
        'column': 'X',
        'type': 'fk',
        'model': Gefahrgutkennzeichen,
        'lookup_field': 'text'
    },
    'instandsetzbar': {
        'tab': 'Input_Lieferant',
        'column': 'Y',
        'type': 'boolean'
    },
    'chargenpflicht': {
        'tab': 'Input_Lieferant',
        'column': 'Z',
        'type': 'boolean'
    },
    'bestellmengeneinheit': {
        'tab': 'Input_Lieferant',
        'column': 'AA',
        'type': 'fk',
        'model': Bestellmengeneinheit,
        'lookup_field': 'text'
    },
    'mindestbestellmenge': {
        'tab': 'Input_Lieferant',
        'column': 'AB',
        'type': 'simple'
    },
    'lieferzeit': {
        'tab': 'Input_Lieferant',
        'column': 'AC',
        'type': 'simple'
    },
    'einheit_l_b_h': {
        'tab': 'Input_Lieferant',
        'column': 'AD',
        'type': 'simple'
    },
    'laenge': {
        'tab': 'Input_Lieferant',
        'column': 'AE',
        'type': 'simple'
    },
    'breite': {
        'tab': 'Input_Lieferant',
        'column': 'AF',
        'type': 'simple'
    },
    'hoehe': {
        'tab': 'Input_Lieferant',
        'column': 'AG',
        'type': 'simple'
    },
    'preis': {
        'tab': 'Input_Lieferant',
        'column': 'AH',
        'type': 'simple'
    },
    'waehrung': {
        'tab': 'Input_Lieferant',
        'column': 'AI',
        'type': 'simple'
    },
    'preiseinheit': {
        'tab': 'Input_Lieferant',
        'column': 'AJ',
        'type': 'simple'
    },
    'lagerfaehigkeit': {
        'tab': 'Input_Lieferant',
        'column': 'AK',
        'type': 'simple'
    },
    'exportkontrollauflage': {
        'tab': 'Input_Lieferant',
        'column': 'AL',
        'type': 'boolean'
    },
    'cage_code': {
        'tab': 'Input_Lieferant',
        'column': 'AM',
        'type': 'simple'
    },
    'hersteller_name': {
        'tab': 'Input_Lieferant',
        'column': 'AN',
        'type': 'simple'
    },
    'hersteller_adresse': {
        'tab': 'Input_Lieferant',
        'column': 'AO',
        'type': 'simple'
    },
    'hersteller_plz': {
        'tab': 'Input_Lieferant',
        'column': 'AP',
        'type': 'simple'
    },
    'hersteller_ort': {
        'tab': 'Input_Lieferant',
        'column': 'AQ',
        'type': 'simple'
    },
    'revision': {
        'tab': 'Input_Lieferant',
        'column': 'AR',
        'type': 'simple'
    },
    'bemerkung': {
        'tab': 'Input_Lieferant',
        'column': 'AS',
        'type': 'simple'
    },
# End IL
# Start GD
    'begru': {
        'tab': 'Grunddaten',
        'column': 'C',
        'type': 'fk',
        'model': BEGRU,
        'lookup_field': 'text'
    },
    'sparte': {
        'tab': 'Grunddaten',
        'column': 'D',
        'type': 'fk',
        'model': Sparte,
        'lookup_field': 'text'
    },
    'geschaeftspartner': {
        'tab': 'Grunddaten',
        'column': 'E',
        'type': 'simple'
    },
    'warengruppe': {
        'tab': 'Grunddaten',
        'column': 'F',
        'type': 'simple'
    },
    'uebersetzungsstatus': {
        'tab': 'Grunddaten',
        'column': 'G',
        'type': 'fk',
        'model': Uebersetzungsstatus,
        'lookup_field': 'text'
    },
    'verteilung_an_psd': {
        'tab': 'Grunddaten',
        'column': 'H',
        'type': 'boolean'
    },
    'revision_eigen': {
        'tab': 'Grunddaten',
        'column': 'I',
        'type': 'simple'
    },
    'zertifiziert_fuer_flug': {
        'tab': 'Grunddaten',
        'column': 'J',
        'type': 'boolean'
    },
    'verteilung_an_ruag': {
        'tab': 'Grunddaten',
        'column': 'K',
        'type': 'boolean'
    },
    'revision_fremd': {
        'tab': 'Grunddaten',
        'column': 'L',
        'type': 'simple'
    },
    'a_nummer': {
        'tab': 'Grunddaten',
        'column': 'M',
        'type': 'simple'
    },
    'materialart_grunddaten': {
        'tab': 'Grunddaten',
        'column': 'N',
        'type': 'fk',
        'model': Materialart,
        'lookup_field': 'text'
    },
    'produkthierarchie': {
        'tab': 'Grunddaten',
        'column': 'O',
        'type': 'simple'
    },
    'rueckfuehrungscode': {
        'tab': 'Grunddaten',
        'column': 'P',
        'type': 'fk',
        'model': Rueckfuehrungscode,
        'lookup_field': 'text'
    },
    'serialnummerprofil': {
        'tab': 'Grunddaten',
        'column': 'Q',
        'type': 'fk',
        'model': Serialnummerprofil,
        'lookup_field': 'text'
    },
    'endbevorratet': {
        'tab': 'Grunddaten',
        'column': 'R',
        'type': 'simple'
    },
    'materialzustandsverwaltung': {
        'tab': 'Grunddaten',
        'column': 'S',
        'type': 'simple'
    },
# End GD
# Start SMDA
    'werkzuordnung_1': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'C',
        'type': 'padded_fk',
        'model': Werkzuordnung_1,
        'lookup_field': 'text',
        'length': 4
    },
    'werkzuordnung_2': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'D',
        'type': 'padded_fk',
        'model': Werkzuordnung_2,
        'lookup_field': 'text',
        'length': 4
    },
    'werkzuordnung_3': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'E',
        'type': 'padded_fk',
        'model': Werkzuordnung_3,
        'lookup_field': 'text',
        'length': 4
    },
    'werkzuordnung_4': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'F',
        'type': 'padded_fk',
        'model': Werkzuordnung_4,
        'lookup_field': 'text',
        'length': 4
    },
    'allgemeine_positionstypengruppe': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'G',
        'type': 'fk',
        'model': AllgemeinePositionstypengruppe,
        'lookup_field': 'text'
    },
    'spare_part_class_code': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'H',
        'type': 'fk',
        'model': SparePartClassCode,
        'lookup_field': 'text'
    },
    'fertigungssteuerer': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'I',
        'type': 'fk',
        'model': Fertigungssteuerer,
        'lookup_field': 'text'
    },
    'sonderablauf': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'J',
        'type': 'fk',
        'model': Sonderablauf,
        'lookup_field': 'text'
    },
    'temperaturbedingung': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'K',
        'type': 'padded_fk',
        'model': Temperaturbedingung,
        'lookup_field': 'text',
        'length': 2
    },
    'systemmanager': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'L',
        'type': 'simple'
    },
    'mietrelevanz': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'M',
        'type': 'boolean'
    },
    'nachschubklasse': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'N',
        'type': 'simple'
    },
    'materialeinstufung_nach_zuva': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'O',
        'type': 'fk',
        'model': MaterialeinstufungNachZUVA,
        'lookup_field': 'text'
    },
    'orderbuchpflicht': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'P',
        'type': 'boolean'
    },
    'verteilung_apm_kerda': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'Q',
        'type': 'boolean'
    },
    'verteilung_svsaa': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'R',
        'type': 'boolean'
    },
    'verteilung_cheops': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'S',
        'type': 'boolean'
    },
    'zuteilung': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'T',
        'type': 'fk',
        'model': Zuteilung,
        'lookup_field': 'text'
    },
    'auspraegung': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'U',
        'type': 'padded_fk',
        'model': Auspraegung,
        'lookup_field': 'text',
        'length': 2
    },
    'verkaufsorg': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'V',
        'type': 'simple'
    },
    'vertriebsweg': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'W',
        'type': 'simple'
    },
    'auszeichnungsfeld': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'X',
        'type': 'simple'
    },
    'preissteuerung': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'Y',
        'type': 'simple'
    },
    'preisermittlung': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'Z',
        'type': 'simple'
    },
    'bewertungsklasse': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AA',
        'type': 'fk',
        'model': Bewertungsklasse,
        'lookup_field': 'text'
    },
    'fuehrendes_material': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AB',
        'type': 'simple'
    },
    'kennzeichen_komplexes_system': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AC',
        'type': 'boolean'
    },
    'kennziffer_bamf': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AD',
        'type': 'simple'
    },
    'next_higher_assembly': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AE',
        'type': 'simple'
    },
    'externe_warengruppe': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AF',
        'type': 'simple'
    },
    'repararaturlokation': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AG',
        'type': 'simple'
    },
# End SMDA
}

