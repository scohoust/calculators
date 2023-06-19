import streamlit as st

st.title('Vancomycin calculator')

css = r'''
    <style>
        [data-testid="stForm"] {border: 0px; padding: inherit;}
        .result { background-colour: #fcb900; }
    </style>
'''

st.markdown(css, unsafe_allow_html=True)
    
st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method")
st.selectbox('Administer by', ('Central', 'Peripheral'), key="route")

form = st.form(key="calc")
crea = form.number_input('Serum creatinine')
renal = form.checkbox('On haemodialysis')

if st.session_state.method == 'Loading':
  weight = form.number_input('Acutal body weight')

if st.session_state.method == 'Maintainence':
  level = form.number_input('Vanc level')
  
  if st.session_state.route == 'Central':
      infusion = form.select_slider('Current rate', 
                              options=['1.1', '2.2', '4.2', '6.3', '8.3', '10.4', '12.5'])
  if st.session_state.route == 'Peripheral':
      infusion = form.select_slider('Current rate', 
                              options=['2.1', '4.2', '8.3', '12.5', '16.7', '20.8', '25.0'])            
      
submitted = form.form_submit_button('Submit')

if not submitted:
  st.stop();



st.write('Successfully submitted!')

st.divider()

route = st.session_state.route
if route == 'Central':
    route_load_dilution = 'diluted in *100 ml* of 0.9% NaCl or 5% glucose'
if route == 'Peripheral':
    route_load_dilution = 'diluted in *250 ml* of 0.9% NaCl or 5% glucose'

if st.session_state.method == 'Loading':
    st.markdown('<div class="result">)
    st.write('## Vancomycin :blue[Loading] dose -', route)
    st.divider()
    if renal == True or crea >100:
        st.write('### *750 mg*', route_load_dilution)
    else:
        if weight >= 70:
            st.write('### *1.25 g*', route_load_dilution)
        if weight >= 50 and weight < 70:
            st.write('### *1 g*', route_load_dilution)
        if weight < 50:
            st.write('### *750 mg*', route_load_dilution)
        
    st.write('Administered over **2** hours')

    st.markdown('</div')
             
