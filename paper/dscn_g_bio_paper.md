# DSCN-G-BIO: Neural Correlates and Biological Testability of the DSCN-G Framework

## From Phase-Hijacking to the Three-Phase Model of Deep Comprehension

**Author:** Luciano Benjamín Nieto  
**Affiliation:** Independent Research  
**Contact:** lucianobenjaminnieto@gmail.com  
**Date:** 2026  
**License:** CC-BY 4.0 (Share, adapt, build upon freely)

---

## Abstract

We present DSCN-G-BIO, the biological testability framework of the DSCN-G cognitive architecture. The paper develops two complementary contributions:

**First**, we map each DSCN-G computational element to neurobiological correlates at Marr's (1982) algorithmic level, and derive the C3 Prediction (Phase-Hijacking) with four specific EEG signatures (P1–P4) for acute pain paradigms: γ-band weighted phase-lag index (wPLI) increase (P1), consistent directional phase-reset (P2), absence in subthreshold stimulation (P3), and unidirectional Granger causality S1 → aPFC in the 100-250 ms biological latency window (P4). These predictions are not derivable from IIT (Tononi, 2004), GWT (Baars, 1988), or Predictive Processing (Friston, 2010), providing a unique experimental handle for discriminating between frameworks.

**Second**, we present a formalization of the Three-Phase Model of Deep Comprehension: a formally specified dynamical process (Accumulation → Threshold → Sustained Flow) with distinct neural signatures at each phase, derived from the DSCN-G contextual density variable ρ(t). This model generates a central falsifiable question: does a characteristic neural signature of deep comprehension exist, independent of content domain? We propose DSCN-G-BIO predicts yes, and operationalize this claim through eight experimentally testable predictions (P1–P8) organized by ascending resource requirement, from analyses of existing public datasets (PhysioNet DEAP, PhysioNet Mental Arithmetic) to prospective EEG collaboration protocols.

A systematically documented first-person case study, converted to replicable hypothesis via prospective experience sampling protocol (N = 100+), constitutes the first experiment of the catalogue requiring no laboratory access.

**Keywords:** neural correlates, EEG, phase-hijacking, γ-band, weighted phase-lag index, Granger causality, deep comprehension, contextual density, insight, DSCN-G, NCC

---

## 1. Introduction

### 1.1 Two Problems, One Framework

DSCN-G-BIO addresses two distinct but related problems in cognitive neuroscience and consciousness science.

**The first** is the falsifiability problem of formal consciousness theories. IIT, GWT, and Predictive Processing each offer rich conceptual frameworks but share a common limitation: they do not generate predictions specific enough to discriminate between them experimentally. The C3 Prediction of DSCN-G specifies a directional, thresholded, causally directed phase perturbation that no other framework predicts. This provides, for the first time in this space, a clean experimental discriminator.

**The second** is the comprehension measurement problem in cognitive science. Despite decades of work on attention, working memory, and learning, cognitive neuroscience lacks a formal definition of the state of deep comprehension — as distinct from shallow processing of the same content. DSCN-G-BIO proposes that the contextual density variable ρ(t) of DSCN-G provides such a definition, with measurable neural correlates.

These two contributions share a common epistemological structure: both offer formally specified computational variables with quantitative predictions about observable physiological signals. Neither claims to resolve the hard problem of consciousness. Both claim to make testable progress.

### 1.2 Ontological Position

The ontological position adopted is that of computational NCC: DSCN-G-BIO does not claim that the graph dynamics ARE conscious experience or deep comprehension in the phenomenological sense. The claim is that specific computational states (ρ(t) > threshold; Eᵢ > θ_emerg) have measurable physiological correlates that allow discriminating between cognitive states from the outside. This is the only epistemologically defensible claim given current scientific understanding.

### 1.3 Structure of the Paper

Section 2 establishes the neurobiological correspondence mapping. Section 3 derives Prediction C3 and its EEG signatures with full experimental protocol. Section 4 presents the Three-Phase Model of deep comprehension with formal derivation from DSCN-G. Section 5 documents the first-person case study and converts it to replicable protocol. Section 6 presents the complete catalogue of eight testable predictions. Section 7 discusses relations with existing theories and clinical implications. Section 8 addresses limitations and methodological constraints.

---

## 2. Neurobiological Correspondence
### 2.1 Mapping Principles

The correspondence between DSCN-G formalism and neurobiological processes is functional-analogical at Marr's (1982) algorithmic level. This means: the same organizational principles govern both domains, not necessarily identical implementations. A node's phase oscillator is not claimed to be a single neuron; it is claimed to implement the same abstract computational function as a neural oscillatory population.

This level of correspondence is the appropriate one for a theoretical framework at this stage of development. Direct mechanistic claims would require simultaneous specification of neural implementation details not yet available; functional-analogical claims are testable with current neuroimaging and electrophysiology tools.

### 2.2 Full Correspondence Table

