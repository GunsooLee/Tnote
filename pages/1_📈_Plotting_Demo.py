import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Word Cloude")
st.sidebar.header("워드클라우드 결과")
st.write(
    """워드클라우드 결과입니다."""
)
display_word_cloud(result)
