import streamlit as st

st.title('Vancomycin calculator')

css = r'''
    <style>
        [data-testid="stForm"] {border: 0px; padding: inherit;}
    </style>
'''

st.markdown(css, unsafe_allow_html=True)
    
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

if st.session_state.method == 'Loading':
    st.title('Vancomycin :blue[Loading] dose - '. st.session_state['route'])
    st.divider();
    if renal == True or crea >100:
        st.write('**750 mg**')
        st.write('Administered over 2 hours')
    
             
