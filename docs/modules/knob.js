/**
 * FLKnob — Generic Rotary Controller for FL Studio Plugin Aesthetic
 * Encapsulates rotor rotation, SVG arc ring, drag physics, wheel, and double-click reset.
 * Completely agnostic of DSP or backend logic.
 */

export class FLKnob {
  /**
   * @param {HTMLElement} element - Knob DOM container
   * @param {Object} options - Optional configuration overrides
   */
  constructor(element, options = {}) {
    this.el = element;
    this.knobId = options.knobId || element.dataset.knob;
    this.min = options.min !== undefined ? options.min : parseFloat(element.dataset.min ?? 0);
    this.max = options.max !== undefined ? options.max : parseFloat(element.dataset.max ?? 100);
    this.step = options.step !== undefined ? options.step : parseFloat(element.dataset.step ?? 1);
    this.defaultVal = options.default !== undefined ? options.default : parseFloat(element.dataset.default ?? element.dataset.val ?? this.min);
    this.val = options.val !== undefined ? options.val : parseFloat(element.dataset.val ?? this.defaultVal);
    this.unit = options.unit !== undefined ? options.unit : (element.dataset.unit || '');
    this.isCustom = false;

    this.rotor = element.querySelector('.knob-rotor');
    this.ring = element.querySelector('.ring-active');
    this.readout = options.readoutEl || document.getElementById(`readout_${this.knobId}`);
    this.customBadge = options.customBadgeEl || document.getElementById(`custom_${this.knobId}`);

    this.startY = 0;
    this.startVal = 0;
    this.isDragging = false;
    this.listeners = [];

    this.init();
  }

  init() {
    this.updateVisuals();

    // Mouse drag
    this.el.addEventListener('mousedown', (e) => {
      // Don't drag if clicking an info button or badge
      if (e.target.closest('.info-btn') || e.target.closest('.badge-custom')) return;
      this.onStart(e.clientY);
    });

    window.addEventListener('mousemove', (e) => {
      if (this.isDragging) this.onMove(e.clientY, e.shiftKey);
    });

    window.addEventListener('mouseup', () => this.onEnd());

    // Touch drag
    this.el.addEventListener('touchstart', (e) => {
      if (e.target.closest('.info-btn') || e.target.closest('.badge-custom')) return;
      if (e.touches.length === 1) this.onStart(e.touches[0].clientY);
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
      if (this.isDragging && e.touches.length === 1) this.onMove(e.touches[0].clientY, false);
    }, { passive: true });

    window.addEventListener('touchend', () => this.onEnd());

    // Mouse wheel (fine tune with Shift)
    this.el.addEventListener('wheel', (e) => {
      e.preventDefault();
      const mult = e.shiftKey ? 0.2 : 1.0;
      const delta = (e.deltaY < 0 ? this.step : -this.step) * mult;
      this.setValue(this.val + delta, true);
    }, { passive: false });

    // Double-click reset to default
    this.el.addEventListener('dblclick', (e) => {
      if (e.target.closest('.info-btn') || e.target.closest('.badge-custom')) return;
      this.setValue(this.defaultVal, true);
    });
  }

  onStart(clientY) {
    this.isDragging = true;
    this.startY = clientY;
    this.startVal = this.val;
    document.body.style.cursor = 'ns-resize';
  }

  onMove(clientY, isShift) {
    if (!this.isDragging) return;
    const dy = this.startY - clientY;
    const range = this.max - this.min;
    const baseSensitivity = range / 200; // 200px travel = full range
    const sensitivity = isShift ? baseSensitivity * 0.2 : baseSensitivity;
    const newVal = this.startVal + dy * sensitivity;
    this.setValue(newVal, true);
  }

  onEnd() {
    if (this.isDragging) {
      this.isDragging = false;
      document.body.style.cursor = '';
    }
  }

  onChange(cb) {
    if (typeof cb === 'function') this.listeners.push(cb);
  }

  /**
   * Set knob value, clamp, round to step, and update visuals.
   * @param {number} newVal
   * @param {boolean} triggerUpdate
   */
  setValue(newVal, triggerUpdate = true) {
    const clamped = Math.max(this.min, Math.min(this.max, newVal));
    const stepsCount = Math.round((clamped - this.min) / this.step);
    const precision = this.step < 0.01 ? 4 : (this.step < 0.1 ? 2 : (this.step < 1 ? 1 : 0));
    this.val = +(this.min + stepsCount * this.step).toFixed(precision);
    this.isCustom = false;

    this.updateVisuals();

    if (triggerUpdate) {
      for (const cb of this.listeners) {
        cb(this.val, this.knobId);
      }
      this.el.dispatchEvent(new CustomEvent('knob:change', {
        bubbles: true,
        detail: { knobId: this.knobId, val: this.val, isCustom: false }
      }));
    }
  }

  /**
   * Mark this knob as CUSTOM (broken curve from advanced parameter edit).
   */
  setCustom(isCustom) {
    this.isCustom = !!isCustom;
    this.updateVisuals();
  }

  /**
   * Update visual rotor angle, SVG arc stroke, readout text, and custom state.
   */
  updateVisuals() {
    const norm = Math.max(0, Math.min(1, (this.val - this.min) / (this.max - this.min)));
    const angle = -135 + norm * 270;

    if (this.rotor) {
      this.rotor.style.transform = `rotate(${angle}deg)`;
    }

    if (this.ring) {
      const arcLength = norm * 188.5; // circumference of r=30 circle over 270° is ~141.4, r=40 is ~188.5
      this.ring.style.strokeDasharray = `${arcLength} 300`;
    }

    if (this.customBadge) {
      this.customBadge.style.display = this.isCustom ? 'inline-flex' : 'none';
    }

    if (this.readout) {
      if (this.isCustom) {
        this.readout.textContent = 'CUSTOM';
        this.readout.classList.add('custom-val');
      } else {
        this.readout.classList.remove('custom-val');
        let displayStr = '';
        if (this.unit === 'Hz') {
          displayStr = `${Math.round(this.val)} Hz`;
        } else if (this.unit === 'dB') {
          const sign = this.val > 0 ? '+' : '';
          const dec = this.val % 1 === 0 ? 0 : (this.step < 0.1 ? 2 : 1);
          displayStr = `${sign}${this.val.toFixed(dec)} dB`;
        } else if (this.unit === '%') {
          displayStr = `${Math.round(this.val)}%`;
        } else {
          const dec = this.step < 0.01 ? 4 : (this.step < 0.1 ? 2 : (this.step < 1 ? 1 : 0));
          displayStr = `${this.val.toFixed(dec)}${this.unit ? ' ' + this.unit : ''}`;
        }
        this.readout.textContent = displayStr;
      }
    }
  }
}
