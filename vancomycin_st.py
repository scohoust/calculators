import streamlit as st

st.title('Vancomycin calculator')

if 'method' not in st.session_state:
  st.session_state['method'] = 'nil'

st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method")
st.selectbox('Administer by', ('Central', 'Peripheral'), key="route")

form = st.form(key="calc")
crea = form.number_input('Serum creatinine')
renal = form.checkbox('On haemodialysis')

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
