# The Perceptual Blind Spots of Human Hearing

## A reference for exploiting the limits of auditory perception in forensic footprint removal

> **Purpose:** This document catalogs every scientifically established limitation, threshold, and blind spot of the human auditory system. Each entry explains the phenomenon, states the numerical bounds, and derives an **Operational Rule** -- a concrete constraint that NaSuno's removal algorithms can exploit to guarantee inaudibility.
>
> **Principle:** We do not need to preserve the signal perfectly. We need to preserve the signal *as the human ear perceives it*. Everything below the ear's detection threshold is free real estate for watermark removal.

---

## 1. Simultaneous Masking (Frequency-Domain Masking)

### The Phenomenon

When a loud sound (the **masker**) is present at one frequency, it raises the hearing threshold at nearby frequencies. Quieter sounds that fall below this raised threshold become completely inaudible -- they are "masked." This is the single most powerful perceptual principle for hiding signal modifications.

### The Science

The cochlea (inner ear) performs a mechanical frequency analysis along its length. Each point on the basilar membrane responds to a range of frequencies, not a single frequency. When a strong signal excites a region, it physically saturates that region's hair cells, preventing them from responding to weaker nearby signals.

The masking effect is **asymmetric**: a masker at frequency `f` masks higher frequencies more effectively than lower frequencies. This is because the basilar membrane's traveling wave propagates from base (high freq) to apex (low freq), so a low-frequency masker's excitation pattern extends further into the high-frequency region.

### The Numbers

| Parameter | Value | Source |
|-----------|-------|--------|
| Masking spread (downward, below masker) | ~25 dB/Bark | Zwicker & Fastl (1999) |
| Masking spread (upward, above masker) | ~10 dB/Bark at low levels, ~5 dB/Bark at high levels | Zwicker & Fastl (1999) |
| Masking depth at masker frequency | 0 dB (masker fully masks itself) | -- |
| Masking at 1 Bark distance | ~15-20 dB below masker | Painter & Spanias (2000) |
| Masking at 2 Bark distance | ~25-35 dB below masker | Painter & Spanias (2000) |
| Noise masking tone (NMT) | ~5 dB less effective than tone masking noise | ISO 11172-3 |
| Masking is level-dependent | Upward spread increases ~25 dB per 40 dB increase in masker level | Moore (2012) |

### Masking Spread Function (Schroeder Model)

For a masker at Bark rate `z_m` with level `L_m` (dB SPL), the masking threshold at Bark rate `z` is approximately:

```
T(z) = L_m - 27 + 0.37 * max(L_m - 40, 0) * (z - z_m)    [for z > z_m, upward]
T(z) = L_m - 27 - (z_m - z) * 25                           [for z < z_m, downward]
```

> [!WARNING]
> This is the single-masker model. For multiple simultaneous maskers, the combined threshold uses power-law summation (ISO 11172-3, Psychoacoustic Model 2):
> `T_combined = (sum(T_i^0.3))^(1/0.3)` where each `T_i` is a linear-scale masking threshold.
> This is less than linear summation but more than simple max -- two equal-level maskers provide approximately 3 dB more masking than one alone. NaSuno's perceptual engine must use this power-law model, not simple max.

### Operational Rules for NaSuno

> **Rule M1:** Any modification to a spectral bin that keeps the modification's energy below the simultaneous masking threshold of neighboring bins is inaudible. Compute the masking threshold from the local spectral peaks using power-law summation (alpha = 0.3) and constrain all attenuation/addition to stay below it.

> **Rule M2:** Modifications near strong spectral peaks (harmonics of pitched instruments, formants of voice) can be larger in magnitude than modifications in spectrally quiet regions. A 10 dB modification next to a -20 dBFS harmonic is inaudible; the same 10 dB modification in a spectral valley would be obvious.

> **Rule M3:** Modifications at frequencies ABOVE a strong masker can be 10-15 dB larger than modifications BELOW it (asymmetric masking). Exploit this: when removing a watermark at 18 kHz that sits above musical content at 8-12 kHz, the musical content masks the removal artifacts upward.

