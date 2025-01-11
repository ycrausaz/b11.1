CREATE OR REPLACE VIEW marc_werksdaten
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    a.lieferzeit AS plifz,
    b.text AS werks,
    'ND'::text AS dismm,
    c.text AS fevor,
        CASE
            WHEN a.orderbuchpflicht = true THEN 'X'::text
        END AS kordb
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN b11_1_fertigungssteuerer c ON a.fertigungssteuerer_id = c.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
