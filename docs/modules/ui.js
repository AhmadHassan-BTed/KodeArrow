/**
 * NaSuno UI Controller Module
 * Manages dual-mode panel tab switching, info popovers, preset dropdowns, and bypass controls.
 */

export class UIController {
  constructor(registry, options = {}) {
    this.registry = registry;
    this.onPresetSelect = options.onPresetSelect || (() => {});
    this.onBypassToggle = options.onBypassToggle || (() => {});

    this.activePanel = 'evasion';
    this.activePopoverKnob = null;

    this.initTabs();
    this.initPopovers();
    this.initPresetDropdown();
    this.initBypassToggle();
  }

  // ==========================================================================
  // Panel Tab Switching (Evasion Mode vs Advanced Mode vs Config I/O)
  // ==========================================================================
  initTabs() {
    const tabs = document.querySelectorAll('.panel-tab');
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const targetPanel = tab.dataset.panel;
        this.switchPanel(targetPanel);
      });
    });
  }

  switchPanel(panelId) {
    this.activePanel = panelId;

    // Update tab button classes
    document.querySelectorAll('.panel-tab').forEach((tab) => {
      tab.classList.toggle('active', tab.dataset.panel === panelId);
    });

    // Update panel view visibility
    document.querySelectorAll('.rack-panel-view').forEach((view) => {
      view.classList.toggle('active', view.dataset.panelView === panelId);
    });

    // Hide any open popover
    this.hidePopover();
  }

  // ==========================================================================
  // Info Popover System (Single shared modal/popover)
  // ==========================================================================
  initPopovers() {
    const popover = document.getElementById('infoPopover');
    const closeBtn = document.getElementById('popoverCloseBtn');
    const backdrop = document.getElementById('popoverBackdrop');

    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.hidePopover());
    }
    if (backdrop) {
      backdrop.addEventListener('click', () => this.hidePopover());
    }

    // Keyboard dismissal
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.hidePopover();
    });
  }

  /**
   * Show info popover for a composite knob.
   * @param {string} knobId
   * @param {HTMLElement} triggerEl
   */
  showCompositeInfo(knobId, triggerEl) {
    const knob = this.registry.compositeKnobs.find((k) => k.id === knobId);
    if (!knob || !knob.info) return;

    const popover = document.getElementById('infoPopover');
    const titleEl = document.getElementById('popoverTitle');
    const badgeEl = document.getElementById('popoverBadge');
    const bodyEl = document.getElementById('popoverBody');
    const backdrop = document.getElementById('popoverBackdrop');
    if (!popover || !bodyEl) return;

    if (titleEl) titleEl.textContent = knob.info.title || knob.label;
    if (badgeEl) {
      badgeEl.textContent = `${knob.moduleTitle} • LIVE DSP`;
      badgeEl.className = `popover-badge badge-${knob.ring}`;
    }

    // Build driven params list
    let drivenHtml = '';
    if (knob.curves && knob.curves.length > 0) {
      drivenHtml = `
        <div class="popover-section">
          <div class="popover-section-title">DRIVES ${knob.curves.length} PARAMETERS</div>
          <ul class="popover-driven-list">
            ${knob.curves
              .map((c) => {
                const isDsp = c.target.startsWith('__dsp__.');
                const targetName = isDsp ? c.target.replace('__dsp__.', 'Live DSP: ') : c.target;
                return `<li><code>${targetName}</code>: ${c.lo} → ${c.hi}</li>`;
              })
              .join('')}
          </ul>
        </div>
      `;
    }

    bodyEl.innerHTML = `
      <div class="popover-section">
        <div class="popover-section-title">DEFEATS DETECTION VECTOR</div>
        <p class="popover-highlight">${knob.info.defeats}</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">DESCRIPTION</div>
        <p>${knob.info.description}</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">HOW IT WORKS</div>
        <p>${knob.info.howItWorks}</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">FIDELITY TRADEOFF</div>
        <p>${knob.info.tradeoff}</p>
      </div>
      ${drivenHtml}
    `;

    popover.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
  }

  /**
   * Show info popover for a raw parameter.
   * @param {string} rawKey
   * @param {HTMLElement} triggerEl
   */
  showRawParamInfo(rawKey, triggerEl) {
    const raw = this.registry.rawParams.find((p) => p.key === rawKey);
    if (!raw) return;

    const popover = document.getElementById('infoPopover');
    const titleEl = document.getElementById('popoverTitle');
    const badgeEl = document.getElementById('popoverBadge');
    const bodyEl = document.getElementById('popoverBody');
    const backdrop = document.getElementById('popoverBackdrop');
    if (!popover || !bodyEl) return;

    if (titleEl) titleEl.textContent = raw.label;
    if (badgeEl) {
      badgeEl.textContent = raw.subsystemTitle || raw.subsystem.toUpperCase();
      badgeEl.className = 'popover-badge';
    }

    const parentKnob = this.registry.compositeKnobs.find((k) => k.id === raw.parentComposite);
    const parentLabel = parentKnob ? parentKnob.label : 'None';

    bodyEl.innerHTML = `
      <div class="popover-section">
        <div class="popover-section-title">PARAMETER KEY</div>
        <code>${raw.key}</code>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">DESCRIPTION</div>
        <p>${raw.info}</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">PARENT COMPOSITE KNOB</div>
        <p class="popover-highlight">${parentLabel}</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">SPECIFICATION</div>
        <p>Range: ${raw.min} – ${raw.max} ${raw.unit} | Default: ${raw.default} | Step: ${raw.step}</p>
      </div>
    `;

    popover.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
  }

  hidePopover() {
    const popover = document.getElementById('infoPopover');
    const backdrop = document.getElementById('popoverBackdrop');
    if (popover) popover.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
  }

  // ==========================================================================
  // Preset Dropdown
  // ==========================================================================
  initPresetDropdown() {
    const btn = document.getElementById('presetSelectorBtn');
    const dropdown = document.getElementById('presetDropdown');
    if (!btn || !dropdown) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('open');
    });

    dropdown.querySelectorAll('.preset-opt').forEach((opt) => {
      opt.addEventListener('click', (e) => {
        e.stopPropagation();
        const presetKey = opt.dataset.preset;
        this.setPresetDisplay(presetKey);
        this.onPresetSelect(presetKey);
        dropdown.classList.remove('open');
      });
    });

    window.addEventListener('click', () => {
      dropdown.classList.remove('open');
    });
  }

  setPresetDisplay(presetKey) {
    const nameEl = document.getElementById('currentPresetName');
    if (presetKey === 'custom') {
      if (nameEl) nameEl.textContent = 'Custom';
      document.querySelectorAll('.preset-opt').forEach((btn) => btn.classList.remove('active'));
      return;
    }
    const p = this.registry?.presets?.[presetKey];
    if (!p) return;
    if (nameEl) nameEl.textContent = p.name;

    document.querySelectorAll('.preset-opt').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.preset === presetKey);
    });
  }

  // ==========================================================================
  // Bypass Toggle & Info Popover
  // ==========================================================================
  initBypassToggle() {
    const bypassBtn = document.getElementById('bypassBtn');
    const bypassLed = document.getElementById('bypassLed');
    const bypassText = document.getElementById('bypassText');
    const dspInfoBtn = document.getElementById('dspInfoBtn');

    if (dspInfoBtn) {
      dspInfoBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.showDspBypassInfo();
      });
    }

    if (!bypassBtn) return;

    bypassBtn.addEventListener('click', () => {
      const isCurrentlyBypassed = this.isBypassed;
      const nextBypassed = !isCurrentlyBypassed;
      this.setBypassState(nextBypassed);
      this.onBypassToggle(nextBypassed);
    });
  }

  setBypassState(bypassed) {
    this.isBypassed = !!bypassed;
    const bypassLed = document.getElementById('bypassLed');
    const bypassText = document.getElementById('bypassText');
    if (this.isBypassed) {
      if (bypassLed) {
        bypassLed.classList.remove('active');
        bypassLed.classList.add('bypassed');
      }
      if (bypassText) bypassText.textContent = 'BYPASS (RAW)';
    } else {
      if (bypassLed) {
        bypassLed.classList.add('active');
        bypassLed.classList.remove('bypassed');
      }
      if (bypassText) bypassText.textContent = 'DSP ACTIVE';
    }
  }

  showDspBypassInfo() {
    const popover = document.getElementById('infoPopover');
    const titleEl = document.getElementById('popoverTitle');
    const badgeEl = document.getElementById('popoverBadge');
    const bodyEl = document.getElementById('popoverBody');
    const backdrop = document.getElementById('popoverBackdrop');
    if (!popover || !bodyEl) return;

    if (titleEl) titleEl.textContent = 'DSP Engine & A/B Bypass';
    if (badgeEl) {
      badgeEl.textContent = 'SYSTEM CORE • REAL-TIME';
      badgeEl.className = 'popover-badge badge-orange';
    }

    bodyEl.innerHTML = `
      <div class="popover-section">
        <div class="popover-section-title">FUNCTION & PURPOSE</div>
        <p class="popover-highlight">Instant A/B comparison between active evasion DSP processing and the raw unprocessed audio.</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">MODES OF OPERATION</div>
        <p><strong>• DSP ACTIVE (Green LED) [Recommended]</strong>: The complete 14-stage real-time psychoacoustic DSP engine is actively processing the audio stream in your browser. All notch filters, harmonic combustors, allpass phase scatterers, analog saturators, and dynamic compressors are applied live to defeat AI watermarks and detection signatures.</p>
        <p style="margin-top: 8px;"><strong>• BYPASS (RAW) (Red/Dim LED)</strong>: Instantly bypasses all 14 DSP stages via click-free crossfade, routing the raw, un-evaded audio direct to your speakers. Use this to audition the exact delta difference between your clean master and the original track.</p>
      </div>
      <div class="popover-section">
        <div class="popover-section-title">HOW TO USE</div>
        <p>Keep <strong>DSP ACTIVE</strong> while tuning knobs and evaluating evasion effectiveness. Toggle to <strong>BYPASS</strong> at any time to verify that audio quality and transparent fidelity remain uncompromised.</p>
      </div>
    `;

    popover.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
  }
}
