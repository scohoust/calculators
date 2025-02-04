import streamlit as st
import pandas as pd

data = {
    'Central': ['1.1', '2.1', '3.1', '4.2', '6.3', '8.3', '10.4', '13', '15'],
    'Peripheral': ['2.1', '4.2', '6.2', '8.3', '13', '17', '21', '25', '29']
}

rates = pd.DataFrame(data)

def get_vanco_parameters(crcl, is_cv=False):
    """
    Returns a dictionary with the appropriate vancomycin dosing parameters
    based on the patient's creatinine clearance (crcl) and whether they are on
    continuous renal replacement therapy (is_cv).
    
    The returned dictionary contains:
      - 'dose': The approximate 24-hour vancomycin dose in mg.
      - 'central_rate': The infusion pump rate (mL/hr) for Central administration.
      - 'peripheral_rate': The infusion pump rate (mL/hr) for Peripheral administration.
    """
    if is_cv:  # Patient is on CVVHD/CVVHDF
        return {"dose": 1000, "central_rate": 4.2, "peripheral_rate": 8.3}
    
    # Use the CrCl ranges from your table
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
    else:  # crcl < 20
        return {"dose": 250, "central_rate": 1.1, "peripheral_rate": 2.1}


st.title('Continuous Vancomycin calculator')

css = r'''
    <style>
        [data-testid="stForm"] {border: 0px; padding: inherit;}
        hr { margin: 0px; } 
        div[class="starkdown"]  {
        padding: 5px; border: 1px; border-color: #000; border-style: solid; background-color: #fcb900;
        }
    </style>
'''

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
st.markdown(css, unsafe_allow_html=True)

with st.sidebar:
    st.header("Dose calculator")
    st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method", index=None, placeholder="Start here")
    st.selectbox('Route of administration', ('Central', 'Peripheral'), key="route", index=None, placeholder="Route")


if st.session_state.method == 'Loading':
    form = st.form(key="calc")
    age = form.number_input('Age', placeholder="", min_value=16, value=None)
    sex = form.selectbox('Sex', ('Male', 'Female'))
    crea = form.number_input('Serum creatinine', placeholder="umol/L", min_value=5, value=None)
    renal = form.checkbox('On continuous renal replacement (CVVHD/CVVHF)')
    weight = form.number_input('Acutal body weight', placeholder="kg", value=None)
    

    submitted = form.form_submit_button('Submit')

if st.session_state.method == 'Maintainence':
    form = st.form(key="calc")
      
    level = form.number_input('Vanc level', value=None, placeholder="mg/L", step=1e-1)
  
    if st.session_state.route == 'Central':
          infusion = form.select_slider('Current rate (ml/hr)', 
                              options=rates['Central'].unique())
        
    if st.session_state.route == 'Peripheral':
          infusion = form.select_slider('Current rate (ml/hr)', 
                              options=rates['Peripheral'].unique())    
        
    submitted = form.form_submit_button('Submit')

if not st.session_state.method:
    st.stop()
    
if not submitted:
    st.stop()

#Error checking
if not st.session_state.route:
    st.divider()
    st.error('No route selected')
    st.stop()


if st.session_state.method == 'Loading':
    if crea == None:
        st.divider()
        st.error('No creatinine entered')
        st.stop()

    if weight == None:
        st.divider()
        st.error('No weight entered')
        st.stop()
            
    if age == None:
        st.divider()
        st.error('No age entered')
        st.stop()
        
    if age < 18 or age > 80:
        st.error('Check the age - it is out of a normal range')
        st.divider()
               
    if crea < 20 or crea > 200:
        st.error('Check the creatinine - it is out of a normal range')
        st.divider()
        
    if weight < 40 or weight > 110:
        st.error('Check the weight - it is out of a normal range')
        st.divider()

if st.session_state.method == 'Maintainence':
    if level == None:
        st.divider()
        st.error('No vancomycin level entered')
        st.stop()
        
    if level < 7 or level > 35:
        st.error('Check the vancomycin level - it is out of a normal range')
        st.divider()


