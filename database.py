import pandas as pd


OPERATIONS = [
    "Turning", "Facing", "Threading", "Grooving", "Parting / Cut-Off",
    "Drilling", "Reaming", "Boring", "Milling", "End Milling",
    "Face Milling", "Slot Milling", "Grinding", "Shaping",
    "Planing", "Tapping", "Broaching", "Knurling",
    "Gear Cutting", "Sawing", "EDM Machining",
    "Laser Beam Machining", "CNC Machining"
]

WORKPIECE_MATERIALS = [
    "Aluminium",
    "Aluminium Alloy",
    "Copper",
    "Brass",
    "Bronze",
    "Mild Steel",
    "Low Carbon Steel",
    "Medium Carbon Steel",
    "High Carbon Steel",
    "Alloy Steel",
    "Tool Steel",
    "Grey Cast Iron",
    "Ductile Cast Iron",
    "White Cast Iron",
    "Stainless Steel",
    "Austenitic Stainless Steel",
    "Ferritic Stainless Steel",
    "Martensitic Stainless Steel",
    "Titanium Alloy",
    "Nickel Alloy",
    "Inconel",
    "Engineering Plastics",
    "Composites"
]

TOOL_MATERIALS = [
    "High Speed Steel (HSS)",
    "High Carbon Steel",
    "Carbon Tool Steel",
    "Cast Alloy",
    "Uncoated Carbide",
    "Coated Carbide",
    "Alumina Ceramic",
    "Silicon Nitride Ceramic",
    "Mixed Ceramic",
    "Cubic Boron Nitride (CBN)",
    "Polycrystalline Diamond (PCD)",
    "TiN Coated Tool",
    "TiAlN Coated Tool",
    "AlCrN Coated Tool",
    "DLC Coated Tool"
]