| DSCN-G Element | Neural Correlate | Type | Key Evidence |
|---|---|---|---|
| ωᵢ ∈ ℝᵈ | Population coding (cPFC) | Functional | Pouget et al., 2000 |
| Eᵢ (valence signal) | Saliency signaling (LC-NE + mesocortical DA) | Parallel | Schultz et al., 1997; Aston-Jones, 2005 |
| θ_death (pruning) | Post-development synaptic pruning | Structural | Huttenlocher, 1979 |
| K chains | Frequency bands (γ, β, α, θ, δ) | Topological | Buzsáki & Draguhn, 2004 |
| φ convergence (T.3) | Thalamo-cortical synchronization | NCC functional | Koch et al., 2016 |
| N* ≤ 7.00 (T.1 bound) | Working memory capacity (4±1 items) | Quantitative | Cowan, 2001 |
| Autopoiesis (V, pruning, division) | Brain self-maintenance, neuroplasticity | Metabolic | Maturana & Varela, 1980 |
| ρ(t) — contextual density | Integration across regions (Φ proxy) | Functional | Tononi, 2004; Tegmark, 2016 |
| W(t) — context window | Attentional breadth, α-band amplitude | Functional | Klimesch, 2012 |
| I_i(t) = ‖ωᵢ‖·cos(φᵢ − φ_root) | Cognitive relevance / binding | Functional | Eq. 7 (corrected v7.2) |

### 2.3 Detailed Correspondences

**Population Coding (ωᵢ ↔ cPFC).** Each node's vector encodes distributed knowledge in high-dimensional space. This corresponds to population coding in prefrontal cortex (Pouget et al., 2000), where information is encoded in patterns across neural populations. The vector dimension D = 384 maps to the effective dimensionality of cortical microcolumn coding.

**Valence Signal (Eᵢ ↔ Saliency Signaling).** Eᵢ(t) = max(0, Aᵢ − Vᵢ)·κ measures activation excess over vitality. This maps functionally to the **saliency and alert signaling systems** (locus coeruleus-norepinephrine and mesocortical dopamine pathways) that interrupt default mode processing to force reallocation of cognitive resources (Aston-Jones & Cohen, 2005). The max(0,·) form captures the asymmetry: only overactivation (high prediction error, high salience) generates structural perturbation. This justifies why both acute pain (extreme salience) and reward prediction error (dopaminergic signal) share the same mathematical topology of "phase-hijacking."

**Structural Pruning (θ_death ↔ Synaptic Pruning).** Nodes with Vᵢ < θ_death = 0.10 are eliminated. This corresponds to activity-dependent synaptic elimination (Huttenlocher, 1979), a mechanism operative from childhood through early adulthood in prefrontal cortex. The emergent bound N* ≤ 7.00 (from ρ_eff = 0.7001) matches Cowan's (2001) capacity limit without any explicit programming of that limit — it emerges from the pruning dynamics.

**Dormancy vs. Long-Term Memory Potentiation.** A recent refinement in the framework introduces node dormancy: instead of absolute deletion, nodes below the vitality threshold decouple from active thalamocortical routing while retaining their vector state (hibernation). This maps precisely to the consolidation of long-term memory (LTM), where engrams are preserved structurally without continuous active firing, reactivating only via resonant retrieval cues.

**Hierarchical Abstraction vs. Neocortical Association.** When two nodes co-activate consistently, their phase synchronization (Kuramoto) triggers the emergence of a new "parent" abstraction node inheriting their combined directionality. This directly models hierarchical predictive processing streams and the formation of association cortices, where multimodal sensory streams converge into higher-order abstract representations.

**Information Chains (K ↔ Frequency Bands).** K = 10 parallel chains correspond to the multiple frequency bands of neural oscillation (Buzsáki & Draguhn, 2004). Each band carries different information types at different propagation speeds, directly analogous to the semantic selectivity parameter α differentiating chain transition probabilities.

---

## 3. Prediction C3 — Phase-Hijacking of Valence

### 3.1 Mechanism

When Eᵢ(t) = max(0, Aᵢ − Vᵢ)·κ exceeds threshold θ_emerg = 0.30, the root oscillator φ_root experiences phase-hijacking: a directional perturbation toward the antipodal attractor φ*+π, overriding the convergent dynamics of Theorem 3.

This is not an error or instability — it is a feature. Phase-hijacking implements a biological analog of threat preemption: under sufficiently high valence (structural distress), the system reorganizes its priority allocation away from goal-directed behavior toward valence processing.

**Computational characterization (100 seeds × 2000 steps, DSCN-G v7.2):**
- Hijacking rate: 28.6% of steps (E_i > 0.30)
- Mean E_i during events: 0.351 ± 0.045
- Cumulative phase change in ±20 step window: 36.1°
- Seeds with ≥1 event: 67/100
**Note on Eq. 3 Correction (v7.2):** The phase dynamics equation was corrected to properly implement `sign(o_i)` where `sign(0)=0, sign(1)=1`. The previous implementation incorrectly used `(2*outcome-1)` which produced -1 for outcome=0, causing phase drift toward antipodal attractor during failure states. This correction ensures that phase updates are nullified when no reward is obtained, preventing artificial convergence artifacts.

