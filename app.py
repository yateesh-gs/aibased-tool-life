import matplotlib.pyplot as plt
import streamlit as st

from database import (
    OPERATIONS,
    TOOL_MATERIALS,
    WORKPIECE_MATERIALS,
    expected_values_table,
    machining_dataset_preview,
)
from graphs import (
    depth_life_data,
    feed_life_data,
    speed_life_data,
    wear_progression_data,
)
from prediction import predict_tool_life
from recommendation import get_recommendation
from report import generate_report, report_buffer


st.set_page_config(page_title="Tool Life Estimation", layout="wide")

st.title("AI-Based Tool Life Estimation Dashboard")
st.markdown("### Industrial Predictive Manufacturing Platform")
st.markdown("#### Taylor Equation")
st.latex(r"VT^n = C")

st.sidebar.title("Machining Parameters")

operation = st.sidebar.selectbox("Machining Operation", OPERATIONS)
workpiece_material = st.sidebar.selectbox("Workpiece Material", WORKPIECE_MATERIALS)
material = st.sidebar.selectbox("Tool Material", TOOL_MATERIALS)

speed = st.sidebar.slider("Cutting Speed (m/min)", 60, 220, 120)
feed = st.sidebar.slider("Feed Rate (mm/rev)", 0.1, 0.5, 0.2)
depth = st.sidebar.slider("Depth of Cut (mm)", 1.0, 5.0, 2.0)

prediction = predict_tool_life(speed, feed, depth, material, operation, workpiece_material)
tool_life = prediction.tool_life
condition = prediction.condition

st.subheader("Prediction Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Predicted Tool Life", f"{tool_life} min")

with c2:
    if condition == "GOOD":
        st.success("Tool Condition : GOOD")
    elif condition == "MODERATE WEAR":
        st.warning("Tool Condition : MODERATE WEAR")
    else:
        st.error("Tool Condition : HIGH WEAR")

st.subheader("Recommendation")

recommendation_type, recommendation_text = get_recommendation(workpiece_material, prediction)

if recommendation_type == "warning":
    st.warning(recommendation_text)
elif recommendation_type == "info":
    st.info(recommendation_text)
else:
    st.success(recommendation_text)

wear = prediction.wear_percentage

st.subheader("Tool Wear Meter")
st.progress(wear)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Tool Life vs Cutting Speed")

    speed_vals, life_vals, speed_table = speed_life_data(
        feed,
        depth,
        material,
        operation,
        workpiece_material,
        predict_tool_life,
    )

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(speed_vals, life_vals, marker='o')
    ax1.scatter([speed], [tool_life], color='red', s=80, zorder=5, label="Current Point")
    ax1.set_xlabel("Cutting Speed (m/min)")
    ax1.set_ylabel("Tool Life (min)")
    ax1.grid(True)
    ax1.legend()

    st.pyplot(fig1)

    st.table(speed_table)

with col2:

    st.subheader("Feed Rate vs Tool Life")

    feed_vals, feed_life, feed_table = feed_life_data(
        speed,
        depth,
        material,
        operation,
        workpiece_material,
        predict_tool_life,
    )

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(feed_vals, feed_life, marker='o')
    ax2.scatter([feed], [tool_life], color='red', s=80, zorder=5, label="Current Point")
    ax2.set_xlabel("Feed Rate (mm/rev)")
    ax2.set_ylabel("Tool Life (min)")
    ax2.grid(True)
    ax2.legend()

    st.pyplot(fig2)

    st.table(feed_table)

col3, col4 = st.columns(2)

with col3:

    st.subheader("Depth of Cut vs Tool Life")

    depth_vals, depth_life, depth_table = depth_life_data(
        speed,
        feed,
        material,
        operation,
        workpiece_material,
        predict_tool_life,
    )

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.plot(depth_vals, depth_life, marker='o')
    ax3.scatter([depth], [tool_life], color='red', s=80, zorder=5, label="Current Point")
    ax3.set_xlabel("Depth of Cut (mm)")
    ax3.set_ylabel("Tool Life (min)")
    ax3.grid(True)
    ax3.legend()

    st.pyplot(fig3)

    st.table(depth_table)

with col4:

    st.subheader("Tool Wear Progression")

    time_vals, wear_vals, wear_table = wear_progression_data(
        speed,
        feed,
        depth,
        material,
        operation,
        workpiece_material,
        predict_tool_life,
    )

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    ax4.plot(time_vals, wear_vals, marker='o')
    ax4.scatter([tool_life], [100], color='red', s=80, zorder=5, label="Predicted Tool Life")
    ax4.set_xlabel("Machining Time (min)")
    ax4.set_ylabel("Tool Wear")
    ax4.grid(True)
    ax4.legend()

    st.pyplot(fig4)

    st.table(wear_table)

st.subheader("Expected Values Table")

table_data = expected_values_table(
    operation,
    workpiece_material,
    material,
    speed,
    feed,
    depth,
    tool_life,
    condition,
)

st.table(table_data)

st.subheader("Machining Dataset Preview")

dataset_preview = machining_dataset_preview(
    operation,
    workpiece_material,
    material,
    speed,
    feed,
    depth,
    predict_tool_life,
)

st.dataframe(dataset_preview)

st.subheader("Download Report")

report = generate_report(
    operation,
    workpiece_material,
    material,
    speed,
    feed,
    depth,
    prediction,
    recommendation_text,
)

st.download_button(
    label="Download Report",
    data=report_buffer(report),
    file_name="tool_life_report.txt",
    mime="text/plain"
)

st.markdown("---")
st.markdown("Tool Life Estimation using Taylor Equation and AI")