WORKPIECE_DATABASE = {
    "Aluminium": {
        "machinability": 1.80,
        "hardness_category": "Very Soft",
        "speed_factor": 1.75,
        "wear_factor": 0.55,
        "abrasiveness": 0.45,
        "thermal_load": 0.62,
        "recommended_tools": ["Uncoated Carbide", "High Speed Steel (HSS)", "DLC Coated Tool"],
        "reason": "Commercial aluminium has excellent machinability and high thermal conductivity; sharp HSS or carbide tools reduce built-up edge."
    },
    "Aluminium Alloy": {
        "machinability": 1.45,
        "hardness_category": "Soft to Medium",
        "speed_factor": 1.55,
        "wear_factor": 0.70,
        "abrasiveness": 0.72,
        "thermal_load": 0.78,
        "recommended_tools": ["Uncoated Carbide", "DLC Coated Tool", "High Speed Steel (HSS)"],
        "reason": "Aluminium alloys machine easily but can form built-up edge, so sharp carbide or HSS tooling is preferred."
    },
    "Copper": {
        "machinability": 0.65,
        "hardness_category": "Soft and Ductile",
        "speed_factor": 0.85,
        "wear_factor": 0.78,
        "abrasiveness": 0.58,
        "thermal_load": 0.68,
        "recommended_tools": ["Uncoated Carbide", "High Speed Steel (HSS)", "DLC Coated Tool"],
        "reason": "Copper is soft but gummy; sharp positive-rake tools help control smearing and built-up edge."
    },
    "Brass": {
        "machinability": 1.65,
        "hardness_category": "Soft to Medium",
        "speed_factor": 1.45,
        "wear_factor": 0.62,
        "abrasiveness": 0.60,
        "thermal_load": 0.65,
        "recommended_tools": ["High Speed Steel (HSS)", "Uncoated Carbide", "TiN Coated Tool"],
        "reason": "Free-machining brass cuts cleanly with low cutting forces, making HSS and carbide both practical choices."
    },
    "Bronze": {
        "machinability": 0.90,
        "hardness_category": "Medium",
        "speed_factor": 0.95,
        "wear_factor": 0.92,
        "abrasiveness": 0.92,
        "thermal_load": 0.82,
        "recommended_tools": ["Uncoated Carbide", "Coated Carbide", "TiN Coated Tool"],
        "reason": "Bronze grades are tougher and more abrasive than brass, so carbide improves edge life in production cutting."
    },
    "Mild Steel": {
        "machinability": 1.18,
        "hardness_category": "Low",
        "speed_factor": 1.10,
        "wear_factor": 0.88,
        "abrasiveness": 0.82,
        "thermal_load": 0.90,
        "recommended_tools": ["High Speed Steel (HSS)", "Uncoated Carbide", "TiN Coated Tool"],
        "reason": "Mild steel is ductile and relatively easy to machine, though sharp tools help avoid built-up edge."
    },
    "Low Carbon Steel": {
        "machinability": 1.18,
        "hardness_category": "Low",
        "speed_factor": 1.10,
        "wear_factor": 0.88,
        "abrasiveness": 0.82,
        "thermal_load": 0.90,
        "recommended_tools": ["High Speed Steel (HSS)", "Uncoated Carbide", "TiN Coated Tool"],
        "reason": "Low carbon steel is ductile and relatively easy to machine, though sharp tools help avoid built-up edge."
    },
    "Medium Carbon Steel": {
        "machinability": 1.00,
        "hardness_category": "Medium",
        "speed_factor": 1.00,
        "wear_factor": 1.00,
        "abrasiveness": 1.00,
        "thermal_load": 1.00,
        "recommended_tools": ["Uncoated Carbide", "Coated Carbide", "TiN Coated Tool"],
        "reason": "Medium carbon steel is commonly machined with carbide or coated carbide; HSS is acceptable at conservative speeds."
    },
    "High Carbon Steel": {
        "machinability": 0.78,
        "hardness_category": "High",
        "speed_factor": 0.78,
        "wear_factor": 1.20,
        "abrasiveness": 1.15,
        "thermal_load": 1.08,
        "recommended_tools": ["Coated Carbide", "TiAlN Coated Tool", "Uncoated Carbide"],
        "reason": "High carbon steel has higher hardness and abrasion than mild steel, so carbide or coated carbide gives better wear control."
    },
    "Alloy Steel": {
        "machinability": 0.72,
        "hardness_category": "Medium to High",
        "speed_factor": 0.74,
        "wear_factor": 1.28,
        "abrasiveness": 1.18,
        "thermal_load": 1.12,
        "recommended_tools": ["Coated Carbide", "TiAlN Coated Tool", "Uncoated Carbide"],
        "reason": "Alloy steels often combine strength, hardness, and heat generation, making coated carbide the safer production choice."
    },
    "Tool Steel": {
        "machinability": 0.48,
        "hardness_category": "Very High",
        "speed_factor": 0.55,
        "wear_factor": 1.55,
        "abrasiveness": 1.42,
        "thermal_load": 1.28,
        "recommended_tools": ["Coated Carbide", "Cubic Boron Nitride (CBN)", "Mixed Ceramic"],
        "reason": "Tool steel is hard and wear-resistant, requiring high hot-hardness tooling and conservative cutting speeds."
    },
    "Grey Cast Iron": {
        "machinability": 0.95,
        "hardness_category": "Medium",
        "speed_factor": 0.95,
        "wear_factor": 1.22,
        "abrasiveness": 1.30,
        "thermal_load": 0.88,
        "recommended_tools": ["Alumina Ceramic", "Uncoated Carbide", "Coated Carbide"],
        "reason": "Grey cast iron is abrasive due to graphite and hard inclusions, so ceramic or carbide tools provide strong wear resistance."
    },
    "Ductile Cast Iron": {
        "machinability": 0.78,
        "hardness_category": "Medium to High",
        "speed_factor": 0.82,
        "wear_factor": 1.32,
        "abrasiveness": 1.25,
        "thermal_load": 0.98,
        "recommended_tools": ["Uncoated Carbide", "Coated Carbide", "Silicon Nitride Ceramic"],
        "reason": "Ductile cast iron is tougher than grey iron and still abrasive, so carbide or coated carbide is preferred."
    },
    "White Cast Iron": {
        "machinability": 0.25,
        "hardness_category": "Extremely High",
        "speed_factor": 0.35,
        "wear_factor": 1.85,
        "abrasiveness": 1.75,
        "thermal_load": 1.10,
        "recommended_tools": ["Cubic Boron Nitride (CBN)", "Mixed Ceramic", "Coated Carbide"],
        "reason": "White cast iron contains hard carbides and is extremely abrasive, requiring ceramic or very wear-resistant coated tooling."
    },
    "Stainless Steel": {
        "machinability": 0.58,
        "hardness_category": "Medium with Work Hardening",
        "speed_factor": 0.62,
        "wear_factor": 1.38,
        "abrasiveness": 1.12,
        "thermal_load": 1.32,
        "recommended_tools": ["Coated Carbide", "TiAlN Coated Tool", "Alumina Ceramic"],
        "reason": "Stainless steel tends to work-harden and retains heat, so coated carbide is preferred for stable production machining."
    },
    "Austenitic Stainless Steel": {
        "machinability": 0.58,
        "hardness_category": "Medium with Work Hardening",
        "speed_factor": 0.62,
        "wear_factor": 1.38,
        "abrasiveness": 1.12,
        "thermal_load": 1.32,
        "recommended_tools": ["Coated Carbide", "TiAlN Coated Tool", "Alumina Ceramic"],
        "reason": "Austenitic stainless steel work-hardens strongly and retains heat, making coated carbide the preferred tool material."
    },
    "Ferritic Stainless Steel": {
        "machinability": 0.78,
        "hardness_category": "Medium",
        "speed_factor": 0.78,
        "wear_factor": 1.12,
        "abrasiveness": 1.00,
        "thermal_load": 1.10,
        "recommended_tools": ["Coated Carbide", "Uncoated Carbide", "TiN Coated Tool"],
        "reason": "Ferritic stainless steel is less work-hardening than austenitic grades but still benefits from carbide tooling."
    },
    "Martensitic Stainless Steel": {
        "machinability": 0.52,
        "hardness_category": "High",
        "speed_factor": 0.58,
        "wear_factor": 1.45,
        "abrasiveness": 1.25,
        "thermal_load": 1.18,
        "recommended_tools": ["Coated Carbide", "Cubic Boron Nitride (CBN)", "Mixed Ceramic"],
        "reason": "Martensitic stainless steel is harder and more abrasive, so hot-hard coated carbide or ceramic tooling is appropriate."
    },
    "Titanium Alloy": {
        "machinability": 0.52,
        "hardness_category": "High Strength",
        "speed_factor": 0.48,
        "wear_factor": 1.62,
        "abrasiveness": 1.18,
        "thermal_load": 1.45,
        "recommended_tools": ["Coated Carbide", "AlCrN Coated Tool", "TiAlN Coated Tool"],
        "reason": "Titanium has poor thermal conductivity and requires tools with high hot hardness and controlled cutting parameters."
    },
    "Nickel Alloy": {
        "machinability": 0.42,
        "hardness_category": "High Strength",
        "speed_factor": 0.42,
        "wear_factor": 1.72,
        "abrasiveness": 1.22,
        "thermal_load": 1.52,
        "recommended_tools": ["Coated Carbide", "AlCrN Coated Tool", "Alumina Ceramic"],
        "reason": "Nickel alloys are heat resistant and work-harden under load, demanding high hot-hardness tools and lower speeds."
    },
    "Inconel": {
        "machinability": 0.30,
        "hardness_category": "Very High Strength Superalloy",
        "speed_factor": 0.32,
        "wear_factor": 1.95,
        "abrasiveness": 1.35,
        "thermal_load": 1.70,
        "recommended_tools": ["Alumina Ceramic", "Cubic Boron Nitride (CBN)", "AlCrN Coated Tool"],
        "reason": "Inconel keeps strength at high temperature and concentrates heat at the cutting edge, causing severe notch and crater wear."
    },
    "Engineering Plastics": {
        "machinability": 1.70,
        "hardness_category": "Low",
        "speed_factor": 1.35,
        "wear_factor": 0.50,
        "abrasiveness": 0.42,
        "thermal_load": 0.55,
        "recommended_tools": ["High Speed Steel (HSS)", "Uncoated Carbide", "DLC Coated Tool"],
        "reason": "Engineering plastics cut easily but need sharp tools and heat control to avoid melting or dimensional distortion."
    },
    "Composites": {
        "machinability": 0.38,
        "hardness_category": "Abrasive Fiber Reinforced",
        "speed_factor": 0.62,
        "wear_factor": 1.80,
        "abrasiveness": 1.85,
        "thermal_load": 0.95,
        "recommended_tools": ["Polycrystalline Diamond (PCD)", "DLC Coated Tool", "Coated Carbide"],
        "reason": "Fiber-reinforced composites are highly abrasive and require wear-resistant tooling with controlled cutting forces."
    }
}