---

## 2. Temporal Masking (Time-Domain Masking)

### The Phenomenon

Masking is not instantaneous -- it extends in time. A loud sound masks quieter sounds that occur both **after** it (forward masking / post-masking) and **before** it (backward masking / pre-masking). This means brief modifications during or near transients (drum hits, consonants, note onsets) are effectively invisible.

### The Numbers

| Parameter | Value | Source |
|-----------|-------|--------|
| **Forward masking duration** | 100-200 ms | Zwicker & Fastl (1999) |
| Forward masking depth at 5 ms | ~30 dB | Oxenham (2001) |
| Forward masking depth at 20 ms | ~20 dB | Oxenham (2001) |
| Forward masking depth at 50 ms | ~10 dB | Oxenham (2001) |
| Forward masking depth at 100 ms | ~5 dB | Oxenham (2001) |
| Forward masking depth at 200 ms | ~0 dB (gone) | Oxenham (2001) |
| **Backward masking duration** | 5-20 ms | Zwicker & Fastl (1999) |
| Backward masking depth at 5 ms | ~15 dB | Oxenham (2001) |
| **Temporal integration window** | ~200 ms | Moore (2012) |

> [!NOTE]
> The exact values depend on masker level, frequency, and duration. These are representative values for moderate-level maskers. At high masker levels (> 80 dB SPL), forward masking can extend beyond 200 ms and reach deeper attenuation.

### Forward Masking Decay Function

Masking threshold decay after a masker offset at `t = 0`:

```
T(t) = L_masker - 10 * log10(1 + t/tau)    [dB SPL]
```

Where `tau` is approximately 3-5 ms for brief maskers and 10-20 ms for sustained maskers.

### Operational Rules for NaSuno

> **Rule T1:** Modifications made within 20 ms after a transient (drum hit, consonant onset, note attack) can be up to 20 dB larger than steady-state modifications. Schedule aggressive removal operations to coincide with detected transient events.

> **Rule T2:** Modifications made within 5 ms before a transient can be up to 15 dB larger than normal. This is "free" processing time.

> **Rule T3:** The ear integrates energy over approximately 200 ms. A brief modification (<5 ms) is perceived only by its time-averaged energy contribution, not its instantaneous peak. A 1ms click at -30 dBFS is inaudible when averaged into a 200 ms window; it becomes roughly -53 dBFS effective.

> **Rule T4:** Crossfades between processing blocks should be at least 5 ms (220 samples at 44.1 kHz) to avoid audible discontinuities. Prefer 10-20 ms for safety.

---

## 3. Critical Bands and the Bark Scale

### The Phenomenon

The cochlea divides the audible spectrum into approximately 24 **critical bands** (Bark bands). Within a single critical band, the ear cannot resolve individual frequency components -- it perceives their combined energy as a single "auditory event." This means modifications within a critical band that preserve total band energy are largely inaudible.

### The Bark Scale

| Bark | Center Freq (Hz) | Bandwidth (Hz) | Lower Edge (Hz) | Upper Edge (Hz) |
|------|-------------------|-----------------|------------------|------------------|
| 1 | 50 | 80 | 0 | 100 |
| 2 | 150 | 100 | 100 | 200 |
| 3 | 250 | 100 | 200 | 300 |
| 4 | 350 | 100 | 300 | 400 |
| 5 | 450 | 110 | 400 | 510 |
| 6 | 570 | 120 | 510 | 630 |
| 7 | 700 | 140 | 630 | 770 |
| 8 | 840 | 150 | 770 | 920 |
| 9 | 1000 | 160 | 920 | 1080 |
| 10 | 1170 | 190 | 1080 | 1270 |
| 11 | 1370 | 210 | 1270 | 1480 |
| 12 | 1600 | 240 | 1480 | 1720 |
| 13 | 1850 | 280 | 1720 | 2000 |
| 14 | 2150 | 320 | 2000 | 2320 |
| 15 | 2500 | 380 | 2320 | 2700 |
| 16 | 2900 | 450 | 2700 | 3150 |
| 17 | 3400 | 550 | 3150 | 3700 |
| 18 | 4000 | 700 | 3700 | 4400 |
| 19 | 4800 | 900 | 4400 | 5300 |
| 20 | 5800 | 1100 | 5300 | 6400 |
| 21 | 7000 | 1300 | 6400 | 7700 |
| 22 | 8500 | 1800 | 7700 | 9500 |
| 23 | 10500 | 2500 | 9500 | 12000 |
| 24 | 13500 | 3500 | 12000 | 15500 |
| 25 | 19500 | 7000+ | 15500 | 22050+ |

