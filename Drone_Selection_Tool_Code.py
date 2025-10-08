# app.py
import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ---- bring in your static data from a separate file ----
from criteria_data import (
    CATEGORY_OPTIONS,
    weights_dict,
    Criteria_Scores_Frame_Material,
    Criteria_Scores_MIL_STD,
    Criteria_Scores_Flight_Control_Board,
)

# ---------------- Page setup ----------------
st.set_page_config(page_title="Drone Selection Tool", layout="wide")
st.title("🛩️ Drone Selection Tool")
st.write("Upload an Excel file with drone data, apply filters, and rank drones by criteria.")

# ---------------- Helpers: scoring & utilities ----------------
def add_scores_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a 'Score' for each row using the weights of its own Category (row-wise).
    Adds *_Score helper columns when a weighted feature exists.
    Also adds a 'Rating' (stars) derived from the Score.
    Returns a new DataFrame.
    """
    out = df.copy()

    # Normalize Category for matching
    if "Category" not in out.columns:
        return out
    out["Category"] = (
        out["Category"].astype(str).str.replace("_", " ").str.strip().str.lower()
    )

    # Ensure Score column exists
    if "Score" not in out.columns:
        out["Score"] = 0.0

    # Iterate each category group and score with that category's weights
    for cat, weights in weights_dict.items():
        mask = out["Category"] == cat
        if not mask.any():
            continue

        # Clear any previous score columns for this subset
        for col in weights.keys():
            out.loc[mask, f"{col}_Score"] = 0.0

        sub = out.loc[mask].copy()
        for col, w in weights.items():
            if col not in sub.columns:
                continue

            # categorical mappings
            if col == "Frame_Material":
                sc = sub[col].map(Criteria_Scores_Frame_Material).fillna(0) * w
            elif col == "Flight_Control_Board":
                sc = sub[col].map(Criteria_Scores_Flight_Control_Board).fillna(0) * w
            elif col == "MIL-STD-810G/MIL-STD-810H":
                sc = sub[col].map(Criteria_Scores_MIL_STD).fillna(0) * w
            else:
                # numeric normalization within this category subset
                s = pd.to_numeric(sub[col], errors="coerce")
                mn, mx = s.min(), s.max()
                if pd.isna(mn) or pd.isna(mx) or mx <= mn:
                    norm = pd.Series(0, index=sub.index, dtype=float)
                else:
                    norm = (s - mn) / (mx - mn)
                sc = norm.fillna(0) * w

            out.loc[mask, f"{col}_Score"] = sc

        score_cols = [f"{c}_Score" for c in weights.keys() if f"{c}_Score" in out.columns]
        if score_cols:
            out.loc[mask, "Score"] = out.loc[mask, score_cols].sum(axis=1).round(2)

    # Optional human-readable rating from Score
    def to_rating(x: float) -> str:
        if pd.isna(x):
            return ""
        if x >= 0.85: return "★★★★★"
        if x >= 0.70: return "★★★★"
        if x >= 0.55: return "★★★"
        if x >= 0.40: return "★★"
        return "★"

    out["Rating"] = out["Score"].apply(to_rating)
    return out


def filter_subset(data: pd.DataFrame, cat: str, bat: str, frm: str, fcb: str) -> pd.DataFrame:
    """Apply categorical filters."""
    sub = data.copy()
    if "Category" in sub.columns:
        sub["Category"] = sub["Category"].astype(str).str.replace("_", " ").str.strip().str.lower()

    if cat != "All Drones" and "Category" in sub.columns:
        sub = sub[sub["Category"] == cat.lower()]
    if bat != "All" and "Battery_Type" in sub.columns:
        sub = sub[sub["Battery_Type"] == bat]
    if frm != "All" and "Frame_Material" in sub.columns:
        sub = sub[sub["Frame_Material"] == frm]
    if fcb != "All" and "Flight_Control_Board" in sub.columns:
        sub = sub[sub["Flight_Control_Board"] == fcb]
    return sub


def dynamic_options(sub: pd.DataFrame):
    """Return dropdown value lists (FCB, Battery, Frame) with 'All' first."""
    fcb = ["All"]
    bat = ["All"]
    frm = ["All"]
    if "Flight_Control_Board" in sub.columns:
        fcb += sorted(sub["Flight_Control_Board"].dropna().astype(str).unique().tolist())
    if "Battery_Type" in sub.columns:
        bat += sorted(sub["Battery_Type"].dropna().astype(str).unique().tolist())
    if "Frame_Material" in sub.columns:
        frm += sorted(sub["Frame_Material"].dropna().astype(str).unique().tolist())
    return fcb, bat, frm


def apply_numeric_thresholds(data: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
    """Keep rows where each numeric column is >= its threshold (if threshold > 0)."""
    out = data.copy()
    for col, val in thresholds.items():
        if col in out.columns and float(val) > 0:
            s = pd.to_numeric(out[col], errors="coerce").fillna(0)
            out = out[s >= float(val)]
    return out


def score_dataframe_for_selected_category(data: pd.DataFrame, category_key: str) -> pd.DataFrame:
    """
    Score the current filtered result using weights of the **selected** category.
    This is independent of the global row-wise add_scores_by_category().
    """
    if category_key not in weights_dict:
        return data

    tmp = data.copy()
    w = weights_dict[category_key]

    for col, weight in w.items():
        if col not in tmp.columns:
            continue

        # categorical
        if col == "Frame_Material":
            tmp[f"{col}_Score"] = tmp[col].map(Criteria_Scores_Frame_Material).fillna(0) * weight
            continue
        if col == "Flight_Control_Board":
            tmp[f"{col}_Score"] = tmp[col].map(Criteria_Scores_Flight_Control_Board).fillna(0) * weight
            continue
        if col == "MIL-STD-810G/MIL-STD-810H":
            tmp[f"{col}_Score"] = tmp[col].map(Criteria_Scores_MIL_STD).fillna(0) * weight
            continue

        # numeric
        s = pd.to_numeric(tmp[col], errors="coerce").fillna(0)
        mn, mx = s.min(), s.max()
        norm = (s - mn) / (mx - mn) if mx > mn else 0
        tmp[f"{col}_Score"] = norm * weight

    score_cols = [c for c in tmp.columns if c.endswith("_Score")]
    if score_cols:
        tmp["Score"] = tmp[score_cols].sum(axis=1).round(2)
        tmp = tmp.sort_values("Score", ascending=False)
    return tmp


def excel_download_button(df_to_export: pd.DataFrame, label="📥 Export to Excel", filename="filtered_drones.xlsx"):
    """Render a download button for a DataFrame."""
    if df_to_export is None or df_to_export.empty:
        return
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_to_export.to_excel(w, index=False, sheet_name="Results")
    st.download_button(
        label,
        buf.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def plot_weights(category_key: str):
    """Draw pie + horizontal bar charts with a shared, consistent color palette."""
    if category_key not in weights_dict:
        return

    labels = list(weights_dict[category_key].keys())
    values = list(weights_dict[category_key].values())

    # --- consistent colors for both plots ---
    cmap = plt.get_cmap("tab10")
    colors = [cmap(i % cmap.N) for i in range(len(labels))]

    fig, axs = plt.subplots(1, 2, figsize=(10, 4), dpi=110)
    fig.suptitle(f"Influence Weights – {category_key.title()}", fontsize=13, weight="bold")

    # Pie (use same colors)
    axs[0].pie(values, autopct="%1.1f%%", startangle=90, colors=colors)
    axs[0].set_title("Pie")

    # Bar (use same colors, one per bar)
    axs[1].barh(labels, values, color=colors)
    axs[1].invert_yaxis()
    axs[1].set_title("Bar")
    axs[1].set_xlabel("Weight")

    st.pyplot(fig)



def _update_min_inputs_from_subset():
    """
    Auto-fill min numeric inputs based on the selected category subset.
    Called on category change and once after upload.
    """
    if "df_scored" not in st.session_state:
        return
    base = st.session_state.df_scored.copy()

    cat = st.session_state.get("selected_category", "All Drones")
    if cat != "All Drones" and "Category" in base.columns:
        sub = base[base["Category"] == cat.lower()]
    else:
        sub = base

    if sub.empty:
        return

    def smin(col):
        return float(pd.to_numeric(sub[col], errors="coerce").min()) if col in sub.columns else 0.0

    st.session_state["min_flight_time"] = smin("Flight_Time_(min)")
    st.session_state["min_wind_resistance"] = smin("Wind_Resistance_(km/h)")
    st.session_state["min_weight_lifting_capacity"] = smin("Weight-Lifting_Capacity_(kg)")
    st.session_state["min_max_speed"] = smin("Max_Speed_(km/h)")
    st.session_state["min_transmitter_range"] = smin("Transmitter_Range_(km)")
    st.session_state["min_camera_resolution"] = smin("Camera_Resolution_(MP)")
    st.session_state["min_battery_mah"] = smin("Battery_(mAh)")
    st.session_state["min_weight_kg"] = smin("Weight_(kg)")

# ---------------- Upload ----------------
uploaded = st.file_uploader("📂 Upload Excel (.xlsx)", type=["xlsx"])
if not uploaded:
    st.info("Please upload an Excel file to continue.")
    st.stop()

df_raw = pd.read_excel(uploaded)

# Normalize Category for consistent matching
if "Category" in df_raw.columns:
    df_raw["Category"] = (
        df_raw["Category"].astype(str).str.replace("_", " ").str.strip().str.lower()
    )

# Compute a global score for each drone within its own category (row-wise)
df_scored = add_scores_by_category(df_raw)
st.session_state.df_scored = df_scored  # keep in session for quick access

# ---------------- Init default state ----------------
for k, v in {
    "selected_category": "All Drones",
    "selected_battery_type": "All",
    "selected_frame_material": "All",
    "selected_flight_control_board": "All",
    "number_of_drones": 5,
    "min_flight_time": 0.0,
    "min_wind_resistance": 0.0,
    "min_weight_lifting_capacity": 0.0,
    "min_max_speed": 0.0,
    "min_transmitter_range": 0.0,
    "min_camera_resolution": 0.0,
    "min_battery_mah": 0.0,
    "min_weight_kg": 0.0,
}.items():
    st.session_state.setdefault(k, v)

# First-time auto-fill of numeric mins after data load
if "did_init_defaults" not in st.session_state:
    _update_min_inputs_from_subset()
    st.session_state.did_init_defaults = True

# ---------------- Filters UI ----------------
st.subheader("Filters")

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    selected_category = st.selectbox(
        "Drone Category",
        ["All Drones"] + CATEGORY_OPTIONS,
        index=(0 if st.session_state.selected_category == "All Drones"
               else 1 + CATEGORY_OPTIONS.index(st.session_state.selected_category)
               if st.session_state.selected_category in CATEGORY_OPTIONS else 0),
        key="selected_category",
        on_change=_update_min_inputs_from_subset,
    )
    number_of_drones = st.number_input(
        "How many drones?",
        min_value=1,
        value=int(st.session_state.number_of_drones),
        step=1,
        key="number_of_drones",
    )

# Build dynamic dropdown options using category-only subset
subset_for_opts = filter_subset(
    df_scored,
    st.session_state.selected_category,
    "All", "All", "All",
)
fcb_opts, bat_opts, frm_opts = dynamic_options(subset_for_opts)

with c2:
    st.number_input("Min flight time (min)", min_value=0.0, value=float(st.session_state.min_flight_time), key="min_flight_time")
    st.number_input("Min wind (km/h)", min_value=0.0, value=float(st.session_state.min_wind_resistance), key="min_wind_resistance")

with c3:
    st.number_input("Min lifting (kg)", min_value=0.0, value=float(st.session_state.min_weight_lifting_capacity), key="min_weight_lifting_capacity")
    st.number_input("Min max speed (km/h)", min_value=0.0, value=float(st.session_state.min_max_speed), key="min_max_speed")

with c4:
    st.number_input("Min range (km)", min_value=0.0, value=float(st.session_state.min_transmitter_range), key="min_transmitter_range")
    st.number_input("Min camera (MP)", min_value=0.0, value=float(st.session_state.min_camera_resolution), key="min_camera_resolution")

with c5:
    st.number_input("Min battery (mAh)", min_value=0.0, value=float(st.session_state.min_battery_mah), key="min_battery_mah")
    st.selectbox("Battery Type", bat_opts, index=0 if st.session_state.selected_battery_type not in bat_opts else bat_opts.index(st.session_state.selected_battery_type), key="selected_battery_type")

with c6:
    st.number_input("Min weight (kg)", min_value=0.0, value=float(st.session_state.min_weight_kg), key="min_weight_kg")
    st.selectbox("Frame Material", frm_opts, index=0 if st.session_state.selected_frame_material not in frm_opts else frm_opts.index(st.session_state.selected_frame_material), key="selected_frame_material")
    st.selectbox("Flight Control Board", fcb_opts, index=0 if st.session_state.selected_flight_control_board not in fcb_opts else fcb_opts.index(st.session_state.selected_flight_control_board), key="selected_flight_control_board")

# Columns chooser
expected_cols = [
    "Manufacturer","Model","Type","Flight_Time_(min)","Wind_Resistance_(km/h)",
    "Weight-Lifting_Capacity_(kg)","Max_Speed_(km/h)","Transmitter_Range_(km)",
    "Camera_Resolution_(MP)","Battery_Type","Battery_(mAh)","Weight_(kg)",
    "Frame_Material","Flight_Control_Board","MIL-STD-810G/MIL-STD-810H","Category",
    "Score","Rating"
]
default_cols = [c for c in expected_cols if c in df_scored.columns]
selected_columns = st.multiselect(
    "Select columns to display",
    options=expected_cols,
    default=default_cols,
)

# Reset button
if st.button("Reset Filters"):
    for k, v in {
        "selected_category": "All Drones",
        "selected_battery_type": "All",
        "selected_frame_material": "All",
        "selected_flight_control_board": "All",
        "number_of_drones": 5,
        "min_flight_time": 0.0,
        "min_wind_resistance": 0.0,
        "min_weight_lifting_capacity": 0.0,
        "min_max_speed": 0.0,
        "min_transmitter_range": 0.0,
        "min_camera_resolution": 0.0,
        "min_battery_mah": 0.0,
        "min_weight_kg": 0.0,
    }.items():
        st.session_state[k] = v
    _update_min_inputs_from_subset()
    st.rerun()

# ---------------- Calculate & Display ----------------
st.subheader("Results")
if st.button("Calculate"):
    # 1) Apply categorical filters
    sub = filter_subset(
        df_scored,
        st.session_state.selected_category,
        st.session_state.selected_battery_type,
        st.session_state.selected_frame_material,
        st.session_state.selected_flight_control_board,
    )
    if sub.empty:
        st.info("No drones for the selected categorical filters.")
        st.stop()

    # 2) Apply numeric thresholds
    thresholds = {
        "Flight_Time_(min)": st.session_state.min_flight_time,
        "Wind_Resistance_(km/h)": st.session_state.min_wind_resistance,
        "Weight-Lifting_Capacity_(kg)": st.session_state.min_weight_lifting_capacity,
        "Max_Speed_(km/h)": st.session_state.min_max_speed,
        "Transmitter_Range_(km)": st.session_state.min_transmitter_range,
        "Camera_Resolution_(MP)": st.session_state.min_camera_resolution,
        "Battery_(mAh)": st.session_state.min_battery_mah,
        "Weight_(kg)": st.session_state.min_weight_kg,
    }
    sub = apply_numeric_thresholds(sub, thresholds)
    if sub.empty:
        st.info("No drones meet the current numeric criteria.")
        st.stop()

    # 3) Score the filtered set using the **selected category's** weights
    cat_key = st.session_state.selected_category
    scored = score_dataframe_for_selected_category(sub, cat_key) if cat_key in weights_dict else sub.copy()

    # 4) Top-N
    n = max(int(st.session_state.number_of_drones), 1)
    top = scored.head(n)

    # 5) Display selected columns
    show_cols = [c for c in selected_columns if c in top.columns]
    view = top.loc[:, show_cols] if show_cols else top
    st.dataframe(view, use_container_width=True)

    # 6) Export button
    excel_download_button(view)

    # 7) Full Excel (global per-row score within each drone's own category)
    with st.expander("View full Excel (scored by own category)"):
        st.dataframe(df_scored, use_container_width=True)

    # 8) Weight charts
    if cat_key in weights_dict:
        st.subheader("Influence Charts")
        plot_weights(cat_key)