CUTTING_TOOL_DATABASE = {
    "High Speed Steel (HSS)": {
        "hardness_level": "High",
        "hot_hardness": 0.62,
        "wear_resistance": 0.65,
        "toughness": 1.18,
        "speed_capability": 0.55,
        "taylor_n": 0.12,
        "taylor_c": 95,
        "suitable_workpieces": [
            "Aluminium", "Aluminium Alloy", "Copper", "Brass",
            "Mild Steel", "Low Carbon Steel", "Medium Carbon Steel", "Ferritic Stainless Steel",
            "Engineering Plastics"
        ]
    },
    "High Carbon Steel": {
        "hardness_level": "Medium",
        "hot_hardness": 0.40,
        "wear_resistance": 0.45,
        "toughness": 0.76,
        "speed_capability": 0.32,
        "taylor_n": 0.10,
        "taylor_c": 42,
        "suitable_workpieces": ["Aluminium", "Aluminium Alloy", "Brass", "Engineering Plastics"]
    },
    "Carbon Tool Steel": {
        "hardness_level": "Medium High",
        "hot_hardness": 0.46,
        "wear_resistance": 0.52,
        "toughness": 0.82,
        "speed_capability": 0.38,
        "taylor_n": 0.11,
        "taylor_c": 55,
        "suitable_workpieces": [
            "Aluminium", "Aluminium Alloy", "Copper", "Brass",
            "Bronze", "Mild Steel", "Low Carbon Steel", "Engineering Plastics"
        ]
    },
    "Cast Alloy": {
        "hardness_level": "High",
        "hot_hardness": 0.82,
        "wear_resistance": 0.86,
        "toughness": 0.72,
        "speed_capability": 0.70,
        "taylor_n": 0.18,
        "taylor_c": 145,
        "suitable_workpieces": [
            "Bronze", "Mild Steel", "Low Carbon Steel", "Medium Carbon Steel",
            "Grey Cast Iron", "Ductile Cast Iron"
        ]
    },
    "Uncoated Carbide": {
        "hardness_level": "Very High",
        "hot_hardness": 1.00,
        "wear_resistance": 1.00,
        "toughness": 0.92,
        "speed_capability": 1.00,
        "taylor_n": 0.25,
        "taylor_c": 280,
        "suitable_workpieces": [
            "Aluminium", "Aluminium Alloy", "Copper", "Brass", "Bronze",
            "Mild Steel", "Low Carbon Steel", "Medium Carbon Steel", "High Carbon Steel",
            "Alloy Steel", "Grey Cast Iron", "Ductile Cast Iron",
            "Stainless Steel", "Austenitic Stainless Steel", "Ferritic Stainless Steel",
            "Martensitic Stainless Steel", "Titanium Alloy", "Engineering Plastics"
        ]
    },
    "Coated Carbide": {
        "hardness_level": "Very High",
        "hot_hardness": 1.18,
        "wear_resistance": 1.24,
        "toughness": 0.86,
        "speed_capability": 1.18,
        "taylor_n": 0.30,
        "taylor_c": 360,
        "suitable_workpieces": [
            "Aluminium Alloy", "Bronze", "Mild Steel", "Low Carbon Steel", "Medium Carbon Steel",
            "High Carbon Steel", "Alloy Steel", "Tool Steel", "Grey Cast Iron",
            "Ductile Cast Iron", "White Cast Iron", "Stainless Steel", "Austenitic Stainless Steel",
            "Ferritic Stainless Steel", "Martensitic Stainless Steel", "Titanium Alloy",
            "Nickel Alloy", "Inconel", "Composites"
        ]
    },
    "Alumina Ceramic": {
        "hardness_level": "Extremely High",
        "hot_hardness": 1.42,
        "wear_resistance": 1.38,
        "toughness": 0.42,
        "speed_capability": 1.55,
        "taylor_n": 0.45,
        "taylor_c": 520,
        "suitable_workpieces": [
            "Grey Cast Iron", "White Cast Iron", "Stainless Steel", "Austenitic Stainless Steel",
            "Martensitic Stainless Steel", "Tool Steel", "Nickel Alloy", "Inconel"
        ]
    },
    "Silicon Nitride Ceramic": {
        "hardness_level": "Extremely High",
        "hot_hardness": 1.35,
        "wear_resistance": 1.30,
        "toughness": 0.58,
        "speed_capability": 1.45,
        "taylor_n": 0.42,
        "taylor_c": 490,
        "suitable_workpieces": ["Grey Cast Iron", "Ductile Cast Iron", "Nickel Alloy"]
    },
    "Mixed Ceramic": {
        "hardness_level": "Extremely High",
        "hot_hardness": 1.48,
        "wear_resistance": 1.46,
        "toughness": 0.48,
        "speed_capability": 1.62,
        "taylor_n": 0.47,
        "taylor_c": 560,
        "suitable_workpieces": [
            "Tool Steel", "White Cast Iron", "Martensitic Stainless Steel",
            "Nickel Alloy", "Inconel"
        ]
    },
    "Cubic Boron Nitride (CBN)": {
        "hardness_level": "Ultra Hard",
        "hot_hardness": 1.62,
        "wear_resistance": 1.68,
        "toughness": 0.62,
        "speed_capability": 1.70,
        "taylor_n": 0.50,
        "taylor_c": 620,
        "suitable_workpieces": [
            "Tool Steel", "White Cast Iron", "Martensitic Stainless Steel",
            "Nickel Alloy", "Inconel"
        ]
    },
    "Polycrystalline Diamond (PCD)": {
        "hardness_level": "Ultra Hard",
        "hot_hardness": 0.95,
        "wear_resistance": 1.82,
        "toughness": 0.55,
        "speed_capability": 1.85,
        "taylor_n": 0.55,
        "taylor_c": 700,
        "suitable_workpieces": [
            "Aluminium", "Aluminium Alloy", "Copper", "Brass", "Bronze",
            "Engineering Plastics", "Composites"
        ]
    },
    "TiN Coated Tool": {
        "hardness_level": "Very High",
        "hot_hardness": 1.05,
        "wear_resistance": 1.12,
        "toughness": 0.88,
        "speed_capability": 1.05,
        "taylor_n": 0.27,
        "taylor_c": 315,
        "suitable_workpieces": [
            "Brass", "Bronze", "Mild Steel", "Low Carbon Steel", "Medium Carbon Steel",
            "Ferritic Stainless Steel"
        ]
    },
    "TiAlN Coated Tool": {
        "hardness_level": "Very High",
        "hot_hardness": 1.30,
        "wear_resistance": 1.34,
        "toughness": 0.82,
        "speed_capability": 1.32,
        "taylor_n": 0.33,
        "taylor_c": 410,
        "suitable_workpieces": [
            "High Carbon Steel", "Alloy Steel", "Stainless Steel", "Austenitic Stainless Steel",
            "Titanium Alloy", "Nickel Alloy"
        ]
    },
    "AlCrN Coated Tool": {
        "hardness_level": "Very High",
        "hot_hardness": 1.38,
        "wear_resistance": 1.42,
        "toughness": 0.80,
        "speed_capability": 1.42,
        "taylor_n": 0.35,
        "taylor_c": 440,
        "suitable_workpieces": ["Titanium Alloy", "Nickel Alloy", "Inconel", "Tool Steel"]
    },
    "DLC Coated Tool": {
        "hardness_level": "Very High",
        "hot_hardness": 0.88,
        "wear_resistance": 1.30,
        "toughness": 0.78,
        "speed_capability": 1.28,
        "taylor_n": 0.31,
        "taylor_c": 380,
        "suitable_workpieces": [
            "Aluminium", "Aluminium Alloy", "Copper", "Engineering Plastics", "Composites"
        ]
    }
}

