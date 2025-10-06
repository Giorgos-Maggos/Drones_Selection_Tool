import pandas as pd
import matplotlib.pyplot as plt
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import ttk
from tkinter import Tk, StringVar, IntVar, DoubleVar, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Global variable to store the DataFrame
df = None

# Drone categories dictionary
categories = {
    1: "agricultural",
    2: "fpv",
    3: "delivery",
    4: "photography and videography",
    5: "inspection and mapping",
    6: "surveillance and security",
    7: "swarms"
}

# Weights for features of each category
weights_dict = {
    "agricultural": {
        "Flight_Time_(min)": 0.25,
        "Camera_Resolution_(MP)": 0.15,
        "Weight-Lifting_Capacity_(kg)": 0.20,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.10,
        "Battery_(mAh)": 0.10,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05
    },
    "fpv": {
        'Flight_Time_(min)': 0.15,
        'Camera_Resolution_(MP)': 0.20,
        'Wind_Resistance_(km/h)': 0.10,
        'Battery_(mAh)': 0.10,
        'Transmitter_Range_(km)': 0.05,
        'Frame_Material': 0.05,
        'Flight_Control_Board': 0.25,
        'Max_Speed_(km/h)': 0.10
    },
    "delivery": {
        "Battery_(mAh)": 0.25,
        "Weight-Lifting_Capacity_(kg)": 0.25,
        "Flight_Time_(min)": 0.2,
        "Max_Speed_(km/h)": 0.15,
        "Transmitter_Range_(km)": 0.1,
        "Frame_Material": 0.05
    },
    "photography and videography": {
        "Flight_Time_(min)": 0.25,
        "Camera_Resolution_(MP)": 0.30,
        "Weight_(kg)": 0.15,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.10,
        "Battery_(mAh)": 0.05,
        "Frame_Material": 0.03,
        "Flight_Control_Board": 0.02
    },
    "inspection and mapping": {
        "Flight_Time_(min)": 0.30,
        "Camera_Resolution_(MP)": 0.25,
        "Weight-Lifting_Capacity_(kg)": 0.20,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.05,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05
    },
    "surveillance and security": {
        "Flight_Time_(min)": 0.30,
        "Camera_Resolution_(MP)": 0.25,
        "Wind_Resistance_(km/h)": 0.20,
        "Battery_(mAh)": 0.10,
        "Transmitter_Range_(km)": 0.05,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05
    },
    "swarms": {
        "Flight_Time_(min)": 0.20,
        "Camera_Resolution_(MP)": 0.15,
        "Weight-Lifting_Capacity_(kg)": 0.10,
        "Wind_Resistance_(km/h)": 0.10,
        "Transmitter_Range_(km)": 0.25,
        "Battery_(mAh)": 0.10,
        "Frame_Material": 0.05,
        "Flight_Control_Board": 0.05
    }
}

# Non-numeric criteria mappings
Criteria_Scores_Frame_Material = {
    "Carbon Fiber": 1.0,
    "Titanium": 0.95,
    "Magnesium Alloy": 0.85,
    "Aluminum": 0.8,
    "Composite": 0.75,
    "Plastic": 0.5,
    "EPO Foam": 0.45,
    "Foam": 0.4,
    "Fiber": 0.7,
    "Composite Material": 0.8
}

Criteria_Scores_MIL_STD = {
    "Yes": 1,
    "No": 0
}

