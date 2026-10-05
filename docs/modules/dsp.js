/**
 * NaSuno Real-Time DSP Processing Engine & Offline Lossless WAV Exporter
 * Implements a complete 14-node Web Audio processing cascade:
 *  1. Stride Comb Disrupter (172.3 Hz neural frame harmonics)
 *  2. Stego Strip (cepstral echo cancellation & micro-decorrelation)
 *  3. Ultrasonic Carrier Notches (15.5k, 17.5k, 19.5k surgical IIR filters)
 *  4. Neural Scrub (dynamic high-frequency residual attenuation)
 *  5. Spectral Blend (Mel-domain resonant peak smoothing)
 *  6. Phase Scatter (3-stage all-pass phase dispersion network)
 *  7. Stat Normalize (polynomial soft-knee kurtosis shaper)
 *  8. Hash Break (anti-AcoustID micro-warp delay modulation LFO)
 *  9. Room Inject (multi-tap early reflection acoustic space network)
 * 10. Texture Inject (analog harmonic tape/tube saturation exciter)
 * 11. Bandwidth Heal (high-shelf air band restoration EQ)
 * 12. Dynamics Naturalizer (studio feed-forward compressor)
 * 13. Quality Gate (psychoacoustic brickwall safety limiter)
 * 14. Master Gain Staging & A/B Dry/Wet click-free bypass
 */

export class NaSunoDSP {
  constructor() {
    this.ctx = null;
    this.source = null;
    this.destination = null;
    this.isBypassed = false;

    // 1. Stride Remove (172.3 Hz neural frame rate comb filter)
    this.stride1 = null;
    this.stride2 = null;

    // 2. Stego Strip (cepstral echo cancellation)
    this.stegoComb = null;

    // 3. Ultrasonic Carrier Notches (15.5k, 17.5k, 19.5k)
    this.notch1 = null;
    this.notch2 = null;
    this.notch3 = null;

    // 4. Neural Scrub (high-frequency residual filter)
    this.neuralFilter = null;

    // 5. Spectral Blend (Mel-domain resonant peak smoother)
    this.blendFilter1 = null;
    this.blendFilter2 = null;

    // 6. Phase Scatter (3-stage all-pass phase dispersion network)
    this.allpass1 = null;
    this.allpass2 = null;
    this.allpass3 = null;

    // 7. Stat Normalize (polynomial wave shaper)
    this.statShaper = null;

    // 8. Hash Break (anti-AcoustID micro-warp delay + LFO)
    this.hashDelay = null;
    this.hashLfo = null;
    this.hashLfoGain = null;

    // 9. Room Inject (multi-tap early reflection network)
    this.roomSend = null;
    this.roomDelay1 = null;
    this.roomDelay2 = null;
    this.roomFilter = null;
    this.roomReturn = null;
    this.roomMixBus = null;

    // 10. Texture Inject (analog harmonic saturator)
    this.textureShaper = null;

    // 11. Bandwidth Heal (air-band high shelf)
    this.shelf = null;

    // 12. Dynamics Naturalizer (studio compressor)
    this.dynamicsComp = null;

    // 13. Quality Gate (brickwall safety limiter)
    this.qualityLimiter = null;

    // 14. Output Gain, Bypass routing & Dual Analysers (Raw vs Processed)
    this.outGain = null;
    this.wetGain = null;
    this.dryGain = null;
    this.rawAnalyser = null; // Pre-DSP raw audio analyser (faded ghost trace)
    this.analyser = null;    // Post-DSP active evasion analyser (vivid cyan trace)

    // Cache of active parameters
    this.params = {
      carrierErase: 50,
      strideRemove: 35,
      stegoStrip: 45,
      neuralScrub: 45,
      spectralBlend: 40,
      phaseScatter: 40,
      statNormalize: 40,
      hashBreak: 30,
      roomInject: 35,
      textureInject: 35,
      bandwidthHeal: 0.25,
      dynamicsNatural: 40,
      qualityGate: 3,
      outputGain: 0.0,
    };
  }

  /**
   * Generate static polynomial waveshaper curve for soft-knee normalization.
   * Includes peak unity normalization factor to eliminate gain-staging drop and limiter pumping.
   */
  static makeStatCurve(amount = 0.4, n = 2048) {
    const curve = new Float32Array(n);
    const k = Math.max(0, Math.min(1, amount));
    const normFactor = 1 + 0.25 * k;
    for (let i = 0; i < n; i++) {
      const x = (i * 2) / n - 1;
      // Soft saturation that squashes high statistical outliers with unity peak normalization
      curve[i] = (x / (1 + 0.25 * k * Math.abs(x))) * normFactor;
    }
    return curve;
  }

  /**
   * Generate harmonic saturation curve (analog tape/tube exciter).
   */
  static makeTextureCurve(amount = 0.35, n = 2048) {
    const curve = new Float32Array(n);
    const drive = 1.0 + amount * 1.5;
    for (let i = 0; i < n; i++) {
      const x = (i * 2) / n - 1;
      // Asymmetric polynomial creating subtle 2nd and 3rd harmonics
      const driven = x * drive;
      curve[i] = Math.tanh(driven) * (1.0 - 0.05 * amount * (x * x));
    }
    return curve;
  }

