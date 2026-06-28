from compatibility import primary_recommended_tool, recommended_cutting_tools


def get_recommended_tool(workpiece_material):
    return primary_recommended_tool(workpiece_material)


def get_recommendation(workpiece_material, prediction):
    tools = ", ".join(recommended_cutting_tools(workpiece_material))

    if not prediction.compatibility["is_compatible"]:
        return (
            "warning",
            f"{prediction.compatibility['reason']} Recommended cutting tools: {tools}."
        )

    if prediction.tool_life < 25:
        return "warning", "Reduce cutting speed and feed rate to improve tool life."

    if prediction.tool_life < 45:
        return "info", f"Moderate machining condition. Recommended cutting tools: {tools}."

    return "success", f"Machining parameters are within safe operating condition. Recommended cutting tools: {tools}."