Criteria_Scores_Flight_Control_Board = {
    "RTK/GNSS": 0.85,
    "Wing FC200": 0.8,
    "APM": 0.75,
    "GNSS": 0.7,
    "eMotion": 0.9,
    "Airbus FC45": 1.0,
    "Airbus FC30": 0.95,
    "Autel FC04": 0.88,
    "Autel FC": 0.85,
    "Autel Autonomy": 0.9,
    "Delair FC": 0.9,
    "PABLO AIR FC10": 0.82,
    "Quantum FC": 0.78,
    "QBase 3D": 0.76,
    "senseFly FC05": 0.85,
    "Trimble FC": 0.84,
    "Wing FC25": 0.83,
    "Wingcopter FC1000": 0.92,
    "Wing FC198": 0.9,
    "Wingcopter FC": 0.88,
    "Wingtra FC": 0.9,
    "Zipline FC30": 0.93,
    "Zipline FC20": 0.9,
    "Zipline FC45": 0.95,
    "Alpha FC09": 0.85,
    "Naza": 0.8,
    "Amazon FC30": 0.9,
    "Amazon FC27": 0.88,
    "Amazon FC25": 0.86,
    "Pixhawk": 1.0,
    "DJI FC": 0.95,
    "DJI N3": 0.94,
    "DJI A3": 1.0,
    "Flytrex FC30": 0.9,
    "Flytrex FC12": 0.88,
    "Harris FC": 0.87,
    "Terra FC": 0.86,
    "XAG FC": 0.92,
    "Yuneec FC": 0.85,
    "Yuneec Controller": 0.8,
    "Freefly FC06": 0.9,
    "Intel FC": 0.89,
    "UPS FC22": 0.9,
    "UPS FC10": 0.87,
    "Workhorse FC22": 0.9,
    "Workhorse FC20": 0.87,
    "Acecore FC": 0.88,
    "Aeryon Flight Control": 0.92,
    "Furling32 Board": 0.85,
    "Connex Controller": 0.8,
    "Arris FC": 0.82,
    "BetaFPV F7": 0.78,
    "F3 FC": 0.75,
    "Blade Controller": 0.8,
    "Contixo FC": 0.83,
    "Eachine FC": 0.78,
    "Eachine Board": 0.76,
    "Easy Aerial FC": 0.88,
    "EHang FC08": 0.9,
    "EMAX FC": 0.84,
    "EMAX Tinyhawk Board": 0.8,
    "Shark Byte Controller": 0.79,
    "FLIR FC": 0.86,
    "Flirtey FC4": 0.84,
    "Flirtey FC12": 0.85,
    "Flyability FC": 0.87,
    "F7 Flight Controller": 0.85,
    "Ninja Controller": 0.8,
    "Freefly Alta": 0.92,
    "GDU FC": 0.88,
    "F4 FC": 0.82,
    "F4 HD Controller": 0.84,
    "F4 Dolphin": 0.8,
    "Kakute F7": 0.86,
    "Hubsan FC": 0.8,
    "Hubsan Zino Board": 0.78,
    "Proteus FC": 0.83,
    "Stinger Board": 0.8,
    "Vortex FC": 0.84,
    "JJRC FC": 0.78,
    "Kespry FC": 0.85,
    "LHI Board": 0.8,
    "Lockheed FC": 0.92,
    "Lumenier FC": 0.87,
    "Manna FC20": 0.88,
    "Matternet FC2": 0.9,
    "mdCockpit": 0.84,
    "Parrot FC": 0.8,
    "ANAFI FPV Board": 0.8,
    "Percepto FC07": 0.85,
    "Potensic Controller": 0.78,
    "PowerVision FC": 0.86,
    "Ruko FC": 0.77,
    "Skydio X2 Board": 0.88,
    "Skydio FC": 0.86,
    "SkyDrop FC20": 0.87,
    "SkyDrop FC10": 0.85,
    "Skyzone Controller": 0.75,
    "Crossfire FC": 0.8,
    "T-Drones FC": 0.85,
    "UPair FC": 0.8,
    "Walkera FC": 0.78,
    "Walkera FC250": 0.8,
    "Aero FC": 0.88,
    "VTOL": 0.92,
    "Bell FC40": 0.9,
    "DHL FC40": 0.88,
    "Elroy FC50": 0.9,
    "Volansi FC10": 0.85,
    "Intel FC": 0.9,
    "UVify FC": 0.8,
    "Verify FC": 0.7,
    "HighGreat FC": 0.65,
    "CollMot Custom FC": 0.8,
    "Dronisos FC": 0.6,
    "EHang Custom FC": 0.7,
    "Damoda Show FC": 0.9,
    "Verge Aero Custom FC": 0.5,
    "MMC Custom FC": 0.4,
    "Pixiel Custom FC": 0.3,
    "AscTec / (Intel) FC": 0.8,
    "SkyElements Custom FC": 0.9,
    "Botlab Custom FC": 0.5,
    "Flock Drone Art Custom FC": 0.6
}

# GUI Setup
root = Tk()
root.title("Drone Selection Tool")
root.geometry("800x600")

# ttkbootstrap style for dark theme
style = Style("darkly")

# Variables for user input
selected_category = StringVar(value="")
number_of_drones = IntVar(value=0)
min_flight_time = DoubleVar(value=0.0)
min_wind_resistance = DoubleVar(value=0.0)
min_weight_lifting_capacity = DoubleVar(value=0.0)
min_max_speed = DoubleVar(value=0.0)
min_transmitter_range = DoubleVar(value=0.0)
min_camera_resolution = DoubleVar(value=0.0)
min_battery_mah = IntVar(value=0)
min_weight_kg = DoubleVar(value=0.0)

# Flight Control Board Options
flight_control_board_options = [
    "All", "RTK/GNSS", "Wing FC200", "APM", "GNSS", "eMotion", "Airbus FC45", "Airbus FC30",
    "PX4", "Autel FC04", "Autel FC", "Autel Autonomy", "Delair FC", "Trimble FC",
    "Wing FC25", "Wingcopter FC1000", "Zipline FC30", "Zipline FC20", "Pixhawk",
    "DJI FC", "DJI N3", "DJI A3", "Flytrex FC30", "Harris FC", "Naza", "Intel FC",
    "UPS FC22", "Workhorse FC22", "Acecore FC", "Aeryon Flight Control", "BetaFPV F7",
    "F3 FC", "Kakute F7", "Shark Byte Controller", "Easy Aerial FC", "EHang FC08",
    "F4 HD Controller", "Proteus FC", "Skydio X2 Board", "SkyDrop FC20", "Standard Ruko Controller",
    "Lockheed FC", "Matternet FC2", "mdCockpit", "Percepto FC07", "PowerVision FC","Intel FC",
    "UVify FC", "Verify FC", "HighGreat FC", "CollMot Custom FC", "Dronisos FC", "EHang Custom FC",
    "Damoda Show FC", "Verge Aero Custom FC", "MMC Custom FC", "Pixiel Custom FC", "AscTec / (Intel) FC",
    "SkyElements Custom FC", "Botlab Custom FC", "Flock Drone Art Custom FC",
]
selected_flight_control_board = StringVar(value="All")  # Αρχική τιμή "All"

