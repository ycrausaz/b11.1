# editable_fields_config.py

EDITABLE_FIELDS_IL = [
'positions_nr', #B
'referenznummer_leiferant', #C
'kurztext_de', #D
'kurztext_fr', #E
'kurztext_en', #F
'grunddatentext_de_1_zeile', #G
'grunddatentext_de_2_zeile', #H
'grunddatentext_fr_1_zeile', #I
'grunddatentext_fr_2_zeile', #J
'grunddatentext_en_1_zeile', #K
'grunddatentext_en_2_zeile', #L
'basismengeneinheit', #M
'bruttogewicht', #N
#'gewichtseinheit', #O
'nettogewicht', #P
'groesse_abmessung', #Q
'ean_upc_code', #R
'nato_stock_number', #S
'nsn_gruppe_klasse', #T
'nato_versorgungs_nr', #U
'herstellerteilenummer', #V
'normbezeichnung', #W
'gefahrgutkennzeichen', #X
'instandsetzbar', #Y
'chargenpflicht', #Z
'bestellmengeneinheit', #AA
'mindestbestellmenge', #AB
'lieferzeit', #AC
'einheit_l_b_h', #AD
'laenge', #AE
'breite', #AF
'hoehe', #AG
'preis', #AH
#'waehrung', #AI
'preiseinheit', #AJ
'lagerfaehigkeit', #AK
'exportkontrollauflage', #AL
'cage_code', #AM
'hersteller_name', #AN
'hersteller_adresse', #AO
'hersteller_plz', #AP
'hersteller_ort', #AQ
'revision', #AR
'bemerkung', #AS
]


EDITABLE_FIELDS_GD = [
'begru', #C
'sparte', #D
'geschaeftspartner', #D
'warengruppe', #F
'uebersetzungsstatus', #G
'verteilung_an_psd', #H
'revision_eigen', #I
'zertifiziert_fuer_flug', #J
'verteilung_an_ruag', #K
#'revision_fremd', #L
'a_nummer', #M
'materialart_grunddaten', #N
'produkthierarchie', #O
'rueckfuehrungscode', #P
'serialnummerprofil', #Q
#'endbevorratet', #---
#'materialzustandsverwaltung', #S
#'transfer_comment',
]


EDITABLE_FIELDS_SMDA = [
'werkzuordnung_1', #C
'werkzuordnung_2', #D
'werkzuordnung_3', #E
'werkzuordnung_4', #F
'allgemeine_positionstypengruppe', #G
'spare_part_class_code', #H
'fertigungssteuerer', #I
'sonderablauf', #J
'temperaturbedingung', #K
'systemmanager', #L
'mietrelevanz', #M
'nachschubklasse', #N
#'materialeinstufung_nach_zuva', #---
'orderbuchpflicht', #P
'verteilung_apm_kerda', #Q
'verteilung_svsaa', #R
#'verteilung_cheops', #---
'zuteilung', #T
'auspraegung', #U
#'verkaufsorg', #V
#'vertriebsweg', #W
#'auszeichnungsfeld', #X
#'preissteuerung', #Y
#'preisermittlung', #Z
'bewertungsklasse', #AA
'fuehrendes_material', #AB
'kennzeichen_komplexes_system', #AC
'kennziffer_bamf', #AD
'next_higher_assembly', #AE
'externe_warengruppe', #AF
#'transfer_comment',
]

EDITABLE_FIELDS = EDITABLE_FIELDS_IL + EDITABLE_FIELDS_GD + EDITABLE_FIELDS_SMDA
