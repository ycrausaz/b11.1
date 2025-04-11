CREATE OR REPLACE VIEW marc_werksdaten
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    a.lieferzeit AS plifz,
    b.text AS werks,
    'ND'::text AS dismm,
    'X'::text AS kautb,
    c.text AS fevor,
    d.text AS sernp,
        CASE
            WHEN a.orderbuchpflicht = true THEN 'X'::text
            ELSE NULL::text
        END AS kordb
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
     LEFT JOIN b11_1_fertigungssteuerer c ON a.fertigungssteuerer_id = c.idx
     LEFT JOIN b11_1_serialnummerprofil d ON a.serialnummerprofil_id = d.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