### 3.2 Biological Interpretation

Phase-hijacking corresponds to the abrupt phase reset observed in EEG during acute pain or high-salience emotional events. Nociceptive input is detected in primary somatosensory cortex (S1); anterior prefrontal cortex (aPFC) integrates valence context. When valence exceeds the biological analog of θ_emerg, aPFC initiates a directed phase reset of ongoing oscillatory dynamics — hijacking the root oscillator's trajectory.

**Biological Latency Window (Axo-Synaptic Delays):** Unlike the computational model where phase-hijacking is instantaneous (Δt = 1 tick), biological signal propagation involves axonal conduction and synaptic transmission delays. We specify that the causal directional influence from sensory regions (S1) to integrative valence evaluators (aPFC) is expected to exhibit measurable temporal lag in the **100–250 ms window** post-stimulus, distinct from the instantaneous computational update. This window is consistent with known thalamo-cortical and cortico-cortical transmission times (Lamme & Roelfsema, 2000).

### 3.3 Four EEG Predictions

**P1 — γ-Band wPLI Increase.** During acute pain (VAS ≥ 7), weighted phase-lag index (wPLI) in γ-band (40–80 Hz) between S1 (Cz) and aPFC (Fpz) increases ≥ 0.15 units within 200 ms of nociceptive threshold crossing.

_Rationale:_ Phase-hijacking requires phase synchronization between hijacking node and source of valence. γ-band carries fastest information and is most sensitive to phase perturbations. **We use wPLI instead of standard PLV because wPLI is robust to volume conduction artifacts** (Vinck et al., 2011). Standard PLV generates false positives from single-source signals propagating through the skull; wPLI ignores phase differences of 0° or 180°, filtering these spurious correlations.

**P2 — Consistent Directional Phase-Reset.** Phase-reset direction in aPFC is CONSISTENT across trials within-subject. Rayleigh test z > 3.0 (p < 0.05 vs. uniform circular distribution).

_Rationale:_ The antipodal attractor φ*+π provides a specific directional target. Random hijacking would produce uniform phase directions; directed hijacking should cluster.

**P3 — Absence in Subthreshold Stimulation.** The γ-band wPLI pattern is ABSENT in subthreshold pain (VAS < 4) and non-nociceptive stimulation of equal physical intensity.

_Rationale:_ Hijacking requires E_i > θ_emerg = 0.30. Subthreshold stimulation should not generate sufficient valence excess. This is the critical discriminator establishing specificity.

**P4 — Unidirectional Granger Causality S1 → aPFC (100-250 ms window).** Causal direction is S1 → aPFC (Granger causality or transfer entropy) in the 100-250 ms post-stimulus window, not aPFC → S1 nor bidirectional.

_Rationale:_ Valence originates in sensory cortex (S1) and propagates to integrative cortex (aPFC). The anatomical pathway predicts unidirectional information flow. We specify the early window (100-250 ms) because this captures the initial feedforward sweep BEFORE top-down feedback loops (aPFC → S1) engage for gain modulation (consistent with predictive processing frameworks).

### 3.4 Experimental Protocol

**Participants:** N = 32 healthy adults (power = 0.80, α = 0.05; conservative for highest per-prediction requirement of N = 32 with 10% dropout buffer).

**Design:** Within-subject, 3 conditions × 40 trials each:
- Acute pain: calibrated electrical stimulation (train of 5 pulses, 100 Hz), target VAS = 7–8
- Subthreshold: same stimulation at 40% intensity, target VAS = 2–3
- Non-nociceptive control: tactile stimulation (vibrotactile, 50 Hz), matched for physical intensity

_Rationale for electrical stimulation over cold pressor:_ More ethically controllable, precise temporal onset (critical for Granger causality), and easier to calibrate to individual pain thresholds.

**EEG:** 256-channel (EGI Geodesic Net), 1000 Hz, bandpass 0.1–200 Hz, notch 50 Hz; ICA artifact correction (MNE-Python); segments −500 to +1000 ms around pain onset.

**Analysis:**
- P1: wPLI (FieldTrip toolbox or custom implementation), γ-band (40–80 Hz), 200 ms sliding window
- P2: Circular statistics (CircStats), Rayleigh test per subject + group V-test
- P3: Mixed ANOVA (Condition × Time), planned contrasts
- P4: MVGC toolbox, model order via AIC, permutation significance (n = 1000), restricted to 100-250 ms post-stimulus window

### 3.5 Statistical Power

