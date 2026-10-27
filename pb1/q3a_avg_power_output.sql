SELECT round(avg(rotational_speed_rpm * torque_nm * 0.1047), 0) AS avg_power_watts FROM obt_columnar;