  /**
   * Initialize all 14 DSP nodes in the provided AudioContext.
   * @param {AudioContext} ctx
   */
  init(ctx) {
    this.ctx = ctx;
    const now = ctx.currentTime;

    // 1. Stride Remove (172.3 Hz & 344.6 Hz periodic frame harmonic notches - safe high-fidelity cut)
    this.stride1 = ctx.createBiquadFilter();
    this.stride1.type = 'peaking';
    this.stride1.frequency.setValueAtTime(172.3, now);
    this.stride1.Q.setValueAtTime(6.0, now);
    this.stride1.gain.setValueAtTime(-3.5, now);

    this.stride2 = ctx.createBiquadFilter();
    this.stride2.type = 'peaking';
    this.stride2.frequency.setValueAtTime(344.6, now);
    this.stride2.Q.setValueAtTime(7.0, now);
    this.stride2.gain.setValueAtTime(-2.45, now);

    // 2. Stego Strip (Cepstral echo filter at 3800 Hz)
    this.stegoComb = ctx.createBiquadFilter();
    this.stegoComb.type = 'peaking';
    this.stegoComb.frequency.setValueAtTime(3800, now);
    this.stegoComb.Q.setValueAtTime(3.0, now);
    this.stegoComb.gain.setValueAtTime(-3.6, now);

    // 3. Ultrasonic Carrier Notches (15.5k, 17.5k, 19.5k)
    this.notch1 = ctx.createBiquadFilter();
    this.notch1.type = 'notch';
    this.notch1.frequency.setValueAtTime(15500, now);
    this.notch1.Q.setValueAtTime(17.0, now);

    this.notch2 = ctx.createBiquadFilter();
    this.notch2.type = 'notch';
    this.notch2.frequency.setValueAtTime(17500, now);
    this.notch2.Q.setValueAtTime(14.5, now);

    this.notch3 = ctx.createBiquadFilter();
    this.notch3.type = 'notch';
    this.notch3.frequency.setValueAtTime(19500, now);
    this.notch3.Q.setValueAtTime(12.0, now);

    // 4. Neural Scrub (high-frequency residual filter calibrated to preserve musical air)
    this.neuralFilter = ctx.createBiquadFilter();
    this.neuralFilter.type = 'highshelf';
    this.neuralFilter.frequency.setValueAtTime(15400, now);
    this.neuralFilter.gain.setValueAtTime(-5.4, now);

    // 5. Spectral Blend (Mel-domain resonant peak smoother)
    this.blendFilter1 = ctx.createBiquadFilter();
    this.blendFilter1.type = 'peaking';
    this.blendFilter1.frequency.setValueAtTime(4200, now);
    this.blendFilter1.Q.setValueAtTime(2.0, now);
    this.blendFilter1.gain.setValueAtTime(-2.4, now);

    this.blendFilter2 = ctx.createBiquadFilter();
    this.blendFilter2.type = 'peaking';
    this.blendFilter2.frequency.setValueAtTime(7600, now);
    this.blendFilter2.Q.setValueAtTime(2.5, now);
    this.blendFilter2.gain.setValueAtTime(-2.8, now);

    // 6. Phase Scatter (3-stage all-pass phase dispersion network)
    this.allpass1 = ctx.createBiquadFilter();
    this.allpass1.type = 'allpass';
    this.allpass1.frequency.setValueAtTime(850, now);
    this.allpass1.Q.setValueAtTime(1.8, now);

    this.allpass2 = ctx.createBiquadFilter();
    this.allpass2.type = 'allpass';
    this.allpass2.frequency.setValueAtTime(2400, now);
    this.allpass2.Q.setValueAtTime(2.2, now);

    this.allpass3 = ctx.createBiquadFilter();
    this.allpass3.type = 'allpass';
    this.allpass3.frequency.setValueAtTime(6800, now);
    this.allpass3.Q.setValueAtTime(2.6, now);

    // 7. Stat Normalize (polynomial wave shaper)
    this.statShaper = ctx.createWaveShaper();
    this.statShaper.curve = NaSunoDSP.makeStatCurve(0.4);
    this.statShaper.oversample = '2x';

    // 8. Hash Break (anti-AcoustID micro-warp delay + subtle LFO)
    this.hashDelay = ctx.createDelay(0.05);
    this.hashDelay.delayTime.setValueAtTime(0.003, now);

    this.hashLfo = ctx.createOscillator();
    this.hashLfo.type = 'sine';
    this.hashLfo.frequency.setValueAtTime(0.415, now);

    this.hashLfoGain = ctx.createGain();
    this.hashLfoGain.gain.setValueAtTime(0.00061, now); // ~0.61ms safe micro-warp

    this.hashLfo.connect(this.hashLfoGain);
    this.hashLfoGain.connect(this.hashDelay.delayTime);
    try {
      this.hashLfo.start(now);
    } catch (_) {}

    // 9. Room Inject (multi-tap early reflection acoustic space network - subtle room ambiance)
    this.roomSend = ctx.createGain();
    this.roomSend.gain.setValueAtTime(1.0, now);

    this.roomDelay1 = ctx.createDelay(0.1);
    this.roomDelay1.delayTime.setValueAtTime(0.016, now); // 16ms early tap

    this.roomDelay2 = ctx.createDelay(0.1);
    this.roomDelay2.delayTime.setValueAtTime(0.031, now); // 31ms second tap

    this.roomFilter = ctx.createBiquadFilter();
    this.roomFilter.type = 'lowpass';
    this.roomFilter.frequency.setValueAtTime(4200, now);

    this.roomReturn = ctx.createGain();
    this.roomReturn.gain.setValueAtTime(0.0875, now); // 8.75% subtle room injection

    this.roomMixBus = ctx.createGain();
    this.roomMixBus.gain.setValueAtTime(1.0, now);

    // 10. Texture Inject (analog harmonic tape/tube saturation exciter)
    this.textureShaper = ctx.createWaveShaper();
    this.textureShaper.curve = NaSunoDSP.makeTextureCurve(0.35);
    this.textureShaper.oversample = '2x';

    // 11. Bandwidth Heal (air-band high shelf)
    this.shelf = ctx.createBiquadFilter();
    this.shelf.type = 'highshelf';
    this.shelf.frequency.setValueAtTime(12000, now);
    this.shelf.gain.setValueAtTime(0.25, now);

    // 12. Dynamics Naturalizer (studio feed-forward compressor - transparent bus dynamics)
    this.dynamicsComp = ctx.createDynamicsCompressor();
    this.dynamicsComp.threshold.setValueAtTime(-13.2, now);
    this.dynamicsComp.knee.setValueAtTime(10.0, now);
    this.dynamicsComp.ratio.setValueAtTime(2.5, now);
    this.dynamicsComp.attack.setValueAtTime(0.025, now);
    this.dynamicsComp.release.setValueAtTime(0.14, now);

    // 13. Quality Gate (brickwall safety limiter preventing digital overs)
    this.qualityLimiter = ctx.createDynamicsCompressor();
    this.qualityLimiter.threshold.setValueAtTime(-0.8, now);
    this.qualityLimiter.knee.setValueAtTime(0.0, now); // hard knee
    this.qualityLimiter.ratio.setValueAtTime(20.0, now); // brickwall
    this.qualityLimiter.attack.setValueAtTime(0.003, now);
    this.qualityLimiter.release.setValueAtTime(0.05, now);

    // 14. Output Gain & Bypass routing
    this.outGain = ctx.createGain();
    this.outGain.gain.setValueAtTime(1.0, now); // 0 dB

    this.wetGain = ctx.createGain();
    this.wetGain.gain.setValueAtTime(1.0, now);

    this.dryGain = ctx.createGain();
    this.dryGain.gain.setValueAtTime(0.0, now);

    // Dual Spectrum Analysers (Raw Input Ghost Trace & Processed Active Trace)
    this.rawAnalyser = ctx.createAnalyser();
    this.rawAnalyser.fftSize = 2048;
    this.rawAnalyser.smoothingTimeConstant = 0.8;

    this.analyser = ctx.createAnalyser();
    this.analyser.fftSize = 2048;
    this.analyser.smoothingTimeConstant = 0.8;
  }

