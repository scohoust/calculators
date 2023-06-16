import streamlit as st

st.title('Vancomycin calculator')

if 'method' not in st.session_state:
  st.session_state['method'] = 'nil'
  st.button('Loading', key="method")
  st.button('Maintainence', key="method"  
else
  st.write(st.session_state.method)
            
            
      
