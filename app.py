"""Streamlit entry point for SPHEREx Signal Lab."""

import streamlit as st

from src.data_access.irsa_client import IRSAQueryError
from src.data_access.observation_search import search_spherex_observations

st.set_page_config(page_title="SPHEREx Signal Lab", page_icon="🔭", layout="wide")

st.title("🔭 SPHEREx Signal Lab")
st.caption("See what changed. Understand why. Investigate the evidence.")
st.markdown(
    "Search public SPHEREx archive metadata around a sky position. This first "
    "version focuses on data access and feasibility; it does not yet detect "
    "transients or classify astronomical sources."
)

with st.sidebar:
    st.header("Sky region")
    ra = st.number_input("Right ascension (degrees)", 0.0, 360.0, 180.0, 0.01, format="%.5f")
    dec = st.number_input("Declination (degrees)", -90.0, 90.0, 0.0, 0.01, format="%.5f")
    radius_arcmin = st.slider("Search radius (arcminutes)", 1, 60, 5)
    collections = st.multiselect(
        "SPHEREx collections",
        ["spherex_dr1", "spherex_qr3"],
        default=["spherex_dr1", "spherex_qr3"],
    )
    search_clicked = st.button("Search observations", type="primary", use_container_width=True)

st.subheader("Archive search")
st.write(f"Search centre: RA **{ra:.5f}°**, Dec **{dec:.5f}°** · Radius: **{radius_arcmin} arcmin**")

if search_clicked:
    st.session_state.pop("spherex_results", None)
    if not collections:
        st.warning("Select at least one SPHEREx collection.")
    else:
        with st.spinner("Querying NASA/IPAC IRSA..."):
            try:
                st.session_state["spherex_results"] = search_spherex_observations(
                    ra_deg=ra,
                    dec_deg=dec,
                    radius_arcmin=float(radius_arcmin),
                    collections=collections,
                )
            except (IRSAQueryError, ValueError) as exc:
                st.error("The archive query could not be completed.")
                st.exception(exc)
            except Exception as exc:
                st.error("An unexpected error occurred during the archive query.")
                st.exception(exc)

results = st.session_state.get("spherex_results")
if results is not None:
    st.divider()
    st.subheader("Search results")
    if results.empty:
        st.info("No observations were returned. Try another sky position or a larger search radius.")
    else:
        st.metric("Rows returned by archive", len(results))
        st.dataframe(results, use_container_width=True, hide_index=True)
        st.warning(
            "More than one returned row does not automatically mean the observations "
            "are scientifically comparable. Product type, bandpass, epoch, quality "
            "information, and image characteristics must be checked first."
        )
        st.download_button(
            "Download results as CSV",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name="spherex_observation_search.csv",
            mime="text/csv",
        )

st.divider()
st.caption(
    "Data source: NASA/IPAC Infrared Science Archive (IRSA). "
    "A metadata search alone does not establish scientific comparability."
)