  /**
   * Connect an audio source to the complete DSP cascade and destination.
   * @param {AudioNode} sourceNode
   * @param {AudioNode} destinationNode
   */
  connect(sourceNode, destinationNode) {
    this.source = sourceNode;
    this.destination = destinationNode;

    // Route raw pre-DSP signal to rawAnalyser for real-time visual comparison
    sourceNode.connect(this.rawAnalyser);

    // --- WET CHAIN ---
    // Source -> Stride 1 -> Stride 2
    sourceNode.connect(this.stride1);
    this.stride1.connect(this.stride2);

    // -> Stego Comb
    this.stride2.connect(this.stegoComb);

    // -> Ultrasonic Carrier Notches (15.5k -> 17.5k -> 19.5k)
    this.stegoComb.connect(this.notch1);
    this.notch1.connect(this.notch2);
    this.notch2.connect(this.notch3);

    // -> Neural Scrub Filter
    this.notch3.connect(this.neuralFilter);

    // -> Spectral Blend Peaking Filters
    this.neuralFilter.connect(this.blendFilter1);
    this.blendFilter1.connect(this.blendFilter2);

    // -> Phase Scatter (All-Pass Cascade)
    this.blendFilter2.connect(this.allpass1);
    this.allpass1.connect(this.allpass2);
    this.allpass2.connect(this.allpass3);

    // -> Stat Normalize (Polynomial WaveShaper)
    this.allpass3.connect(this.statShaper);

    // -> Hash Break (Micro-warp Delay)
    this.statShaper.connect(this.hashDelay);

    // -> Room Inject parallel branch:
    //    Direct path to roomMixBus
    this.hashDelay.connect(this.roomMixBus);
    //    Parallel reflection path:
    this.hashDelay.connect(this.roomSend);
    this.roomSend.connect(this.roomDelay1);
    this.roomDelay1.connect(this.roomDelay2);
    this.roomDelay2.connect(this.roomFilter);
    this.roomFilter.connect(this.roomReturn);
    this.roomReturn.connect(this.roomMixBus);

    // -> Texture Inject (Harmonic Saturation)
    this.roomMixBus.connect(this.textureShaper);

    // -> Bandwidth Heal (Air-band High Shelf)
    this.textureShaper.connect(this.shelf);

    // -> Dynamics Naturalizer Compressor
    this.shelf.connect(this.dynamicsComp);

    // -> Quality Gate Brickwall Limiter
    this.dynamicsComp.connect(this.qualityLimiter);

    // -> Wet Gain -> Master Output Gain
    this.qualityLimiter.connect(this.wetGain);
    this.wetGain.connect(this.outGain);

    // --- DRY CHAIN (for click-free A/B bypass) ---
    sourceNode.connect(this.dryGain);
    this.dryGain.connect(this.outGain);

    // Master Output -> Analyser -> Destination Speakers
    this.outGain.connect(this.analyser);
    this.analyser.connect(destinationNode);
  }

