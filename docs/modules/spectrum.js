/**
 * Real-Time Logarithmic Spectrum Canvas Renderer
 * High-precision 20 Hz - 22.05 kHz logarithmic FFT visualizer with carrier watermark zones.
 * Pure real data from Web Audio AnalyserNodes — zero synthetic sine simulations.
 * Dual-Trace Overlay:
 *   - Faded Ghost Trace (Amber/Orange): Raw, unprocessed pre-DSP audio
 *   - Live Evasion Trace (Cyan/Blue): Active real-time DSP processed audio
 */

export class SpectrumRenderer {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.getAudioCtx = options.getAudioCtx || (() => null);
    this.getDSP = options.getDSP || (() => null);
    this.getIsPlaying = options.getIsPlaying || (() => false);

    this.minFreq = 20;
    this.maxFreq = 22050;
    this.minDB = -100;
    this.maxDB = 0;

    this.rawFreqData = null;
    this.procFreqData = null;
    this.animId = null;
    this.isRunning = false;

    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.displayWidth = rect.width;
    this.displayHeight = rect.height;
  }

  freqToX(freq, width) {
    const minLog = Math.log10(this.minFreq);
    const maxLog = Math.log10(this.maxFreq);
    const fLog = Math.log10(Math.max(this.minFreq, Math.min(this.maxFreq, freq)));
    return ((fLog - minLog) / (maxLog - minLog)) * width;
  }

  xToFreq(x, width) {
    const minLog = Math.log10(this.minFreq);
    const maxLog = Math.log10(this.maxFreq);
    return Math.pow(10, minLog + (x / width) * (maxLog - minLog));
  }

  dbToY(db, height) {
    const clamped = Math.max(this.minDB, Math.min(this.maxDB, db));
    return (1 - (clamped - this.minDB) / (this.maxDB - this.minDB)) * height;
  }

  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    const render = () => {
      if (!this.isRunning) return;
      this.draw();
      this.animId = requestAnimationFrame(render);
    };
    this.animId = requestAnimationFrame(render);
  }

  stop() {
    this.isRunning = false;
    if (this.animId) {
      cancelAnimationFrame(this.animId);
      this.animId = null;
    }
  }

  calculatePoints(freqData, binCount, sr, width, height) {
    const binHz = sr / (binCount * 2);
    const points = [];
    const step = 2; // Sample every 2 display pixels for 60fps high precision
    for (let x = 0; x <= width; x += step) {
      const f = this.xToFreq(x, width);
      const k = f / binHz;
      const kLo = Math.floor(k);
      const kHi = Math.min(binCount - 1, Math.ceil(k));
      const frac = k - kLo;

      let dbVal = -100;
      if (kLo < binCount) {
        const valLo = freqData[kLo];
        const valHi = freqData[kHi];
        dbVal = valLo * (1 - frac) + valHi * frac;
      }

      const y = this.dbToY(dbVal, height);
      points.push({ x, y });
    }
    return points;
  }

  draw() {
    const ctx = this.ctx;
    const width = this.displayWidth;
    const height = this.displayHeight;
    const dsp = this.getDSP();
    const audioCtx = this.getAudioCtx();
    const isPlaying = this.getIsPlaying();

    // 1. Clear background
    ctx.fillStyle = '#090b0e';
    ctx.fillRect(0, 0, width, height);

    // 2. Horizontal dB grid lines
    ctx.lineWidth = 1;
    ctx.strokeStyle = '#181e26';
    ctx.fillStyle = '#4a5362';
    ctx.font = '9px "JetBrains Mono", monospace';
    ctx.textAlign = 'left';

    const dbTicks = [0, -20, -40, -60, -80];
    for (const db of dbTicks) {
      const y = this.dbToY(db, height);
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
      ctx.fillText(`${db} dB`, 8, y - 3);
    }

    // 3. Vertical frequency grid lines
    const freqTicks = [
      { f: 50, label: '50' },
      { f: 100, label: '100' },
      { f: 250, label: '250' },
      { f: 500, label: '500' },
      { f: 1000, label: '1k' },
      { f: 2500, label: '2.5k' },
      { f: 5000, label: '5k' },
      { f: 10000, label: '10k' },
      { f: 15000, label: '15k' },
      { f: 20000, label: '20k' },
    ];

    ctx.textAlign = 'center';
    for (const tick of freqTicks) {
      const x = this.freqToX(tick.f, width);
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
      ctx.fillText(tick.label, x, height - 6);
    }

    // 4. Highlight AI carrier watermark zones (15.5k, 17.5k, 19.5k)
    const carrierBands = [
      { lo: 15000, hi: 16000, label: '15.5k' },
      { lo: 17000, hi: 18000, label: '17.5k' },
      { lo: 19000, hi: 20000, label: '19.5k' },
    ];
    for (const b of carrierBands) {
      const xLo = this.freqToX(b.lo, width);
      const xHi = this.freqToX(b.hi, width);
      ctx.fillStyle = 'rgba(255, 118, 25, 0.06)';
      ctx.fillRect(xLo, 0, xHi - xLo, height);

      ctx.strokeStyle = 'rgba(255, 118, 25, 0.25)';
      ctx.setLineDash([2, 4]);
      ctx.beginPath();
      ctx.moveTo((xLo + xHi) / 2, 0);
      ctx.lineTo((xLo + xHi) / 2, height - 16);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // 5. Dual Spectrum Curves (Ghost Original vs Live Processed)
    if (isPlaying && dsp && audioCtx) {
      const sr = audioCtx.sampleRate;

      // Allocate buffers if needed
      const binCount = dsp.analyser ? dsp.analyser.frequencyBinCount : 1024;
      if (!this.procFreqData || this.procFreqData.length !== binCount) {
        this.procFreqData = new Float32Array(binCount);
      }
      if (!this.rawFreqData || this.rawFreqData.length !== binCount) {
        this.rawFreqData = new Float32Array(binCount);
      }

      // --- TRACE A: FADED AI ORIGINAL SPECTRUM (RAW PRE-DSP - GLOWING BLUE) ---
      if (dsp.rawAnalyser) {
        dsp.rawAnalyser.getFloatFrequencyData(this.rawFreqData);
        const rawPoints = this.calculatePoints(this.rawFreqData, binCount, sr, width, height);

        // Faint Cyan Underglow (AI)
        ctx.beginPath();
        ctx.moveTo(0, height);
        for (let i = 0; i < rawPoints.length; i++) {
          ctx.lineTo(rawPoints[i].x, rawPoints[i].y);
        }
        ctx.lineTo(width, height);
        ctx.closePath();
        const rawGrad = ctx.createLinearGradient(0, 0, 0, height);
        rawGrad.addColorStop(0, 'rgba(0, 229, 255, 0.15)');
        rawGrad.addColorStop(0.5, 'rgba(0, 229, 255, 0.04)');
        rawGrad.addColorStop(1, 'rgba(0, 229, 255, 0.0)');
        ctx.fillStyle = rawGrad;
        ctx.fill();

        // Faded Cyan Dashed Reference Stroke (AI Raw)
        ctx.lineWidth = 1.3;
        ctx.strokeStyle = 'rgba(0, 229, 255, 0.65)';
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        for (let i = 0; i < rawPoints.length; i++) {
          if (i === 0) ctx.moveTo(rawPoints[i].x, rawPoints[i].y);
          else ctx.lineTo(rawPoints[i].x, rawPoints[i].y);
        }
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // --- TRACE B: VIVID ORANGE HUMANIZED SPECTRUM (POST-DSP - GLOWING ORANGE) ---
      if (dsp.analyser) {
        dsp.analyser.getFloatFrequencyData(this.procFreqData);
        const procPoints = this.calculatePoints(this.procFreqData, binCount, sr, width, height);

        // Vivid Orange Gradient Underglow (Humanized)
        ctx.beginPath();
        ctx.moveTo(0, height);
        for (let i = 0; i < procPoints.length; i++) {
          ctx.lineTo(procPoints[i].x, procPoints[i].y);
        }
        ctx.lineTo(width, height);
        ctx.closePath();
        const procGrad = ctx.createLinearGradient(0, 0, 0, height);
        procGrad.addColorStop(0, 'rgba(255, 122, 0, 0.35)');
        procGrad.addColorStop(0.5, 'rgba(255, 122, 0, 0.10)');
        procGrad.addColorStop(1, 'rgba(255, 122, 0, 0.0)');
        ctx.fillStyle = procGrad;
        ctx.fill();

        // Solid Vivid Orange High-Resolution Hairline Curve (Humanized)
        ctx.lineWidth = 1.8;
        ctx.strokeStyle = '#ff7a00';
        ctx.shadowColor = '#ff7a00';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        for (let i = 0; i < procPoints.length; i++) {
          if (i === 0) ctx.moveTo(procPoints[i].x, procPoints[i].y);
          else ctx.lineTo(procPoints[i].x, procPoints[i].y);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // --- HUD DUAL-TRACE OVERLAY LEGEND ---
      const legX = width - 12;
      ctx.textAlign = 'right';
      ctx.font = '700 8.5px "JetBrains Mono", monospace';

      // AI Raw Legend (Blue)
      ctx.fillStyle = 'rgba(0, 229, 255, 0.75)';
      ctx.fillText('┄┄ AI ORIGINAL (RAW INPUT)', legX, 16);

      // Humanized Output Legend (Orange)
      ctx.fillStyle = '#ff7a00';
      ctx.fillText('── HUMANIZED (OUTPUT)', legX, 28);

    } else {
      // Idle state: dual clean baselines
      const rawBaselineY = this.dbToY(-96, height);
      const procBaselineY = this.dbToY(-95, height);

      // Faded cyan AI ghost baseline
      ctx.strokeStyle = 'rgba(0, 229, 255, 0.25)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 3]);
      ctx.beginPath();
      ctx.moveTo(0, rawBaselineY);
      ctx.lineTo(width, rawBaselineY);
      ctx.stroke();
      ctx.setLineDash([]);

      // Orange Humanized baseline
      ctx.strokeStyle = 'rgba(255, 122, 0, 0.35)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, procBaselineY);
      ctx.lineTo(width, procBaselineY);
      ctx.stroke();

      // Idle HUD Legend
      const legX = width - 12;
      ctx.textAlign = 'right';
      ctx.font = '700 8.5px "JetBrains Mono", monospace';
      ctx.fillStyle = 'rgba(0, 229, 255, 0.5)';
      ctx.fillText('┄┄ AI ORIGINAL (RAW INPUT)', legX, 16);
      ctx.fillStyle = 'rgba(255, 122, 0, 0.6)';
      ctx.fillText('── HUMANIZED (OUTPUT)', legX, 28);
    }
  }
}
