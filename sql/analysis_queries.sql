-- AI4I observations are synthetic records, not a unique fleet of assets.
-- Overall counts and observed failure percentage.
SELECT COUNT(*) AS observations, SUM(machine_failure) AS failures,
       ROUND(100.0 * AVG(machine_failure), 2) AS failure_percent
FROM machine_observations;

-- Failure breakdown by product type.
SELECT product_type, COUNT(*) AS observations, SUM(machine_failure) AS failures,
       ROUND(100.0 * AVG(machine_failure), 2) AS failure_percent
FROM machine_observations GROUP BY product_type ORDER BY product_type;

-- Operating measurement means by actual outcome.
SELECT machine_failure, COUNT(*) AS observations,
       ROUND(AVG(air_temperature_k), 2) AS avg_air_temp_k,
       ROUND(AVG(process_temperature_k), 2) AS avg_process_temp_k,
       ROUND(AVG(rotational_speed_rpm), 2) AS avg_speed_rpm,
       ROUND(AVG(torque_nm), 2) AS avg_torque_nm,
       ROUND(AVG(tool_wear_min), 2) AS avg_wear_min
FROM machine_observations GROUP BY machine_failure ORDER BY machine_failure;

-- Failure rate across recorded tool-wear bands (descriptive, not temporal).
SELECT CASE WHEN tool_wear_min < 100 THEN '0-99'
            WHEN tool_wear_min < 200 THEN '100-199' ELSE '200+' END AS wear_band,
       COUNT(*) AS observations, SUM(machine_failure) AS failures,
       ROUND(100.0 * AVG(machine_failure), 2) AS failure_percent
FROM machine_observations GROUP BY wear_band ORDER BY wear_band;