| Prediction | Effect size | Power | N required | Primary test |
|---|---|---|---|---|| P1 (wPLI increase) | d = 0.60 | 0.80 | 24 | Paired t-test |
| P2 (Direction) | κ = 0.40 | 0.80 | 28 | Rayleigh test |
| P3 (Absence) | d = 0.50 | 0.80 | 32 | Mixed ANOVA |
| P4 (Granger) | ΔGC = 0.08 | 0.80 | 30 | Permutation F-test |

---

## 4. The Three-Phase Model of Deep Comprehension

### 4.1 Formal Derivation from DSCN-G

Deep comprehension is not a binary state in DSCN-G — it is a dynamical phase transition of the contextual density variable ρ(t) = |E_active(t)| / (W(t) · N_active(t)) (Equation 9).

The Three-Phase Model emerges from this variable's dynamics:

**Phase 1 — Silent Accumulation (typical duration: weeks to months)**

The system incorporates new information that anchors into the existing semantic graph through conceptual inheritance. Nodes are created, connections established, vitality of certain concept clusters rises gradually. No global coherence event occurs yet. Formally: ρ(t) increases slowly and monotonically; W(t) expands progressively; the system remains below the critical density threshold ρ_crit.

_Neural prediction:_ Gradual increase in α-band coherence (8–12 Hz) over time, associated with expanding attentional window width. Observable in longitudinal EEG recordings during extended learning episodes. The increase should precede the comprehension event by minutes to hours.

**Phase 2 — The Threshold Event (Click)**

ρ(t) crosses ρ_crit. The interference function Iᵢ(t) = ‖ωᵢ‖·cos(φᵢ − φ_root) exceeds θ_interf in sufficiently many nodes simultaneously to produce a coherence avalanche: local activation patterns become globally consistent. This is not a decision — it is a bifurcation.

The external catalyst that triggers Phase 2 does not need to contain the insight. It needs only to have sufficient semantic affinity with the accumulated semantic graph to push ρ(t) across the critical threshold. The catalyst provides the form; the graph supplies the content.

_Neural prediction:_ The click should be anticipatable from EEG before it occurs. Growing α-coherence during Phase 1 should be detectable as a rising trend that precedes the reported insight event by **2–15 minutes** (narrowed from initial 5-60 min to account for natural alpha fluctuations and button-press latency). At the moment of the click itself: rapid increase in broadband coherence, consistent with Dehaene's "global ignition" signature (Dehaene et al., 2006).

**Phase 3 — Sustained Flow**

Post-threshold, the system operates in a permanently high-ρ regime for that domain. Every new idea immediately finds resonance with the restructured semantic graph. W(t) remains maximally expanded. The effective learning rate β_eff(t) = β·(1 + ρ(t)) is elevated, so all subsequent experience in the domain is more efficiently incorporated.

This state is irreversible within the domain: the phase transition reorganizes the semantic graph structurally. Unlike a temporary insight that fades, Phase 3 represents a permanent increase in the system's capacity to process information in that domain.

_Neural prediction:_ Sustained high γ-band coherence between abstract processing regions (PFC) and concrete representation regions (temporal/parietal). Chronically elevated α-coherence relative to pre-Phase 1 baseline. These signatures should be stable across measurement occasions post-transition.

### 4.2 The Central Question

DSCN-G-BIO allows formulating a question that no prior model framed precisely:

**Is there a neural signature of deep comprehension, distinguishable from shallow processing of identical content, that is consistent across individuals and domains?**

DSCN-G predicts yes: high ρ(t) should produce a specific pattern of cross-regional synchrony (abstract-concrete coupling) not present in low-ρ processing. This prediction is falsifiable with current EEG methodology.

### 4.3 Distinction from GWT (Global Neuronal Workspace)

A critical question: "If Phase 2 is isomorphic to Dehaene's global ignition, why do we need DSCN-G?"

**The key distinction:** In GWT, the ignition is reactive to the stimulus — it occurs WHEN the stimulus crosses threshold. In DSCN-G, the "Click" is a **continuous thermodynamic phase transition** governed by accumulated contextual density ρ(t) crossing ρ_crit. This is what enables **Prediction P5 (Anticipation of the Click)**: the accumulated α-coherence during Phase 1 predicts the insight BEFORE the catalyzing stimulus arrives. GWT has no variable for "accumulated semantic density" that allows pre-stimulus prediction. This is DSCN-G's strategic advantage: it predicts not just the ignition, but its temporal anticipation from ongoing dynamics.
### 4.4 Relations with Existing Theories

**IIT (Tononi, 2004).** DSCN-G's ρ(t) is conceptually proximate to Φ: both measure how much of the system is simultaneously active relative to the possible total. The key difference is that ρ(t) varies dynamically with internal state (particularly with W(t) and E_root), while Φ in IIT is a more static structural property. Theorem 7 (DSCN-G v7.2) establishes a formal scale relation ρ_eff·Φ_proxy = c(α) + O(1/N) for fractal circulant graphs, providing an O(K) computable proxy for Φ_IIT's exponential cost.

