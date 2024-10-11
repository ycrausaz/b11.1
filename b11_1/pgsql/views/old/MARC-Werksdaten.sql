DROP VIEW IF EXISTS MARC_Werksdaten;
CREATE VIEW MARC_Werksdaten
 AS
 SELECT a.positions_nr AS source_id,
    b.text AS werk,
    'ND'::text AS dismm,
    a.orderbuchpflicht AS kordb
   FROM b11_1_material a
     LEFT JOIN b11_1_werk b ON a.werk_id = b.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
