-- Table de référence des aéroports, alimentée depuis OurAirports (airports.csv)
-- https://davidmegginson.github.io/ourairports-data/airports.csv
-- Domaine public (Open Data Commons Public Domain Dedication).

CREATE TABLE IF NOT EXISTS aeroports (
    id              BIGINT PRIMARY KEY,
    ident           VARCHAR(10) NOT NULL,   -- identifiant OurAirports, souvent = code ICAO
    type            VARCHAR(30),            -- large_airport, medium_airport, small_airport, heliport...
    name            TEXT,
    latitude_deg    DOUBLE PRECISION,
    longitude_deg   DOUBLE PRECISION,
    elevation_ft    INTEGER,
    continent       VARCHAR(5),
    iso_country     VARCHAR(2),
    iso_region      VARCHAR(10),
    municipality    TEXT,
    icao_code       VARCHAR(4),
    iata_code       VARCHAR(3),
    gps_code        VARCHAR(10),
    local_code      VARCHAR(10)
);

CREATE INDEX IF NOT EXISTS idx_aeroports_icao ON aeroports (icao_code);
CREATE INDEX IF NOT EXISTS idx_aeroports_country ON aeroports (iso_country);

-- Vue simplifiée : uniquement les aéroports français avec un code ICAO connu,
-- pour rester léger côté volumétrie pendant le POC.
CREATE OR REPLACE VIEW aeroports_fr AS
SELECT *
FROM aeroports
WHERE iso_country = 'FR'
  AND icao_code IS NOT NULL
  AND type IN ('large_airport', 'medium_airport');