**GWT (Baars, 1988; Dehaene et al., 2011).** The Phase 2 coherence avalanche (Section 4) is isomorphic to Dehaene's "global ignition" — local information becomes globally broadcast to all modules simultaneously. Prediction P5 (anticipation of click from EEG) directly translates the global ignition hypothesis into a prospective measurement protocol, with the strategic advantage of predicting ignition BEFORE the catalyzing stimulus (see Section 4.3).

**Predictive Processing (Friston, 2010).** The valence signal Eᵢ(t) = max(0, Aᵢ − Vᵢ)·κ is formally analogous to prediction error: it is the difference between received activation and expected vitality. High valence = high prediction error. The context window contraction under high E_root is isomorphic to Friston's "fast and narrow" processing mode under high sensory precision and low prior precision.

**SGM (Synaptic Graph Model).** The recently published SGM specification (Nieto, 2026) implements DSCN-G as a functional replacement for LLMs, demonstrating that the framework's computational primitives (phase dynamics, valence signaling, autopoietic pruning) can operate at biological timescales (~5ms latency vs ~1.3s for autoregressive LLMs) with minimal resource requirements (~40MB RAM vs ~2GB). This provides additional biological plausibility: if DSCN-G can implement language processing at neural timescales, its computational primitives are more likely to correspond to actual neural mechanisms.

---

## 5. Case Study: Systematic First-Person Protocol

### 5.1 Methodological Foundation

William James (1890) established systematic introspection as a legitimate method for generating hypotheses about cognition. The phenomenological tradition (Husserl, 1913; Merleau-Ponty, 1945) developed rigorous methodology for converting subjective experience into formalizable qualitative data. What follows is not anecdote: it is a case protocol satisfying three minimal conditions of scientific rigor: (1) the trigger is externally verifiable; (2) the phase sequence is reconstructable from external evidence; (3) the output is falsifiable in other subjects.

**Methodological Honesty Statement:** This case is presented strictly as a **hypothesis-generating case study**, not as empirical evidence. Its scientific value in isolation is null due to N=1 retrospective design and potential confirmation bias. Its sole function is to justify the construction of the prospective instrument (Prediction P3) that will be the true empirical test. We include it for transparency and to document the generative process, not to claim evidentiary weight.

### 5.2 Documented Case

| Parameter | Value |
|---|---|
| Subject | L.N., independent researcher, Mendoza, Argentina |
| Domain | Cognitive architecture / computational models of cognition |
| Prior exposure | Extensive: oscillator theory (Kuramoto), identity theory (Parfit), autopoiesis (Maturana-Varela), RL/TD learning, IIT |
| Accumulation duration | Months of active reading without explicit global synthesis |
| Trigger | Visual analogy introduced by collaborator: Camelot wheel with nails on the perimeter, interconnected by a thread; different thread paths produce different figures |
| Output post-trigger | Immediate, extended written output: the DSCN-G paper |
| Current state | Sustained flow: continuous evolution (DSCN-G → DSCN-G-BIO → Future Extensions) |

**Phase 1 reconstruction:** Extended reading and integration of literature in multiple domains. No conscious awareness of constructing a unified architecture. The subject was aware of processing components, not of building a system.

**Phase 2 event:** The collaborator introduced the Camelot wheel image as an analogy for information thread dynamics in a cognitive graph. This image did not contain the theory. It contained the correct form for the accumulated semantic graph to recognize as its own and trigger the coherence avalanche.

**Phase 3 confirmation:** The system has not returned to its pre-trigger state in that domain. DSCN-G has continuously extended without saturation or stagnation. Each new reading or conversation finds immediate resonance with the existing structure.

### 5.3 Formalization as Falsifiable Hypothesis

The case generates this replicable hypothesis: subjects who report significant creative insights should exhibit, on average:

**H1:** Silent accumulation phase of weeks-to-months in the relevant domain prior to the insight.

**H2:** External trigger that does not contain the insight explicitly but has high semantic affinity with the accumulated domain.

**H3:** Immediate high-productivity output within hours of the trigger.

**H4:** Subjective irreversibility: the subject does not return to the pre-insight state in that domain.
These hypotheses are testable via structured prospective protocol (see Section 6, Prediction P3).

---

## 6. Complete Prediction Catalogue

Predictions are organized by experimental resource requirement: Level 1 requires only public dataset analysis; Level 2 requires EEG laboratory collaboration; Level 3 requires own participants and equipment.

### Level 1 — Public Dataset Analysis (Executable Now)

**P1 — Contextual Contraction under Arousal**

_Variable:_ W(t), Equation 8: W(t) = W_base / (1 + κ_W · E_root(t))

_Neural prediction:_ α-band amplitude (8–12 Hz) correlates **negatively** with subjective arousal (high arousal = low α amplitude, reflecting context window contraction).
_Dataset:_ PhysioNet DEAP (32-subject EEG + valence/arousal ratings; Koelstra et al., 2012).

