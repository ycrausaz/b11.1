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
    a.preisermittlung as mlast
   FROM symm_material a
     LEFT JOIN symm_werkzuordnung_1 b ON a.werkzuordnung_1_id = b.id
     LEFT JOIN symm_bewertungsklasse f ON a.bewertungsklasse_id = f.id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr, b.text;
