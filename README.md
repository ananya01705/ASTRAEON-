# SPHEREx Signal Lab

**See what changed. Understand why. Investigate the evidence.**

SPHEREx Signal Lab is an early-stage, explainable exploration tool for searching real SPHEREx observations from NASA/IPAC's Infrared Science Archive (IRSA), inspecting observation metadata, and checking whether compatible observations exist for a future time-domain comparison workflow.

## Current development stage

This repository begins with a deliberately small feasibility MVP:

1. Search SPHEREx DR1 and QR3 observations around a sky position.
2. Display returned observation metadata.
3. Inspect whether the search returned more than one observation and identify possible follow-up analysis targets.

Image alignment, difference imaging, source detection, spectral analysis, and candidate scoring are **not implemented yet**. They will be added only after real data retrieval and FITS inspection have been tested.

## Data source

- SPHEREx archive at NASA/IPAC Infrared Science Archive (IRSA)
- SIA2 endpoint: https://irsa.ipac.caltech.edu/SIA
- Initial collections: `spherex_dr1` and `spherex_qr3`

The app queries public archive metadata. It does not claim to discover Planet X or classify astronomical objects.

## Run locally

Python 3.11 is recommended.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Current status

- [x] Repository initialized
- [ ] Verify IRSA query from the local environment
- [ ] Confirm a sky region with multiple compatible observations
- [ ] Download and inspect a real FITS product
- [ ] Add scientifically valid temporal comparison

## Scientific caution

A result count greater than one does not automatically mean that two observations are scientifically comparable. Collection, product type, bandpass, time, quality information, and image characteristics must be checked before any temporal analysis.

## Acknowledgement

This project uses publicly available SPHEREx data served by NASA/IPAC IRSA. Follow the archive's current acknowledgement and citation requirements when using released data products.

## License

MIT