# Battery type options
battery_type_options = ["All", "Li-Ion", "Li-Po", "Li-S", "Hybrid"]
selected_battery_type = StringVar(value="All")

# Frame Material Options
frame_material_options = [
    "All", "Composite", "Carbon Fiber", "Plastic", "Foam", "EPO Foam",
    "Aluminum", "Aluminum Alloy", "Magnesium Alloy", "Titanium", "Aluminum & Carbon",
    "Plastic & Composite", "Carbon & Plastic", "Plastic & Composite"
]
selected_frame_material = StringVar(value="All")


# Main frame
frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Input Section
input_frame = ttk.LabelFrame(frame, text="Filters", padding=10)
input_frame.grid(row=0, column=0, columnspan=2, sticky=EW, pady=10)

input_frame.columnconfigure(index=5, weight=1)

common_font = ("Helvetica", 10)

# Labels και entries
label_category = ttk.Label(input_frame, text="Select Drone Category:", font=common_font, style="TLabel")
label_category.grid(row=0, column=0, sticky=W, pady=5, padx=5)

category_dropdown = ttk.Combobox(input_frame, textvariable=selected_category,
                                 values=["All Drones"] + list(categories.values()))
category_dropdown.grid(row=0, column=1, pady=5, padx=5, sticky=EW)
category_dropdown.configure(font=common_font)

label_wind_resistance = ttk.Label(input_frame, text="Minimum Wind Resistance (km/h):", font=common_font, style="TLabel")
label_wind_resistance.grid(row=0, column=2, sticky=W, pady=5, padx=5)

entry_wind_resistance = ttk.Entry(input_frame, textvariable=min_wind_resistance)
entry_wind_resistance.grid(row=0, column=3, pady=5, padx=10, sticky=EW)
entry_wind_resistance.configure(font=common_font)

label_how_many = ttk.Label(input_frame, text="How many drones?", font=common_font, style="TLabel")
label_how_many.grid(row=1, column=0, sticky=W, pady=5, padx=5)

entry_how_many = ttk.Entry(input_frame, textvariable=number_of_drones)
entry_how_many.grid(row=1, column=1, pady=5, padx=5, sticky=EW)
entry_how_many.configure(font=common_font)

label_min_flight_time = ttk.Label(input_frame, text="Minimum flight time (min):", font=common_font, style="TLabel")
label_min_flight_time.grid(row=2, column=0, sticky=W, pady=5, padx=5)

entry_min_flight_time = ttk.Entry(input_frame, textvariable=min_flight_time)
entry_min_flight_time.grid(row=2, column=1, pady=5, padx=5, sticky=EW)
entry_min_flight_time.configure(font=common_font)

label_weight_lifting_capacity = ttk.Label(input_frame, text="Minimum Weight-Lifting Capacity (kg):", font=common_font, style="TLabel")
label_weight_lifting_capacity.grid(row=1, column=2, sticky=W, pady=5, padx=5)

entry_weight_lifting_capacity = ttk.Entry(input_frame, textvariable=min_weight_lifting_capacity)
entry_weight_lifting_capacity.grid(row=1, column=3, pady=5, padx=10, sticky=EW)
entry_weight_lifting_capacity.configure(font=common_font)

label_max_speed = ttk.Label(input_frame, text="Minimum Max Speed (km/h):", font=common_font, style="TLabel")
label_max_speed.grid(row=2, column=2, sticky=W, pady=5, padx=5)

entry_max_speed = ttk.Entry(input_frame, textvariable=min_max_speed)
entry_max_speed.grid(row=2, column=3, pady=5, padx=10, sticky=EW)
entry_max_speed.configure(font=common_font)

label_transmitter_range = ttk.Label(input_frame, text="Minimum Transmitter Range (km):", font=common_font, style="TLabel")
label_transmitter_range.grid(row=3, column=0, sticky=W, pady=5, padx=5)

entry_transmitter_range = ttk.Entry(input_frame, textvariable=min_transmitter_range, width=20)
entry_transmitter_range.grid(row=3, column=1, pady=5, padx=5, sticky=EW)
entry_transmitter_range.configure(font=common_font)

label_camera_resolution = ttk.Label(input_frame, text="Minimum Camera Resolution (MP):", font=common_font, style="TLabel")
label_camera_resolution.grid(row=3, column=2, sticky=W, pady=5, padx=5)

