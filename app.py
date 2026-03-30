"""TPM Core Math — Phase Framework Series, Riman-27"""
import math

PHI  = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)

def tpm_tension(n):
    return SQRT5 ** (n - 1)

def tpm_angle(n, N, b=1.0, n_res=0):
    """
    Full TPM bond angle with Resonance Rule (Riman-27).
    N_eff = N + (b-1)*n_res/N  if b > 1
    """
    steps = []
    T = tpm_tension(n)
    steps.append(f"T(n) = (√5)^({n}−1) = {T:.6f}")

    # Resonance correction
    if b > 1.0 and n_res > 0:
        delta = (b - 1.0) * n_res / N
        N_eff = N + delta
        steps.append(f"Resonance: N_eff = {N} + ({b}−1)×{n_res}/{N} = {N_eff:.6f}")
    else:
        N_eff = float(N)
        steps.append(f"N_eff = {N_eff:.6f} (no resonance correction)")

    D = T / N_eff
    steps.append(f"D = T/N_eff = {T:.6f}/{N_eff:.6f} = {D:.6f}")

    cos_val = 1.0 - D
    cos_clamped = max(-1.0, min(1.0, cos_val))
    theta = math.degrees(math.acos(cos_clamped))
    steps.append(f"cos(θ) = 1−D = {cos_val:.6f}  →  θ = {theta:.4f}°")

    return {
        "T": T, "N_eff": N_eff, "D": D,
        "cos_theta": cos_val, "theta_deg": theta,
        "valid": -1.0 <= cos_val <= 1.0,
        "steps": steps,
    }
  
