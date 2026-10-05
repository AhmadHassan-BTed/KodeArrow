/**
 * NaSuno Browser Persistence Module
 * - LocalStorage for DSP knob values, presets, bypass state, and raw parameters
 * - IndexedDB for persisting user-uploaded audio files across browser reloads
 */

const SETTINGS_KEY = 'nasuno_engine_settings_v3';
const DB_NAME = 'NaSunoAudioDB';
const DB_VERSION = 1;
const STORE_NAME = 'uploaded_tracks';
const AUDIO_RECORD_KEY = 'active_track';

export class PersistenceManager {
  /**
   * Save DSP knob values, preset key, raw state, and bypass flag.
   * @param {Object} settings
   */
  static saveSettings(settings = {}) {
    try {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    } catch (e) {
      console.warn('LocalStorage save failed:', e);
    }
  }

  /**
   * Load saved DSP settings. Returns null if none found.
   * @returns {Object|null}
   */
  static loadSettings() {
    try {
      const data = localStorage.getItem(SETTINGS_KEY);
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.warn('LocalStorage load failed:', e);
      return null;
    }
  }

  /**
   * Clear saved DSP settings.
   */
  static clearSettings() {
    try {
      localStorage.removeItem(SETTINGS_KEY);
    } catch (e) {}
  }

  /**
   * Open IndexedDB instance with Promise wrapper.
   * @returns {Promise<IDBDatabase>}
   */
  static openDB() {
    return new Promise((resolve, reject) => {
      if (typeof window === 'undefined' || !window.indexedDB) {
        return reject(new Error('IndexedDB not supported'));
      }
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME);
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  /**
   * Save an uploaded audio File/Blob/ArrayBuffer to IndexedDB.
   * @param {ArrayBuffer|Blob|File} audioData
   * @param {string} fileName
   * @returns {Promise<boolean>}
   */
  static async saveUploadedAudio(audioData, fileName) {
    try {
      const db = await this.openDB();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const record = {
          data: audioData,
          fileName: fileName,
          timestamp: Date.now(),
        };
        const putReq = store.put(record, AUDIO_RECORD_KEY);
        putReq.onsuccess = () => resolve(true);
        putReq.onerror = () => reject(putReq.error);
      });
    } catch (err) {
      console.warn('IndexedDB saveUploadedAudio error:', err);
      return false;
    }
  }

  /**
   * Load the active uploaded audio file from IndexedDB.
   * Returns { data, fileName, timestamp } or null.
   * @returns {Promise<Object|null>}
   */
  static async loadUploadedAudio() {
    try {
      const db = await this.openDB();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readonly');
        const store = tx.objectStore(STORE_NAME);
        const getReq = store.get(AUDIO_RECORD_KEY);
        getReq.onsuccess = () => resolve(getReq.result || null);
        getReq.onerror = () => reject(getReq.error);
      });
    } catch (err) {
      console.warn('IndexedDB loadUploadedAudio error:', err);
      return null;
    }
  }

  /**
   * Clear any persisted uploaded audio from IndexedDB.
   * @returns {Promise<void>}
   */
  static async clearUploadedAudio() {
    try {
      const db = await this.openDB();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const store = tx.objectStore(STORE_NAME);
        const delReq = store.delete(AUDIO_RECORD_KEY);
        delReq.onsuccess = () => resolve(true);
        delReq.onerror = () => reject(delReq.error);
      });
    } catch (err) {
      console.warn('IndexedDB clearUploadedAudio error:', err);
    }
  }
}
