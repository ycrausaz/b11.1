CREATE OR REPLACE VIEW mbew_buchhaltung
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS bwkey,
    a.auszeichnungsfeld AS vprsv,
    a.preis AS verpr,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    f.text AS bklas,
        CASE
            WHEN a.auszeichnungsfeld IS NULL THEN ''::text
            ELSE '2'::text
        END AS mlast
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
