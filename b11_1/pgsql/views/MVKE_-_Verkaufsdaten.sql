CREATE OR REPLACE VIEW mvke_verkaufsdaten
 AS
 SELECT a.id AS tmp_id,
    a.positions_nr AS source_id,
    a.verkaufsorg AS vkorg,
    a.vertriebsweg AS vtweg,
    c.text AS mtpos
   FROM b11_1_material a
     LEFT JOIN b11_1_allgemeinepositionstypengruppe c ON c.idx = a.allgemeine_positionstypengruppe_id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr;
