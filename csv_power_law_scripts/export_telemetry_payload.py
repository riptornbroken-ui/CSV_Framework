import sqlite3
import json
import os

db_path = "csv_telemetry.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT step, max_shear_rate, mean_viscosity, max_velocity FROM lattice_telemetry")
    rows = cursor.fetchall()
    conn.close()
    
    payload = {
        "simulation_metadata": {"model": "Power-Law Xel Lattice", "grid_size": 64},
        "telemetry_records": [
            {"step": r[0], "max_shear_rate": r[1], "mean_viscosity": r[2], "max_velocity": r[3]}
            for r in rows
        ]
    }
    
    with open("power_law_telemetry_payload.json", "w") as f:
        json.dump(payload, f, indent=4)
    print("Generated: power_law_telemetry_payload.json")
else:
    print("Database not found. Run the telemetry script first.")