### Conversion Formulas

```
Bark = 13 * arctan(0.00076 * f_Hz) + 3.5 * arctan((f_Hz / 7500)^2)
```

```
ERB (Equivalent Rectangular Bandwidth) = 24.7 * (4.37 * f_kHz + 1)    [Hz]
```

### Operational Rules for NaSuno

> **Rule B1:** Redistributing energy WITHIN a single critical band is largely inaudible. If a watermark occupies a single spectral bin within a Bark band, the energy can be spread across the entire band (median-smoothed) without perceptible change, as long as total band energy is preserved within 1 dB.

> **Rule B2:** Critical bandwidth increases dramatically above 5 kHz. At 15 kHz, a single critical band spans ~3500 Hz. Modifications within this range that preserve total energy are undetectable. This is why high-frequency watermark removal is so safe -- the ear literally cannot resolve individual components in these wide bands.

> **Rule B3:** Below 500 Hz, critical bands are narrow (~100 Hz). Modifications in the bass region must be more precise and narrowband to avoid audibility. Notch filters below 500 Hz should have Q > 30 to stay within a single critical band.

---

## 4. Phase Perception

### The Phenomenon

Human phase perception is extremely limited. For **steady-state** tones, phase is almost completely inaudible. Phase perception exists only in specific, narrow conditions.

### The Critical Distinction: Steady-State vs. Transient

> [!IMPORTANT]
> Ohm's Acoustic Law (1843) establishes that the ear is predominantly a magnitude analyzer. This is correct for steady-state sounds. However, phase coherence across frequency bins determines the **temporal shape** of transient events (attacks, consonants, drum hits). Randomizing phase during transients converts sharp attacks into diffuse noise-like energy spread over time. This is audible.
>
> Grey & Gordon (1978) demonstrated that timbre perception depends heavily on "synchronicity of onsets" and "inharmonic attack transients" -- both of which are phase-dependent properties.

### The Numbers

| Condition | Phase JND | Source |
|-----------|-----------|--------|
| Steady-state, > 3 kHz | Not measurable (phase is inaudible) | Ohm (1843), Moore (2012) |
| Steady-state, 1-3 kHz | ~30 degrees (0.52 radians) | Patterson (1987) |
| Steady-state, < 500 Hz | ~10-15 degrees (0.17-0.26 radians) | Moore (2012) |
| Harmonic complex, relative phase | ~20-30 degrees at low harmonics | Plomp & Steeneken (1969) |
| **Transient events, ANY frequency** | **Phase must be preserved** | Grey & Gordon (1978), McAdams (1984) |

### Operational Rules for NaSuno

> **Rule P1 (CORRECTED):** Above 3 kHz, phase can be freely randomized **only during steady-state frames** (sustained notes, chords, held tones). During transient frames (drum hits, consonant attacks, note onsets), the inter-bin phase relationship must be preserved to maintain the temporal shape of the attack.

> **Rule P2:** Below 1 kHz, phase must be preserved within ~15 degrees (0.26 radians) to avoid perceptible changes in "roughness" quality, even during steady-state.

> **Rule P3:** Phase perturbation must be SMOOTH across adjacent frames to avoid creating amplitude modulation. Use slowly-varying phase offsets (correlation time > 50 ms).

