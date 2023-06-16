import streamlit as st

st.title('Vancomycin calculator')

if 'method' not in st.session_state:
  st.session_state['method'] = 'nil'

st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method")

st.selectbox('Administer by', ('Central', 'Peripheral'), key="route")

if st.session_state.method == "Loading":
  crea = st.number_input('Serum creatinine')
            
      