for tool_data in CUTTING_TOOL_DATABASE.values():
    tool_data["recommended_workpieces"] = tool_data["suitable_workpieces"]

WORKPIECE_ENGINEERING_PROPERTIES = {
    "Aluminium": {"hardness_bhn": 30, "toughness_index": 0.45, "thermal_conductivity_w_mk": 237, "chemical_reactivity": 0.65, "machinability_rating": 350},
    "Aluminium Alloy": {"hardness_bhn": 95, "toughness_index": 0.58, "thermal_conductivity_w_mk": 165, "chemical_reactivity": 0.70, "machinability_rating": 250},
    "Copper": {"hardness_bhn": 55, "toughness_index": 0.70, "thermal_conductivity_w_mk": 390, "chemical_reactivity": 0.55, "machinability_rating": 60},
    "Brass": {"hardness_bhn": 80, "toughness_index": 0.50, "thermal_conductivity_w_mk": 120, "chemical_reactivity": 0.35, "machinability_rating": 300},
    "Bronze": {"hardness_bhn": 100, "toughness_index": 0.72, "thermal_conductivity_w_mk": 60, "chemical_reactivity": 0.42, "machinability_rating": 80},
    "Mild Steel": {"hardness_bhn": 125, "toughness_index": 0.82, "thermal_conductivity_w_mk": 52, "chemical_reactivity": 0.45, "machinability_rating": 140},
    "Low Carbon Steel": {"hardness_bhn": 125, "toughness_index": 0.82, "thermal_conductivity_w_mk": 52, "chemical_reactivity": 0.45, "machinability_rating": 140},
    "Medium Carbon Steel": {"hardness_bhn": 180, "toughness_index": 0.78, "thermal_conductivity_w_mk": 45, "chemical_reactivity": 0.48, "machinability_rating": 100},
    "High Carbon Steel": {"hardness_bhn": 240, "toughness_index": 0.72, "thermal_conductivity_w_mk": 43, "chemical_reactivity": 0.50, "machinability_rating": 70},
    "Alloy Steel": {"hardness_bhn": 260, "toughness_index": 0.86, "thermal_conductivity_w_mk": 38, "chemical_reactivity": 0.55, "machinability_rating": 65},
    "Tool Steel": {"hardness_bhn": 420, "toughness_index": 0.70, "thermal_conductivity_w_mk": 25, "chemical_reactivity": 0.58, "machinability_rating": 45},
    "Grey Cast Iron": {"hardness_bhn": 210, "toughness_index": 0.38, "thermal_conductivity_w_mk": 48, "chemical_reactivity": 0.32, "machinability_rating": 85},
    "Ductile Cast Iron": {"hardness_bhn": 230, "toughness_index": 0.74, "thermal_conductivity_w_mk": 36, "chemical_reactivity": 0.35, "machinability_rating": 70},
    "White Cast Iron": {"hardness_bhn": 520, "toughness_index": 0.30, "thermal_conductivity_w_mk": 22, "chemical_reactivity": 0.35, "machinability_rating": 20},
    "Stainless Steel": {"hardness_bhn": 190, "toughness_index": 0.95, "thermal_conductivity_w_mk": 16, "chemical_reactivity": 0.72, "machinability_rating": 45},
    "Austenitic Stainless Steel": {"hardness_bhn": 190, "toughness_index": 0.95, "thermal_conductivity_w_mk": 16, "chemical_reactivity": 0.72, "machinability_rating": 45},
    "Ferritic Stainless Steel": {"hardness_bhn": 170, "toughness_index": 0.72, "thermal_conductivity_w_mk": 25, "chemical_reactivity": 0.62, "machinability_rating": 75},
    "Martensitic Stainless Steel": {"hardness_bhn": 300, "toughness_index": 0.68, "thermal_conductivity_w_mk": 24, "chemical_reactivity": 0.65, "machinability_rating": 50},
    "Titanium Alloy": {"hardness_bhn": 330, "toughness_index": 0.88, "thermal_conductivity_w_mk": 7, "chemical_reactivity": 0.90, "machinability_rating": 30},
    "Nickel Alloy": {"hardness_bhn": 310, "toughness_index": 0.92, "thermal_conductivity_w_mk": 12, "chemical_reactivity": 0.82, "machinability_rating": 25},
    "Inconel": {"hardness_bhn": 360, "toughness_index": 0.95, "thermal_conductivity_w_mk": 11, "chemical_reactivity": 0.88, "machinability_rating": 18},
    "Engineering Plastics": {"hardness_bhn": 20, "toughness_index": 0.55, "thermal_conductivity_w_mk": 0.30, "chemical_reactivity": 0.20, "machinability_rating": 220},
    "Composites": {"hardness_bhn": 180, "toughness_index": 0.62, "thermal_conductivity_w_mk": 5, "chemical_reactivity": 0.40, "machinability_rating": 35}
}

