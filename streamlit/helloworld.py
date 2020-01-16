import streamlit as st
import numpy as np
import pandas as pd

st.title("my first app")

x = st.slider("x")
y = x + 3
y