entry_camera_resolution = ttk.Entry(input_frame, textvariable=min_camera_resolution)
entry_camera_resolution.grid(row=3, column=3, pady=5, padx=10, sticky=EW)
entry_camera_resolution.configure(font=common_font)

label_battery_mah = ttk.Label(input_frame, text="Minimum Battery (mAh):", font=common_font, style="TLabel")
label_battery_mah.grid(row=4, column=0, sticky=W, pady=5, padx=5)

entry_battery_mah = ttk.Entry(input_frame, textvariable=min_battery_mah)
entry_battery_mah.grid(row=4, column=1, pady=5, padx=10, sticky=EW)
entry_battery_mah.configure(font=common_font)

label_weight_kg = ttk.Label(input_frame, text="Minimum Weight (kg):", font=common_font, style="TLabel")
label_weight_kg.grid(row=4, column=2, sticky=W, pady=5, padx=5)

entry_weight_kg = ttk.Entry(input_frame, textvariable=min_weight_kg)
entry_weight_kg.grid(row=4, column=3, pady=5, padx=10, sticky=EW)
entry_weight_kg.configure(font=common_font)

label_battery_type = ttk.Label(input_frame, text="Battery Type:", font=common_font, style="TLabel")
label_battery_type.grid(row=0, column=4, sticky=W, pady=5, padx=5)

battery_type_dropdown = ttk.Combobox(input_frame, textvariable=selected_battery_type, values=battery_type_options, width=20)
battery_type_dropdown.grid(row=0, column=5, pady=5, padx=5, sticky=W)
battery_type_dropdown.configure(font=common_font)

# Frame Material Label
label_frame_material = ttk.Label(input_frame, text="Frame Material:", font=common_font, style="TLabel")
label_frame_material.grid(row=1, column=4, pady=5, padx=5, sticky=W)

# Frame Material Dropdown
frame_material_dropdown = ttk.Combobox(input_frame, textvariable=selected_frame_material, values=frame_material_options, width=20)
frame_material_dropdown.grid(row=1, column=5, pady=5, padx=5, sticky=W)
frame_material_dropdown.configure(font=common_font)

# Flight Control Board Label
label_flight_control_board = ttk.Label(input_frame, text="Flight Control Board:", font=common_font, style="TLabel")
label_flight_control_board.grid(row=2, column=4, pady=5, padx=5, sticky=W)  # Τοποθέτηση κάτω από το Frame Material

# Flight Control Board Dropdown
flight_control_board_dropdown = ttk.Combobox(input_frame, textvariable=selected_flight_control_board, values=flight_control_board_options, width=20)
flight_control_board_dropdown.grid(row=2, column=5, pady=5, padx=5, sticky=W)  # Ευθυγράμμιση και μέγεθος
flight_control_board_dropdown.configure(font=common_font)


# Button Section
button_frame = ttk.Frame(frame, padding=10)
button_frame.grid(row=1, column=0, columnspan=2, sticky=EW)

button_import = ttk.Button(button_frame, text="Import", style="info.TButton")
button_import.pack(side=LEFT, padx=10)

button_calculate = ttk.Button(button_frame, text="Calculate", style="success.TButton")
button_calculate.pack(side=LEFT, padx=10)

button_export = ttk.Button(button_frame, text="Export", style="primary.TButton")
button_export.pack(side=LEFT, padx=10)

button_view_full_excel = ttk.Button(button_frame, text="View Full Excel", style="warning.TButton")
button_view_full_excel.pack(side=LEFT, padx=10)

# Results Section
results_frame = ttk.LabelFrame(frame, text="Results", padding=10)
results_frame.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=10)

tree = ttk.Treeview(results_frame, show="headings", height=10)
tree.pack(fill=BOTH, expand=True)

# Columns Selection Section
checkbox_frame = ttk.LabelFrame(frame, text="Select Columns to Display", padding=10)
checkbox_frame.grid(row=3, column=0, columnspan=6, pady=10, sticky=EW)

# Chart Display Section
chart_frame = ttk.LabelFrame(frame, text="Influence Charts", padding=10)
chart_frame.grid(row=4, column=0, columnspan=6, sticky=EW, pady=10)

for i in range(6):
    checkbox_frame.columnconfigure(i, weight=1, uniform="columns")

available_columns = [
    "Manufacturer", "Model", "Type", "Flight_Time_(min)", "Wind_Resistance_(km/h)",
    "Weight-Lifting_Capacity_(kg)", "Max_Speed_(km/h)", "Transmitter_Range_(km)",
    "Camera_Resolution_(MP)", "Battery_Type", "Battery_(mAh)", "Weight_(kg)", "Frame_Material",
    "Flight_Control_Board", "MIL-STD-810G/MIL-STD-810H", "Category", "Score"
]

selected_columns = {col: IntVar(value=1, master=root) for col in available_columns}