TOOL_ENGINEERING_PROPERTIES = {
    "High Speed Steel (HSS)": {"hot_hardness_c": 600, "fracture_toughness_mpa": 26, "wear_resistance_index": 62, "oxidation_resistance_c": 600, "max_cutting_speed": 80, "suitable_applications": "low and medium speed general machining"},
    "High Carbon Steel": {"hot_hardness_c": 250, "fracture_toughness_mpa": 12, "wear_resistance_index": 35, "oxidation_resistance_c": 250, "max_cutting_speed": 25, "suitable_applications": "very low speed cutting of soft materials"},
    "Carbon Tool Steel": {"hot_hardness_c": 300, "fracture_toughness_mpa": 14, "wear_resistance_index": 42, "oxidation_resistance_c": 300, "max_cutting_speed": 35, "suitable_applications": "low speed cutting and forming tools"},
    "Cast Alloy": {"hot_hardness_c": 760, "fracture_toughness_mpa": 10, "wear_resistance_index": 70, "oxidation_resistance_c": 800, "max_cutting_speed": 140, "suitable_applications": "cast irons and steels at moderate speed"},
    "Uncoated Carbide": {"hot_hardness_c": 900, "fracture_toughness_mpa": 11, "wear_resistance_index": 82, "oxidation_resistance_c": 850, "max_cutting_speed": 260, "suitable_applications": "general production machining of steels, cast irons, and non-ferrous alloys"},
    "Coated Carbide": {"hot_hardness_c": 1000, "fracture_toughness_mpa": 10, "wear_resistance_index": 90, "oxidation_resistance_c": 950, "max_cutting_speed": 360, "suitable_applications": "high productivity machining of steels, stainless steels, cast irons, and heat-resistant alloys"},
    "Alumina Ceramic": {"hot_hardness_c": 1200, "fracture_toughness_mpa": 4, "wear_resistance_index": 94, "oxidation_resistance_c": 1200, "max_cutting_speed": 620, "suitable_applications": "high speed finishing of cast iron and hardened heat-resistant alloys"},
    "Silicon Nitride Ceramic": {"hot_hardness_c": 1150, "fracture_toughness_mpa": 7, "wear_resistance_index": 90, "oxidation_resistance_c": 1100, "max_cutting_speed": 540, "suitable_applications": "interrupted and rough machining of cast irons and nickel alloys"},
    "Mixed Ceramic": {"hot_hardness_c": 1250, "fracture_toughness_mpa": 5, "wear_resistance_index": 96, "oxidation_resistance_c": 1250, "max_cutting_speed": 680, "suitable_applications": "hard turning and high-speed finishing"},
    "Cubic Boron Nitride (CBN)": {"hot_hardness_c": 1350, "fracture_toughness_mpa": 6, "wear_resistance_index": 98, "oxidation_resistance_c": 1300, "max_cutting_speed": 750, "suitable_applications": "hardened steels, white cast iron, and superalloy finishing"},
    "Polycrystalline Diamond (PCD)": {"hot_hardness_c": 700, "fracture_toughness_mpa": 5, "wear_resistance_index": 100, "oxidation_resistance_c": 700, "max_cutting_speed": 1200, "suitable_applications": "aluminium, copper alloys, plastics, and abrasive composites"},
    "TiN Coated Tool": {"hot_hardness_c": 850, "fracture_toughness_mpa": 10, "wear_resistance_index": 78, "oxidation_resistance_c": 650, "max_cutting_speed": 240, "suitable_applications": "general steels and non-ferrous materials with lower friction"},
    "TiAlN Coated Tool": {"hot_hardness_c": 1050, "fracture_toughness_mpa": 9, "wear_resistance_index": 88, "oxidation_resistance_c": 900, "max_cutting_speed": 420, "suitable_applications": "dry and high-temperature machining of steels, stainless steels, and titanium alloys"},
    "AlCrN Coated Tool": {"hot_hardness_c": 1100, "fracture_toughness_mpa": 9, "wear_resistance_index": 92, "oxidation_resistance_c": 1050, "max_cutting_speed": 460, "suitable_applications": "high-temperature machining of titanium, nickel alloys, and Inconel"},
    "DLC Coated Tool": {"hot_hardness_c": 650, "fracture_toughness_mpa": 8, "wear_resistance_index": 92, "oxidation_resistance_c": 450, "max_cutting_speed": 700, "suitable_applications": "aluminium, copper, plastics, and composites where low friction is critical"}
}

