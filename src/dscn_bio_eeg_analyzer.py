"""
==============================================================================
DSCN-BIO EXPERIMENTAL SCRIPT v4.0: THE THREE-PHASE MODEL OF DEEP COMPREHENSION
==============================================================================

UPDATED TO MATCH APPENDIX B SPECIFICATIONS:
- wPLI (Weighted Phase-Lag Index) instead of PLV (ignores volume conduction)
- Synthetic EMG artifact injection at insight_point (simulates facial micromovements)
- Mock ICA rejection (PCA-based component removal as proxy for ICA)
- Granger Causality analysis for Phase-Hijacking (P6)
- Theoretically justified rho(t) proxy

Hypothesis tested:
P5: Rising trend in alpha coherence preceding the insight event (Phase 1).
P4: Rapid phase-transition into sustained gamma cross-coherence (Phase 2->3).
P6: Unidirectional Granger causality S1 -> aPFC during phase-hijacking.

Author: Luciano Benjamín Nieto
Date: 2026
License: MIT (Share freely, build upon it, no restrictions)
==============================================================================
"""

import numpy as np
import scipy.signal as signal
from scipy.stats import pearsonr, f_oneway
from scipy.linalg import lstsq
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# SECTION 1: SYNTHETIC EEG GENERATION WITH PHYSIOLOGICAL NOISE
# =============================================================================

def generate_synthetic_eeg(n_samples=5000, fs=250, insight_point=3500, 
                           inject_emg=True, emg_duration_ms=200):
    """
    Generates synthetic EEG data simulating the Three-Phase Model for two regions
    (e.g., Fz and Pz) to test our detection pipeline before running on real data.
    
    UPDATED v4.0:
    - Injects synthetic EMG artifact at insight_point (simulating facial micromovements
      during the "aha!" moment: smile, eye opening, etc.)
    - EMG is broadband noise (30-150 Hz) with exponential decay, mimicking real muscle
      artifact characteristics.
    
    Parameters:
    -----------
    n_samples : int        Total number of samples
    fs : int
        Sampling frequency in Hz
    insight_point : int
        Sample index where the "insight" (Phase 2) occurs
    inject_emg : bool
        Whether to inject EMG artifact at insight_point (for testing wPLI robustness)
    emg_duration_ms : int
        Duration of EMG artifact in milliseconds
    
    Returns:
    --------
    t : array
        Time vector
    sig_Fz : array
        Synthetic EEG signal for frontal region (Fz)
    sig_Pz : array
        Synthetic EEG signal for parietal region (Pz)
    """
    t = np.arange(n_samples) / fs
    
    # 1. Base noise (1/f spectrum - realistic for EEG)
    # Using Brownian noise as approximation of 1/f
    noise_Fz = np.cumsum(np.random.randn(n_samples)) * 0.05
    noise_Pz = np.cumsum(np.random.randn(n_samples)) * 0.05
    
    # 2. Phase 1 (Accumulation): Growing alpha coherence (8-12 Hz) before insight
    alpha_env = np.zeros(n_samples)
    alpha_env[:insight_point] = np.linspace(0, 1.5, insight_point)  # Ramping up
    alpha_env[insight_point:] = 0.5  # Drop after insight (context window collapse)
    
    alpha_Fz = np.sin(2 * np.pi * 10 * t) * alpha_env
    # Pz phase-locks to Fz increasingly (simulating growing coherence)
    phase_lag_alpha = np.pi/4 * (1 - alpha_env/2)
    alpha_Pz = np.sin(2 * np.pi * 10 * t - phase_lag_alpha) * alpha_env
    
    # 3. Phase 2 & 3 (Threshold & Flow): Gamma burst & sustained cross-coherence (30-80 Hz)
    gamma_env = np.zeros(n_samples)
    # Ignition burst (Phase 2 - "Click")
    gamma_env[insight_point:insight_point+200] = np.hanning(200) * 3.0
    # Sustained flow (Phase 3)
    gamma_env[insight_point+200:] = 1.5
    
    gamma_Fz = np.sin(2 * np.pi * 45 * t) * gamma_env
    phase_lag_gamma = np.pi/8
    gamma_Pz = np.sin(2 * np.pi * 45 * t - phase_lag_gamma) * gamma_env
    
    # Combine signals
    sig_Fz = noise_Fz + alpha_Fz + gamma_Fz
    sig_Pz = noise_Pz + alpha_Pz + gamma_Pz    
    # 4. INJECT EMG ARTIFACT (v4.0 - Appendix B.3.1)
    # Simulates facial micromovements (smile, eye opening) during insight moment
    # EMG is broadband (30-150 Hz) with characteristic burst morphology
    if inject_emg:
        emg_samples = int(emg_duration_ms * fs / 1000)
        emg_start = insight_point
        emg_end = min(insight_point + emg_samples, n_samples)
        
        # Generate broadband EMG noise (30-150 Hz)
        emg_noise_Fz = np.random.randn(emg_end - emg_start) * 2.0
        emg_noise_Pz = np.random.randn(emg_end - emg_start) * 2.0
        
        # Apply exponential decay envelope (EMG bursts have this morphology)
        decay = np.exp(-np.linspace(0, 3, emg_end - emg_start))
        emg_noise_Fz *= decay
        emg_noise_Pz *= decay
        
        # Bandpass filter to EMG range (30-150 Hz)
        b, a = signal.butter(4, [30/(fs/2), 150/(fs/2)], btype='band')
        emg_noise_Fz = signal.filtfilt(b, a, emg_noise_Fz)
        emg_noise_Pz = signal.filtfilt(b, a, emg_noise_Pz)
        
        # Inject into signals
        sig_Fz[emg_start:emg_end] += emg_noise_Fz
        sig_Pz[emg_start:emg_end] += emg_noise_Pz
    
    return t, sig_Fz, sig_Pz