> **Rule P4:** Phase perturbation must be SMOOTH across adjacent frequency bins to avoid creating temporal dispersion (smearing of transients). Apply phase changes with a frequency-domain smoothing kernel of at least 5 bins.

> **Rule P5 (NEW):** During transient frames: apply a single slowly-varying GROUP PHASE offset (same offset to all bins in the frame). This shifts the entire transient in time by < 1 sample without smearing its shape. This disrupts inter-frame phase coherence (what detectors measure) without affecting intra-frame phase relationships (what the ear uses for transient perception).

---

## 5. Amplitude (Loudness) Perception

### Equal-Loudness Contours (ISO 226:2023)

The ear's sensitivity varies dramatically with frequency. At typical listening levels (60-80 dB SPL), the ear is most sensitive between 2-5 kHz (the resonance of the ear canal) and far less sensitive below 200 Hz and above 10 kHz.

### Key Sensitivity Values at 60 dB SPL (phon)

| Frequency (Hz) | Threshold of Hearing (dB SPL) | Sensitivity Relative to 1 kHz |
|----------------|-------------------------------|-------------------------------|
| 20 | ~75 | -45 dB (ear is very insensitive) |
| 50 | ~43 | -15 dB |
| 100 | ~27 | -5 dB |
| 200 | ~15 | +2 dB |
| 500 | ~5 | +5 dB |
| 1000 | ~4 | 0 dB (reference) |
| 2000 | ~-2 | +6 dB (most sensitive region) |
| 3000 | ~-4 | +8 dB (peak sensitivity) |
| 4000 | ~-4 | +8 dB |
| 5000 | ~-1 | +5 dB |
| 8000 | ~15 | -6 dB |
| 10000 | ~20 | -10 dB |
| 12000 | ~25 | -15 dB |
| 15000 | ~40 | -30 dB (sensitivity dropping fast) |
| 18000 | ~55+ | -45 dB+ (near-inaudible for most adults) |
| 20000 | ~75+ | -60 dB+ (inaudible for most adults) |

### Amplitude JND (Weber's Law for Loudness)

| Parameter | Value | Source |
|-----------|-------|--------|
| Intensity JND (broadband noise) | ~0.5-1.0 dB | Miller (1947), Jesteadt et al. (1977) |
| Intensity JND (pure tones, 1 kHz) | ~1.0 dB at moderate levels | Riesz (1928) |
| Intensity JND (complex signals, music) | ~0.5-1.5 dB | -- |
| Loudness JND in LUFS (integrated) | ~1.0 LU | ITU-R BS.1770 practice |

### Operational Rules for NaSuno

> **Rule L1:** Modifications at frequencies below 100 Hz can be 5-15 dB larger than modifications at 2-4 kHz before reaching audibility. The ear is inherently insensitive to bass frequencies.

> **Rule L2:** Modifications above 12 kHz can be 15-30 dB larger than modifications at 2-4 kHz. Above 15 kHz, modifications of 30+ dB are routine in lossy codecs.

> **Rule L3:** The most dangerous frequency range for modifications is 2-5 kHz. The ear is maximally sensitive here. Watermark removal in this range must be limited to <1 dB of net level change per critical band.

> **Rule L4:** Overall loudness change of the entire signal must stay within 1 LU (LUFS) to be imperceptible.

---

## 6. High-Frequency Hearing Loss by Age

### Hearing Upper Limit by Age

| Age | Typical Upper Hearing Limit | Sensitivity at 16 kHz |
|-----|----------------------------|----------------------|
| < 18 | 19-20 kHz | -10 to -20 dB relative to 1 kHz |
| 18-25 | 17-19 kHz | -20 to -30 dB |
| 25-35 | 15-17 kHz | -30 to -40 dB |
| 35-45 | 13-16 kHz | -40 to -50 dB |
| 45-55 | 11-14 kHz | Typically inaudible |
| 55+ | 8-12 kHz | Typically inaudible |

### Operational Rules for NaSuno

> **Rule HF1:** Any content above 16 kHz can be freely modified for the overwhelming majority of listeners.

