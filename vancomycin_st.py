import streamlit as st

st.title('Vancomycin calculator')

if 'method' not in st.session_state:
  st.session_state['method'] = 'nil'

st.selectbox('Calculate which dose', ('Loading', 'Maintainence'), key="method")


            
      
