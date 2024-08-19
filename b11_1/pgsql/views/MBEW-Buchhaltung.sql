DROP VIEW IF EXISTS MBEW_Buchhaltung;
CREATE VIEW MBEW_Buchhaltung
 AS
 SELECT a.positions_nr AS source_id,
    b.text AS bwkey,
    a.preis AS verpr,
    a.preis AS stprs,
    a.preiseinheit AS peinh,
    f.text AS bklas
   FROM b11_1_material a
     LEFT JOIN b11_1_werk b ON a.werk_id = b.id
     LEFT JOIN b11_1_bewertungsklasse f ON a.bewertungsklasse_id = f.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