route = st.session_state.route
if route == 'Central':
    route_load_dilution = ''
    route_renal_start = 'administered at :red[_4.2 ml/hr_] using a *500mg/50ml* concentration' 
    route_start_normal = 'administered at :red[_6.3 ml/hr_] using a *500mg/50ml* concentration' 
if route == 'Peripheral':
    route_load_dilution = ''
    route_renal_start = 'administered at :red[_8.3 ml/hr_] using a *250mg/50ml* concentration' 
    route_start_normal = 'administered at :red[_12.5 ml/hr_] using a *250mg/50ml* concentration' 

if st.session_state.method == 'Loading':
    
    crcl = ((140 - age) * weight) / crea
    if sex == 'Male':
        crcl = crcl * 1.23
    else:
        crcl = crcl * 1.04

    vanco_params = get_vanco_parameters(crcl, is_cv=renal)

   
    with st.container():
        st.write('### Vancomycin *Loading* dose -', route)
        if weight >= 140:
            st.info('#### :red[*3000 mg*]')
            st.write('#### And please inform pharmacy team')
        if weight >= 110 and weight < 139:
            st.info('#### :red[*3000 mg*]')
        if weight >= 100 and weight < 110:
            st.info('#### :red[*2750 mg*]')
        if weight >= 90 and weight < 99:
            st.info('#### :red[*2500 mg*]')
        if weight >= 80 and weight < 89:
            st.info('#### :red[*2250 mg*]')
        if weight >= 65 and weight < 79:
            st.info('#### :red[*2000 mg*]')
        if weight >= 60 and weight < 64:
            st.info('#### :red[*1750 mg*]')
        if weight >= 55 and weight < 59:
            st.info('#### :red[*1500 mg*]')
        if weight >= 50 and weight < 54:
            st.info('#### :red[*1250 mg*]')    
        if weight < 50:
            st.info('#### :red[*1000 mg*]')
        
        #st.write('Administered over **2** hours')

        
        st.write('#### Immediately followed by an continuous infusion:')
        st.info(f'Crea Cl: {crcl}')
        st.info(f"Approximate 24-hour vancomycin dose: {vanco_params['dose']} mg")
          
        route = st.session_state.route
        if route == 'Central':
            st.info(f"#### *{vanco_params['dose']} mg* over 24 hours \n #### :red[{vanco_params['central_rate']}] mL/hr using a 500mg/50mL concentration")
        elif route == 'Peripheral':
            st.info(f"Recommended infusion rate: {vanco_params['peripheral_rate']} mL/hr using a 250mg/50mL concentration")
            
    
if st.session_state.method == 'Maintainence':
    with st.container():
        st.write('### Vancomycin *Maintainence* infusion -', route)
        st.write('Target daily level is **20 mg/L**. Do not adjust if vancomycin started in last **6 hours**')
        st.divider()
        current = rates.index[rates[route]==infusion].tolist()

        if level >= 15 and level <= 25:
            st.info('#### No change - continue current rate')

        if level < 15 and level >= 10:
             if current[0] == 7:
                st.info('#### Already on maximum rate - discuss with pharmacist')
             else:            
                new = current[0] + 1
                st.info(f'#### Increase daily dose\n #### New rate: :red[ {rates[route].iloc[new]} ml/hr]')

        if level > 25 and level < 30:
            if current[0] == 0:
                st.info('#### Already on minimum rate - discuss with pharmacist')
            else:    
                new = current[0] - 1
                st.info(f'#### Decrease daily dose\n #### New rate: :red[ {rates[route].iloc[new]} ml/hr]')
                
        if level >= 30:
                st.info('#### Stop infusion for at least **6 hours**\n #### Consider repeat sample \n #### Discuss new rate with pharmacist')
                
        if level < 10:
                new = current[0] + 2
                st.info(f'#### Ensure infusion has not started in the last **6 hours** \n #### Administer :red[*1000 mg*] bolus AND increase daily dose\n #### New rate: :red[ {rates[route].iloc[new]} ml/hr]')
        
    