  /**
   * Update real-time DSP parameters smoothly from a specific composite knob.
   * Zero delay: applies immediately with 25ms smoothing to prevent clicks.
   * @param {string} knobId
   * @param {number} val
   * @param {Object} rawUpdates
   */
  updateFromKnob(knobId, val, rawUpdates = {}) {
    if (!this.ctx) return;
    this.params[knobId] = val;
    const now = this.ctx.currentTime;
    const ramp = 0.025; // 25ms click-free audio automation

    switch (knobId) {
      case 'carrierErase': {
        const norm = val / 100;
        // Wide delta: Q widens down to 2.2 at 100% (broad notch sweep), 28.0 at 0% (surgical)
        const q1 = 28.0 - 25.5 * norm;
        const q2 = 24.0 - 21.5 * norm;
        const q3 = 20.0 - 18.0 * norm;
        if (this.notch1) this.notch1.Q.setTargetAtTime(q1, now, ramp);
        if (this.notch2) this.notch2.Q.setTargetAtTime(q2, now, ramp);
        if (this.notch3) this.notch3.Q.setTargetAtTime(q3, now, ramp);
        break;
      }
      case 'strideRemove': {
        const norm = val / 100;
        // Calibrated cuts from 0 dB down to -10 dB on 172.3 Hz & -7 dB on 344.6 Hz (preserves bass body)
        const cut1 = 0.0 - 10.0 * norm;
        const cut2 = 0.0 - 7.0 * norm;
        if (this.stride1) this.stride1.gain.setTargetAtTime(cut1, now, ramp);
        if (this.stride2) this.stride2.gain.setTargetAtTime(cut2, now, ramp);
        break;
      }
      case 'stegoStrip': {
        const norm = val / 100;
        // De-echo comb cut calibrated from 0 dB down to -8 dB (preserves ear-canal resonance presence)
        const cut = 0.0 - 8.0 * norm;
        if (this.stegoComb) this.stegoComb.gain.setTargetAtTime(cut, now, ramp);
        break;
      }
      case 'neuralScrub': {
        const norm = val / 100;
        // High-shelf cutoff sweeps 19 kHz down to 11 kHz, and cut from 0 dB down to -12 dB (preserves air & cymbals)
        const freq = 19000 - 8000 * norm;
        const cut = 0.0 - 12.0 * norm;
        if (this.neuralFilter) {
          this.neuralFilter.frequency.setTargetAtTime(freq, now, ramp);
          this.neuralFilter.gain.setTargetAtTime(cut, now, ramp);
        }
        break;
      }
      case 'spectralBlend': {
        const norm = val / 100;
        // Resonant peak cuts from 0 dB down to -6 dB and -7 dB (smooths unnatural Mel spikes without scooping)
        const cut1 = 0.0 - 6.0 * norm;
        const cut2 = 0.0 - 7.0 * norm;
        if (this.blendFilter1) this.blendFilter1.gain.setTargetAtTime(cut1, now, ramp);
        if (this.blendFilter2) this.blendFilter2.gain.setTargetAtTime(cut2, now, ramp);
        break;
      }
      case 'phaseScatter': {
        const norm = val / 100;
        // Allpass Q scales from 0.5 up to 8.5 for intense spatial phase dispersion
        const q1 = 0.5 + 7.5 * norm;
        const q2 = 0.8 + 8.0 * norm;
        const q3 = 1.0 + 8.5 * norm;
        if (this.allpass1) this.allpass1.Q.setTargetAtTime(q1, now, ramp);
        if (this.allpass2) this.allpass2.Q.setTargetAtTime(q2, now, ramp);
        if (this.allpass3) this.allpass3.Q.setTargetAtTime(q3, now, ramp);
        break;
      }
      case 'statNormalize': {
        const norm = val / 100;
        if (this.statShaper) {
          // Polynomial wave shaper saturation amount with unity peak normalization
          this.statShaper.curve = NaSunoDSP.makeStatCurve(norm);
        }
        break;
      }
      case 'hashBreak': {
        const norm = val / 100;
        // Delay modulation depth from 0.0001s up to 0.0018s (~1.8ms) & LFO speed 0.25 to 0.8 Hz (avoids flutter/wow)
        const depth = 0.0001 + 0.0017 * norm;
        const rate = 0.25 + 0.55 * norm;
        if (this.hashLfoGain) this.hashLfoGain.gain.setTargetAtTime(depth, now, ramp);
        if (this.hashLfo) this.hashLfo.frequency.setTargetAtTime(rate, now, ramp);
        break;
      }
      case 'roomInject': {
        const norm = val / 100;
        // Wet reflection mix from 0.0 (dry) up to 0.25 (subtle room ambiance without slap echo)
        const wet = 0.0 + 0.25 * norm;
        if (this.roomReturn) this.roomReturn.gain.setTargetAtTime(wet, now, ramp);
        break;
      }
      case 'textureInject': {
        const norm = val / 100;
        if (this.textureShaper) {
          // Drive scales for warm analog saturation
          this.textureShaper.curve = NaSunoDSP.makeTextureCurve(norm);
        }
        break;
      }
      case 'bandwidthHeal': {
        // Air band shelf gain from -6 dB up to +6 dB at 12 kHz
        const gain = val;
        if (this.shelf) this.shelf.gain.setTargetAtTime(gain, now, ramp);
        break;
      }
      case 'dynamicsNatural': {
        const norm = val / 100;
        // Threshold from -6 dB down to -24 dB, ratio from 1.5:1 up to 4:1 (preserves transient punch & dynamic range)
        const thresh = -6.0 - 18.0 * norm;
        const ratio = 1.5 + 2.5 * norm;
        if (this.dynamicsComp) {
          this.dynamicsComp.threshold.setTargetAtTime(thresh, now, ramp);
          this.dynamicsComp.ratio.setTargetAtTime(ratio, now, ramp);
        }
        break;
      }
      case 'qualityGate': {
        const lvl = Math.max(1, Math.min(5, val));
        const thresh = -0.2 - 0.45 * lvl; // -0.65 dB down to -2.45 dB brickwall ceiling
        if (this.qualityLimiter) this.qualityLimiter.threshold.setTargetAtTime(thresh, now, ramp);
        break;
      }
      case 'outputGain': {
        const gainLinear = Math.pow(10, (val * 1.2) / 20); // clean output staging
        if (this.outGain) this.outGain.gain.setTargetAtTime(gainLinear, now, ramp);
        break;
      }
    }
  }