> **Rule HF2:** Content between 12-16 kHz can tolerate modifications of 10-20 dB without audibility for most adult listeners (>25 years old).

> **Rule HF3:** For maximum safety across all age groups, limit modifications above 12 kHz to 6 dB and above 16 kHz to unlimited. This is the `gentle` profile constraint.

---

## 7. Frequency Discrimination (Pitch JND)

| Frequency | Pure Tone JND (cents) | Pure Tone JND (Hz) | Complex Tone JND (cents) |
|-----------|----------------------|--------------------|-----------------------|
| 100 Hz | ~3 cents | 0.17 Hz | ~5-10 cents |
| 250 Hz | ~2 cents | 0.29 Hz | ~3-5 cents |
| 500 Hz | ~1.5 cents | 0.43 Hz | ~3-5 cents |
| 1000 Hz | ~1 cent | 0.58 Hz | ~5 cents |
| 2000 Hz | ~1.5 cents | 1.73 Hz | ~5-8 cents |
| 4000 Hz | ~3 cents | 6.93 Hz | ~10 cents |
| 8000 Hz | ~8 cents | 37 Hz | ~20 cents |
| 12000 Hz | ~20 cents | 139 Hz | ~50+ cents |

### Operational Rules for NaSuno

> **Rule F1:** A micro pitch-shift of 3 cents (frequency multiplication by 1.00173) is below the JND for complex tones at all frequencies. Safe for perceptual hash disruption.

> **Rule F2:** At frequencies above 4 kHz, pitch shifts of up to 10 cents are below JND. At frequencies above 8 kHz, shifts of 20+ cents are undetectable.

> **Rule F3:** The pitch JND for music (complex signals with multiple harmonics) is approximately 5 cents across most of the spectrum. NaSuno can safely apply up to 3 cents of pitch perturbation as a universal operation.

> [!WARNING]
> A 2-3 cent pitch shift does NOT guarantee Chromaprint/AcoustID hash disruption. Chroma feature quantization is far coarser than 2 cents. The probability of flipping a chroma class with 2-3 cents is approximately 4-6% per pitch per analysis window. Hash disruption should be verified post-processing and supplemented with sample-level micro-stuttering.

---

## 8. Temporal Resolution

| Parameter | Value | Source |
|-----------|-------|--------|
| Gap detection threshold (broadband) | ~2-3 ms | Green (1973) |
| Gap detection threshold (narrowband) | ~5-8 ms | Eddins et al. (1992) |
| Temporal modulation transfer function -3 dB | ~4-8 Hz | Viemeister (1979) |
| Maximum detectable modulation rate | ~60-100 Hz | Kohlrausch et al. (2000) |
| Auditory temporal integration window | ~150-200 ms | Moore (2012) |

### Operational Rules for NaSuno

> **Rule TR1:** The ear integrates energy over ~200 ms. A 1-sample spike at -40 dBFS, averaged over 200 ms at 44.1 kHz, contributes -93 dBFS effective energy. Inaudible.

> **Rule TR2:** Crossfade windows must be at least 3 ms to avoid gap detection. Use 5-10 ms for safety. At 44.1 kHz, 10 ms = 441 samples.

> **Rule TR3:** Amplitude modulation between 4-60 Hz must stay below ~1 dB depth to be imperceptible.

> **Rule TR4:** The ear cannot detect timing shifts smaller than ~2 ms in complex signals. Micro-timing perturbation of up to 1 ms is transparent.

---

## 9. Distortion Perception

### Total Harmonic Distortion (THD) Thresholds

| Signal Type | THD Audibility Threshold | Source |
|-------------|-------------------------|--------|
| Pure tone (1 kHz) | ~0.1-0.3% (-50 to -60 dB) | Temme et al. (2014) |
| Complex tone (multi-harmonic) | ~0.5-1.0% (-40 to -46 dB) | Temme et al. (2014) |
| Broadband music | ~1-3% (-30 to -40 dB) | Olive et al. (2018) |
| Speech | ~3-5% (-26 to -30 dB) | -- |

