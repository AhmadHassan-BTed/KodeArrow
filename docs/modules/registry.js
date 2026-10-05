/**
 * NaSuno DOM Registry & Wiring Engine
 * Fetches knob-registry.json and dynamically renders Evasion Mode knobs,
 * Advanced Mode raw parameter accordions, and Config I/O panels.
 * Zero hardcoded HTML: complete UI structure is data-driven.
 * Zero emojis: uses clean, razor-sharp SVG vector iconography.
 */

import { FLKnob } from './knob.js';

// SVG Vector Icon Templates
const SVG_ICONS = {
  info: `<svg class="svg-icon-info" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`,
  reset: `<svg class="svg-icon-reset" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>`,
  chevron: `<svg class="svg-chevron-arrow" width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg>`,
  slider: `<svg class="svg-icon-slider" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>`,
  download: `<svg class="svg-icon-btn" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
  upload: `<svg class="svg-icon-upload" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
  apply: `<svg class="svg-icon-btn" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>`,
  save: `<svg class="svg-icon-btn" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>`,
};

export class RegistryDOM {
  constructor(registry) {
    this.registry = registry;
    this.knobsMap = {};
    this.rawInputsMap = {};
  }

  /**
   * Fetch registry JSON from path.
   * @param {string} url
   * @returns {Promise<Object>}
   */
  static async load(url = 'knob-registry.json') {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load registry: HTTP ${res.status}`);
    return await res.json();
  }

  /**
   * Render all three panels into their designated DOM containers.
   * @param {Object} options
   */
  renderAll(options = {}) {
    this.renderEvasionPanel(options.onKnobInfoClick, options.onResetToCurve);
    this.renderAdvancedPanel(options.onRawInfoClick, options.onRawInputChange);
    this.renderConfigPanel(options.onDownloadTemplate, options.onImport, options.onExport);
  }

  /**
   * Render Evasion Mode (14 composite knobs across 4 modules).
   */
  renderEvasionPanel(onInfoClick, onResetToCurve) {
    const container = document.getElementById('evasionPanel');
    if (!container) return;
    container.innerHTML = '';

    // Group composite knobs by module
    const modules = [
      { id: 'watermarkErase', title: 'WATERMARK ERASE', subtitle: 'Direct removal of embedded AI marks', color: 'cyan' },
      { id: 'fingerprintScatter', title: 'FINGERPRINT SCATTER', subtitle: 'Spectral shape & phase coherence disruption', color: 'cyan' },
      { id: 'naturalization', title: 'NATURALIZATION', subtitle: 'Acoustic realism & room signature restoration', color: 'green' },
      { id: 'masteringQuality', title: 'MASTERING & QUALITY', subtitle: 'Dynamic density & perceptual firewall gates', color: 'orange' },
    ];

    for (const mod of modules) {
      const modKnobs = this.registry.compositeKnobs.filter((k) => k.module === mod.id);
      if (modKnobs.length === 0) continue;

      const modCard = document.createElement('div');
      modCard.className = `rack-module-card border-${mod.color}`;
      modCard.innerHTML = `
        <div class="module-header">
          <div class="module-title-wrap">
            <span class="module-pill pill-${mod.color}">${mod.title}</span>
            <span class="module-desc">${mod.subtitle}</span>
          </div>
          <span class="module-count">${modKnobs.length} VECTORS</span>
        </div>
        <div class="module-knobs-grid" id="grid_${mod.id}"></div>
      `;

      const grid = modCard.querySelector(`#grid_${mod.id}`);

      for (const k of modKnobs) {
        const knobCol = document.createElement('div');
        knobCol.className = 'knob-col';
        knobCol.innerHTML = `
          <div class="knob-label-row">
            <span class="knob-label" title="${k.label}">${k.label}</span>
            <button class="info-btn" data-composite-info="${k.id}" title="Vector information" aria-label="Vector Info">
              ${SVG_ICONS.info}
            </button>
          </div>
          <div class="fl-knob-wrapper"
               data-knob="${k.id}"
               data-min="${k.min}"
               data-max="${k.max}"
               data-step="${k.step}"
               data-val="${k.default}"
               data-unit="${k.unit}">
            <svg class="knob-ring-svg" viewBox="0 0 76 76">
              <circle class="ring-bg" cx="38" cy="38" r="30"></circle>
              <circle class="ring-active ring-${k.ring}" cx="38" cy="38" r="30"></circle>
            </svg>
            <div class="knob-rotor">
              <div class="rotor-cap"></div>
              <div class="rotor-pointer"></div>
            </div>
          </div>
          <div class="knob-readout-row">
            <div class="knob-readout" id="readout_${k.id}">--</div>
            <button class="badge-custom" id="custom_${k.id}" data-reset-knob="${k.id}" title="Values diverged from curve. Click to reset." style="display: none;">
              CUSTOM ${SVG_ICONS.reset}
            </button>
          </div>
        `;

        // Wire info button
        const infoBtn = knobCol.querySelector('.info-btn');
        if (infoBtn && onInfoClick) {
          infoBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            onInfoClick(k.id, infoBtn);
          });
        }