  /**
   * Update real-time DSP immediately when a raw parameter is edited in Advanced Mode.
   * Directly routes the low-level parameter to the respective DSP AudioParam.
   * @param {string} rawKey
   * @param {number} val
   */
  updateFromRawKey(rawKey, val) {
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const ramp = 0.025;

    if (rawKey === 'classical.carrier_notch_q') {
      const q = Math.max(2.0, Math.min(65.0, val * 0.5));
      if (this.notch1) this.notch1.Q.setTargetAtTime(q, now, ramp);
      if (this.notch2) this.notch2.Q.setTargetAtTime(q * 0.85, now, ramp);
      if (this.notch3) this.notch3.Q.setTargetAtTime(q * 0.7, now, ramp);
    } else if (rawKey === 'upsampler.max_cut_db') {
      const safeCut = Math.min(10.0, val);
      if (this.stride1) this.stride1.gain.setTargetAtTime(-safeCut, now, ramp);
      if (this.stride2) this.stride2.gain.setTargetAtTime(-safeCut * 0.7, now, ramp);
    } else if (rawKey === 'classical.max_echo_cut_db') {
      const safeCut = Math.min(8.0, val * 0.45);
      if (this.stegoComb) this.stegoComb.gain.setTargetAtTime(-safeCut, now, ramp);
    } else if (rawKey === 'neural_residual.high_freq_damping') {
      const cut = -Math.min(12.0, val * 15); // safe air damping
      if (this.neuralFilter) this.neuralFilter.gain.setTargetAtTime(cut, now, ramp);
    } else if (rawKey === 'mel_domain.blend_ratio_max') {
      const cut = -Math.min(6.0, val * 8);
      if (this.blendFilter1) this.blendFilter1.gain.setTargetAtTime(cut, now, ramp);
      if (this.blendFilter2) this.blendFilter2.gain.setTargetAtTime(cut * 0.9, now, ramp);
    } else if (rawKey === 'phase_decorrelate.steady_state_dispersion_max') {
      const q = 0.5 + val * 12;
      if (this.allpass1) this.allpass1.Q.setTargetAtTime(q, now, ramp);
      if (this.allpass2) this.allpass2.Q.setTargetAtTime(q * 1.2, now, ramp);
      if (this.allpass3) this.allpass3.Q.setTargetAtTime(q * 1.4, now, ramp);
    } else if (rawKey === 'distribution_noise_level') {
      const norm = Math.min(1.0, val * 100);
      if (this.statShaper) this.statShaper.curve = NaSunoDSP.makeStatCurve(norm);
    } else if (rawKey === 'hash_disrupt.base_cents') {
      const depth = Math.max(0.0001, Math.min(0.0018, (val / 100) * 0.018));
      if (this.hashLfoGain) this.hashLfoGain.gain.setTargetAtTime(depth, now, ramp);
    } else if (rawKey === 'hash_disrupt.wow_rate_hz') {
      const safeRate = Math.min(0.8, val);
      if (this.hashLfo) this.hashLfo.frequency.setTargetAtTime(safeRate, now, ramp);
    } else if (rawKey === 'environment.early_reflection_level') {
      const safeWet = Math.min(0.25, val);
      if (this.roomReturn) this.roomReturn.gain.setTargetAtTime(safeWet, now, ramp);
    } else if (rawKey === 'harmonic_distortion_amount') {
      const norm = Math.min(1.0, val * 100);
      if (this.textureShaper) this.textureShaper.curve = NaSunoDSP.makeTextureCurve(norm);
    } else if (rawKey === 'mastering.air_gain_db_max') {
      if (this.shelf) this.shelf.gain.setTargetAtTime(val, now, ramp);
    } else if (rawKey === 'dynamics.compressor_threshold_db') {
      const safeThresh = Math.max(-24.0, val);
      if (this.dynamicsComp) this.dynamicsComp.threshold.setTargetAtTime(safeThresh, now, ramp);
    } else if (rawKey === 'dynamics.compressor_ratio') {
      const safeRatio = Math.min(4.0, val);
      if (this.dynamicsComp) this.dynamicsComp.ratio.setTargetAtTime(safeRatio, now, ramp);
    } else if (rawKey === 'firewall.brickwall_ceiling_db') {
      if (this.qualityLimiter) this.qualityLimiter.threshold.setTargetAtTime(val, now, ramp);
    }
  }