### Operational Rules for NaSuno

> **Rule D1:** Nonlinear processing must keep THD below 0.1% for isolated tones and below 1% for complex music.

> **Rule D2:** Music masks its own distortion products far more effectively than isolated test tones. NaSuno can be more aggressive in dense musical passages.

> **Rule D3:** Even-order harmonics (2nd, 4th) are perceptually less objectionable than odd-order (3rd, 5th). Prefer asymmetric saturation: `y = x + 0.01 * x^2 - 0.02 * x^3`.

---

## 10. Stereo and Spatial Perception

| Parameter | Value | Source |
|-----------|-------|--------|
| Interaural Time Difference (ITD) JND | ~10-20 microseconds | Klump & Eady (1956) |
| ITD used for localization | Below ~1.5 kHz | Rayleigh (1907) |
| Interaural Level Difference (ILD) JND | ~1 dB | Mills (1958) |
| ILD used for localization | Above ~1.5 kHz | Rayleigh (1907) |
| Cross-correlation coefficient JND | ~0.04 (from 1.0 to 0.96) | Pollack & Trittipoe (1959) |

### Operational Rules for NaSuno

> **Rule S1:** For stereo material, both channels must be modified identically below 1.5 kHz to preserve ITD.

> **Rule S2:** Above 1.5 kHz, per-channel level differences must stay within 1 dB to preserve ILD-based imaging.

> **Rule S3:** Cross-channel correlation must remain above 0.96 if original was > 0.98.

---

## 11. Noise Perception and Noise Floors

| Context | Masking Noise Floor | Implication |
|---------|-------------------|-------------|
| Quiet studio recording | -80 dBFS to -90 dBFS | Modifications must be below -85 dBFS |
| Typical music production | -60 dBFS to -70 dBFS | Modifications below -65 dBFS are masked |
| Compressed/loud music | -40 dBFS to -55 dBFS | Modifications below -50 dBFS are invisible |
| AI-generated audio | -70 dBFS to -100 dBFS | Unnaturally clean; adding noise HELPS realism |

### Operational Rules for NaSuno

> **Rule N1:** Any modification whose energy is 10 dB below the measured noise floor is absolutely safe.

> **Rule N2:** AI-generated audio typically has an unnaturally low noise floor. Adding shaped comfort noise at the measured noise floor + 3 dB simultaneously masks removal artifacts, raises the floor to natural levels, and disrupts statistical patterns.

> **Rule N3:** Dither for quantization disruption should be calibrated to the noise floor.

---

## 12. Cognitive and Attentional Masking

| Context | Informational Masking Strength |
|---------|-------------------------------|
| Solo instrument / vocal | Low |
| Small ensemble (2-4 parts) | Moderate |
| Full band mix (5-10 parts) | High |
| Dense electronic / orchestral | Very high |
| Music with lyrics | Very high for instrumental details |

### Operational Rules for NaSuno

> **Rule C1:** The denser the mix, the more aggressive NaSuno can be. Solo piano -> gentle; 12-track electronic -> aggressive.

> **Rule C2:** Vocal content masks instrumental details. Modifications to non-vocal bands are harder for listeners to detect during sung passages.

> **Rule C3:** Musical expectations mask deviations. Micro pitch-shifts of 2-3 cents are undetectable in polyphonic music.

---

## 13. Musical Context Masking

### Operational Rules for NaSuno

> **Rule MU1:** Detect harmonic structure and schedule modifications to coincide with harmonic peaks. A notch filter at a harmonic frequency is masked by the harmonic itself.

> **Rule MU2:** Detect transients via onset detection. Apply aggressive removal in the 50 ms window following each transient, where temporal masking provides 20-30 dB of free headroom.

> **Rule MU3:** During sustained notes, limit modifications to the simultaneous masking threshold. During transients, exploit the additional temporal masking headroom.

---

## 14. Summary: The Safe Operating Envelope

### Combined Perceptual Budget per Frequency Region

