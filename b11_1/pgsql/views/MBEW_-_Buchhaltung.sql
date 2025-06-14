CREATE OR REPLACE VIEW mbew_buchhaltung
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    b.text AS bwkey,
    a.preissteuerung AS vprsv,
    a.preis AS verpr,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    f.text AS bklas,
    a.preisermittlung AS mlast
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.idx
     LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.idx
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
