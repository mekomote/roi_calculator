import streamlit as st

# Custom CSS to change slider, text, and bar colors
st.markdown("""
    <style>
    /* Slider color */
    .stSlider > div > div > div > div {
        background: #205587;
    }

    /* Text color */
    .css-1cp3ece p, .css-1cpxqw2 h1, .css-1cpxqw2 h2, .css-1cpxqw2 h3 {
        color: #205587;
    }

    /* Metric text color */
    .css-1v0mbdj {
        color: #205587 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Lifemote RoI Calculator")

# Input Sliders
cases_per_month = st.slider("Cases per month", 1000, 100000, 10000, step=1000)
call_cost_per_hour = st.slider("Call cost per hour (€)", 5, 100, 25)
aht_baseline = st.slider("Baseline AHT (minutes)", 5, 60, 20)
aht_improved = st.slider("Improved AHT (minutes)", 5, 60, 15)
fcr_baseline = st.slider("Baseline FCR (%)", 0, 100, 60)
fcr_improved = st.slider("Improved FCR (%)", 0, 100, 70)
truck_roll_percentage_baseline = st.slider("Baseline Truck Roll (%)", 0, 100, 15)
truck_roll_percentage_improved = st.slider("Improved Truck Roll (%)", 0, 100, 10)
truck_roll_cost = st.slider("Truck Roll Cost (€)", 50, 500, 150)

# Function Definitions
def calculate_call_deflections_savings(reduced_cases, call_cost, aht):
    return reduced_cases * (call_cost * (aht / 60))

def calculate_aht_improvement_savings(cases, baseline_aht, improved_aht, call_cost):
    return cases * call_cost * ((baseline_aht - improved_aht) / 60)

def calculate_fcr_improvement_savings(cases, baseline_fcr, improved_fcr, call_cost, aht):
    reduced_repeat_cases = cases * (improved_fcr - baseline_fcr) / 100
    return reduced_repeat_cases * (call_cost * (aht / 60))

def calculate_truck_roll_reduction_savings(cases, baseline_percentage, improved_percentage, roll_cost):
    reduced_truck_rolls = cases * (baseline_percentage - improved_percentage) / 100
    return reduced_truck_rolls * roll_cost

# Call Deflections Savings: Assuming 10% of cases are deflected
call_deflections_savings = calculate_call_deflections_savings(
    cases_per_month * 0.10, call_cost_per_hour, aht_baseline
)

# Other Savings
aht_improvement_savings = calculate_aht_improvement_savings(
    cases_per_month, aht_baseline, aht_improved, call_cost_per_hour
)

fcr_improvement_savings = calculate_fcr_improvement_savings(
    cases_per_month, fcr_baseline, fcr_improved, call_cost_per_hour, aht_baseline
)

truck_roll_reduction_savings = calculate_truck_roll_reduction_savings(
    cases_per_month, truck_roll_percentage_baseline, truck_roll_percentage_improved, truck_roll_cost
)

# Total Savings
total_savings = (call_deflections_savings + aht_improvement_savings +
                 fcr_improvement_savings + truck_roll_reduction_savings)

# Display Results
st.subheader("Savings Breakdown")
st.write(f"Call Deflections Savings: €{call_deflections_savings:,.2f}")
st.write(f"AHT Improvement Savings: €{aht_improvement_savings:,.2f}")
st.write(f"FCR Improvement Savings: €{fcr_improvement_savings:,.2f}")
st.write(f"Truck Roll Reduction Savings: €{truck_roll_reduction_savings:,.2f}")
st.subheader("Total Savings")
st.metric(label="Total Savings (€)", value=f"€{total_savings:,.2f}")
