/**
 * NaSuno Config I/O Module
 * Handles EngineConfig template generation, JSON schema validation, file import/export.
 * Fully compatible with Python `nasuno clean input.wav --config engine_knobs.json`.
 */

export class ConfigIO {
  /**
   * Generate a complete JSON template matching Python EngineConfig dataclass layout.
   * Includes all 222 parameters with comments, defaults, and ranges.
   * @param {Object} registry
   * @returns {string} Formatted JSON string
   */
  static generateTemplate(registry) {
    const template = {
      _comment: "NaSuno EngineConfig Master Tuning Template (v2.4)",
      processing_level: "moderate",
      filter_order: 2,
      filter_width_multiplier: 1.0,
      noise_level: 0.00005,
      skip_low_freq_threshold: 250,
      timing_stretch_range: 0.003,
      distribution_noise_level: 0.0005,
      harmonic_distortion_amount: 0.005,
      phase_variance: 0.005,
      micro_dynamics_amount: 0.001,
      timing_variation_range: 0.002,
      segment_overlap_ratio: 0.5,
      stft_size: 2048,
      enable_watermark_removal: true,
      enable_pattern_normalization: true,
      enable_timing_variations: true,
      enable_harmonic_adjustments: true,
    };

    // Subsystems
    const subsystems = [
      'firewall', 'perceptual', 'mel_domain', 'neural_residual', 'sync_disrupt',
      'upsampler', 'classical', 'phase_decorrelate', 'resynthesis', 'statistical',
      'quantization', 'bandwidth', 'environment', 'bispectral', 'lpc_residual',
      'disclosure', 'hash_disrupt', 'mastering', 'pipeline'
    ];

    for (const sub of subsystems) {
      template[sub] = {};
    }

    // Add tunable raw params
    for (const p of registry.rawParams) {
      if (p.subsystem === 'top') {
        template[p.key] = p.default;
      } else if (template[p.subsystem]) {
        const subKey = p.key.split('.')[1];
        template[p.subsystem][subKey] = p.default;
      }
    }

    // Add fixed params
    for (const f of registry.fixedParams) {
      if (!f.key.includes('.')) {
        template[f.key] = f.value;
      } else {
        const [sub, subKey] = f.key.split('.');
        if (template[sub]) {
          template[sub][subKey] = f.value;
        }
      }
    }

    return JSON.stringify(template, null, 2);
  }

  /**
   * Export the current state as a valid EngineConfig JSON string.
   * @param {Object} rawState - Current values of raw parameters
   * @param {Object} registry - Knob registry
   * @param {string} currentPreset - Active preset level
   * @returns {string} Formatted JSON string
   */
  static exportConfig(rawState, registry, currentPreset = 'moderate') {
    const config = {
      processing_level: currentPreset,
      segment_overlap_ratio: 0.5,
      enable_watermark_removal: true,
      enable_pattern_normalization: true,
      enable_timing_variations: true,
      enable_harmonic_adjustments: true,
    };

    // Initialize subsystem objects
    const subsystems = [
      'firewall', 'perceptual', 'mel_domain', 'neural_residual', 'sync_disrupt',
      'upsampler', 'classical', 'phase_decorrelate', 'resynthesis', 'statistical',
      'quantization', 'bandwidth', 'environment', 'bispectral', 'lpc_residual',
      'disclosure', 'hash_disrupt', 'mastering', 'pipeline'
    ];
    for (const sub of subsystems) {
      config[sub] = {};
    }

    // Populate fixed params first
    for (const f of registry.fixedParams) {
      if (!f.key.includes('.')) {
        config[f.key] = f.value;
      } else {
        const [sub, subKey] = f.key.split('.');
        if (config[sub]) config[sub][subKey] = f.value;
      }
    }

    // Populate current tunable values
    for (const p of registry.rawParams) {
      const currentVal = rawState[p.key] !== undefined ? rawState[p.key] : p.default;
      if (p.subsystem === 'top') {
        config[p.key] = currentVal;
      } else if (config[p.subsystem]) {
        const subKey = p.key.split('.')[1];
        config[p.subsystem][subKey] = currentVal;
      }
    }

    return JSON.stringify(config, null, 2);
  }

  /**
   * Validate and parse imported JSON string into a flat parameter map.
   * @param {string} jsonStr
   * @param {Object} registry
   * @returns {{ success: boolean, params: Object, errors: string[], warnings: string[] }}
   */
  static parseAndValidate(jsonStr, registry) {
    const errors = [];
    const warnings = [];
    const params = {};

    let parsed = null;
    try {
      parsed = JSON.parse(jsonStr);
    } catch (e) {
      return { success: false, params: {}, errors: [`JSON Syntax Error: ${e.message}`], warnings: [] };
    }

    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
      return { success: false, params: {}, errors: ['Root configuration must be a JSON object.'], warnings: [] };
    }

    // Flatten nested JSON
    const flatImport = {};
    for (const [key, val] of Object.entries(parsed)) {
      if (key.startsWith('_')) continue; // Skip comments
      if (typeof val === 'object' && val !== null && !Array.isArray(val)) {
        for (const [subKey, subVal] of Object.entries(val)) {
          flatImport[`${key}.${subKey}`] = subVal;
        }
      } else {
        flatImport[key] = val;
      }
    }

    // Validate against known raw parameters
    for (const p of registry.rawParams) {
      if (flatImport[p.key] !== undefined) {
        const val = Number(flatImport[p.key]);
        if (isNaN(val)) {
          warnings.push(`Param ${p.key}: invalid number value "${flatImport[p.key]}", using default.`);
        } else {
          // Clamp to min/max
          const clamped = Math.max(p.min, Math.min(p.max, val));
          if (clamped !== val) {
            warnings.push(`Param ${p.key}: value ${val} out of range [${p.min}, ${p.max}], clamped to ${clamped}.`);
          }
          params[p.key] = clamped;
        }
      }
    }

    return {
      success: errors.length === 0,
      params,
      errors,
      warnings,
      detectedPreset: parsed.processing_level || null,
    };
  }

  /**
   * Trigger browser file download with given text content.
   * @param {string} filename
   * @param {string} content
   * @param {string} mimeType
   */
  static downloadFile(filename, content, mimeType = 'application/json') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}
