# tpm-molecular-predictor
# TPM Molecular Bond Angle Predictor

**Toroidal Phase Metric — Phase Framework Series**  
Nicolae Pascal · Independent Researcher · Renazzo (FE), Italy  
pascalnicolae78@gmail.com

---

## What this is

A molecular geometry predictor based on a single topological formula.
Bond angles of molecules are derived from two parameters:

- **n** — dimensional geometry (2=planar, 3=volumetric)
- **N** — number of electron domains

**Core algorithm (3 steps):**
```
T(n) = (√5)^(n-1)     dimensional tension
D    = T(n) / N        phase distance
θ    = arccos(1 − D)   bond angle
```

No empirical parameters. No fitting. Pure geometry.

## Validated results

| Molecule          | TPM (°)  | Experimental (°) | Error   |
|-------------------|----------|------------------|---------|
| Water H₂O         | 104.48   | 104.5            | < 0.1%  |
| Ammonia NH₃        | 104.48   | 107.0            | 2.4%    |
| Methane CH₄        | 104.48   | 109.5            | 4.6%    |
| Cuprate O-Cu-O     | 96.77    | 95–100           | < 2%    |
| Graphene twist     | 1.118°   | 1.05–1.16°       | < 2%    |

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repo → `app.py`
4. Deploy

## Theory

Based on the Phase Framework Series (Riman-1 through Riman-26):
- Riman-10: Cuprate superconductors, Cooper pair angle 96.77°
- Riman-11: Room-temperature superconductivity prediction (72°)
- Riman-14: Twisted graphene magic angle 1.118°
- Riman-15: Dimensional Tension Rule T(n) = (√5)^(n-1)

Preprints: [Zenodo — Nicolae Pascal](https://zenodo.org)