# Checkboxes to grid
row, col = 0, 0
for col_name in available_columns:
    checkbox = ttk.Checkbutton(
        checkbox_frame,
        text=col_name.replace("_", " "),
        variable=selected_columns[col_name]
    )
    checkbox.grid(row=row, column=col, sticky=W, padx=5, pady=2)
    col += 1
    if col >= 6:
        col = 0
        row += 1


# Functions
def import_file():
    global df
    file_path = askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel files", "*.xlsx")]
    )
    if file_path:
        try:
            df = pd.read_excel(file_path)
            if 'Category' in df.columns:
                df['Category'] = df['Category'].str.replace('_', ' ').str.strip().str.lower()
            messagebox.showinfo("Success", "File imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the file.\nError: {e}")


button_import.config(command=import_file)

def update_filters():
    global df
    if df is None:
        messagebox.showerror("Error", "No data loaded. Please import a file first.")
        return

    # Step 1: Filter DataFrame based on selected category
    selected_category_value = selected_category.get()
    if selected_category_value != "All Drones":
        filtered_df = df[df['Category'] == selected_category_value].copy()
    else:
        filtered_df = df

    # Step 2: Extract unique values for each dropdown menu
    # Ensure columns exist to avoid errors
    flight_control_boards = (
        filtered_df['Flight_Control_Board'].dropna().unique().tolist()
        if 'Flight_Control_Board' in filtered_df.columns else []
    )
    battery_types = (
        filtered_df['Battery_Type'].dropna().unique().tolist()
        if 'Battery_Type' in filtered_df.columns else []
    )
    frame_materials = (
        filtered_df['Frame_Material'].dropna().unique().tolist()
        if 'Frame_Material' in filtered_df.columns else []
    )

    # Step 3: Update dropdown menus dynamically
    flight_control_board_dropdown['values'] = ["All"] + flight_control_boards
    battery_type_dropdown['values'] = ["All"] + battery_types
    frame_material_dropdown['values'] = ["All"] + frame_materials

    # Reset dropdowns to "All"
    selected_flight_control_board.set("All")
    selected_battery_type.set("All")
    selected_frame_material.set("All")

category_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())


def display_results():
    global df
    if df is None:
        messagebox.showerror("Error", "No data loaded. Please import a file first.")
        return

    # Retrieve current dropdown selections
    current_category = selected_category.get()
    current_battery = selected_battery_type.get()
    current_frame = selected_frame_material.get()
    current_fcb = selected_flight_control_board.get()

    # Retrieve the user-entered numeric values
    user_min_time = min_flight_time.get()
    user_min_wind = min_wind_resistance.get()
    user_min_weight = min_weight_lifting_capacity.get()
    user_min_speed = min_max_speed.get()
    user_min_range = min_transmitter_range.get()
    user_min_camera = min_camera_resolution.get()
    user_min_battery = min_battery_mah.get()
    user_min_weight_kg = min_weight_kg.get()

    # Start with the full dataset and filter based on dropdown selections.
    subset = df.copy()
    if current_category != "All Drones":
        subset = subset[subset['Category'] == current_category].copy()
    if current_battery != "All":
        subset = subset[subset['Battery_Type'] == current_battery].copy()
    if current_frame != "All":
        subset = subset[subset['Frame_Material'] == current_frame].copy()
    if current_fcb != "All":
        subset = subset[subset['Flight_Control_Board'] == current_fcb].copy()

    # Create a mapping for each numeric criterion:
    criteria = {
        "Flight Time (min)": (user_min_time, "Flight_Time_(min)"),
        "Wind Resistance (km/h)": (user_min_wind, "Wind_Resistance_(km/h)"),
        "Weight-Lifting Capacity (kg)": (user_min_weight, "Weight-Lifting_Capacity_(kg)"),
        "Max Speed (km/h)": (user_min_speed, "Max_Speed_(km/h)"),
        "Transmitter Range (km)": (user_min_range, "Transmitter_Range_(km)"),
        "Camera Resolution (MP)": (user_min_camera, "Camera_Resolution_(MP)"),
        "Battery (mAh)": (user_min_battery, "Battery_(mAh)"),
        "Weight (kg)": (user_min_weight_kg, "Weight_(kg)")
    }

    # Validate each numeric input against the allowed range in the filtered subset.
    for label, (user_value, col_name) in criteria.items():
        try:
            allowed_min = subset[col_name].min()
            allowed_max = subset[col_name].max()
        except Exception as e:
            continue  # Skip the check if the column doesn't exist
        if user_value < allowed_min or user_value > allowed_max:
            messagebox.showerror(
                "Invalid Input",
                f"For category '{current_category}', the allowed range for {label} is between {allowed_min} and {allowed_max}."
            )
            return  # Stop processing if any input is invalid

    # Apply the numeric filters to obtain the final filtered DataFrame.
    filtered_df = subset[
        (subset['Flight_Time_(min)'] >= user_min_time) &
        (subset['Wind_Resistance_(km/h)'] >= user_min_wind) &
        (subset['Weight-Lifting_Capacity_(kg)'] >= user_min_weight) &
        (subset['Max_Speed_(km/h)'] >= user_min_speed) &
        (subset['Transmitter_Range_(km)'] >= user_min_range) &
        (subset['Camera_Resolution_(MP)'] >= user_min_camera) &
        (subset['Battery_(mAh)'] >= user_min_battery) &
        (subset['Weight_(kg)'] >= user_min_weight_kg)
        ].copy()

    if filtered_df.empty:
        messagebox.showinfo("No Data", "No drones meet the current filter criteria.")
        tree.delete(*tree.get_children())
        return

    # New Check for "How many drones?"
    # Allowed minimum is 1, allowed maximum is the number of drones available.
    num_drones = number_of_drones.get()
    allowed_min_drones = 1
    allowed_max_drones = len(filtered_df)
    if num_drones < allowed_min_drones or num_drones > allowed_max_drones:
        messagebox.showerror(
            "Invalid Input",
            f"For the current filtered dataset, the number of drones must be between {allowed_min_drones} and {allowed_max_drones}."
        )
        return

    # Continue with Score Calculation (if applicable)
    weights = weights_dict.get(current_category, {})
    for column, weight in weights.items():
        if column in filtered_df.columns:
            if column == 'Frame_Material':
                filtered_df[f"{column}_Score"] = filtered_df[column].map(Criteria_Scores_Frame_Material).fillna(0)
            elif column == 'Flight_Control_Board':
                filtered_df[f"{column}_Score"] = filtered_df[column].map(Criteria_Scores_Flight_Control_Board).fillna(0)
            elif column == 'MIL-STD-810G/MIL-STD-810H':
                filtered_df[f"{column}_Score"] = filtered_df[column].map(Criteria_Scores_MIL_STD).fillna(0)
            else:
                min_val = filtered_df[column].min()
                max_val = filtered_df[column].max()
                if max_val > min_val:
                    filtered_df[f"{column}_Score"] = ((filtered_df[column] - min_val) / (max_val - min_val)) * weight
                else:
                    filtered_df[f"{column}_Score"] = 0

    filtered_df.fillna(0, inplace=True)
    score_columns = [f"{col}_Score" for col in weights.keys() if f"{col}_Score" in filtered_df.columns]
    filtered_df['Score'] = filtered_df[score_columns].sum(axis=1).round(2)
    filtered_df.sort_values(by='Score', ascending=False, inplace=True)

    # Display only the number of drones requested by the user.
    drones_top = filtered_df.head(num_drones)
    update_tree(drones_top)

    # New: Update the charts in the main board
    update_charts()


