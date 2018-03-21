DROP TABLE IF EXISTS usages;
CREATE TABLE usages (
  date DATE,
  time TIME,
  house_id INTEGER,
  usage NUMERIC,
  forecast NUMERIC,
  negociate INTEGER CHECK (negociate=0 OR negociate=1),
  negociate_load INTEGER CHECK (negociate_load BETWEEN 0 AND 8),
  green_energy INTEGER CHECK (green_energy BETWEEN 0 AND 15)
);