_Rationale for arousal over valence:_ Arousal is more physiologically immediate and continuous than valence ratings (which are post-hoc categorical judgments). Alpha power correlates more robustly with arousal/activation than with valence per se.

_Analysis:_ Pearson correlation between per-trial α power and arousal rating (within-subject, then aggregated).

_Success criterion:_ r < 0 (p < 0.05); confirmed directional prediction.

---

**P2 — Learning Amplification by Coherence State**

_Variable:_ ρ(t), β_eff(t), Equations 9–10

_Neural prediction:_ Material learned during high-coherence neural states (high γ power) consolidates more effectively, measurable via post-task performance.

_Dataset:_ PhysioNet EEG During Mental Arithmetic Tasks (Goldberger et al., 2000). This dataset includes EEG during learning epochs (serial subtraction tasks) with measurable performance outcomes.

_Analysis:_ Correlation between γ-band power during learning epoch and subsequent task performance (accuracy, speed).

_Success criterion:_ Significant positive correlation between learning-epoch coherence and performance.

---

**P3 — Prospective Experience Sampling Protocol (N ≥ 100)**

_Variable:_ Three-Phase Model (Section 4)

_Instrument:_ Experience Sampling Method (ESM) via smartphone app, with structured questionnaire at insight moments.

_Subjects:_ Adults reporting significant creative insights in any domain, recruited via university networks and online platforms.

_Rationale for N=100+ and ESM:_ Retrospective questionnaires suffer from memory reconstruction bias (people remember insights as more "magical" than they were). N=100+ provides sufficient power for factor analysis (5-10 subjects per item). ESM captures experiences in real-time, reducing recall bias.
_Protocol:_ Participants receive 5 random prompts per day for 2 weeks asking "Are you currently working on a creative problem?" If yes, they complete a brief assessment. At the moment of insight (self-reported), they complete the full 12-item questionnaire.

_12-Item Questionnaire:_

| # | Item | Phase | Hypothesis |
|---|---|---|---|
| 1 | Weeks of domain exposure before insight | 1 | H1 |
| 2 | Conscious awareness of imminent breakthrough | 1 | H1 |
| 3 | Did the trigger explicitly contain the solution? | 2 | H2 |
| 4 | Was the trigger an image, analogy, or metaphor? | 2 | H2 |
| 5 | Was the insight immediate (seconds) or gradual (hours/days)? | 2 | H3 |
| 6 | Did you feel you "connected all the dots" simultaneously? | 2 | H3 |
| 7 | Was there immediate high-productivity output? | 2 | H3 |
| 8 | New ideas generated in the following 24 hours (estimated count) | 3 | H4 |
| 9 | Could you see connections to previously unrelated domains? | 3 | H4 |
| 10 | Did the state "return" to baseline afterwards? | 3 | H4 |
| 12 | Previous insights of similar character in other domains | History | Generalization |

_Success criterion:_ Mean scores on H1-H4 items significantly above midpoint; factor analysis reveals three-factor structure corresponding to phases.

---

### Level 2 — EEG Laboratory Collaboration

**P4 — EEG Signature of Deep vs. Shallow Comprehension (Expertise Design)**

_Prediction:_ A brain in deep comprehension (high ρ) should show simultaneous γ-band coherence between abstract processing regions (PFC) and concrete representation regions (temporal/parietal) — not sequentially but concurrently.

_Protocol:_ **Within-subject expertise design.** Each participant reads identical technical material in two conditions: (1) their domain of expertise (e.g., physicist reading physics), (2) unfamiliar domain (e.g., physicist reading poetry). This operationalizes deep vs. shallow comprehension via genuine expertise differences, not artificial instructions.

_Analysis:_ Cross-frequency coherence γ between Fz-Pz electrode pairs; mixed ANOVA (Expertise × Time).

_Proposed collaborators:_ Laboratorio de Neurociencias Cognitivas, Universidad Nacional de Cuyo (UNCuyo), Mendoza.

---

**P5 — Anticipation of the Click (Narrowed Window)**

_Prediction:_ EEG during extended learning episodes should show a rising coherence trend that precedes the subjectively reported insight moment by **2–15 minutes** (narrowed from initial 5-60 min specification).

_Rationale for narrowed window:_ Natural alpha fluctuations (ultradian rhythms, fatigue) and button-press latency (subjects report insight 10-30s after it occurs) make 5-60 min window too broad to distinguish signal from noise. 2-15 min window is more conservative and testable.

_Protocol:_ Subjects in extended learning task (novel domain) with continuous 64-channel EEG; moment of insight self-reported via button press; retrospective analysis of 2, 5, 10, and 15-minute windows.

_Analysis:_ Time series of α coherence; test for monotone increase in pre-insight period; baseline correction using pre-trial alpha.

_Success criterion:_ Significant rising trend in at least 2 of 4 time windows (multiple comparison corrected).