button_calculate.config(command=display_results)


def update_tree(data):
    tree.delete(*tree.get_children())
    tree["columns"] = []

    columns_to_display = [col for col, var in selected_columns.items() if var.get() == 1]
    if not columns_to_display:
        messagebox.showinfo("No Columns Selected", "Please select at least one column to display.")
        return

    tree["columns"] = columns_to_display
    for col in columns_to_display:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, anchor=CENTER, width=150)

    for _, row in data.iterrows():
        tree.insert("", "end", values=[row[col] if col in row else "" for col in columns_to_display])


def export_to_excel():
    data = []
    columns = tree["columns"]

    for child in tree.get_children():
        row = tree.item(child)["values"]
        data.append(row)

    if not data:
        messagebox.showinfo("No Data", "There is no data to export.")
        return

    df_export = pd.DataFrame(data, columns=columns)
    file_path = asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Save as"
    )
    if file_path:
        df_export.to_excel(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Data successfully exported to {file_path}")


def view_full_excel():
    global df
    if df is None:
        messagebox.showerror("Error", "No data loaded. Please import a file first.")
        return

    excel_window = Tk()
    excel_window.title("Full Excel View")
    excel_window.geometry("900x600")

    tree_excel = ttk.Treeview(excel_window, show="headings", height=25)
    tree_excel.pack(fill=BOTH, expand=True)

    tree_excel["columns"] = df.columns.tolist()
    for col in df.columns:
        tree_excel.heading(col, text=col)
        tree_excel.column(col, anchor=CENTER, width=120)

    for _, row in df.iterrows():
        tree_excel.insert("", "end", values=row.tolist())

    close_button = ttk.Button(excel_window, text="Close", command=excel_window.destroy, style="danger.TButton")
    close_button.pack(pady=10)


button_export.config(command=export_to_excel)
button_view_full_excel.config(command=view_full_excel)

def update_charts():
    # Clear any previous charts
    for widget in chart_frame.winfo_children():
        widget.destroy()

    selected_category_value = selected_category.get()
    if not selected_category_value or selected_category_value == "All Drones":
        return

    weights = weights_dict.get(selected_category_value, {})
    if not weights:
        return

    labels = list(weights.keys())
    values = list(weights.values())
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
              "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]

    # Same figure setup as your original, so the bar chart stays the same
    fig, axs = plt.subplots(1, 2, figsize=(9, 4), dpi=120)

    # Same overall title
    fig.suptitle(
        f"Influence Weights for {selected_category_value.title()} Drones",
        fontsize=13, weight='bold', color="purple", y=0.98
    )

    # PIE CHART (left subplot)
    wedges, texts, autotexts = axs[0].pie(
        values,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 7, 'color': "black"},
        radius=1.0  # Make the pie bigger vertically
    )
    # Title above the pie, centered
    axs[0].set_title("Pie Chart", fontsize=11, weight='bold', color="purple",
                     loc='center', pad=8)

    # Legend just to the right of the pie
    axs[0].legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(0.9, 0.5),
        fontsize=8
    )

    # White text for the autopct labels
    for text in autotexts:
        text.set_color("white")
        text.set_fontsize(7)
        text.set_weight("normal")

    # BAR CHART (right subplot)
    axs[1].barh(labels, values, color=colors, edgecolor="black")
    axs[1].set_title("Bar Chart", fontsize=11, weight='bold', color="purple")
    axs[1].set_xlabel("Influence Weight (%)", fontsize=9)
    axs[1].invert_yaxis()  # largest value at top
    axs[1].grid(axis="x", linestyle="--", alpha=0.7)

    fig.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=0.35, wspace=0.4)

    # MANUALLY SHIFT PIE CHART SUBPLOT
    # 1. Remember the bar-chart position so it is not altered.
    bar_pos = axs[1].get_position()  # (x0, y0, x1, y1) in figure coords

    # 2. Re-assign the bar chart to exactly the same position (locks it in place)
    axs[1].set_position(bar_pos)

    # 3. Shift/enlarge the pie chart subplot to the far left
    axs[0].set_position([0.02, bar_pos.y0, 0.3, bar_pos.height])

    # Embed the figure in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

