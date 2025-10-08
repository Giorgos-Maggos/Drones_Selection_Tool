# criteria_data.py
# ---------------- Static configuration data ----------------

CATEGORY_OPTIONS = [
    "agricultural",
    "fpv",
    "delivery",
    "photography and videography",
    "inspection and mapping",
    "surveillance and security",
    "swarms",
]

weights_dict = {
    "agricultural": {
        "Flight_Time_(min)": 0.25,
        "Camera_Resolution_(MP)": 0.15,
        "Weight-Lifting_Capacity_(kg)": 0.20,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.10,
        "Battery_(mAh)": 0.10,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05,
    },
    "fpv": {
        "Flight_Time_(min)": 0.15,
        "Camera_Resolution_(MP)": 0.20,
        "Wind_Resistance_(km/h)": 0.10,
        "Battery_(mAh)": 0.10,
        "Transmitter_Range_(km)": 0.05,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.25,
        "Max_Speed_(km/h)": 0.10,
    },
    "delivery": {
        "Battery_(mAh)": 0.25,
        "Weight-Lifting_Capacity_(kg)": 0.25,
        "Flight_Time_(min)": 0.20,
        "Max_Speed_(km/h)": 0.15,
        "Transmitter_Range_(km)": 0.10,
        "Frame_Material": 0.05,
    },
    "photography and videography": {
        "Flight_Time_(min)": 0.25,
        "Camera_Resolution_(MP)": 0.30,
        "Weight_(kg)": 0.15,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.10,
        "Battery_(mAh)": 0.05,
        "Frame_Material": 0.03,
        "Flight_Control_Board": 0.02,
    },
    "inspection and mapping": {
        "Flight_Time_(min)": 0.30,
        "Camera_Resolution_(MP)": 0.25,
        "Weight-Lifting_Capacity_(kg)": 0.20,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.05,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05,
    },
    "surveillance and security": {
        "Flight_Time_(min)": 0.30,
        "Camera_Resolution_(MP)": 0.25,
        "Wind_Resistance_(km/h)": 0.20,
        "Battery_(mAh)": 0.10,
        "Transmitter_Range_(km)": 0.05,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05,
    },
    "swarms": {
        "Flight_Time_(min)": 0.20,
        "Camera_Resolution_(MP)": 0.15,
        "Weight-Lifting_Capacity_(kg)": 0.10,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.25,
        "Battery_(mAh)": 0.10,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05,
    },
}

Criteria_Scores_Frame_Material = {
    "Carbon Fiber": 1.0,
    "Titanium": 0.95,
    "Magnesium Alloy": 0.85,
    "Aluminum": 0.80,
    "Composite": 0.75,
    "Plastic": 0.50,
    "EPO Foam": 0.45,
    "Foam": 0.40,
    "Fiber": 0.70,
    "Composite Material": 0.80,
}

Criteria_Scores_MIL_STD = {"Yes": 1, "No": 0}

Criteria_Scores_Flight_Control_Board = {
    "RTK/GNSS": 0.85,
    "Wing FC200": 0.80,
    "APM": 0.75,
    "DJI A3": 1.00,
    "DJI N3": 0.94,
    "Pixhawk": 1.00,
    "Freefly Alta": 0.92,
    "Wingtra FC": 0.90,
    "Zipline FC30": 0.93,
    "Delair FC": 0.90,
    "Autel FC": 0.85,
    "Intel FC": 0.89,
    "VTOL": 0.92,
    "Skydio FC": 0.86,
    "Parrot FC": 0.80,
    "Yuneec FC": 0.85,
    "Flirtey FC4": 0.84,
    "Workhorse FC22": 0.90,
}
