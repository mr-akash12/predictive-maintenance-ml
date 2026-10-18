-- One AI4I observation per UDI. Neither timestamps nor true machine identities exist.
CREATE TABLE IF NOT EXISTS machine_observations (
  udi INTEGER PRIMARY KEY,
  product_id TEXT NOT NULL,
  product_type TEXT NOT NULL CHECK (product_type IN ('L', 'M', 'H')),
  air_temperature_k REAL,
  process_temperature_k REAL,
  rotational_speed_rpm INTEGER,
  torque_nm REAL,
  tool_wear_min INTEGER,
  machine_failure INTEGER NOT NULL CHECK (machine_failure IN (0, 1)),
  twf INTEGER NOT NULL, hdf INTEGER NOT NULL, pwf INTEGER NOT NULL,
  osf INTEGER NOT NULL, rnf INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_observations_type ON machine_observations(product_type);
CREATE INDEX IF NOT EXISTS idx_observations_failure ON machine_observations(machine_failure);
