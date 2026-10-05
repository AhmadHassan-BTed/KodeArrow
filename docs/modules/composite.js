/**
 * Composite Knob Scaling Curve Engine
 * Evaluates bidirectional mapping between 14 high-level evasion knobs and 91 EngineConfig parameters.
 * Zero code duplication: all curve endpoints and rules are driven by knob-registry.json.
 */

export class CompositeEngine {
  /**
   * Linear interpolation helper.
   */
  static lerp(lo, hi, norm) {
    return lo + (hi - lo) * norm;
  }

  /**
   * Reverse linear interpolation helper clamped to [0, 1].
   */
  static reverseLerp(val, lo, hi) {
    if (Math.abs(hi - lo) < 1e-12) return 0;
    return Math.max(0, Math.min(1, (val - lo) / (hi - lo)));
  }

  /**
   * Find composite knob definition by ID.
   * @param {string} knobId
   * @param {Object} registry
   */
  static getCompositeKnob(knobId, registry) {
    return registry.compositeKnobs.find((k) => k.id === knobId) || null;
  }

  /**
   * Find raw parameter definition by key.
   * @param {string} rawKey
   * @param {Object} registry
   */
  static getRawParam(rawKey, registry) {
    return registry.rawParams.find((p) => p.key === rawKey) || null;
  }

  /**
   * Find parent composite knob for a given raw parameter key.
   * @param {string} rawKey
   * @param {Object} registry
   */
  static getKnobForRawParam(rawKey, registry) {
    const raw = this.getRawParam(rawKey, registry);
    if (!raw || !raw.parentComposite || raw.parentComposite === 'unassigned') return null;
    return this.getCompositeKnob(raw.parentComposite, registry);
  }

  /**
   * Forward mapping: Composite knob value -> raw parameter and DSP parameter updates.
   * @param {string} knobId
   * @param {number} knobVal
   * @param {Object} registry
   * @returns {{ rawUpdates: Object, dspUpdates: Object }}
   */
  static mapForward(knobId, knobVal, registry) {
    const knob = this.getCompositeKnob(knobId, registry);
    if (!knob) return { rawUpdates: {}, dspUpdates: {} };

    const norm = Math.max(0, Math.min(1, (knobVal - knob.min) / (knob.max - knob.min)));
    const rawUpdates = {};
    const dspUpdates = {};

    for (const curve of knob.curves) {
      let mappedVal = 0;

      if (curve.type === 'stepped') {
        // e.g. neural_residual.tier (1 to 4 stepped across range)
        const stepIndex = Math.min(curve.hi - curve.lo, Math.floor(norm * (curve.hi - curve.lo + 1)));
        mappedVal = curve.lo + stepIndex;
      } else if (curve.type === 'int') {
        mappedVal = Math.round(this.lerp(curve.lo, curve.hi, norm));
      } else {
        mappedVal = this.lerp(curve.lo, curve.hi, norm);
      }

      // Special parametric rules
      if (curve.target === 'hash_disrupt.wow_depth_cents') {
        const base = rawUpdates['hash_disrupt.base_cents'] ?? this.lerp(0.5, 6.0, norm);
        mappedVal = +(base * 0.33).toFixed(3);
      } else if (curve.target === 'firewall.structural_bark_floor_db') {
        mappedVal = +(knobVal * 1.8).toFixed(2);
      } else if (curve.target === 'mastering.air_gain_db_min') {
        mappedVal = +Math.max(0, knobVal - 0.15).toFixed(3);
      } else if (curve.target === 'mastering.air_gain_db_max') {
        mappedVal = +Math.max(0.05, knobVal + 0.15).toFixed(3);
      }

      if (curve.target.startsWith('__dsp__.')) {
        const dspKey = curve.target.replace('__dsp__.', '');
        dspUpdates[dspKey] = mappedVal;
      } else {
        rawUpdates[curve.target] = mappedVal;
      }
    }

    return { rawUpdates, dspUpdates };
  }

  /**
   * Reverse mapping: Check if raw parameters still match the composite curve,
   * or if a manual edit broke the relationship into CUSTOM mode.
   * @param {string} editedRawKey
   * @param {number} editedRawValue
   * @param {Object} registry
   * @param {Object} currentRawState - Map of all current raw parameter values
   * @returns {{ knobId: string, isCustom: boolean, val: number|null }}
   */
  static mapReverse(editedRawKey, editedRawValue, registry, currentRawState) {
    const parentKnob = this.getKnobForRawParam(editedRawKey, registry);
    if (!parentKnob) return null;

    // Find the curve corresponding to this edited key
    const primaryCurve = parentKnob.curves.find((c) => c.target === editedRawKey);
    if (!primaryCurve) return null;

    // Invert primary curve to find what knob value would produce this raw value
    let inferredNorm = 0;
    if (primaryCurve.type === 'stepped') {
      inferredNorm = this.reverseLerp(editedRawValue, primaryCurve.lo, primaryCurve.hi);
    } else {
      inferredNorm = this.reverseLerp(editedRawValue, primaryCurve.lo, primaryCurve.hi);
    }

    const inferredKnobVal = +(parentKnob.min + inferredNorm * (parentKnob.max - parentKnob.min)).toFixed(
      parentKnob.step < 0.1 ? 2 : (parentKnob.step < 1 ? 1 : 0)
    );

    // Now test ALL parameters driven by this composite knob against inferred position
    let isCustom = false;
    for (const curve of parentKnob.curves) {
      if (curve.target.startsWith('__dsp__.')) continue;

      let expected = 0;
      if (curve.type === 'stepped') {
        const stepIndex = Math.min(curve.hi - curve.lo, Math.floor(inferredNorm * (curve.hi - curve.lo + 1)));
        expected = curve.lo + stepIndex;
      } else if (curve.type === 'int') {
        expected = Math.round(this.lerp(curve.lo, curve.hi, inferredNorm));
      } else {
        expected = this.lerp(curve.lo, curve.hi, inferredNorm);
      }

      if (curve.target === 'hash_disrupt.wow_depth_cents') {
        const base = this.lerp(0.5, 6.0, inferredNorm);
        expected = +(base * 0.33).toFixed(3);
      } else if (curve.target === 'firewall.structural_bark_floor_db') {
        expected = +(inferredKnobVal * 1.8).toFixed(2);
      } else if (curve.target === 'mastering.air_gain_db_min') {
        expected = +Math.max(0, inferredKnobVal - 0.15).toFixed(3);
      } else if (curve.target === 'mastering.air_gain_db_max') {
        expected = +Math.max(0.05, inferredKnobVal + 0.15).toFixed(3);
      }

      const actual = curve.target === editedRawKey ? editedRawValue : currentRawState[curve.target];
      if (actual !== undefined) {
        const span = Math.abs(curve.hi - curve.lo) || 1.0;
        const relativeError = Math.abs(actual - expected) / span;
        if (relativeError > 0.08) { // 8% tolerance threshold
          isCustom = true;
          break;
        }
      }
    }

    return {
      knobId: parentKnob.id,
      isCustom,
      val: isCustom ? null : inferredKnobVal,
    };
  }
}