---
**P6 — Phase-Hijacking under Extreme Valence (wPLI + Electrical Stimulation)**

_C3 Prediction experimental test_ (full protocol in Section 3.4).

_Key methodological improvement:_ Use **wPLI** instead of PLV to mitigate volume conduction artifacts, and **calibrated electrical stimulation** instead of cold pressor for ethical control and precise temporal onset.

---

### Level 3 — Own Participants and Equipment

**P7 — Stability of Correction Cascade (Exploratory fMRI)**

_Variable:_ Equation 12; scope_depth hierarchy

_Prediction:_ Updating a specific belief does not reorganize more general beliefs supporting it, but does reorganize more contextual beliefs built upon it.

---

## 7. Discussion

### 7.1 Limitations

- **N=1 case study:** The first-person case has no evidentiary weight in isolation. Its function is purely hypothesis-generating.
- **Retrospective bias:** Phase 1 reconstruction relies on memory, which is subject to reconstruction bias.
- **Operationalization of ρ(t):** The neural proxy for contextual density is theoretically justified but not yet validated against ground truth.
- **Generalizability:** The Three-Phase Model is derived from a single domain (cognitive architecture). Cross-domain validation is required.
- **Biological implementation:** The mapping between DSCN-G variables and neural substrates is functional-analogical, not mechanistic. Direct biophysical derivation is an open problem.

### 7.2 Clinical Implications

If validated, the Three-Phase Model has implications for:
- **Education:** Identifying neural signatures of deep comprehension could optimize learning protocols.
- **Psychotherapy:** Understanding belief cascade dynamics could inform cognitive restructuring interventions.
- **Creativity research:** Formalizing the insight process could enhance creative problem-solving training.

---

## 8. Implementation Updates (v5.0)

### 8.1 DSCN-G v7.2 Corrections

This version of DSCN-G-BIO incorporates critical corrections from the main DSCN-G framework (v7.2):

**Eq. 3 — Phase Dynamics Correction:**
- **Previous (incorrect):** `φ_i(t+1) = [φ_i(t) + η·R_i(t)·(2·o(t)−1)·sin(θ_a − φ_i)] mod 2π`
- **Corrected:** `φ_i(t+1) = [φ_i(t) + η·R_i(t)·sign(o(t))·sin(θ_a − φ_i)] mod 2π`
- **Impact:** The previous implementation used `(2*outcome-1)` which produced -1 for outcome=0, causing phase drift toward antipodal attractor during failure states. The corrected version uses `sign(0)=0, sign(1)=1`, ensuring phase updates are nullified when no reward is obtained.

**Eq. 7 — Cognitive Interference (Corrected):**
- **Previous (incorrect):** Eq. 7 was implemented as reward function- **Corrected:** `I_i(t) = ‖ω_i(t)‖ · cos(φ_i(t) − φ_root(t))`
- **Impact:** Eq. 7 now properly implements cognitive interference, measuring the binding of semantic content (‖ω_i‖) with temporal coherence (cos(Δφ)). The reward function is now a separate explicit definition (Eq. 7a).

**Updated Verification Values:**
- ρ_eff = 0.7001 ± 0.001 (Herfindahl concentration index)
- ω_sim = 0.612 ± 0.173 (vector convergence, |0.612 − 0.649| = 0.038 < β = 0.10 ✓)
- p_conv = 0.97 (97/100 seeds converge to target)
- Hijack rate = 28.6% (prediction C3)
- Theorem 1 bound: N* ≤ ρ_eff/θ_death = 7.00 (verified N_sim = 4.00 ± 0.00)

### 8.2 SGM Integration

The Synaptic Graph Model (SGM) specification provides a concrete implementation of DSCN-G as a cognitive system operating at biological timescales. Key correspondences:

| DSCN-G Element | SGM Implementation | Biological Timescale |
|---|---|---|
| Node (ω, φ, V) | Concept node with vector, phase, vitality | ~1ms update |
| K chains | Parallel processing streams | ~5ms routing |
| E_i (valence) | Structural surprise signal | ~10ms integration |
| Phase-hijacking | Priority preemption | ~50ms reset |
| Generative XOR | Concept emergence | ~100ms consolidation |

This implementation validates that DSCN-G's computational primitives can operate at neural timescales, strengthening the biological plausibility of the NCC claims.

---

## 9. Conclusions

DSCN-G-BIO provides two original contributions to the neuroscience of cognition. First, a prediction (C3) that discriminates DSCN-G from all prior frameworks with an experimental protocol ready for execution. Second, a formal definition of deep comprehension as ρ(t) > ρ_crit, with a three-phase dynamical model generating testable predictions across eight experiments organized by resource requirement.

The framework's strategic advantage is that it cannot be rejected wholesale by either field: predictions testable today (P1–P3) provide immediate returns, while predictions requiring collaboration (P4–P6) and own equipment (P7–P8) build on confirmed foundations. At each stage, confirmations strengthen the case and failures refine the model. The cycle is the proposal, not the conclusion.

