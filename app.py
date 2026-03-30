"""
TPM Molecular Bond Angle Predictor v2
Nicolae Pascal — Independent Researcher, Renazzo (FE), Italy
Phase Framework Series: Riman-10, Riman-14, Riman-15, Riman-27
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# ── CONSTANTS ──────────────────────────────────────────────────────────────
PHI   = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)

# ── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TPM Molecular Predictor",
    page_icon="⚛",
    layout="wide",
)

# ── CORE MATH ──────────────────────────────────────────────────────────────
def tpm_angle(n, N, b=1.0, n_res=0):
    """
    Riman-15 + Riman-27:
      T(n)   = (sqrt5)^(n-1)
      N_eff  = N + (b-1)*n_res/N   [Resonance Rule]
      D      = T / N_eff
      theta  = arccos(1 - D)
    """
    T = SQRT5 ** (n - 1)
    N_eff = N + (b - 1.0) * n_res / N if (b > 1.0 and n_res > 0) else float(N)
    D = T / N_eff
    cos_val = 1.0 - D
    valid = -1.0 <= cos_val <= 1.0
    theta = math.degrees(math.acos(max(-1.0, min(1.0, cos_val)))) if valid else None
    return {"T": T, "N_eff": N_eff, "D": D, "cos": cos_val, "theta": theta, "valid": valid}

# ── MOLECULE DATABASE ──────────────────────────────────────────────────────
MOLECULES = {
    "Water H2O":           {"n":3,"N":4,"b":1.0,"n_res":0, "exp":104.5, "cat":"Validated",
                            "desc":"2 bonds + 2 lone pairs · sp3 · volumetric"},
    "Benzene C-C-C":       {"n":3,"N":3,"b":1.5,"n_res":2, "exp":120.0, "cat":"Validated",
                            "desc":"Pure resonance sp2 · bond order 1.5 · 2 resonant bonds"},
    "SO2":                 {"n":3,"N":3,"b":1.5,"n_res":2, "exp":119.5, "cat":"Validated",
                            "desc":"Resonance + lone pair on S · bond order 1.5"},
    "Cuprate O-Cu-O":      {"n":2,"N":2,"b":1.0,"n_res":0, "exp":97.5,  "cat":"Validated",
                            "desc":"2D planar · Cooper pair geometry · buckling angle CuO2"},
    "Graphene magic angle":{"n":2,"N":2,"b":1.0,"n_res":0, "exp":1.118, "cat":"Validated",
                            "desc":"D = sqrt5/2 projected as twist angle · mode=magic_angle",
                            "mode":"magic_angle"},
    "Ammonia NH3":         {"n":3,"N":4,"b":1.0,"n_res":0, "exp":107.0, "cat":"Approximate",
                            "desc":"3 bonds + 1 lone pair · lone pair steric effect (Riman-28)"},
    "Methane CH4":         {"n":3,"N":4,"b":1.0,"n_res":0, "exp":109.5, "cat":"Approximate",
                            "desc":"4 bonds 0 lone pairs · bond steric effect (Riman-28)"},
    "Ozone O3":            {"n":3,"N":3,"b":1.5,"n_res":2, "exp":116.8, "cat":"Approximate",
                            "desc":"Resonance + lone pair on O · lone pair correction pending"},
    "ClF3":                {"n":3,"N":5,"b":1.0,"n_res":0, "exp":87.5,  "cat":"Approximate",
                            "desc":"5 domains · T-shaped · 3 bonds + 2 lone pairs"},
}

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.title("⚛ TPM Molecular Predictor")
st.sidebar.markdown("**Nicolae Pascal**  \nRenazzo (FE), Italy  \npascalnicolae78@gmail.com")
st.sidebar.divider()
st.sidebar.markdown("### Algorithm (3 steps)")
st.sidebar.latex(r"T(n) = (\sqrt{5})^{n-1}")
st.sidebar.latex(r"N_{eff} = N + \frac{(b-1)\cdot n_{res}}{N}")
st.sidebar.latex(r"\theta = \arccos(1 - \frac{T}{N_{eff}})")
st.sidebar.divider()
st.sidebar.markdown(f"**√5** = {SQRT5:.5f}  (ΔΦ barrier)  \n**φ** = {PHI:.5f}  (non-intersection op)")
st.sidebar.divider()
st.sidebar.markdown("**Riman-10** · Cuprates  \n**Riman-14** · Graphene  \n**Riman-15** · Tension rule  \n**Riman-27** · Resonance correction")

# ── MAIN HEADER ────────────────────────────────────────────────────────────
st.title("⚛ Molecular Bond Angle Predictor")
st.markdown("*Toroidal Phase Metric — molecular geometry from one topological operator: ΔΦ = √5*")
st.divider()

tab1, tab2, tab3 = st.tabs(["📐 Molecule Library", "🔧 Custom Calculator", "📊 Comparison Chart"])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — MOLECULE LIBRARY
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    col_sel, col_res = st.columns([1, 2])

    with col_sel:
        st.subheader("Select")
        filt = st.radio("Filter", ["All", "Validated", "Approximate"], horizontal=True)
        filtered = {k: v for k, v in MOLECULES.items() if filt == "All" or v["cat"] == filt}
        mol_name = st.selectbox("Molecule", list(filtered.keys()), label_visibility="collapsed")
        mol = filtered[mol_name]

        st.info(
            f"**n = {mol['n']}** ({'planar' if mol['n']==2 else 'volumetric'})  \n"
            f"**N = {mol['N']}** electron domains  \n"
            f"**b = {mol['b']}** bond order  \n"
            f"**n_res = {mol['n_res']}** resonant bonds  \n\n"
            f"{mol['desc']}"
        )

    with col_res:
        st.subheader("Step-by-step derivation")

        res = tpm_angle(mol["n"], mol["N"], mol["b"], mol["n_res"])
        mode = mol.get("mode", "standard")
        predicted = res["D"] if mode == "magic_angle" else res["theta"]
        label = f"{predicted:.4f}°" if predicted is not None else "invalid"

        # Display steps
        step1 = f"**Step 1 — Tension:** T({mol['n']}) = (√5)^{mol['n']-1} = **{res['T']:.6f}**"
        if mol["b"] > 1.0:
            step2 = (f"**Step 2 — Resonance (Riman-27):** "
                     f"N_eff = {mol['N']} + ({mol['b']}-1)×{mol['n_res']}/{mol['N']} = **{res['N_eff']:.6f}**")
        else:
            step2 = f"**Step 2 — N_eff:** = {res['N_eff']:.6f} (no resonance)"

        step3 = f"**Step 3 — Phase distance:** D = {res['T']:.6f} / {res['N_eff']:.6f} = **{res['D']:.6f}**"

        if mode == "magic_angle":
            step4 = f"**Step 4 — Magic angle projection:** θ_magic = D = **{res['D']:.4f}°**"
        else:
            step4 = (f"**Step 4 — Bond angle:** cos(θ) = 1 − {res['D']:.6f} = {res['cos']:.6f}  \n"
                     f"θ = arccos({res['cos']:.6f}) = **{label}**")

        for step in [step1, step2, step3, step4]:
            st.markdown(step)

        st.divider()

        # Result metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("TPM Prediction", label)

        exp_v = mol.get("exp")
        if exp_v and predicted:
            err = abs(predicted - exp_v) / exp_v * 100
            m2.metric("Experimental", f"{exp_v}°")
            color_note = "✅ excellent" if err < 1 else "✅ good" if err < 3 else "⚡ approx"
            m3.metric("Deviation", f"{err:.2f}%", delta=color_note, delta_color="off")
        else:
            m2.metric("Experimental", "—")
            m3.metric("Deviation", "—")

        if mol["cat"] == "Validated":
            st.success("✅ Validated — deviation < 3%")
        else:
            st.warning("⚡ Approximate — lone pair steric correction pending (Riman-28)")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — CUSTOM CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Calculate for any molecule")
    st.markdown("Enter parameters — the algorithm is always the same 3 steps.")

    cc1, cc2 = st.columns(2)

    with cc1:
        n_c  = st.radio("**n** — geometry",
                        [2, 3],
                        format_func=lambda x: (
                            "n=2 · planar (2D layer, orbit, surface)" if x == 2
                            else "n=3 · volumetric (3D crystal, nucleus, molecular node)"))
        N_c  = st.number_input("**N** — electron domains (bonds + lone pairs)", 1, 12, 4)
        b_c  = st.number_input("**b** — bond order", 1.0, 3.0, 1.0, 0.5)
        nr_c = 0
        if b_c > 1.0:
            nr_c = st.number_input("**n_res** — resonant bonds", 0, 8, 2)
        lbl_c = st.text_input("Label", "My molecule")
        exp_c = st.number_input("Known experimental angle (°) — optional", 0.0, 180.0, 0.0)

    with cc2:
        res_c = tpm_angle(n_c, N_c, b_c, nr_c)

        if res_c["valid"]:
            st.success(f"### θ = {res_c['theta']:.4f}°")
            st.code(
                f"n       = {n_c}\n"
                f"N       = {N_c}\n"
                f"b       = {b_c}\n"
                f"n_res   = {nr_c}\n"
                f"─────────────────────\n"
                f"T(n)    = (√5)^{n_c-1} = {res_c['T']:.6f}\n"
                f"N_eff   = {res_c['N_eff']:.6f}\n"
                f"D       = {res_c['D']:.6f}\n"
                f"cos(θ)  = {res_c['cos']:.6f}\n"
                f"θ       = {res_c['theta']:.4f}°",
                language="text",
            )
            if exp_c > 0:
                err_c = abs(res_c["theta"] - exp_c) / exp_c * 100
                st.metric("Deviation from experiment", f"{err_c:.2f}%")

            # Gauge chart
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=res_c["theta"],
                number={"suffix": "°", "font": {"size": 40}},
                gauge={
                    "axis": {"range": [0, 180], "tickwidth": 1},
                    "bar": {"color": "#0096c7", "thickness": 0.25},
                    "bgcolor": "white",
                    "steps": [
                        {"range": [0, 90],   "color": "#caf0f8"},
                        {"range": [90, 120], "color": "#90e0ef"},
                        {"range": [120,180], "color": "#48cae4"},
                    ],
                    "threshold": {
                        "line": {"color": "#d62828", "width": 3},
                        "value": res_c["theta"],
                    },
                },
                title={"text": lbl_c},
            ))
            fig_g.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_g, use_container_width=True)
        else:
            st.error(f"cos(θ) = {res_c['cos']:.4f} is outside [−1, 1]. Adjust parameters.")

    # Sweep chart
    st.divider()
    st.subheader(f"Angle vs N  (n={n_c}, b={b_c})")
    N_vals = list(range(1, 13))
    a_vals = []
    for Nv in N_vals:
        rv = tpm_angle(n_c, Nv, b_c, min(nr_c, Nv))
        a_vals.append(rv["theta"])

    fig_sw = go.Figure(go.Scatter(
        x=N_vals, y=a_vals, mode="lines+markers",
        line=dict(color="#0096c7", width=2),
        marker=dict(size=9, color="#d62828", symbol="circle"),
    ))
    fig_sw.update_layout(
        xaxis_title="N (electron domains)",
        yaxis_title="θ (degrees)",
        height=300,
        margin=dict(l=50, r=20, t=10, b=50),
    )
    st.plotly_chart(fig_sw, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — COMPARISON CHART
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("TPM vs Experimental — all molecules")

    rows = []
    for name, mol in MOLECULES.items():
        res = tpm_angle(mol["n"], mol["N"], mol["b"], mol["n_res"])
        mode = mol.get("mode", "standard")
        pred = res["D"] if mode == "magic_angle" else res["theta"]
        exp_v = mol.get("exp")
        err = abs(pred - exp_v) / exp_v * 100 if (pred and exp_v) else None
        short = name.split(" ")[0] + (" " + name.split(" ")[1] if len(name.split(" ")) > 1 else "")
        rows.append({"name": short, "pred": pred, "exp": exp_v, "err": err, "cat": mol["cat"]})

    names  = [r["name"]  for r in rows]
    preds  = [r["pred"]  for r in rows]
    exps   = [r["exp"]   for r in rows]
    errs   = [r["err"]   for r in rows]
    bar_colors = ["#0096c7" if r["cat"] == "Validated" else "#f4a261" for r in rows]

    fig3 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            "Bond angles — TPM (blue/orange) vs Experimental (red)",
            "Deviation %  (green line = 2% threshold)"
        ),
        vertical_spacing=0.2,
    )
    fig3.add_trace(go.Bar(name="TPM", x=names, y=preds,
                          marker_color=bar_colors, opacity=0.85), row=1, col=1)
    fig3.add_trace(go.Bar(name="Experimental", x=names, y=exps,
                          marker_color="#d62828", opacity=0.55), row=1, col=1)
    fig3.add_trace(go.Bar(name="Error %", x=names, y=errs,
                          marker_color=bar_colors, showlegend=False), row=2, col=1)
    fig3.add_hline(y=2, row=2, col=1,
                   line=dict(color="green", dash="dash", width=1.5),
                   annotation_text="2%", annotation_font_color="green")

    fig3.update_layout(
        height=540, barmode="group",
        margin=dict(l=50, r=20, t=60, b=60),
        legend=dict(orientation="h", y=1.06),
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Summary stats
    valid_errs = [e for e in errs if e is not None]
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Molecules tested", len(rows))
    s2.metric("Error < 1%",  f"{sum(1 for e in valid_errs if e < 1)}/{len(valid_errs)}")
    s3.metric("Error < 3%",  f"{sum(1 for e in valid_errs if e < 3)}/{len(valid_errs)}")
    s4.metric("Avg deviation", f"{sum(valid_errs)/len(valid_errs):.2f}%")

    st.divider()
    st.markdown("""
**Status after Riman-27 (Resonance Rule):**

| Issue | Before | After |
|---|---|---|
| SO₂ | 10.3% error | **0.42%** ✅ |
| Benzene | 10% error | **0.00%** ✅ exact |
| O₃ | 13% error | **2.74%** ⚡ |

**Still open — Riman-28 (Lone Pair Correction):**
- NH₃ 2.4% · O₃ 2.7% · CH₄ 4.6%
- Pattern: molecules with lone pairs on central atom have slight angle compression.
- The algebra is the next step.

**Zero empirical parameters.** All results from T(n) = (√5)^(n-1) and one resonance rule.
""")

# ── FOOTER ────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Phase Framework Series (Riman-10 · Riman-14 · Riman-15 · Riman-27) · "
    "Nicolae Pascal · Independent Researcher · Renazzo (FE) Italy · "
    "pascalnicolae78@gmail.com"
        )
