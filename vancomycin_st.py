import streamlit as st
import pandas as pd

# --------------------------
# Data and Global Functions
# --------------------------
data = {
    'Central': [1.1, 2.1, 3.1, 4.2, 6.3, 8.3, 10.4, 13, 15],
    'Peripheral': [2.1, 4.2, 6.2, 8.3, 13, 17, 21, 25, 29]
}
rates = pd.DataFrame(data)

def get_vanco_parameters(crcl, is_cv=False):
    if is_cv:
        return {"dose": 1000, "central_rate": 4.2, "peripheral_rate": 8.3}
    if crcl > 110:
        return {"dose": 3000, "central_rate": 13, "peripheral_rate": 25}
    elif 90 <= crcl <= 100:
        return {"dose": 2500, "central_rate": 10.4, "peripheral_rate": 21}
    elif 75 <= crcl <= 89:
        return {"dose": 2000, "central_rate": 8.3, "peripheral_rate": 17}
    elif 50 <= crcl <= 74:
        return {"dose": 1500, "central_rate": 6.3, "peripheral_rate": 13}
    elif 40 <= crcl <= 49:
        return {"dose": 1000, "central_rate": 4.2, "peripheral_rate": 8.3}
    elif 30 <= crcl <= 39:
        return {"dose": 750, "central_rate": 3.1, "peripheral_rate": 6.2}
    elif 20 <= crcl <= 29:
        return {"dose": 500, "central_rate": 2.1, "peripheral_rate": 4.2}
    else:
        return {"dose": 250, "central_rate": 1.1, "peripheral_rate": 2.1}

def calculate_loading_dose(age, sex, crea, weight, renal):
    # Calculate CrCl using the Cockcroft–Gault formula:
    crcl = ((140 - age) * weight) / crea
    crcl *= 1.23 if sex == 'Male' else 1.04
    return get_vanco_parameters(crcl, is_cv=renal)

def adjust_maintenance_rate(rates, route, current_rate, level):
    # Find the current index in the DataFrame's column for the route.
    current_index = rates.index[rates[route] == current_rate].tolist()[0]
    if 15 <= level <= 25:
        return current_rate, 'No change'
    elif level < 15:
        new_index = min(current_index + 1, len(rates[route]) - 1)
        return rates[route].iloc[new_index], 'Increase dose'
    elif level > 25:
        new_index = max(current_index - 1, 0)
        return rates[route].iloc[new_index], 'Decrease dose'

def validate_input(value, name, min_val, max_val):
    if value is None:
        st.error(f'No {name} entered')
        st.stop()
    if not (min_val <= value <= max_val):
        st.error(f'Check the {name} - it is out of a normal range ({min_val} to {max_val})')

# --------------------------
# Define Helper Functions for Forms
# --------------------------
def loading_form():
    form = st.form(key="loading_form")
    age = form.number_input('Age', min_value=16, value=None, help="Enter the patient's age")
    sex = form.selectbox('Sex', ('Male', 'Female'))
    crea = form.number_input('Serum creatinine (umol/L)', min_value=5, value=None, help="Enter the serum creatinine in umol/L")
    renal = form.checkbox('On continuous renal replacement (CVVHD/CVVHF)')
    weight = form.number_input('Actual body weight (kg)', min_value=1, value=None, help="Enter the actual body weight in kg")
    submitted = form.form_submit_button('Submit')
    return submitted, age, sex, crea, renal, weight

def maintenance_form(rates, route):
    form = st.form(key="maintenance_form")
    level = form.number_input('Vancomycin level (mg/L)', value=None, placeholder="mg/L", step=1e-1)
    if route == 'Central':
        infusion = form.select_slider('Current rate (ml/hr)', options=rates['Central'].unique())
    else:
        infusion = form.select_slider('Current rate (ml/hr)', options=rates['Peripheral'].unique())
    submitted = form.form_submit_button('Submit')
    return submitted, level, infusion

# --------------------------
# Styling and Sidebar
# --------------------------
st.title('Continuous Vancomycin Calculator')

css = r'''
    <style>
        [data-testid="stForm"] {border: 0; padding: inherit;}
        hr { margin: 0; } 
        div[class="starkdown"] {
            padding: 5px; border: 1px solid #000; background-color: #fcb900;
        }
    </style>
'''
hide_default_format = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)
st.markdown(css, unsafe_allow_html=True)

with st.sidebar:
    st.header("Dose Calculator")
    method = st.selectbox('Calculate which dose', ('Loading', 'Maintenance'), key="method", placeholder="Start here")
    route = st.selectbox('Route of administration', ('Central', 'Peripheral'), key="route", placeholder="Route")

# --------------------------
# Main Flow
# --------------------------
if method == 'Loading':
    submitted, age, sex, crea, renal, weight = loading_form()
    if not submitted:
        st.stop()
    validate_input(age, "age", 18, 80)
    validate_input(crea, "creatinine", 20, 200)
    validate_input(weight, "weight", 40, 110)
    
    vanco_params = calculate_loading_dose(age, sex, crea, weight, renal)
    with st.container():
        st.write('### Vancomycin *Loading* Dose -', route)
        # Here you can include your weight-based loading dose recommendations:
        if weight >= 140:
            st.info('#### :red[*3000 mg*]')
            st.write('#### And please inform pharmacy team')
        elif weight >= 110 and weight < 139:
            st.info('#### :red[*3000 mg*]')
        elif weight >= 100 and weight < 110:
            st.info('#### :red[*2750 mg*]')
        elif weight >= 90 and weight < 99:
            st.info('#### :red[*2500 mg*]')
        elif weight >= 80 and weight < 89:
            st.info('#### :red[*2250 mg*]')
        elif weight >= 65 and weight < 79:
            st.info('#### :red[*2000 mg*]')
        elif weight >= 60 and weight < 64:
            st.info('#### :red[*1750 mg*]')
        elif weight >= 55 and weight < 59:
            st.info('#### :red[*1500 mg*]')
        elif weight >= 50 and weight < 54:
            st.info('#### :red[*1250 mg*]')
        else:
            st.info('#### :red[*1000 mg*]')
            
        st.write('#### Immediately followed by a continuous infusion:')
        if route == 'Central':
            st.info(f"#### *{vanco_params['dose']} mg* over 24 hours \n#### :red[{vanco_params['central_rate']} mL/hr] using a 500mg/50mL concentration")
        else:
            st.info(f"#### *{vanco_params['dose']} mg* over 24 hours \n#### :red[{vanco_params['peripheral_rate']} mL/hr] using a 250mg/50mL concentration")

elif method == 'Maintenance':
    submitted, level, infusion = maintenance_form(rates, route)
    if not submitted:
        st.stop()
    validate_input(level, "vancomycin level", 7, 35)
    
    with st.container():
        st.write('### Vancomycin *Maintenance* Infusion -', route)
        st.write('Target daily level is **20 mg/L**. Do not adjust if vancomycin started in the last **6 hours**')
        st.divider()
        new_rate, guidance = adjust_maintenance_rate(rates, route, infusion, level)
        if guidance == 'No change':
            st.info('#### No change - continue current rate')
        else:
            st.info(f'#### {guidance}\n#### New rate: :red[{new_rate} mL/hr]')