  /**
   * Bulk-update all 14 DSP nodes from the full state dictionary.
   * @param {Object} compositeValues
   * @param {Object} rawState
   */
  updateAllFromState(compositeValues = {}, rawState = {}) {
    for (const [knobId, val] of Object.entries(compositeValues)) {
      this.updateFromKnob(knobId, val);
    }
    for (const [rawKey, val] of Object.entries(rawState)) {
      this.updateFromRawKey(rawKey, val);
    }
  }

  /**
   * Toggle A/B Bypass cleanly with 30ms ramp.
   * @param {boolean} bypass
   */
  setBypass(bypass) {
    this.isBypassed = !!bypass;
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const rampTime = 0.03;

    if (this.isBypassed) {
      this.wetGain.gain.setTargetAtTime(0.0, now, rampTime);
      this.dryGain.gain.setTargetAtTime(1.0, now, rampTime);
    } else {
      this.wetGain.gain.setTargetAtTime(1.0, now, rampTime);
      this.dryGain.gain.setTargetAtTime(0.0, now, rampTime);
    }
  }

  /**
   * Disconnect all nodes safely.
   */
  disconnect() {
    try {
      if (this.source) this.source.disconnect();
      if (this.stride1) this.stride1.disconnect();
      if (this.stride2) this.stride2.disconnect();
      if (this.stegoComb) this.stegoComb.disconnect();
      if (this.notch1) this.notch1.disconnect();
      if (this.notch2) this.notch2.disconnect();
      if (this.notch3) this.notch3.disconnect();
      if (this.neuralFilter) this.neuralFilter.disconnect();
      if (this.blendFilter1) this.blendFilter1.disconnect();
      if (this.blendFilter2) this.blendFilter2.disconnect();
      if (this.allpass1) this.allpass1.disconnect();
      if (this.allpass2) this.allpass2.disconnect();
      if (this.allpass3) this.allpass3.disconnect();
      if (this.statShaper) this.statShaper.disconnect();
      if (this.hashDelay) this.hashDelay.disconnect();
      if (this.roomSend) this.roomSend.disconnect();
      if (this.roomDelay1) this.roomDelay1.disconnect();
      if (this.roomDelay2) this.roomDelay2.disconnect();
      if (this.roomFilter) this.roomFilter.disconnect();
      if (this.roomReturn) this.roomReturn.disconnect();
      if (this.roomMixBus) this.roomMixBus.disconnect();
      if (this.textureShaper) this.textureShaper.disconnect();
      if (this.shelf) this.shelf.disconnect();
      if (this.dynamicsComp) this.dynamicsComp.disconnect();
      if (this.qualityLimiter) this.qualityLimiter.disconnect();
      if (this.wetGain) this.wetGain.disconnect();
      if (this.dryGain) this.dryGain.disconnect();
      if (this.outGain) this.outGain.disconnect();
      if (this.rawAnalyser) this.rawAnalyser.disconnect();
      if (this.analyser) this.analyser.disconnect();
    } catch (_) {}
  }

