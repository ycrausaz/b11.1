DROP VIEW IF EXISTS MBEW_Buchhaltung;
CREATE VIEW MBEW_Buchhaltung
 AS
 SELECT a.positions_nr AS source_id,
    b.text AS bwkey,
    c.text as vprsv,
    a.preis AS verpr,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    f.text AS bklas,
    CASE WHEN c.text is null THEN '' ELSE '2' END as mlast
   FROM b11_1_material a
     LEFT JOIN b11_1_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.id
     LEFT JOIN b11_1_preissteuerung c on a.preissteuerung_id = c.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
