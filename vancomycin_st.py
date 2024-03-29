import streamlit as st
import pandas as pd

data = {
    'Central': ['1.1', '2.1', '4.2', '6.3', '8.3', '10.4', '13', '15'],
    'Peripheral': ['2.1', '4.2', '8.3', '13', '17', '21', '25', '29']
}

rates = pd.DataFrame(data)


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
    crea = form.number_input('Serum creatinine', placeholder="umol/L", min_value=5, value=None)
    renal = form.checkbox('On continuous haemodialysis')
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
    with st.container():
        st.write('### Vancomycin *Loading* dose -', route)
        if renal == True or crea > 100:
            st.info('#### :red[*1000 mg*]')
        else:
            if weight >= 100:
                st.info('#### :red[*2500 mg*]')
            if weight >= 80 and weight < 99:
                st.info('#### :red[*2000 mg*]')
            if weight >= 60 and weight < 79:
                st.info('#### :red[*1500 mg*]')
            if weight >= 50 and weight < 59:
                st.info('#### :red[*1000 mg*]')
            if weight < 50:
                st.info('#### :red[*750 mg*]')
        
        #st.write('Administered over **2** hours')

        st.write('#### Immediately followed by an continuous infusion:')
        if renal == True or crea >100:
            st.info(f'#### *1000 mg* over 24 hours {route_renal_start}')
        else:
            st.info(f'#### *1500 mg* over 24 hours {route_start_normal}')
    
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
        
    

        
                
