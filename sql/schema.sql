PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS phoenix_water_production (
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  million_gallons REAL NOT NULL,
  PRIMARY KEY (year, month)
);

CREATE TABLE IF NOT EXISTS phoenix_calls_for_service (
  incident_num TEXT PRIMARY KEY,
  disp_code TEXT,
  disposition TEXT,
  final_radio_code TEXT,
  final_call_type TEXT,
  call_received TEXT,
  hundredblockaddr TEXT,
  grid TEXT
);

CREATE INDEX IF NOT EXISTS idx_calls_type ON phoenix_calls_for_service(final_call_type);
CREATE INDEX IF NOT EXISTS idx_calls_date ON phoenix_calls_for_service(call_received);
