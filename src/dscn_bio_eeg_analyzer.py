"""
==============================================================================
DSCN-G-BIO EXPERIMENTAL SCRIPT v5.0: THE THREE-PHASE MODEL OF DEEP COMPREHENSION
==============================================================================

ACTUALIZADO v5.0 PARA COINCIDIR CON DSCN-G v7.2:
- wPLI (Weighted Phase-Lag Index) en lugar de PLV (mitiga volume conduction)
- Inyección de artefactos EMG sintéticos en insight_point
- Mock ICA rejection (PCA como proxy, reemplazar con MNE en producción)
- Granger Causality para Predicción P6 (Phase-Hijacking)
- Proxy teóricamente justificado de ρ(t)
- Alineado con correcciones v7.2: sign(o_i), Ec. 7 (interferencia cognitiva)
- Valores actualizados: ρ_eff = 0.7001, ω_sim = 0.612 ± 0.173, p_conv = 0.97

Hipótesis testeadas:
P5: Tendencia creciente en coherencia alfa antes del insight (Fase 1).
P4: Transición de fase rápida a coherencia gamma sostenida (Fase 2→3).
P6: Causalidad de Granger unidireccional S1 → aPFC durante phase-hijacking.

Autor: Luciano Benjamín Nieto
Fecha: 2026
Licencia: MIT (Compartir libremente, construir sobre esto, sin restricciones)
==============================================================================
"""

import numpy as np
import scipy.signal as signal
from scipy.stats import pearsonr
from scipy.linalg import lstsq
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# SECCIÓN 1: GENERACIÓN DE EEG SINTÉTICO CON RUIDO FISIOLÓGICO
# =============================================================================

def generate_synthetic_eeg(n_samples=5000, fs=250, insight_point=3500,
                           inject_emg=True, emg_duration_ms=200):
    """
    Genera datos EEG sintéticos simulando el Modelo de Tres Fases para dos
    regiones (Fz y Pz) para testear el pipeline antes de correr en datos reales.
    
    ACTUALIZADO v5.0:
    - Inyecta artefacto EMG sintético en insight_point (simula micromovimientos
      faciales durante el "aha!": sonrisa, apertura de ojos, etc.)
    - EMG es ruido broadband (30-150 Hz) con decaimiento exponencial, imitando
      las características reales de artefactos musculares.
    """
    t = np.arange(n_samples) / fs    
    # 1. Ruido base (espectro 1/f - realista para EEG)
    noise_Fz = np.cumsum(np.random.randn(n_samples)) * 0.05
    noise_Pz = np.cumsum(np.random.randn(n_samples)) * 0.05
    
    # 2. Fase 1 (Acumulación): Coherencia alfa creciente (8-12 Hz) antes del insight
    alpha_env = np.zeros(n_samples)
    alpha_env[:insight_point] = np.linspace(0, 1.5, insight_point)
    alpha_env[insight_point:] = 0.5
    
    alpha_Fz = np.sin(2 * np.pi * 10 * t) * alpha_env
    phase_lag_alpha = np.pi / 4 * (1 - alpha_env / 2)
    alpha_Pz = np.sin(2 * np.pi * 10 * t - phase_lag_alpha) * alpha_env
    
    # 3. Fases 2 y 3 (Umbral y Flow): Burst gamma y coherencia cruzada sostenida
    gamma_env = np.zeros(n_samples)
    gamma_env[insight_point:insight_point + 200] = np.hanning(200) * 3.0
    gamma_env[insight_point + 200:] = 1.5
    
    gamma_Fz = np.sin(2 * np.pi * 45 * t) * gamma_env
    phase_lag_gamma = np.pi / 8
    gamma_Pz = np.sin(2 * np.pi * 45 * t - phase_lag_gamma) * gamma_env
    
    sig_Fz = noise_Fz + alpha_Fz + gamma_Fz
    sig_Pz = noise_Pz + alpha_Pz + gamma_Pz
    
    # 4. INYECCIÓN DE ARTEFACTO EMG (v5.0 - Apéndice B.3.1)
    if inject_emg:
        emg_samples = int(emg_duration_ms * fs / 1000)
        emg_start = insight_point
        emg_end = min(insight_point + emg_samples, n_samples)
        
        emg_noise_Fz = np.random.randn(emg_end - emg_start) * 2.0
        emg_noise_Pz = np.random.randn(emg_end - emg_start) * 2.0
        
        decay = np.exp(-np.linspace(0, 3, emg_end - emg_start))
        emg_noise_Fz *= decay
        emg_noise_Pz *= decay
        
        b, a = signal.butter(4, [30 / (fs / 2), 150 / (fs / 2)], btype='band')
        emg_noise_Fz = signal.filtfilt(b, a, emg_noise_Fz)
        emg_noise_Pz = signal.filtfilt(b, a, emg_noise_Pz)
        
        sig_Fz[emg_start:emg_end] += emg_noise_Fz
        sig_Pz[emg_start:emg_end] += emg_noise_Pz
    
    return t, sig_Fz, sig_Pz

