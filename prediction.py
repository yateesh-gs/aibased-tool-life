from dataclasses import dataclass

from compatibility import evaluate_compatibility
from database import CUTTING_TOOL_DATABASE, OPERATION_FACTORS, WORKPIECE_DATABASE


@dataclass
class PredictionResult:
    tool_life: float
    condition: str
    wear_percentage: int
    compatibility: dict
    engineering_notes: list


def feed_factor(feed):
    return max(0.35, 1.0 / (1.0 + max(0, feed - 0.10) * 2.4))


def depth_factor(depth):
    return max(0.42, 1.0 / (1.0 + max(0, depth - 1.0) * 0.18))


def speed_factor(speed, tool_data, workpiece_data):
    recommended_speed = min(
        tool_data["max_cutting_speed"],
        tool_data["taylor_c"] * 0.46 * workpiece_data["speed_factor"]
    )
    if speed <= recommended_speed:
        return 1.0

    overload = (speed - recommended_speed) / recommended_speed
    return max(0.45, 1.0 - overload * 0.28)


def classify_condition(tool_life, is_compatible):
    if not is_compatible and tool_life < 35:
        return "HIGH WEAR"
    if tool_life > 45:
        return "GOOD"
    if tool_life > 25:
        return "MODERATE WEAR"
    return "HIGH WEAR"


def calculate_wear_percentage(tool_life):
    return max(0, min(100, int((70 - tool_life) * 1.4)))


def predict_tool_life(speed, feed, depth, tool_material, operation, workpiece_material):
    workpiece = WORKPIECE_DATABASE[workpiece_material]
    tool = CUTTING_TOOL_DATABASE[tool_material]
    compatibility = evaluate_compatibility(workpiece_material, tool_material)

    base_life = (tool["taylor_c"] / speed) ** (1 / tool["taylor_n"])
    corrected_life = base_life
    corrected_life *= workpiece["machinability"]
    corrected_life *= 1 / workpiece["wear_factor"]
    corrected_life *= tool["wear_resistance"]
    corrected_life *= OPERATION_FACTORS[operation]
    corrected_life *= feed_factor(feed)
    corrected_life *= depth_factor(depth)
    corrected_life *= speed_factor(speed, tool, workpiece)
    corrected_life *= compatibility["factor"]

    tool_life = round(max(1.0, min(corrected_life, 180.0)), 2)
    condition = classify_condition(tool_life, compatibility["is_compatible"])
    wear_percentage = calculate_wear_percentage(tool_life)

    engineering_notes = [
        f"Taylor constants for {tool_material}: C={tool['taylor_c']}, n={tool['taylor_n']}.",
        f"{workpiece_material} machinability factor: {workpiece['machinability']}.",
        f"Hardness category: {workpiece['hardness_category']}.",
        f"Machinability rating: {workpiece['machinability_rating']} percent of reference free-machining steel.",
        f"Recommended cutting speed factor: {workpiece['speed_factor']}.",
        f"Workpiece wear factor: {workpiece['wear_factor']}.",
        f"Tool hardness level: {tool['hardness_level']}; maximum cutting speed: {tool['max_cutting_speed']} m/min.",
        f"{operation} operation factor: {OPERATION_FACTORS[operation]}.",
        f"Compatibility score: {compatibility['score']}/100; life correction factor: {compatibility['factor']}.",
        f"Compatibility ratios: {compatibility['property_ratios']}."
    ]

    if not compatibility["is_compatible"]:
        engineering_notes.append(compatibility["reason"])

    return PredictionResult(
        tool_life=tool_life,
        condition=condition,
        wear_percentage=wear_percentage,
        compatibility=compatibility,
        engineering_notes=engineering_notes
    )