  /**
   * Export processed AudioBuffer to 16-bit PCM WAV using OfflineAudioContext.
   * Runs the complete 14-node processing cascade offline with current settings,
   * or exports pristine unadulterated PCM directly if in bypass mode.
   * @param {AudioBuffer} audioBuffer
   * @param {Object} params - knob and raw parameter settings
   * @param {boolean} isBypassed - if true, skips wet cascade and encodes raw PCM
   * @returns {Promise<Blob>}
   */
  static async exportWAV(audioBuffer, params = {}, isBypassed = false) {
    if (isBypassed || params.bypass) {
      return this.encodeWAV(audioBuffer);
    }

    const numChannels = audioBuffer.numberOfChannels;
    const length = audioBuffer.length;
    const sampleRate = audioBuffer.sampleRate;

    const offlineCtx = new OfflineAudioContext(numChannels, length, sampleRate);
    const source = offlineCtx.createBufferSource();
    source.buffer = audioBuffer;

    // 1. Stride Notches (Safe cuts: -10 dB on 172.3 Hz & -7 dB on 344.6 Hz)
    const sNorm = (params.strideRemove ?? 35) / 100;
    const s1 = offlineCtx.createBiquadFilter();
    s1.type = 'peaking';
    s1.frequency.value = 172.3;
    s1.Q.value = 6.0;
    s1.gain.value = 0.0 - 10.0 * sNorm;

    const s2 = offlineCtx.createBiquadFilter();
    s2.type = 'peaking';
    s2.frequency.value = 344.6;
    s2.Q.value = 7.0;
    s2.gain.value = 0.0 - 7.0 * sNorm;

    // 2. Stego Comb (De-echo comb cut up to -8 dB)
    const stegoNorm = (params.stegoStrip ?? 45) / 100;
    const stegoComb = offlineCtx.createBiquadFilter();
    stegoComb.type = 'peaking';
    stegoComb.frequency.value = 3800;
    stegoComb.Q.value = 3.0;
    stegoComb.gain.value = 0.0 - 8.0 * stegoNorm;

    // 3. Ultrasonic Carriers (Q widens from 28 down to 2.2 for broad notch sweeps)
    const cNorm = (params.carrierErase ?? 50) / 100;
    const n1 = offlineCtx.createBiquadFilter();
    n1.type = 'notch';
    n1.frequency.value = 15500;
    n1.Q.value = 28.0 - 25.5 * cNorm;

    const n2 = offlineCtx.createBiquadFilter();
    n2.type = 'notch';
    n2.frequency.value = 17500;
    n2.Q.value = 24.0 - 21.5 * cNorm;

    const n3 = offlineCtx.createBiquadFilter();
    n3.type = 'notch';
    n3.frequency.value = 19500;
    n3.Q.value = 20.0 - 18.0 * cNorm;

    // 4. Neural Scrub (Sweeps 19 kHz down to 11 kHz, cut up to -12 dB)
    const neuralNorm = (params.neuralScrub ?? 45) / 100;
    const neuralFilter = offlineCtx.createBiquadFilter();
    neuralFilter.type = 'highshelf';
    neuralFilter.frequency.value = 19000 - 8000 * neuralNorm;
    neuralFilter.gain.value = 0.0 - 12.0 * neuralNorm;

    // 5. Spectral Blend (Resonant peak attenuation up to -6 dB and -7 dB)
    const blendNorm = (params.spectralBlend ?? 40) / 100;
    const b1 = offlineCtx.createBiquadFilter();
    b1.type = 'peaking';
    b1.frequency.value = 4200;
    b1.Q.value = 2.0;
    b1.gain.value = 0.0 - 6.0 * blendNorm;

    const b2 = offlineCtx.createBiquadFilter();
    b2.type = 'peaking';
    b2.frequency.value = 7600;
    b2.Q.value = 2.5;
    b2.gain.value = 0.0 - 7.0 * blendNorm;

    // 6. Phase Scatter All-Pass Cascade (Q up to 8.5 for intense phase dispersion)
    const pNorm = (params.phaseScatter ?? 40) / 100;
    const ap1 = offlineCtx.createBiquadFilter();
    ap1.type = 'allpass';
    ap1.frequency.value = 850;
    ap1.Q.value = 0.5 + 7.5 * pNorm;

    const ap2 = offlineCtx.createBiquadFilter();
    ap2.type = 'allpass';
    ap2.frequency.value = 2400;
    ap2.Q.value = 0.8 + 8.0 * pNorm;

    const ap3 = offlineCtx.createBiquadFilter();
    ap3.type = 'allpass';
    ap3.frequency.value = 6800;
    ap3.Q.value = 1.0 + 8.5 * pNorm;

    // 7. Stat Normalize WaveShaper (Saturation with unity peak normalization)
    const statNorm = (params.statNormalize ?? 40) / 100;
    const statShaper = offlineCtx.createWaveShaper();
    statShaper.curve = NaSunoDSP.makeStatCurve(statNorm);

    // 8. Hash Break (Micro-warp delay offset up to 1.8ms)
    const hashNorm = (params.hashBreak ?? 30) / 100;
    const hashDelay = offlineCtx.createDelay(0.05);
    hashDelay.delayTime.value = 0.0001 + 0.0017 * hashNorm;

    // 9. Room Inject (Early reflection acoustic network - subtle room ambiance)
    const rNorm = (params.roomInject ?? 35) / 100;
    const roomSend = offlineCtx.createGain();
    roomSend.gain.value = 1.0;
    const roomDelay1 = offlineCtx.createDelay(0.1);
    roomDelay1.delayTime.value = 0.016;
    const roomDelay2 = offlineCtx.createDelay(0.1);
    roomDelay2.delayTime.value = 0.031;
    const roomFilter = offlineCtx.createBiquadFilter();
    roomFilter.type = 'lowpass';
    roomFilter.frequency.value = 4200;
    const roomReturn = offlineCtx.createGain();
    roomReturn.gain.value = 0.0 + 0.25 * rNorm;
    const roomMixBus = offlineCtx.createGain();
    roomMixBus.gain.value = 1.0;

    // 10. Texture Inject WaveShaper (Warm tape/tube drive)
    const texNorm = (params.textureInject ?? 35) / 100;
    const textureShaper = offlineCtx.createWaveShaper();
    textureShaper.curve = NaSunoDSP.makeTextureCurve(texNorm);

    // 11. Bandwidth Heal Shelf (Air band gain at 12 kHz)
    const shelf = offlineCtx.createBiquadFilter();
    shelf.type = 'highshelf';
    shelf.frequency.value = 12000;
    shelf.gain.value = params.bandwidthHeal ?? 0.25;

    // 12. Dynamics Compressor (Threshold down to -24 dB, ratio up to 4:1)
    const dynNorm = (params.dynamicsNatural ?? 40) / 100;
    const dynComp = offlineCtx.createDynamicsCompressor();
    dynComp.threshold.value = -6.0 - 18.0 * dynNorm;
    dynComp.ratio.value = 1.5 + 2.5 * dynNorm;
    dynComp.attack.value = 0.025;
    dynComp.release.value = 0.14;

    // 13. Quality Limiter (Ceiling down to -2.45 dB)
    const qLvl = Math.max(1, Math.min(5, params.qualityGate ?? 3));
    const limiter = offlineCtx.createDynamicsCompressor();
    limiter.threshold.value = -0.2 - 0.45 * qLvl;
    limiter.ratio.value = 20.0;
    limiter.attack.value = 0.003;
    limiter.release.value = 0.05;

    // 14. Master Gain
    const outGain = offlineCtx.createGain();
    const gainLinear = Math.pow(10, ((params.outputGain ?? 0.0) * 1.2) / 20);
    outGain.gain.value = gainLinear;

    // Wire complete 14-node cascade in OfflineContext
    source.connect(s1);
    s1.connect(s2);
    s2.connect(stegoComb);
    stegoComb.connect(n1);
    n1.connect(n2);
    n2.connect(n3);
    n3.connect(neuralFilter);
    neuralFilter.connect(b1);
    b1.connect(b2);
    b2.connect(ap1);
    ap1.connect(ap2);
    ap2.connect(ap3);
    ap3.connect(statShaper);
    statShaper.connect(hashDelay);

    // Room Inject parallel branch
    hashDelay.connect(roomMixBus);
    hashDelay.connect(roomSend);
    roomSend.connect(roomDelay1);
    roomDelay1.connect(roomDelay2);
    roomDelay2.connect(roomFilter);
    roomFilter.connect(roomReturn);
    roomReturn.connect(roomMixBus);

    // Continue wet chain through texture, shelf, dynamics, limiter, master gain
    roomMixBus.connect(textureShaper);
    textureShaper.connect(shelf);
    shelf.connect(dynComp);
    dynComp.connect(limiter);
    limiter.connect(outGain);
    outGain.connect(offlineCtx.destination);

    source.start(0);

    const renderedBuffer = await offlineCtx.startRendering();
    return this.encodeWAV(renderedBuffer);
  }

