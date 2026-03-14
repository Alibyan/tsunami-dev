"""Minimal Streamlit demo scaffold for Phase 00."""
import streamlit as st
from src.cache import create_db


st.title("Offshore Quake & Tsunami Triage — Scaffold")
st.markdown("This is a minimal scaffold. Populate the DB via `ingest_usgs.py` and then implement UI panels.")

if st.button("Ensure local DB"):
    path = create_db()
    st.success(f"Created SQLite DB at {path}")