for material_name, properties in WORKPIECE_ENGINEERING_PROPERTIES.items():
    WORKPIECE_DATABASE[material_name].update(properties)

for tool_name, properties in TOOL_ENGINEERING_PROPERTIES.items():
    CUTTING_TOOL_DATABASE[tool_name].update(properties)

OPERATION_FACTORS = {
    "Turning": 1.00,
    "Facing": 0.96,
    "Threading": 0.78,
    "Grooving": 0.72,
    "Parting / Cut-Off": 0.68,
    "Drilling": 0.82,
    "Reaming": 1.08,
    "Boring": 0.94,
    "Milling": 0.84,
    "End Milling": 0.78,
    "Face Milling": 0.86,
    "Slot Milling": 0.70,
    "Grinding": 1.18,
    "Shaping": 0.88,
    "Planing": 0.88,
    "Tapping": 0.72,
    "Broaching": 1.02,
    "Knurling": 0.92,
    "Gear Cutting": 0.76,
    "Sawing": 0.66,
    "EDM Machining": 1.16,
    "Laser Beam Machining": 1.20,
    "CNC Machining": 1.05
}


def expected_values_table(operation, workpiece_material, tool_material, speed, feed, depth, tool_life, condition):
    return pd.DataFrame({
        "Parameter": [
            "Machining Operation",
            "Workpiece Material",
            "Tool Material",
            "Cutting Speed",
            "Feed Rate",
            "Depth of Cut",
            "Predicted Tool Life",
            "Wear Condition"
        ],
        "Value": [
            operation,
            workpiece_material,
            tool_material,
            f"{speed} m/min",
            f"{feed} mm/rev",
            f"{depth} mm",
            f"{tool_life} min",
            condition
        ]
    })


def machining_dataset_preview(operation, workpiece_material, tool_material, speed, feed, depth, predictor):
    rows = []
    for speed_offset, feed_offset in [(-20, -0.04), (-10, -0.02), (0, 0), (10, 0.02), (20, 0.04)]:
        row_speed = max(1, speed + speed_offset)
        row_feed = max(0.01, round(feed + feed_offset, 2))
        result = predictor(row_speed, row_feed, depth, tool_material, operation, workpiece_material)
        rows.append({
            "Operation": operation,
            "Material": tool_material,
            "Cutting Speed": row_speed,
            "Feed Rate": row_feed,
            "Depth of Cut": depth,
            "Tool Life": result.tool_life
        })

    return pd.DataFrame(rows)
