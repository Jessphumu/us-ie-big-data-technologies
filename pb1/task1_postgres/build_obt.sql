CREATE TABLE obt_sensor_events AS
SELECT 
    r.event_id, r.equipment_id, r.timestamp, r.air_temp_k, 
    r.process_temp_k, r.rotational_speed_rpm, r.torque_nm, 
    r.tool_wear_min, r.machine_failure, e.equipment_type, 
    e.plant_location, e.manufacturer, ml.latest_action_taken
FROM raw_sensor_events r
JOIN equipment_master e ON r.equipment_id = e.equipment_id
LEFT JOIN LATERAL (
    SELECT action_taken AS latest_action_taken
    FROM maintenance_logs m
    WHERE m.equipment_id = r.equipment_id 
      AND m.maintenance_date <= r.timestamp
    ORDER BY m.maintenance_date DESC
    LIMIT 1
) ml ON true;
