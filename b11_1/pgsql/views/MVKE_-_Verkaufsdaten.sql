CREATE OR REPLACE VIEW public.mvke_verkaufsdaten
 AS
 SELECT a.positions_nr AS source_id,
    'M100'::text AS vkorg,
    b.text AS vtweg,
    c.text AS mtpos
   FROM b11_1_material a
     LEFT JOIN b11_1_vertriebsweg b ON b.id = a.vertriebsweg_id
     LEFT JOIN b11_1_allgemeinepositionstypengruppe c ON c.id = a.allgemeine_positionstypengruppe_id
  WHERE a.is_transferred = true
  ORDER BY a.positions_nr;
