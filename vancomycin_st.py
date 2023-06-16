import streamlit as st

st.title('Vancomycin calculator')

if 'method' not in st.session_state:
  st.session_state['method'] = 'nil'

st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method")
st.selectbox('Administer by', ('Central', 'Peripheral'), key="route")

crea = st.number_input('Serum creatinine')

if st.session_state.method == 'Maintainence':
  level = st.number_input('Vanc level')
  
  if st.session_state.route == 'Central':
      infusion = st.select_slider('Current rate', 
                              options=['1.1', '2.2', '4.2', '6.3', '8.3', '10.4', '12.5'])
            
      
