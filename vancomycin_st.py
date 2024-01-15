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
    row = st.columns([1, 2])
    crea = row[0].number_input('Serum creatinine', placeholder="umol/L", min_value=5, value=None)
    renal = row[1].checkbox('On continuous haemodialysis')
    weight = form.number_input('Acutal body weight', placeholder="kg", value=None)

    submitted = form.form_submit_button('Submit')

if st.session_state.method == 'Maintainence':
    form = st.form(key="calc")
      
    level = form.number_input('Vanc level', value=15.0)
  
    if st.session_state.route == 'Central':
          infusion = form.select_slider('Current rate', 
                              options=rates['Central'].unique())
        
    if st.session_state.route == 'Peripheral':
          infusion = form.select_slider('Current rate', 
                              options=rates['Peripheral'].unique())    
        
    submitted = form.form_submit_button('Submit')

if not st.session_state.method:
    st.stop()
    
if not submitted:
    st.stop()

#Error checking
if not st.session_state.route:
    st.error('No route selected')
    st.stop()

st.divider()

if st.session_state.method == 'Loading':
    if crea < 20 or crea > 200:
        st.error('Check the creatinine - it is out of a normal range')
    if weight < 40 or weight > 110:
        st.error('Check the weight - it is out of a normal range')

if st.session_state.method == 'Maintainence':
    if level < 7 or level > 35:
        st.error('Check the vancomycin level - it is out of a normal range')




route = st.session_state.route
if route == 'Central':
    route_load_dilution = 'diluted in *100 ml* of 0.9% NaCl or 5% glucose'
    route_renal_start = 'administered at :red[_4.2 ml/hr_] using a *500mg/50ml* concentration' 
    route_start_normal = 'administered at :red[_6.3 ml/hr_] using a *500mg/50ml* concentration' 
if route == 'Peripheral':
    route_load_dilution = 'diluted in *250 ml* of 0.9% NaCl or 5% glucose'
    route_renal_start = 'administered at :red[_8.3 ml/hr_] using a *250mg/50ml* concentration' 
    route_start_normal = 'administered at :red[_12.5 ml/hr_] using a *250mg/50ml* concentration' 

if st.session_state.method == 'Loading':
    with st.container():
        st.write('### Vancomycin :blue[Loading] dose -', route)
        st.divider()
        if renal == True or crea >100:
            st.write('#### :red[*1000 mg*]', route_load_dilution)
        else:
            if weight >= 100:
                st.write('#### :red[*2500 mg*]', route_load_dilution)
            if weight >= 80 and weight < 99:
                st.write('#### :red[*2000 mg*]', route_load_dilution)
            if weight >= 60 and weight < 79:
                st.write('#### :red[*1500 mg*]', route_load_dilution)
            if weight >= 50 and weight < 59:
                st.write('#### :red[*1000 mg*]', route_load_dilution)
            if weight < 50:
                st.write('#### :red[*750 mg*]', route_load_dilution)
        
        st.write('Administered over **2** hours')

        st.write('### Immediately followed by an continuous infusion:')
        if renal == True or crea >100:
            st.write('#### *1 g* over 24 hours', route_renal_start)
        else:
            st.write('#### *1.5 g* over 24 hours', route_start_normal)
    
if st.session_state.method == 'Maintainence':
    with st.container():
        st.write('### Vancomycin :blue[Maintainence] infusion -', route)
        st.write('Target daily level is **20 mg/L**')
        st.write('Do not use if vancomycin started in last **6 hours**')
        st.divider()
        current = rates.index[rates[route]==infusion].tolist()

        if level >= 15 and level <= 25:
            st.write('#### No change - continue current rate')

        if level < 15 and level >= 10:
             if current[0] == 6:
                st.write('#### Already on maximum rate - discuss with pharmacist')
             else:            
                new = current[0] + 1
                st.write('#### Increase daily dose')
                st.write('#### New rate: :red[', rates[route].iloc[new], 'ml/hr]')

        if level > 25 and level < 30:
            if current[0] == 0:
                st.write('#### Already on minimum rate - discuss with pharmacist')
            else:    
                new = current[0] - 1
                st.write('#### Decrease daily dose')
                st.write('#### New rate: :red[', rates[route].iloc[new], 'ml/hr]')
                
        if level >= 30:
                st.write('#### Stop infusion for at least **6 hours**')
                st.write('#### Discuss new rate with pharmacist')
            
        if level < 10:
                st.write('#### Ensure infusion has not started in the last **6 hours**')
                st.write('#### Administer new loading dose')
        
        
        st.write('Ensure daily vancomycin level')

        
                
