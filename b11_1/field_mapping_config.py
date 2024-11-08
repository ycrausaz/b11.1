from .models import *

FIELD_MAPPING = {
    # Simple fields
    'positions_nr': {
        'tab': 'Input_Lieferant',
        'column': 'B',
        'type': 'simple'
    },
    'kurztext_de': {
        'tab': 'Input_Lieferant',
        'column': 'C',
        'type': 'simple'
    },
    'kurztext_fr': {
        'tab': 'Input_Lieferant',
        'column': 'D',
        'type': 'simple'
    },
    'kurztext_en': {
        'tab': 'Input_Lieferant',
        'column': 'E',
        'type': 'simple'
    },
    'grunddatentext_de_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'F',
        'type': 'simple'
    },
    'grunddatentext_de_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'G',
        'type': 'simple'
    },
    'grunddatentext_fr_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'H',
        'type': 'simple'
    },
    'grunddatentext_fr_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'I',
        'type': 'simple'
    },
    'grunddatentext_en_1_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'J',
        'type': 'simple'
    },
    'grunddatentext_en_2_zeile': {
        'tab': 'Input_Lieferant',
        'column': 'K',
        'type': 'simple'
    },
    'basismengeneinheit': {
        'tab': 'Input_Lieferant',
        'column': 'L',
        'type': 'fk',
        'model': Basismengeneinheit,
        'lookup_field': 'text'
    },
    'bruttogewicht': {
        'tab': 'Input_Lieferant',
        'column': 'M',
        'type': 'simple'
    },
    'gewichtseinheit': {
        'tab': 'Input_Lieferant',
        'column': 'N',
        'type': 'simple'
    },
    'nettogewicht': {
        'tab': 'Input_Lieferant',
        'column': 'O',
        'type': 'simple'
    },
    'groesse_abmessung': {
        'tab': 'Input_Lieferant',
        'column': 'P',
        'type': 'simple'
    },
    'ean_upc_code': {
        'tab': 'Input_Lieferant',
        'column': 'Q',
        'type': 'simple'
    },
    'nato_stock_number': {
        'tab': 'Input_Lieferant',
        'column': 'R',
        'type': 'simple'
    },
    'nsn_gruppe_klasse': {
        'tab': 'Input_Lieferant',
        'column': 'S',
        'type': 'simple'
    },
    'nato_versorgungs_nr': {
        'tab': 'Input_Lieferant',
        'column': 'T',
        'type': 'simple'
    },
    'herstellerteilenummer': {
        'tab': 'Input_Lieferant',
        'column': 'U',
        'type': 'simple'
    },
    'normbezeichnung': {
        'tab': 'Input_Lieferant',
        'column': 'V',
        'type': 'simple'
    },
    'gefahrgutkennzeichen': {
        'tab': 'Input_Lieferant',
        'column': 'W',
        'type': 'fk',
        'model': Gefahrgutkennzeichen,
        'lookup_field': 'text'
    },
    'instandsetzbar': {
        'tab': 'Input_Lieferant',
        'column': 'X',
        'type': 'boolean'
    },
    'chargenpflicht': {
        'tab': 'Input_Lieferant',
        'column': 'Y',
        'type': 'boolean'
    },
    'bestellmengeneinheit': {
        'tab': 'Input_Lieferant',
        'column': 'Z',
        'type': 'simple'
    },
    'mindestbestellmenge': {
        'tab': 'Input_Lieferant',
        'column': 'AA',
        'type': 'simple'
    },
    'lieferzeit': {
        'tab': 'Input_Lieferant',
        'column': 'AB',
        'type': 'simple'
    },
    'einheit_l_b_h': {
        'tab': 'Input_Lieferant',
        'column': 'AC',
        'type': 'simple'
    },
    'laenge': {
        'tab': 'Input_Lieferant',
        'column': 'AD',
        'type': 'simple'
    },
    'breite': {
        'tab': 'Input_Lieferant',
        'column': 'AE',
        'type': 'simple'
    },
    'hoehe': {
        'tab': 'Input_Lieferant',
        'column': 'AF',
        'type': 'simple'
    },
    'preis': {
        'tab': 'Input_Lieferant',
        'column': 'AG',
        'type': 'simple'
    },
    'waehrung': {
        'tab': 'Input_Lieferant',
        'column': 'AH',
        'type': 'simple'
    },
    'preiseinheit': {
        'tab': 'Input_Lieferant',
        'column': 'AI',
        'type': 'simple'
    },
    'lagerfaehigkeit': {
        'tab': 'Input_Lieferant',
        'column': 'AJ',
        'type': 'simple'
    },
    'exportkontrollauflage': {
        'tab': 'Input_Lieferant',
        'column': 'AK',
        'type': 'boolean'
    },
    'cage_code': {
        'tab': 'Input_Lieferant',
        'column': 'AL',
        'type': 'simple'
    },
    'hersteller_name': {
        'tab': 'Input_Lieferant',
        'column': 'AM',
        'type': 'simple'
    },
    'hersteller_adresse': {
        'tab': 'Input_Lieferant',
        'column': 'AN',
        'type': 'simple'
    },
    'hersteller_plz': {
        'tab': 'Input_Lieferant',
        'column': 'AO',
        'type': 'simple'
    },
    'hersteller_ort': {
        'tab': 'Input_Lieferant',
        'column': 'AP',
        'type': 'simple'
    },
    'revision': {
        'tab': 'Input_Lieferant',
        'column': 'AQ',
        'type': 'simple'
    },
    'bemerkung': {
        'tab': 'Input_Lieferant',
        'column': 'AR',
        'type': 'simple'
    },





    'endbevorratet': {
        'tab': 'Grunddaten',
        'column': 'R',
        'type': 'simple'
    },
    'warengruppe': {
        'tab': 'Grunddaten',
        'column': 'F',
        'type': 'simple'
    },
    'systemmanager': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'L',
        'type': 'simple'
    },
    'kennziffer_bamf': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'AD',
        'type': 'simple'
    },

    # Foreign key fields
    'begru': {
        'tab': 'Grunddaten',
        'column': 'C',
        'type': 'fk',
        'model': BEGRU,
        'lookup_field': 'text'
    },
    'werkzuordnung_1': {
        'tab': 'Systemmanager - Datenassistent',
        'column': 'C',
        'type': 'fk',
        'model': Werkzuordnung_1,
        'lookup_field': 'text'
    },
}