| Frequency Range | Max Modification (steady-state) | Max Modification (transient window) | Phase Freedom (steady-state) | Phase Freedom (transient) |
|-----------------|--------------------------------|-------------------------------------|------------------------------|--------------------------|
| 0-100 Hz | 3-5 dB | 10-15 dB | 0.2 rad max | Group offset only |
| 100-500 Hz | 1-2 dB | 5-10 dB | 0.25 rad max | Group offset only |
| 500-2000 Hz | 0.5-1 dB | 3-6 dB | 0.3 rad max | Group offset only |
| 2000-5000 Hz | 0.5-1 dB | 3-6 dB | 0.5 rad max | Group offset only |
| 5000-8000 Hz | 1-3 dB | 5-10 dB | 1.0 rad | Group offset only |
| 8000-12000 Hz | 3-6 dB | 10-20 dB | Full random | Group offset only |
| 12000-16000 Hz | 6-15 dB | 20+ dB | Full random | Group offset only |
| 16000-22050 Hz | Unlimited | Unlimited | Full random | Full random |

> [!IMPORTANT]
> These are BASE budgets for spectrally quiet regions. When simultaneous masking, temporal masking, informational masking, and musical context masking are combined, the actual budget is typically 10-20 dB MORE permissive. The "transient window" column applies for 50 ms following a detected transient.

### The Three Tiers of Processing Safety

| Tier | Constraint | Processing Level |
|------|-----------|-----------------|
| **Tier 1: Inaudible** | Stay below absolute threshold of hearing OR below masking threshold | All levels |
| **Tier 2: Below JND** | Stay below Just-Noticeable Difference | gentle, moderate |
| **Tier 3: Masked by context** | Stay below informational/temporal/musical masking threshold | aggressive, extreme |

### Content-Adaptive Quality Thresholds

| Content Density | Correlation Threshold | Max Loudness Delta | Max per-Band Delta |
|----------------|----------------------|-------------------|-------------------|
| Sparse (solo, acoustic) | > 0.97 | < 0.5 LU | < 0.3 dB |
| Moderate (pop, rock) | > 0.94 | < 0.8 LU | < 0.5 dB |
| Dense (electronic, orchestral) | > 0.90 | < 1.0 LU | < 1.0 dB |

### Golden Rule

> Every modification NaSuno makes must satisfy AT LEAST ONE of the three tiers. If none can provide cover, the modification must not be made. The Quality Firewall enforces this with automatic rollback.

---

## References

- Zwicker, E. & Fastl, H. (1999). *Psychoacoustics: Facts and Models.* Springer.
- Moore, B.C.J. (2012). *An Introduction to the Psychology of Hearing.* 6th ed. Brill.
- Painter, T. & Spanias, A. (2000). Perceptual coding of digital audio. *Proc. IEEE*, 88(4), 451-513.
- ISO 226:2023. *Acoustics -- Normal equal-loudness-level contours.*
- ISO 11172-3. *MPEG-1 Audio Layer III (psychoacoustic model).*
- Oxenham, A.J. (2001). Forward masking: Adaptation or integration? *JASA*, 109(2).
- Blauert, J. (1997). *Spatial Hearing.* MIT Press.
- Deutsch, D. (2013). *The Psychology of Music.* 3rd ed. Academic Press.
- Plomp, R. & Steeneken, H.J.M. (1969). Effect of phase on the timbre of complex tones. *JASA*, 46(2B).
- Grey, J.M. & Gordon, J.W. (1978). Perceptual effects of spectral modifications on musical timbres. *JASA*, 63(5).
- McAdams, S. (1984). Spectral fusion, spectral parsing and the formation of auditory images. *PhD thesis, Stanford University.*
- Jesteadt, W., Wier, C.C. & Green, D.M. (1977). Intensity discrimination as a function of frequency and sensation level. *JASA*, 61(1).
- Patterson, R.D. (1987). A pulse ribbon model of monaural phase perception. *JASA*, 82(5).
- Temme, S. et al. (2014). The correlation between distortion audibility and listener preference. *AES Convention 137.*