# =============================================================================
# SECCIÓN 2: WEIGHTED PHASE-LAG INDEX (wPLI) - APÉNDICE B.1.1# =============================================================================

def calculate_wpli(sig1, sig2, band_pass, fs=250, window_size_sec=2.0):
    """
    Calcula el Weighted Phase-Lag Index (wPLI) entre dos señales.
    
    wPLI es robusto a artefactos de volume conduction porque ignora diferencias
    de fase de 0° o 180° (típicas de señales de un único origen propagándose
    por el cráneo).
    
    Fórmula: wPLI = |mean(Im(S))| / mean(|Im(S)|)
    donde S es el espectro cruzado entre las dos señales.
    
    Referencia: Vinck et al. (2011). NeuroImage.
    """
    nyq = fs / 2
    b, a = signal.butter(4, [band_pass[0] / nyq, band_pass[1] / nyq], btype='band')
    
    sig1_filt = signal.filtfilt(b, a, sig1)
    sig2_filt = signal.filtfilt(b, a, sig2)
    
    al1 = signal.hilbert(sig1_filt)
    al2 = signal.hilbert(sig2_filt)
    
    cross_spectrum = al1 * np.conj(al2)
    im_cross = np.imag(cross_spectrum)
    
    window_size = int(window_size_sec * fs)
    n_samples = len(sig1)
    wpli = np.zeros(n_samples)
    
    for i in range(n_samples):
        start = max(0, i - window_size // 2)
        end = min(n_samples, i + window_size // 2)
        
        if end - start < 10:
            wpli[i] = 0
            continue
        
        im_window = im_cross[start:end]
        numerator = np.abs(np.mean(im_window))
        denominator = np.mean(np.abs(im_window))
        
        if denominator > 1e-10:
            wpli[i] = numerator / denominator
        else:
            wpli[i] = 0
    
    return wpli
# =============================================================================
# SECCIÓN 3: MOCK ICA REJECTION (APÉNDICE B.1.2)
# =============================================================================

def mock_ica_rejection(sig1, sig2, fs=250, n_components=2):
    """
    Mock ICA usando PCA como proxy.
    
    En un pipeline real, esto usaría ICA de MNE-Python para identificar y
    remover componentes musculares (EMG) y oculares (EOG). Para testing con
    datos sintéticos, usamos PCA para remover los componentes de mayor varianza
    (que suelen corresponder a artefactos).
    
    NOTA: Esto es una SIMPLIFICACIÓN. ICA real separa fuentes por independencia
    estadística, no varianza. Para producción, reemplazar con MNE.
    """
    X = np.vstack([sig1, sig2]).T
    X_centered = X - np.mean(X, axis=0)
    
    cov = np.cov(X_centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    components = X_centered @ eigenvectors
    components[:, :n_components] = 0
    
    X_clean = components @ eigenvectors.T
    X_clean += np.mean(X, axis=0)
    
    return X_clean[:, 0], X_clean[:, 1]

# =============================================================================
# SECCIÓN 4: GRANGER CAUSALITY (APÉNDICE B.2.1 - PARA P6)
# =============================================================================

def granger_causality(sig1, sig2, max_lag=20, fs=250):
    """
    Computa Causalidad de Granger entre dos señales usando modelo VAR.
    
    Usado para Predicción P6: "Causalidad de Granger unidireccional S1 → aPFC
    durante phase-hijacking."
    
    max_lag=20 corresponde a 80ms a fs=250, dentro de la ventana 100-250ms
    biológicamente plausible especificada en Apéndice B.2.1.
    """
    n = len(sig1)
    best_lag = max_lag    
    # Test 1→2
    X_restricted = np.zeros((n - best_lag, best_lag))
    X_unrestricted = np.zeros((n - best_lag, 2 * best_lag))
    y = sig2[best_lag:]
    
    for i in range(best_lag):
        X_restricted[:, i] = sig2[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, i] = sig2[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, best_lag + i] = sig1[best_lag - i - 1:n - i - 1]
    
    coef_r, _, _, _ = lstsq(X_restricted, y)
    rss_r = np.sum((y - X_restricted @ coef_r) ** 2)
    
    coef_u, _, _, _ = lstsq(X_unrestricted, y)
    rss_u = np.sum((y - X_unrestricted @ coef_u) ** 2)
    
    df1 = best_lag
    df2 = n - 2 * best_lag - 1
    
    f_stat_1_to_2 = ((rss_r - rss_u) / df1) / (rss_u / df2)
    
    # Test 2→1
    y = sig1[best_lag:]
    
    for i in range(best_lag):
        X_restricted[:, i] = sig1[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, i] = sig1[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, best_lag + i] = sig2[best_lag - i - 1:n - i - 1]
    
    coef_r, _, _, _ = lstsq(X_restricted, y)
    rss_r = np.sum((y - X_restricted @ coef_r) ** 2)
    
    coef_u, _, _, _ = lstsq(X_unrestricted, y)
    rss_u = np.sum((y - X_unrestricted @ coef_u) ** 2)
    
    f_stat_2_to_1 = ((rss_r - rss_u) / df1) / (rss_u / df2)
    
    if f_stat_1_to_2 > f_stat_2_to_1 and f_stat_1_to_2 > 3.0:
        direction = "1->2"
    elif f_stat_2_to_1 > f_stat_1_to_2 and f_stat_2_to_1 > 3.0:
        direction = "2->1"
    else:
        direction = "none"
    
    return f_stat_1_to_2, f_stat_2_to_1, direction

# =============================================================================
# SECCIÓN 5: PROXY DE ρ(t)
# =============================================================================
def calculate_rho_proxy(alpha_wpli, gamma_wpli, alpha_weight=0.6, gamma_weight=0.4):
    """
    Proxy teóricamente justificado para densidad contextual ρ(t).
    
    - Alfa wPLI (8-12 Hz) proxea W(t) (ancho de ventana atencional)
    - Gamma wPLI (30-80 Hz) proxea E_active (integración activa)
    
    La combinación ponderada refleja que tanto el scope atencional amplio
    (alfa) COMO la integración local (gamma) contribuyen a ρ(t).
    """
    alpha_norm = (alpha_wpli - np.min(alpha_wpli)) / (np.max(alpha_wpli) - np.min(alpha_wpli) + 1e-10)
    gamma_norm = (gamma_wpli - np.min(gamma_wpli)) / (np.max(gamma_wpli) - np.min(gamma_wpli) + 1e-10)
    
    rho_proxy = alpha_weight * alpha_norm + gamma_weight * gamma_norm
    
    return rho_proxy

# =============================================================================
# SECCIÓN 6: FUNCIONES DSCN-G v7.2 (CORREGIDAS)
# =============================================================================

def ec3_corrected(phi, eta, R_i, outcome, theta_a):
    """
    Ec. 3 — Dinámica de fase Kuramoto acotado (CORREGIDA v7.2)
    
    sign(0)=0, sign(1)=1 (NO más 2*outcome-1)
    
    Esta corrección asegura que cuando outcome=0 (fracaso), el update de fase
    se anula, evitando deriva artificial hacia el atractor antipodal.
    """
    sign_o = 1.0 if outcome > 0.5 else 0.0  # sign(0)=0, sign(1)=1
    return (phi + eta * R_i * sign_o * np.sin(theta_a - phi)) % (2 * np.pi)

def ec7_corrected(omega_norm, phi_i, phi_root):
    """
    Ec. 7 — Interferencia cognitiva (CORREGIDA v7.2)
    
    I_i(t) = ||ω_i(t)|| · cos(φ_i(t) − φ_root(t))
    
    Mide el binding entre contenido semántico (‖ω_i‖) y coherencia temporal
    (cos(Δφ)). No es una función de reward (eso ahora es reward_fn separada).
    """
    return omega_norm * np.cos(phi_i - phi_root)

def reward_fn(theta_a, theta_star):
    """
    Función de reward R(t) ∈ [0,1] (SEPARADA de Ec. 7 en v7.2)
    
    R(t) = exp(-3 · |sin((θ_a − θ*)/2)|)    
    Mapea proximidad angular a reward continuo en [0,1].
    """
    dist = abs(np.sin((theta_a - theta_star) / 2))
    return float(np.exp(-3 * dist)), 1 if dist < np.pi / 8 else 0

# =============================================================================
# SECCIÓN 7: PARÁMETROS DSCN-G v7.2 (ACTUALIZADOS)
# =============================================================================

DSCN_G_PARAMS = {
    # Parámetros del sistema
    "K": 10,              # Cadenas paralelas
    "ETA": 0.05,          # Tasa de aprendizaje de fase
    "BETA": 0.10,         # Tasa de aprendizaje vectorial
    "GAMMA": 0.01,        # Decaimiento de vitalidad
    "THETA_D": 0.10,      # Umbral de poda
    "THETA_DIV": 0.80,    # Umbral de división
    "LAMBDA_VM": 3.0,     # Concentración von Mises
    "ALPHA": 5.0,         # Afinidad de cadenas
    "D_VEC": 4,           # Dimensión vectorial (kernel)
    "KAPPA": 1.0,         # Amplificación de valencia
    "THETA_EMERG": 0.30,  # Umbral de phase-hijacking
    "THETA_STAR": np.pi / 2,  # Fase objetivo
    
    # Valores de verificación (v7.2)
    "RHO_EFF": 0.7001,    # Índice de concentración Herfindahl
    "OMEGA_SIM": 0.612,   # Norma vectorial simulada
    "OMEGA_STD": 0.173,   # Desviación estándar
    "P_CONV": 0.97,       # Tasa de convergencia de fase
    "HIJACK_RATE": 0.286, # Tasa de phase-hijacking
    "N_BOUND": 7.00,      # Cota Teorema 1 (rho_eff/theta_d)
}

# =============================================================================
# SECCIÓN 8: PIPELINE PRINCIPAL DE ANÁLISIS
# =============================================================================

def analyze_three_phase_model(inject_emg=True, use_mock_ica=True):
    """Pipeline principal para testear las predicciones del Modelo de Tres Fases."""
    fs = 250
    n_samples = 6000
    insight_point = 4000
    
    t, fz, pz = generate_synthetic_eeg(
        n_samples=n_samples,
        fs=fs,
        insight_point=insight_point,
        inject_emg=inject_emg
    )    
    if use_mock_ica:
        fz, pz = mock_ica_rejection(fz, pz, fs=fs, n_components=1)
    
    alpha_wpli = calculate_wpli(fz, pz, [8, 12], fs, window_size_sec=2.0)
    gamma_wpli = calculate_wpli(fz, pz, [35, 55], fs, window_size_sec=2.0)
    
    rho_proxy = calculate_rho_proxy(alpha_wpli, gamma_wpli)
    
    return t, alpha_wpli, gamma_wpli, rho_proxy, fz, pz

def test_prediction_p5(t, alpha_wpli, insight_time_sec=16.0):
    """
    Test Predicción P5: Tendencia creciente en coherencia alfa antes del insight.
    """
    pre_start = int((insight_time_sec - 15) * 250)
    pre_end = int((insight_time_sec - 2) * 250)
    
    alpha_pre = alpha_wpli[pre_start:pre_end]
    x = np.arange(len(alpha_pre))
    
    slope, intercept = np.polyfit(x, alpha_pre, 1)
    is_rising = slope > 0.0001
    
    return slope, is_rising

def test_prediction_p4(t, gamma_wpli, insight_time_sec=16.0):
    """
    Test Predicción P4: Transición de fase rápida a coherencia gamma sostenida.
    """
    pre_start = int((insight_time_sec - 5) * 250)
    pre_end = int(insight_time_sec * 250)
    post_start = int((insight_time_sec + 2) * 250)
    post_end = int((insight_time_sec + 7) * 250)
    
    gamma_pre = np.mean(gamma_wpli[pre_start:pre_end])
    gamma_post = np.mean(gamma_wpli[post_start:post_end])
    
    jump_factor = gamma_post / (gamma_pre + 1e-10)
    is_significant_jump = jump_factor > 2.0
    
    return gamma_pre, gamma_post, jump_factor, is_significant_jump

def test_prediction_p6(fz, pz, fs=250, max_lag=25):
    """
    Test Predicción P6: Causalidad de Granger unidireccional S1 → aPFC.
    """
    gc_1_to_2, gc_2_to_1, direction = granger_causality(fz, pz, max_lag=max_lag, fs=fs)
    is_unidirectional = (direction == "1->2")
        return gc_1_to_2, gc_2_to_1, direction, is_unidirectional

# =============================================================================
# SECCIÓN 9: EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DSCN-G-BIO PIPELINE TEST v5.0 - MODELO DE TRES FASES")
    print("Alineado con DSCN-G v7.2 (correcciones: sign(o_i), Ec. 7)")
    print("=" * 80)
    print()
    
    print("Parámetros DSCN-G v7.2:")
    print(f"  ρ_eff = {DSCN_G_PARAMS['RHO_EFF']}")
    print(f"  ω_sim = {DSCN_G_PARAMS['OMEGA_SIM']} ± {DSCN_G_PARAMS['OMEGA_STD']}")
    print(f"  p_conv = {DSCN_G_PARAMS['P_CONV']}")
    print(f"  Hijack rate = {DSCN_G_PARAMS['HIJACK_RATE']*100:.1f}%")
    print(f"  Bound T.1: N* ≤ {DSCN_G_PARAMS['N_BOUND']}")
    print()
    
    print("Corriendo análisis con inyección EMG + mock ICA...")
    t, alpha, gamma, rho, fz, pz = analyze_three_phase_model(
        inject_emg=True,
        use_mock_ica=True
    )
    
    insight_time = 4000 / 250
    print(f"Insight Time: {insight_time}s")
    print()
    
    print("Testeando Predicción P5 (slope de acumulación alfa)...")
    slope, is_rising = test_prediction_p5(t, alpha, insight_time_sec=insight_time)
    print(f"  Slope: {slope:.6f}")
    print(f"  Resultado: {'✓ TENDENCIA CRECIENTE DETECTADA' if is_rising else '✗ Sin tendencia'}")
    print()
    
    print("Testeando Predicción P4 (salto de gamma flow)...")
    gamma_pre, gamma_post, jump_factor, is_jump = test_prediction_p4(
        t, gamma, insight_time_sec=insight_time
    )
    print(f"  Gamma wPLI pre-insight: {gamma_pre:.3f}")
    print(f"  Gamma wPLI post-insight: {gamma_post:.3f}")
    print(f"  Factor de salto: {jump_factor:.2f}x")
    print(f"  Resultado: {'✓ SALTO SIGNIFICATIVO DETECTADO' if is_jump else '✗ Sin salto'}")
    print()
    
    print("Testeando Predicción P6 (Causalidad de Granger S1 → aPFC)...")
    gc_1_to_2, gc_2_to_1, direction, is_unidir = test_prediction_p6(fz, pz)
    print(f"  GC 1->2 (F-stat): {gc_1_to_2:.3f}")    print(f"  GC 2->1 (F-stat): {gc_2_to_1:.3f}")
    print(f"  Dirección: {direction}")
    print(f"  Resultado: {'✓ UNIDIRECCIONAL 1->2' if is_unidir else '✗ No unidireccional'}")
    print()
    
    print("=" * 80)
    print("PIPELINE LISTO PARA DATASETS IN-VIVO (DEAP, PhysioNet, OpenNeuro)")
    print("=" * 80)
    print()
    print("NOTA: Para uso en producción, reemplazar mock_ica_rejection() con ICA de MNE-Python.")
    print("NOTA: Las funciones ec3_corrected() y ec7_corrected() implementan las")
    print("      correcciones de DSCN-G v7.2 (sign(o_i) e interferencia cognitiva).")