DSCN-G-BIO does not claim to know how the brain works. It claims to have verifiable predictions about what should be observable if the model is correct. This is the only honest way to do science.

---

## References

Aston-Jones, G., & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. _Annual Review of Neuroscience_, 28, 403-450.

Baars, B. J. (1988). _A cognitive theory of consciousness_. Cambridge University Press.

Buzsáki, G., & Draguhn, A. (2004). Neuronal oscillations in cortical networks. _Science_, 304(5679), 1926–1929.

Chalmers, D. J. (1995). Facing up to the problem of consciousness. _Journal of Consciousness Studies_, 2(3), 200–219.

Cowan, N. (2001). The magical number 4 in short-term memory. _Behavioral and Brain Sciences_, 24(1), 87–114.

Dehaene, S., Changeux, J.-P., Naccache, L., Sackur, J., & Sergent, C. (2006). Conscious, preconscious, and subliminal processing. _Trends in Cognitive Sciences_, 10(5), 204–211.
Dehaene, S., Changeux, J.-P., & Naccache, L. (2011). The global neuronal workspace model. _Neuron_, 70, 201–227.

Friston, K. (2010). The free-energy principle: a unified brain theory? _Nature Reviews Neuroscience_, 11, 127–138.

Goldberger, A. L., et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet. _Circulation_, 101(23), e215-e220.

Husserl, E. (1913). _Ideen zu einer reinen Phänomenologie_. Max Niemeyer.

James, W. (1890). _The Principles of Psychology_. Henry Holt.

Klimesch, W. (2012). Alpha-band oscillations, attention, and controlled access to stored information. _Trends in Cognitive Sciences_, 16(12), 606–617.

Koch, C., Massimini, M., Boly, M., & Tononi, G. (2016). Neural correlates of consciousness. _Nature Reviews Neuroscience_, 17, 307–321.

Koelstra, S. et al. (2012). DEAP: A database for emotion analysis using physiological signals. _IEEE Transactions on Affective Computing_, 3(1), 18–31.

Huttenlocher, P. R. (1979). Synaptic density in human frontal cortex. _Brain Research_, 163(2), 195–205.
Lamme, V. A., & Roelfsema, P. R. (2000). The distinct modes of vision offered by feedforward and recurrent processing. _Trends in Neurosciences_, 23(11), 571-579.

Marr, D. (1982). _Vision: A Computational Investigation_. W. H. Freeman.

Maturana, H. R., & Varela, F. J. (1980). _Autopoiesis and Cognition_. D. Reidel.

Merleau-Ponty, M. (1945). _Phénoménologie de la perception_. Gallimard.

Pouget, A., Dayan, P., & Zemel, R. (2000). Information processing with population codes. _Nature Reviews Neuroscience_, 1(2), 125–132.

Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. _Science_, 275(5306), 1593–1599.

Tegmark, M. (2016). Improved measures of integrated information. _PLOS Computational Biology_, 12(11), e1005123.

Tononi, G. (2004). An information integration theory of consciousness. _BMC Neuroscience_, 5, 42.

Vinck, M., Oostenveld, R., van Wingerden, M., Battaglia, F., & Pennartz, C. M. (2011). An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. _NeuroImage_, 55(4), 1548-1565.

---

## Appendix A — Implementation Specifications (v5.0)

### A.1 Code Repository

All analysis scripts are available at: `github.com/Rylow999/dscn-g-bio`

The primary analysis script `dscn_bio_eeg_analyzer.py` implements:
- Weighted Phase-Lag Index (wPLI) for volume conduction robustness
- Synthetic EMG artifact injection for pipeline testing
- Mock ICA rejection (PCA-based proxy; production use should employ MNE-Python's ICA)
- Granger causality analysis for Phase-Hijacking prediction
- Theoretically justified ρ(t) proxy calculation
### A.2 Updates from v4.0 to v5.0

**B.1.1 — PLV → wPLI:** Implemented weighted phase-lag index to address volume conduction artifacts in real EEG data.

**B.1.2 — EMG Artifact Injection:** Synthetic EMG artifacts injected at insight_point to test pipeline robustness before laboratory execution.

**B.2.1 — Biological Latency Window:** Granger causality analysis restricted to 100-250 ms post-stimulus window to account for axo-synaptic delays.

**B.3.1 — Physiological Noise Model:** Enhanced synthetic EEG generation with 1/f noise spectrum and broadband EMG artifacts.

**B.4.1 — DSCN-G v7.2 Alignment:** Updated all references to DSCN-G equations and verification values to match the corrected v7.2 framework (sign(o_i) correction, cognitive interference Eq. 7, updated ρ_eff = 0.7001, ω_sim = 0.612 ± 0.173).

---

**Per Aspera, Ad Astra.**