  /**
   * Encode AudioBuffer into 16-bit PCM WAV Blob.
   * @param {AudioBuffer} buffer
   * @returns {Blob}
   */
  static encodeWAV(buffer) {
    const numChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const numSamples = buffer.length;
    const bytesPerSample = 2; // 16-bit
    const blockAlign = numChannels * bytesPerSample;
    const byteRate = sampleRate * blockAlign;
    const dataSize = numSamples * blockAlign;
    const headerSize = 44;
    const totalSize = headerSize + dataSize;

    const arrayBuffer = new ArrayBuffer(totalSize);
    const view = new DataView(arrayBuffer);

    // RIFF chunk descriptor
    this.writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    this.writeString(view, 8, 'WAVE');

    // "fmt " sub-chunk
    this.writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true); // 16-bit

    // "data" sub-chunk
    this.writeString(view, 36, 'data');
    view.setUint32(40, dataSize, true);

    // Write interleaved 16-bit PCM samples
    const channels = [];
    for (let c = 0; c < numChannels; c++) {
      channels.push(buffer.getChannelData(c));
    }

    let offset = 44;
    for (let i = 0; i < numSamples; i++) {
      for (let c = 0; c < numChannels; c++) {
        let sample = channels[c][i];
        sample = Math.max(-1, Math.min(1, sample));
        const intSample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
        view.setInt16(offset, intSample, true);
        offset += 2;
      }
    }

    return new Blob([arrayBuffer], { type: 'audio/wav' });
  }

  static writeString(view, offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }
}
