from io import BytesIO


def generate_report(operation, workpiece_material, tool_material, speed, feed, depth, prediction, recommendation_text=""):
    recommended_tools = ", ".join(prediction.compatibility["recommended_tools"])
    notes = "\n".join(f"- {note}" for note in prediction.engineering_notes)

    return f"""
TOOL LIFE ESTIMATION REPORT

Machining Operation : {operation}
Workpiece Material : {workpiece_material}
Tool Material : {tool_material}

Cutting Speed : {speed} m/min
Feed Rate : {feed} mm/rev
Depth of Cut : {depth} mm

Predicted Tool Life : {prediction.tool_life} min
Wear Condition : {prediction.condition}
Compatibility Check : {"Compatible" if prediction.compatibility["is_compatible"] else "Incompatible"}
Recommended Cutting Tools : {recommended_tools}
Engineering Recommendation : {recommendation_text}

Engineering Notes:
{notes}
"""


def report_buffer(report_text):
    buffer = BytesIO()
    buffer.write(report_text.encode())
    return buffer.getvalue()