def update_default_values():
    global df
    if df is None:
        return

    # Determine the appropriate subset of the data
    selected_cat = selected_category.get()
    if selected_cat == "All Drones":
        subset = df.copy()
    else:
        subset = df[df['Category'] == selected_cat].copy()

    # Update each criteria with the minimum value from the subset.
    try:
        min_val = subset['Flight_Time_(min)'].min()
        min_flight_time.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Wind_Resistance_(km/h)'].min()
        min_wind_resistance.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Weight-Lifting_Capacity_(kg)'].min()
        min_weight_lifting_capacity.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Max_Speed_(km/h)'].min()
        min_max_speed.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Transmitter_Range_(km)'].min()
        min_transmitter_range.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Camera_Resolution_(MP)'].min()
        min_camera_resolution.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Battery_(mAh)'].min()
        min_battery_mah.set(min_val)
    except KeyError:
        pass

    try:
        min_val = subset['Weight_(kg)'].min()
        min_weight_kg.set(min_val)
    except KeyError:
        pass

# Modified update_filters() Function
def update_filters():
    global df
    if df is None:
        return

    # Get current selections
    cat_sel   = selected_category.get()         # e.g., "All Drones" or a specific category
    bat_sel   = selected_battery_type.get()       # e.g., "All" or a specific battery type
    frame_sel = selected_frame_material.get()     # e.g., "All" or "Carbon Fiber"
    fcb_sel   = selected_flight_control_board.get() # e.g., "All" or a specific flight control board

    # Update Battery Type Options
    battery_subset = df.copy()
    if cat_sel != "All Drones":
        battery_subset = battery_subset[battery_subset['Category'] == cat_sel]
    if frame_sel != "All":
        battery_subset = battery_subset[battery_subset['Frame_Material'] == frame_sel]
    if fcb_sel != "All":
        battery_subset = battery_subset[battery_subset['Flight_Control_Board'] == fcb_sel]
    battery_options = sorted(battery_subset['Battery_Type'].dropna().unique().tolist())
    battery_type_dropdown['values'] = ["All"] + battery_options
    # If the current Battery Type selection is no longer valid, reset it to "All"
    if bat_sel != "All" and bat_sel not in battery_options:
        selected_battery_type.set("All")

    # Compute available Frame Materials filtering
    frame_subset = df.copy()
    if cat_sel != "All Drones":
        frame_subset = frame_subset[frame_subset['Category'] == cat_sel]
    if bat_sel != "All":
        frame_subset = frame_subset[frame_subset['Battery_Type'] == bat_sel]
    if fcb_sel != "All":
        frame_subset = frame_subset[frame_subset['Flight_Control_Board'] == fcb_sel]
    frame_options = sorted(frame_subset['Frame_Material'].dropna().unique().tolist())
    frame_material_dropdown['values'] = ["All"] + frame_options
    if frame_sel != "All" and frame_sel not in frame_options:
        selected_frame_material.set("All")

    # Update Flight Control Board Options
    fcb_subset = df.copy()
    if cat_sel != "All Drones":
        fcb_subset = fcb_subset[fcb_subset['Category'] == cat_sel]
    if bat_sel != "All":
        fcb_subset = fcb_subset[fcb_subset['Battery_Type'] == bat_sel]
    if frame_sel != "All":
        fcb_subset = fcb_subset[fcb_subset['Frame_Material'] == frame_sel]
    fcb_options = sorted(fcb_subset['Flight_Control_Board'].dropna().unique().tolist())
    flight_control_board_dropdown['values'] = ["All"] + fcb_options
    if fcb_sel != "All" and fcb_sel not in fcb_options:
        selected_flight_control_board.set("All")

    # Now update the numeric filter defaults based on the current subset using all selections.
    numeric_subset = df.copy()
    if cat_sel != "All Drones":
        numeric_subset = numeric_subset[numeric_subset['Category'] == cat_sel]
    if selected_battery_type.get() != "All":
        numeric_subset = numeric_subset[numeric_subset['Battery_Type'] == selected_battery_type.get()]
    if selected_frame_material.get() != "All":
        numeric_subset = numeric_subset[numeric_subset['Frame_Material'] == selected_frame_material.get()]
    if selected_flight_control_board.get() != "All":
        numeric_subset = numeric_subset[numeric_subset['Flight_Control_Board'] == selected_flight_control_board.get()]

    try:
        min_flight_time.set(numeric_subset['Flight_Time_(min)'].min())
    except Exception as e:
        print("Could not update Flight Time:", e)
    try:
        min_wind_resistance.set(numeric_subset['Wind_Resistance_(km/h)'].min())
    except Exception as e:
        print("Could not update Wind Resistance:", e)
    try:
        min_weight_lifting_capacity.set(numeric_subset['Weight-Lifting_Capacity_(kg)'].min())
    except Exception as e:
        print("Could not update Weight-Lifting Capacity:", e)
    try:
        min_max_speed.set(numeric_subset['Max_Speed_(km/h)'].min())
    except Exception as e:
        print("Could not update Max Speed:", e)
    try:
        min_transmitter_range.set(numeric_subset['Transmitter_Range_(km)'].min())
    except Exception as e:
        print("Could not update Transmitter Range:", e)
    try:
        min_camera_resolution.set(numeric_subset['Camera_Resolution_(MP)'].min())
    except Exception as e:
        print("Could not update Camera Resolution:", e)
    try:
        min_battery_mah.set(numeric_subset['Battery_(mAh)'].min())
    except Exception as e:
        print("Could not update Battery (mAh):", e)
    try:
        min_weight_kg.set(numeric_subset['Weight_(kg)'].min())
    except Exception as e:
        print("Could not update Weight (kg):", e)