        // Wire reset to curve button
        const resetBtn = knobCol.querySelector('.badge-custom');
        if (resetBtn && onResetToCurve) {
          resetBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            onResetToCurve(k.id);
          });
        }

        grid.appendChild(knobCol);

        // Instantiate FLKnob
        const knobEl = knobCol.querySelector('.fl-knob-wrapper');
        const flKnob = new FLKnob(knobEl, {
          knobId: k.id,
          min: k.min,
          max: k.max,
          step: k.step,
          default: k.default,
          val: k.default,
          unit: k.unit,
          readoutEl: knobCol.querySelector(`#readout_${k.id}`),
          customBadgeEl: resetBtn,
        });
        this.knobsMap[k.id] = flKnob;
      }

      container.appendChild(modCard);
    }
  }

  /**
   * Render Advanced Mode (91 raw parameters grouped by subsystem in collapsible accordions).
   */
  renderAdvancedPanel(onInfoClick, onInputChange) {
    const container = document.getElementById('advancedPanel');
    if (!container) return;
    container.innerHTML = `
      <div class="advanced-panel-header">
        <div class="advanced-title-wrap">
          <span class="panel-section-title">FULL SUBSYSTEM MATRIX (91 TUNABLE PARAMETERS)</span>
          <span class="panel-section-subtitle">Exhaustive low-level parameter control across all 24 DSP & detection subsystems.</span>
        </div>
        <div class="advanced-controls">
          <button class="btn-rack-mini" id="btnExpandAllAccordions">EXPAND ALL</button>
          <button class="btn-rack-mini" id="btnCollapseAllAccordions">COLLAPSE ALL</button>
        </div>
      </div>
      <div class="accordions-container" id="accordionsList"></div>
    `;

    const list = container.querySelector('#accordionsList');

    // Group raw params by subsystem
    const grouped = {};
    for (const p of this.registry.rawParams) {
      if (!grouped[p.subsystem]) grouped[p.subsystem] = [];
      grouped[p.subsystem].push(p);
    }

    for (const [sub, params] of Object.entries(grouped)) {
      const subTitle = params[0].subsystemTitle || sub.toUpperCase();
      const accordion = document.createElement('details');
      accordion.className = 'subsystem-accordion';
      accordion.open = sub === 'firewall' || sub === 'classical' || sub === 'neural_residual';

      accordion.innerHTML = `
        <summary class="accordion-summary">
          <div class="summary-left">
            <span class="accordion-arrow">${SVG_ICONS.chevron}</span>
            <span class="summary-title">${subTitle}</span>
            <span class="summary-key"><code>${sub}</code></span>
          </div>
          <span class="summary-badge">${params.length} PARAMS</span>
        </summary>
        <div class="accordion-body">
          <div class="raw-params-grid">
            ${params
              .map((p) => {
                const parentKnob = this.registry.compositeKnobs.find((k) => k.id === p.parentComposite);
                const parentName = parentKnob ? parentKnob.label : 'None';
                return `
                  <div class="raw-param-row" data-param-key="${p.key}">
                    <div class="param-label-wrap">
                      <div class="param-top">
                        <span class="param-label" title="${p.key}">${p.label}</span>
                        <button class="info-btn" data-raw-info="${p.key}" title="Parameter information" aria-label="Param Info">
                          ${SVG_ICONS.info}
                        </button>
                      </div>
                      <div class="param-sub-info">
                        <span class="parent-knob-tag" title="Controlled by composite knob">
                          ${SVG_ICONS.slider} ${parentName}
                        </span>
                        <span class="param-range-tag">[${p.min}…${p.max}] ${p.unit}</span>
                      </div>
                    </div>
                    <div class="param-input-wrap">
                      <input type="number"
                             class="raw-input"
                             id="input_${p.key.replace('.', '_')}"
                             data-key="${p.key}"
                             min="${p.min}"
                             max="${p.max}"
                             step="${p.step}"
                             value="${p.default}">
                    </div>
                  </div>
                `;
              })
              .join('')}
          </div>
        </div>
      `;

      // Wire info buttons inside accordion
      accordion.querySelectorAll('[data-raw-info]').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const key = btn.dataset.rawInfo;
          if (onInfoClick) onInfoClick(key, btn);
        });
      });

      // Wire raw inputs
      accordion.querySelectorAll('.raw-input').forEach((input) => {
        const key = input.dataset.key;
        this.rawInputsMap[key] = input;
        input.addEventListener('change', () => {
          const val = parseFloat(input.value);
          if (onInputChange) onInputChange(key, val);
        });
      });

      list.appendChild(accordion);
    }

    // Expand / Collapse all
    container.querySelector('#btnExpandAllAccordions')?.addEventListener('click', () => {
      container.querySelectorAll('.subsystem-accordion').forEach((acc) => (acc.open = true));
    });
    container.querySelector('#btnCollapseAllAccordions')?.addEventListener('click', () => {
      container.querySelectorAll('.subsystem-accordion').forEach((acc) => (acc.open = false));
    });
  }

  /**
   * Render Config I/O Panel (Download template, import file/paste, export config).
   */
  renderConfigPanel(onDownloadTemplate, onImport, onExport) {
    const container = document.getElementById('configPanel');
    if (!container) return;

    container.innerHTML = `
      <div class="config-panel-container">
        <!-- 1. Download Template Card -->
        <div class="config-card">
          <div class="config-card-header">
            <span class="config-card-title">1. DOWNLOAD CONFIG TEMPLATE</span>
            <span class="config-card-tag">ENGINE_KNOBS.JSON</span>
          </div>
          <p class="config-card-desc">
            Download the complete, validated JSON skeleton containing all 222 EngineConfig parameters,
            defaults, comments, and valid ranges for offline modification and batch processing.
          </p>
          <button class="btn-rack-action" id="btnDownloadTemplate">
            <span class="btn-icon">${SVG_ICONS.download}</span> DOWNLOAD TEMPLATE JSON
          </button>
        </div>

        <!-- 2. Import Config Card -->
        <div class="config-card">
          <div class="config-card-header">
            <span class="config-card-title">2. IMPORT CUSTOM CONFIGURATION</span>
            <span class="config-card-tag">UPLOAD OR PASTE</span>
          </div>
          <p class="config-card-desc">
            Import an existing <code>engine_knobs.json</code> profile or paste JSON directly.
            Values will be validated and synced across Evasion Mode and Advanced Mode.
          </p>
          
          <div class="import-dropzone" id="importDropzone">
            <input type="file" id="configFileInput" accept=".json" style="display:none;">
            <div class="dropzone-content">
              <span class="dropzone-icon">${SVG_ICONS.upload}</span>
              <span class="dropzone-text">Click to choose or drag & drop <code>.json</code> file</span>
            </div>
          </div>

          <div class="paste-area-wrap">
            <label class="paste-label" for="configPasteArea">OR PASTE JSON HERE:</label>
            <textarea class="config-textarea" id="configPasteArea" placeholder='{\n  "processing_level": "moderate",\n  "classical": { "carrier_notch_q": 45 }\n}'></textarea>
          </div>

          <div class="import-status" id="importStatus"></div>

          <button class="btn-rack-action btn-cyan" id="btnApplyConfig">
            <span class="btn-icon">${SVG_ICONS.apply}</span> VALIDATE & APPLY CONFIG
          </button>
        </div>

        <!-- 3. Export Current Card -->
        <div class="config-card">
          <div class="config-card-header">
            <span class="config-card-title">3. EXPORT CURRENT ACTIVE ENGINE STATE</span>
            <span class="config-card-tag">PRODUCTION READY</span>
          </div>
          <p class="config-card-desc">
            Export the active parameter profile as a validated JSON file to save your custom presets
            or deploy directly into your automated mastering workflow.
          </p>
          <button class="btn-rack-action btn-orange" id="btnExportCurrentConfig">
            <span class="btn-icon">${SVG_ICONS.save}</span> EXPORT ENGINE_KNOBS.JSON
          </button>
        </div>
      </div>
    `;

    // 1. Download Template
    container.querySelector('#btnDownloadTemplate')?.addEventListener('click', () => {
      if (onDownloadTemplate) onDownloadTemplate();
    });

    // 2. Import File
    const dropzone = container.querySelector('#importDropzone');
    const fileInput = container.querySelector('#configFileInput');
    const pasteArea = container.querySelector('#configPasteArea');
    const importStatus = container.querySelector('#importStatus');
    const applyBtn = container.querySelector('#btnApplyConfig');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());

      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
      dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
      dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          handleFile(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
          handleFile(e.target.files[0]);
        }
      });
    }

    function handleFile(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (pasteArea) pasteArea.value = e.target.result;
        if (importStatus) {
          importStatus.textContent = `Loaded file: ${file.name} (${file.size} bytes)`;
          importStatus.className = 'import-status success';
        }
      };
      reader.readAsText(file);
    }

    applyBtn?.addEventListener('click', () => {
      const jsonStr = pasteArea?.value.trim() || '';
      if (!jsonStr) {
        if (importStatus) {
          importStatus.textContent = 'Paste JSON or upload a file first.';
          importStatus.className = 'import-status error';
        }
        return;
      }
      if (onImport) onImport(jsonStr, importStatus);
    });

    // 3. Export Current
    container.querySelector('#btnExportCurrentConfig')?.addEventListener('click', () => {
      if (onExport) onExport();
    });
  }

  /**
   * Update value of a raw parameter input field in Advanced Mode.
   * @param {string} key
   * @param {number} val
   */
  setRawInputValue(key, val) {
    const input = this.rawInputsMap[key];
    if (input) {
      input.value = typeof val === 'number' ? +val.toFixed(input.step < 0.01 ? 4 : 2) : val;
    }
  }

  /**
   * Get all current values from Advanced Mode inputs.
   * @returns {Object}
   */
  getAllRawValues() {
    const values = {};
    for (const [key, input] of Object.entries(this.rawInputsMap)) {
      values[key] = parseFloat(input.value);
    }
    return values;
  }
}
