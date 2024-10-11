CREATE OR REPLACE VIEW public.marc_werksdaten
 AS
 SELECT a.positions_nr AS source_id,
    a.lieferzeit AS plifz,
    b.text AS werk,
    'ND'::text AS dismm,
    a.fertigungssteuerer_id AS fevor,
    a.orderbuchpflicht AS kordb
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN b11_1_fertigungssteuerer c ON a.fertigungssteuerer_id = c.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