# =============================================================================
# SECTION 2: WEIGHTED PHASE-LAG INDEX (wPLI) - APPENDIX B.1.1
# =============================================================================

def calculate_wpli(sig1, sig2, band_pass, fs=250, window_size_sec=2.0):
    """
    Calculates the Weighted Phase-Lag Index (wPLI) between two signals.
    
    wPLI is robust to volume conduction artifacts because it ignores phase
    differences of 0° or 180° (which are typical of signals from a single source
    propagating through the skull).
    
    Formula:
        wPLI = |mean(Im(S))| / mean(|Im(S)|)
    
    where S is the cross-spectrum between the two signals.
    
    Reference:
        Vinck et al. (2011). "The pairwise phase consistency: A bias-free measure
        of rhythmic neuronal synchronization." NeuroImage.    
    Parameters:
    -----------
    sig1 : array
        First signal (e.g., Fz)
    sig2 : array
        Second signal (e.g., Pz)
    band_pass : tuple
        Frequency band (low, high) in Hz
    fs : int
        Sampling frequency
    window_size_sec : float
        Window size in seconds for time-resolved wPLI
    
    Returns:
    --------
    wpli : array
        Time-resolved wPLI values
    """
    # Bandpass filter
    nyq = fs / 2
    b, a = signal.butter(4, [band_pass[0]/nyq, band_pass[1]/nyq], btype='band')
    sig1_filt = signal.filtfilt(b, a, sig1)
    sig2_filt = signal.filtfilt(b, a, sig2)
    
    # Hilbert transform to get analytic signal
    al1 = signal.hilbert(sig1_filt)
    al2 = signal.hilbert(sig2_filt)
    
    # Cross-spectrum (complex)
    cross_spectrum = al1 * np.conj(al2)
    
    # Extract imaginary part (this is what makes wPLI robust to volume conduction)
    im_cross = np.imag(cross_spectrum)
    
    # Calculate wPLI over sliding window
    window_size = int(window_size_sec * fs)
    n_samples = len(sig1)
    wpli = np.zeros(n_samples)
    
    # Sliding window calculation
    for i in range(n_samples):
        start = max(0, i - window_size // 2)
        end = min(n_samples, i + window_size // 2)
        
        if end - start < 10:  # Need minimum samples
            wpli[i] = 0
            continue
        
        im_window = im_cross[start:end]        
        # wPLI formula: |mean(Im(S))| / mean(|Im(S)|)
        numerator = np.abs(np.mean(im_window))
        denominator = np.mean(np.abs(im_window))
        
        if denominator > 1e-10:  # Avoid division by zero
            wpli[i] = numerator / denominator
        else:
            wpli[i] = 0
    
    return wpli


# =============================================================================
# SECTION 3: MOCK ICA REJECTION (APPENDIX B.1.2)
# =============================================================================

def mock_ica_rejection(sig1, sig2, fs=250, n_components=2):
    """
    Mock ICA (Independent Component Analysis) rejection using PCA as proxy.
    
    In a real pipeline, this would use MNE-Python's ICA to identify and remove
    muscular (EMG) and ocular (EOG) components. Since we're testing with synthetic
    data and not all users have MNE installed, we use PCA to remove the largest
    variance components (which often correspond to artifacts).
    
    NOTE: This is a SIMPLIFICATION. Real ICA separates sources by statistical
    independence, not variance. For production use, replace with MNE's ICA.
    
    Parameters:
    -----------
    sig1 : array
        First signal (e.g., Fz)
    sig2 : array
        Second signal (e.g., Pz)
    fs : int
        Sampling frequency
    n_components : int
        Number of components to reject (typically 1-2 for EMG/EOG)
    
    Returns:
    --------
    sig1_clean : array
        Cleaned signal 1
    sig2_clean : array
        Cleaned signal 2
    """
    # Stack signals
    X = np.vstack([sig1, sig2]).T  # Shape: (n_samples, 2)
        # Center data
    X_centered = X - np.mean(X, axis=0)
    
    # PCA (simplified ICA proxy)
    # Covariance matrix
    cov = np.cov(X_centered.T)
    
    # Eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Sort by eigenvalue (descending)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Project data into component space
    components = X_centered @ eigenvectors
    
    # Zero out the largest components (assumed to be artifacts)
    components[:, :n_components] = 0
    
    # Project back to sensor space
    X_clean = components @ eigenvectors.T
    
    # Add back mean
    X_clean += np.mean(X, axis=0)
    
    return X_clean[:, 0], X_clean[:, 1]


# =============================================================================
# SECTION 4: GRANGER CAUSALITY (APPENDIX B.2.1 - FOR P6)
# =============================================================================

def granger_causality(sig1, sig2, max_lag=20, fs=250):
    """
    Computes Granger Causality between two signals using a Vector Autoregressive
    (VAR) model.
    
    Granger causality tests whether past values of sig1 improve the prediction
    of sig2 beyond what is achievable using only past values of sig2.
    
    This is used for Prediction P6: "Unidirectional Granger causality S1 -> aPFC
    during phase-hijacking."
    
    Parameters:
    -----------
    sig1 : array
        First signal (e.g., S1 - sensory cortex)
    sig2 : array        Second signal (e.g., aPFC - anterior prefrontal cortex)
    max_lag : int
        Maximum lag in samples (for 100-250 ms window at fs=250, use 25-62 samples)
    fs : int
        Sampling frequency
    
    Returns:
    --------
    gc_1_to_2 : float
        Granger causality from sig1 to sig2 (F-statistic)
    gc_2_to_1 : float
        Granger causality from sig2 to sig1 (F-statistic)
    direction : str
        "1->2" if sig1 causes sig2, "2->1" if sig2 causes sig1, "none" if neither
    """
    n = len(sig1)
    
    # Test Granger causality from sig1 to sig2
    # Model 1 (restricted): sig2(t) = a0 + sum(a_i * sig2(t-i))
    # Model 2 (unrestricted): sig2(t) = a0 + sum(a_i * sig2(t-i)) + sum(b_i * sig1(t-i))
    
    best_lag = max_lag  # Use max_lag for this test
    
    # Prepare data matrices
    X_restricted = np.zeros((n - best_lag, best_lag))
    X_unrestricted = np.zeros((n - best_lag, 2 * best_lag))
    y = sig2[best_lag:]
    
    for i in range(best_lag):
        X_restricted[:, i] = sig2[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, i] = sig2[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, best_lag + i] = sig1[best_lag - i - 1:n - i - 1]
    
    # Fit restricted model
    coef_r, res_r, _, _ = lstsq(X_restricted, y)
    y_pred_r = X_restricted @ coef_r
    rss_r = np.sum((y - y_pred_r) ** 2)
    
    # Fit unrestricted model
    coef_u, res_u, _, _ = lstsq(X_unrestricted, y)
    y_pred_u = X_unrestricted @ coef_u
    rss_u = np.sum((y - y_pred_u) ** 2)
    
    # F-test
    df1 = best_lag
    df2 = n - 2 * best_lag - 1
    f_stat_1_to_2 = ((rss_r - rss_u) / df1) / (rss_u / df2)
    
    # Now test Granger causality from sig2 to sig1
    y = sig1[best_lag:]    
    for i in range(best_lag):
        X_restricted[:, i] = sig1[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, i] = sig1[best_lag - i - 1:n - i - 1]
        X_unrestricted[:, best_lag + i] = sig2[best_lag - i - 1:n - i - 1]
    
    # Fit restricted model
    coef_r, res_r, _, _ = lstsq(X_restricted, y)
    y_pred_r = X_restricted @ coef_r
    rss_r = np.sum((y - y_pred_r) ** 2)
    
    # Fit unrestricted model
    coef_u, res_u, _, _ = lstsq(X_unrestricted, y)
    y_pred_u = X_unrestricted @ coef_u
    rss_u = np.sum((y - y_pred_u) ** 2)
    
    # F-test
    f_stat_2_to_1 = ((rss_r - rss_u) / df1) / (rss_u / df2)
    
    # Determine direction
    if f_stat_1_to_2 > f_stat_2_to_1 and f_stat_1_to_2 > 3.0:  # Threshold F > 3.0
        direction = "1->2"
    elif f_stat_2_to_1 > f_stat_1_to_2 and f_stat_2_to_1 > 3.0:
        direction = "2->1"
    else:
        direction = "none"
    
    return f_stat_1_to_2, f_stat_2_to_1, direction


# =============================================================================
# SECTION 5: CONTEXTUAL DENSITY PROXY (ρ(t))
# =============================================================================

def calculate_rho_proxy(alpha_wpli, gamma_wpli, alpha_weight=0.6, gamma_weight=0.4):
    """
    Calculates a theoretically justified proxy for contextual density ρ(t).
    
    In DSCN-G, ρ(t) = |E_active(t)| / (W(t) · N_active(t))
    
    Operationalization:
    - Alpha wPLI (8-12 Hz) proxies W(t) (attentional window width)
    - Gamma wPLI (30-80 Hz) proxies E_active (active integration)
    
    The weighted combination reflects that both broad attentional scope (alpha)
    AND local integration (gamma) contribute to contextual density.
    
    Parameters:
    -----------
    alpha_wpli : array        Alpha band wPLI values
    gamma_wpli : array
        Gamma band wPLI values
    alpha_weight : float
        Weight for alpha component (default 0.6)
    gamma_weight : float
        Weight for gamma component (default 0.4)
    
    Returns:
    --------
    rho_proxy : array
        Proxy for contextual density ρ(t)
    """
    # Normalize both signals to [0, 1] range
    alpha_norm = (alpha_wpli - np.min(alpha_wpli)) / (np.max(alpha_wpli) - np.min(alpha_wpli) + 1e-10)
    gamma_norm = (gamma_wpli - np.min(gamma_wpli)) / (np.max(gamma_wpli) - np.min(gamma_wpli) + 1e-10)
    
    # Weighted combination
    rho_proxy = alpha_weight * alpha_norm + gamma_weight * gamma_norm
    
    return rho_proxy


# =============================================================================
# SECTION 6: MAIN ANALYSIS PIPELINE
# =============================================================================

def analyze_three_phase_model(inject_emg=True, use_mock_ica=True):
    """
    Main analysis pipeline for testing the Three-Phase Model predictions.
    
    Parameters:
    -----------
    inject_emg : bool
        Whether to inject EMG artifacts (for testing robustness)
    use_mock_ica : bool
        Whether to apply mock ICA rejection
    
    Returns:
    --------
    t : array
        Time vector
    alpha_wpli : array
        Alpha band wPLI
    gamma_wpli : array
        Gamma band wPLI
    rho_proxy : array
        Contextual density proxy
    """
    fs = 250    n_samples = 6000
    insight_point = 4000
    
    # Generate synthetic EEG with EMG artifact injection
    t, fz, pz = generate_synthetic_eeg(
        n_samples=n_samples, 
        fs=fs, 
        insight_point=insight_point,
        inject_emg=inject_emg
    )
    
    # Apply mock ICA rejection if requested (removes EMG artifacts)
    if use_mock_ica:
        fz, pz = mock_ica_rejection(fz, pz, fs=fs, n_components=1)
    
    # Calculate Alpha (8-12 Hz) wPLI
    alpha_wpli = calculate_wpli(fz, pz, [8, 12], fs, window_size_sec=2.0)
    
    # Calculate Gamma (35-55 Hz) wPLI
    gamma_wpli = calculate_wpli(fz, pz, [35, 55], fs, window_size_sec=2.0)
    
    # Calculate rho(t) proxy
    rho_proxy = calculate_rho_proxy(alpha_wpli, gamma_wpli)
    
    return t, alpha_wpli, gamma_wpli, rho_proxy, fz, pz


def test_prediction_p5(t, alpha_wpli, insight_time_sec=16.0):
    """
    Test Prediction P5: Rising trend in alpha coherence preceding the insight event.
    
    The framework predicts that alpha wPLI (proxy for W(t)) should show a monotonic
    increase during Phase 1 (Accumulation), preceding the insight by 5-60 minutes
    (in real experiments). Here we test with synthetic data.
    """
    # Extract pre-insight window (2-15 seconds before insight, representing Phase 1)
    pre_start = int((insight_time_sec - 15) * 250)
    pre_end = int((insight_time_sec - 2) * 250)
    alpha_pre = alpha_wpli[pre_start:pre_end]
    
    # Linear regression to test for rising trend
    x = np.arange(len(alpha_pre))
    slope, intercept = np.polyfit(x, alpha_pre, 1)
    
    # Test if slope is significantly positive
    # (In real analysis, would use proper statistical test)
    is_rising = slope > 0.0001
    
    return slope, is_rising

def test_prediction_p4(t, gamma_wpli, insight_time_sec=16.0):
    """
    Test Prediction P4: Rapid phase-transition into sustained gamma cross-coherence.
    
    The framework predicts that gamma wPLI should show a rapid increase at the
    moment of insight (Phase 2 - "Click"), followed by sustained elevation (Phase 3).
    """
    # Extract pre-insight and post-insight windows
    pre_start = int((insight_time_sec - 5) * 250)
    pre_end = int(insight_time_sec * 250)
    post_start = int((insight_time_sec + 2) * 250)
    post_end = int((insight_time_sec + 7) * 250)
    
    gamma_pre = np.mean(gamma_wpli[pre_start:pre_end])
    gamma_post = np.mean(gamma_wpli[post_start:post_end])
    
    jump_factor = gamma_post / (gamma_pre + 1e-10)
    
    # Test if there's a significant jump (threshold: 2x increase)
    is_significant_jump = jump_factor > 2.0
    
    return gamma_pre, gamma_post, jump_factor, is_significant_jump


def test_prediction_p6(fz, pz, fs=250, max_lag=25):
    """
    Test Prediction P6: Unidirectional Granger causality S1 -> aPFC during phase-hijacking.
    
    In the real experiment, sig1 would be S1 (sensory cortex) and sig2 would be
    aPFC (anterior prefrontal cortex). Here we use Fz and Pz as proxies.
    
    The framework predicts that during phase-hijacking (high valence), information
    flows FROM sensory regions TO integrative regions, not vice versa.
    """
    gc_1_to_2, gc_2_to_1, direction = granger_causality(fz, pz, max_lag=max_lag, fs=fs)
    
    # Test if causality is unidirectional from sig1 to sig2
    is_unidirectional = (direction == "1->2")
    
    return gc_1_to_2, gc_2_to_1, direction, is_unidirectional


# =============================================================================
# SECTION 7: MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("DSCN-BIO PIPELINE TEST v4.0 - THREE-PHASE MODEL")    print("=" * 80)
    print()
    
    # Run analysis with EMG injection and mock ICA (as per Appendix B specifications)
    print("Running analysis with EMG artifact injection + mock ICA rejection...")
    t, alpha, gamma, rho, fz, pz = analyze_three_phase_model(
        inject_emg=True, 
        use_mock_ica=True
    )
    
    insight_time = 4000 / 250
    print(f"Insight Time: {insight_time}s")
    print()
    
    # Test P5: Rising alpha before insight
    print("Testing Prediction P5 (Alpha accumulation slope)...")
    slope, is_rising = test_prediction_p5(t, alpha, insight_time_sec=insight_time)
    print(f"  Slope: {slope:.6f}")
    print(f"  Result: {'✓ RISING TREND DETECTED' if is_rising else '✗ No rising trend'}")
    print()
    
    # Test P4: Gamma jump
    print("Testing Prediction P4 (Gamma flow jump)...")
    gamma_pre, gamma_post, jump_factor, is_jump = test_prediction_p4(
        t, gamma, insight_time_sec=insight_time
    )
    print(f"  Pre-insight gamma wPLI: {gamma_pre:.3f}")
    print(f"  Post-insight gamma wPLI: {gamma_post:.3f}")
    print(f"  Jump factor: {jump_factor:.2f}x")
    print(f"  Result: {'✓ SIGNIFICANT JUMP DETECTED' if is_jump else '✗ No significant jump'}")
    print()
    
    # Test P6: Granger causality
    print("Testing Prediction P6 (Granger causality S1 -> aPFC)...")
    gc_1_to_2, gc_2_to_1, direction, is_unidir = test_prediction_p6(fz, pz)
    print(f"  GC 1->2 (F-stat): {gc_1_to_2:.3f}")
    print(f"  GC 2->1 (F-stat): {gc_2_to_1:.3f}")
    print(f"  Direction: {direction}")
    print(f"  Result: {'✓ UNIDIRECTIONAL 1->2' if is_unidir else '✗ Not unidirectional'}")
    print()
    
    print("=" * 80)
    print("PIPELINE READY FOR IN-VIVO DATASETS (DEAP, PhysioNet, OpenNeuro)")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Download PhysioNet DEAP dataset")
    print("2. Apply this pipeline to real EEG data")
    print("3. Test predictions P1-P8 systematically")
    print()    print("NOTE: For production use, replace mock_ica_rejection() with MNE-Python's ICA.")
    print("      The current implementation uses PCA as a proxy for testing purposes.")