# Bind update_filters() to changes in each dropdown
category_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())
battery_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())
frame_material_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())
flight_control_board_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())


# Reset Filters Button
def reset_filters():
    # Reset dropdowns to default selections
    selected_category.set("All Drones")
    selected_battery_type.set("All")
    selected_frame_material.set("All")
    selected_flight_control_board.set("All")

    if df is not None:
        full_subset = df.copy()
        try:
            min_flight_time.set(full_subset['Flight_Time_(min)'].min())
        except Exception as e:
            print("Could not update Flight Time:", e)
        try:
            min_wind_resistance.set(full_subset['Wind_Resistance_(km/h)'].min())
        except Exception as e:
            print("Could not update Wind Resistance:", e)
        try:
            min_weight_lifting_capacity.set(full_subset['Weight-Lifting_Capacity_(kg)'].min())
        except Exception as e:
            print("Could not update Weight-Lifting Capacity:", e)
        try:
            min_max_speed.set(full_subset['Max_Speed_(km/h)'].min())
        except Exception as e:
            print("Could not update Max Speed:", e)
        try:
            min_transmitter_range.set(full_subset['Transmitter_Range_(km)'].min())
        except Exception as e:
            print("Could not update Transmitter Range:", e)
        try:
            min_camera_resolution.set(full_subset['Camera_Resolution_(MP)'].min())
        except Exception as e:
            print("Could not update Camera Resolution:", e)
        try:
            min_battery_mah.set(full_subset['Battery_(mAh)'].min())
        except Exception as e:
            print("Could not update Battery (mAh):", e)
        try:
            min_weight_kg.set(full_subset['Weight_(kg)'].min())
        except Exception as e:
            print("Could not update Weight (kg):", e)

        # Also update the dropdown option lists based on the full dataset.
        if 'Battery_Type' in df.columns:
            battery_type_dropdown['values'] = ["All"] + sorted(df['Battery_Type'].dropna().unique().tolist())
        if 'Frame_Material' in df.columns:
            frame_material_dropdown['values'] = ["All"] + sorted(df['Frame_Material'].dropna().unique().tolist())
        if 'Flight_Control_Board' in df.columns:
            flight_control_board_dropdown['values'] = ["All"] + sorted(
                df['Flight_Control_Board'].dropna().unique().tolist())


# Create a Reset Filters button in the button section
reset_button = ttk.Button(button_frame, text="Reset Filters", style="secondary.TButton", command=reset_filters)
reset_button.pack(side=LEFT, padx=10)


category_dropdown.bind("<<ComboboxSelected>>", lambda e: update_filters())

root.mainloop()
