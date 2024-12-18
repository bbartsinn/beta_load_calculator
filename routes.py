# routes.py
from flask import Blueprint, request, jsonify
from services.calculation_engine import (
    calculate_unit_loads,
    combined_load,
    calculate_service_parameters
)

api = Blueprint('api', __name__)

@api.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        num_units = data.get("num_units", 1)
        conductor_type = data.get("conductor_type", "Copper")
        units = data.get("units", [])

        units_data = []
        for unit in units:
            result = calculate_unit_loads(unit, conductor_type)
            if result:
                units_data.append(result)

        if not units_data:
            return jsonify({"message": "No valid units provided."}), 400

        combined_no_hvac = combined_load(units_data)
        total_hvac_load = sum(u["calculated_load"] - u["calculated_load_no_hvac"] for u in units_data)
        final_combined_load = combined_no_hvac + total_hvac_load

        service_ocp_label, service_conductor_desc = calculate_service_parameters(final_combined_load, units_data, conductor_type)

        result = {
            "units": units_data,
            "Combined No-HVAC Load (Watts)": combined_no_hvac,
            "Total HVAC Load (Watts)": total_hvac_load,
            "Total Calculated Load (Watts)": final_combined_load,
            "Total Amps": final_combined_load / 240.0,
            "Service OCP size (Amps)": service_ocp_label,
            "Service Conductor Type and Size": service_conductor_desc
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
