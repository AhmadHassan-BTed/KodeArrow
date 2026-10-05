/**
 * NaSuno GitHub Verification & Access Gate
 * Enforces star and follow verification for developer repositories
 * with client-side persistence and dev bypass capabilities.
 *
 * Conceived, Designed, and Authored by Ahmad Hassan (B-Ted)
 */

export const GITHUB_CLIENT_ID = 'Ov23liT2GgHx7axGVy8L';
export const GITHUB_REDIRECT_URI = 'https://AhmadHassan-BTed.github.io/NaSuno/';
export const GITHUB_OAUTH_URL = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(GITHUB_REDIRECT_URI)}&scope=read:user`;

export const EXCLUDED_REPO_KEYS = new Set([
  'ahmadhassan-bted/.github',
  'fractal-compute-orchestrations/.github',
  'ahmadhassan-bted/openopc',
  'ahmadhassan-bted/visiocraft',
  'ahmadhassan-bted/yt-channels-ds-ai-ml-cs',
  'fractal-compute-orchestrations/fractal-privacypolicy',
  'ahmadhassan-bted/attendify',
  'ahmadhassan-bted/portfoliowebsite',
  'ahmadhassan-bted/scrolltoprompt',
  'ahmadhassan-bted/darkument',
  'ahmadhassan-bted/auraeconomy',
  'ahmadhassan-bted/gardenpulse',
  'ahmadhassan-bted/eqai'
]);

export const DEV_BYPASS_KEYS = new Set([
  'btdev',
  'nasuno_admin',
  'nasuno_dev',
  'admin',
  'secret',
  'b-ted',
  'ahmadhassan-bted'
]);

export const FALLBACK_REPOS = {
  'ahmadhassan-bted/nasuno': {
    name: 'AhmadHassan-BTed/NaSuno',
    url: 'https://github.com/AhmadHassan-BTed/NaSuno'
  },
  'ahmadhassan-bted/turnitout-humanizer': {
    name: 'AhmadHassan-BTed/Turnitout-Humanizer',
    url: 'https://github.com/AhmadHassan-BTed/Turnitout-Humanizer'
  },
  'fractal-compute-orchestrations/fractalworkspace': {
    name: 'Fractal-Compute-Orchestrations/FractalWorkspace',
    url: 'https://github.com/Fractal-Compute-Orchestrations/FractalWorkspace'
  },
  'fractal-compute-orchestrations/fractalcore': {
    name: 'Fractal-Compute-Orchestrations/FractalCore',
    url: 'https://github.com/Fractal-Compute-Orchestrations/FractalCore'
  },
  'fractal-compute-orchestrations/fractalandroid': {
    name: 'Fractal-Compute-Orchestrations/FractalAndroid',
    url: 'https://github.com/Fractal-Compute-Orchestrations/FractalAndroid'
  }
};

/**
 * Actively scrubs insecure auth or bypass query parameters from the browser URL.
 * URL parameters are NEVER trusted or used to authorize sessions.
 */
export function cleanInsecureQueryParams() {
  try {
    if (typeof window === 'undefined' || !window.location || !window.history) return;
    const url = new URL(window.location.href);
    let changed = false;
    const badKeys = [
      'key', 'usr', 'user', 'unlock', 'unlocked', 'auth',
      'token', 'code', 'admin', 'secret', 'bypass', 'access'
    ];
    for (const k of badKeys) {
      if (url.searchParams.has(k)) {
        url.searchParams.delete(k);
        changed = true;
      }
    }
    if (changed) {
      const cleanPath = url.pathname + (url.searchParams.toString() ? '?' + url.searchParams.toString() : '') + url.hash;
      window.history.replaceState({}, document.title, cleanPath);
    }
  } catch (_) {}
}

export class AuthPersistence {
  static KEY_UNLOCKED = 'nasuno_unlocked';
  static KEY_USERNAME = 'nasuno_github_username';
  static KEY_LAST_CHECK = 'nasuno_last_check_date';

  /**
   * Resolve valid paths for cookie persistence across root and GitHub Pages subpaths.
   */
  static getCookiePaths() {
    if (typeof window === 'undefined' || !window.location) return ['/'];
    const p = window.location.pathname || '/';
    const base = p.replace(/[^\/]*$/, ''); // e.g. /NaSuno/ on GitHub Pages
    const set = new Set(['/', base, p]);
    return Array.from(set).filter(Boolean);
  }

  static isUnlocked() {
    cleanInsecureQueryParams();
    try {
      const val = localStorage.getItem(this.KEY_UNLOCKED);
      if (val === 'false' || val === '0' || val === 'revoked') return false;
      if (val === 'true' || val === '1') return true;

      // Cookie fallback
      const m = document.cookie.match(new RegExp('(?:^|; )' + this.KEY_UNLOCKED + '=([^;]*)'));
      if (m) {
        const cVal = decodeURIComponent(m[1]).trim().toLowerCase();
        if (cVal === 'false' || cVal === '0' || cVal === 'revoked') return false;
        return cVal === 'true' || cVal === '1';
      }
      return false;
    } catch (_) {
      return false;
    }
  }

  static getSavedUsername() {
    cleanInsecureQueryParams();
    try {
      const u = localStorage.getItem(this.KEY_USERNAME);
      if (u && u.trim()) return u.trim();
      const m = document.cookie.match(new RegExp('(?:^|; )' + this.KEY_USERNAME + '=([^;]*)'));
      return m ? decodeURIComponent(m[1]).trim() : '';
    } catch (_) {
      return '';
    }
  }

  static loginUser(username) {
    cleanInsecureQueryParams();
    const cleanUser = String(username).trim();
    if (!cleanUser) return;

    try {
      localStorage.setItem(this.KEY_UNLOCKED, 'true');
      localStorage.setItem(this.KEY_USERNAME, cleanUser);
      localStorage.setItem(this.KEY_LAST_CHECK, new Date().toISOString().slice(0, 10));

      const maxAge = 31536000; // 1 year
      const isHttps = typeof window !== 'undefined' && window.location && window.location.protocol === 'https:';
      const flags = `; SameSite=Lax${isHttps ? '; Secure; Partitioned' : ''}`;

      for (const p of this.getCookiePaths()) {
        document.cookie = `${this.KEY_UNLOCKED}=true; path=${p}; max-age=${maxAge}${flags}`;
        document.cookie = `${this.KEY_USERNAME}=${encodeURIComponent(cleanUser)}; path=${p}; max-age=${maxAge}${flags}`;
        document.cookie = `${this.KEY_LAST_CHECK}=${new Date().toISOString().slice(0, 10)}; path=${p}; max-age=${maxAge}${flags}`;
      }
    } catch (_) {}
  }

  static logoutUser() {
    cleanInsecureQueryParams();
    try {
      localStorage.setItem(this.KEY_UNLOCKED, 'false');
      localStorage.removeItem(this.KEY_USERNAME);
      localStorage.removeItem(this.KEY_LAST_CHECK);

      const isHttps = typeof window !== 'undefined' && window.location && window.location.protocol === 'https:';
      const flags = `; SameSite=Lax${isHttps ? '; Secure; Partitioned' : ''}`;

      for (const p of this.getCookiePaths()) {
        document.cookie = `${this.KEY_UNLOCKED}=false; path=${p}; max-age=86400${flags}`;
        document.cookie = `${this.KEY_USERNAME}=; path=${p}; max-age=0${flags}`;
        document.cookie = `${this.KEY_LAST_CHECK}=; path=${p}; max-age=0${flags}`;
      }
    } catch (_) {}
  }
}

export function extractGitHubUsername(inputStr) {
  if (!inputStr) return '';
  let s = String(inputStr).trim();
  const match = s.match(/(?:https?:\/\/)?(?:www\.)?github\.com\/([^/?#]+)/i);
  if (match) {
    return match[1].replace(/[^a-zA-Z0-9_-]/g, '');
  }
  s = s.replace(/^@+/, '').replace(/\/+$/, '').trim();
  return s.replace(/[^a-zA-Z0-9_-]/g, '');
}

export function isValidGitHubUsername(username) {
  if (!username || username.length > 39) return false;
  if (isDevSecretKey(username)) return true;
  return /^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$/.test(username);
}

export function isDevSecretKey(inputStr) {
  if (!inputStr) return false;
  const clean = String(inputStr).trim().toLowerCase().replace(/^@+/, '').replace(/\/+$/, '');
  return DEV_BYPASS_KEYS.has(clean);
}

export async function checkIsFollowing(username, targetUser = 'AhmadHassan-BTed') {
  if (isDevSecretKey(username)) return { following: true, rateLimited: false };
  const clean = extractGitHubUsername(username);
  if (!clean) return { following: false, rateLimited: false };
  if (clean.toLowerCase() === targetUser.toLowerCase()) return { following: true, rateLimited: false };

  try {
    const res = await fetch(`https://api.github.com/users/${encodeURIComponent(clean)}/following/${encodeURIComponent(targetUser)}`, {
      headers: { Accept: 'application/vnd.github.v3+json' }
    });
    if (res.status === 403) {
      return { following: false, rateLimited: true };
    }
    // GitHub returns 204 No Content if following, 404 if not
    return { following: res.status === 204 || res.status === 200, rateLimited: false };
  } catch (_) {
    return { following: false, rateLimited: false };
  }
}

export async function getDeveloperRepos() {
  const reposDict = {};

  // 1. Fetch user public repos
  try {
    const res = await fetch('https://api.github.com/users/AhmadHassan-BTed/repos?per_page=100&type=public', {
      headers: { Accept: 'application/vnd.github.v3+json' }
    });
    if (res.ok) {
      const list = await res.json();
      if (Array.isArray(list)) {
        for (const r of list) {
          const fn = r.full_name;
          const fnLower = fn.toLowerCase();
          const isPrivate = r.private === true || r.visibility === 'private';
          if (!isPrivate && !EXCLUDED_REPO_KEYS.has(fnLower)) {
            reposDict[fnLower] = {
              name: fn,
              url: r.html_url || `https://github.com/${fn}`
            };
          }
        }
      }
    }
  } catch (_) {}

  // 2. Fetch org public repos
  try {
    const res = await fetch('https://api.github.com/orgs/Fractal-Compute-Orchestrations/repos?per_page=100&type=public', {
      headers: { Accept: 'application/vnd.github.v3+json' }
    });
    if (res.ok) {
      const list = await res.json();
      if (Array.isArray(list)) {
        for (const r of list) {
          const fn = r.full_name;
          const fnLower = fn.toLowerCase();
          const isPrivate = r.private === true || r.visibility === 'private';
          if (!isPrivate && !EXCLUDED_REPO_KEYS.has(fnLower)) {
            reposDict[fnLower] = {
              name: fn,
              url: r.html_url || `https://github.com/${fn}`
            };
          }
        }
      }
    }
  } catch (_) {}

  // Fallback if network or rate limit occurred
  if (Object.keys(reposDict).length === 0) {
    Object.assign(reposDict, FALLBACK_REPOS);
  }

  return reposDict;
}

export async function verifyAllGitHubStars(username, devRepos) {
  if (isDevSecretKey(username)) {
    return { success: true, message: 'Dev access granted.', unstarred: [] };
  }

  const clean = extractGitHubUsername(username);
  if (!clean) {
    return { success: false, message: 'Invalid username format.', unstarred: [] };
  }

  const userStarredSet = new Set();

  try {
    for (let page = 1; page <= 4; page++) {
      const res = await fetch(`https://api.github.com/users/${encodeURIComponent(clean)}/starred?per_page=100&page=${page}`, {
        headers: { Accept: 'application/vnd.github.v3+json' }
      });
      if (res.status === 404) {
        return { success: false, message: `GitHub user '${clean}' not found. Please check spelling.`, unstarred: [] };
      }
      if (res.status === 403) {
        return {
          success: false,
          isRateLimited: true,
          message: 'GitHub API rate limit reached. Please star repositories directly and use bypass key btdev.',
          unstarred: Object.values(devRepos)
        };
      }
      if (!res.ok) break;

      const pageData = await res.json();
      if (!Array.isArray(pageData) || pageData.length === 0) break;

      for (const item of pageData) {
        if (item.full_name) {
          userStarredSet.add(item.full_name.toLowerCase());
        }
      }
      if (pageData.length < 100) break;
    }

    const unstarred = [];
    for (const [key, repo] of Object.entries(devRepos)) {
      if (!userStarredSet.has(key)) {
        unstarred.push(repo);
      }
    }

    if (unstarred.length === 0) {
      return { success: true, message: 'All repositories verified starred!', unstarred: [] };
    } else {
      return {
        success: false,
        message: `${unstarred.length} repository${unstarred.length === 1 ? '' : 'ies'} remaining to star.`,
        unstarred
      };
    }
  } catch (err) {
    return { success: false, message: `Network error verifying stars: ${err.message}`, unstarred: [] };
  }
}

export async function verifyGitHubStatus(inputStr) {
  cleanInsecureQueryParams();
  const cleanInput = String(inputStr).trim();
  if (isDevSecretKey(cleanInput)) {
    return {
      success: true,
      username: 'DevAdmin',
      message: 'Admin / Dev secret key verified. Full access authorized.',
      isFollowingUser: true,
      isFollowingOrg: true,
      unstarred: [],
      isRateLimited: false
    };
  }

  const username = extractGitHubUsername(cleanInput);
  if (!username) {
    return {
      success: false,
      username: '',
      message: 'Please enter a valid GitHub username.',
      isFollowingUser: false,
      isFollowingOrg: false,
      unstarred: [],
      isRateLimited: false
    };
  }

  if (username.toLowerCase() === 'ahmadhassan-bted') {
    return {
      success: true,
      username: 'AhmadHassan-BTed',
      message: 'Welcome back, Ahmad Hassan! Developer identity confirmed.',
      isFollowingUser: true,
      isFollowingOrg: true,
      unstarred: [],
      isRateLimited: false
    };
  }

  if (!isValidGitHubUsername(username)) {
    return {
      success: false,
      username,
      message: 'Invalid GitHub username format.',
      isFollowingUser: false,
      isFollowingOrg: false,
      unstarred: [],
      isRateLimited: false
    };
  }

  // Parallel follow checks & repo discovery
  const [userFollow, orgFollow, devRepos] = await Promise.all([
    checkIsFollowing(username, 'AhmadHassan-BTed'),
    checkIsFollowing(username, 'Fractal-Compute-Orchestrations'),
    getDeveloperRepos()
  ]);

  const starResult = await verifyAllGitHubStars(username, devRepos);
  const isRateLimited = userFollow.rateLimited || orgFollow.rateLimited || starResult.isRateLimited;

  if (isRateLimited) {
    return {
      success: false,
      username,
      isFollowingUser: userFollow.following,
      isFollowingOrg: orgFollow.following,
      message: 'GitHub API rate limit reached (60 req/hr). Star the repositories below, then use dev bypass key btdev to unlock.',
      unstarred: starResult.unstarred && starResult.unstarred.length > 0 ? starResult.unstarred : Object.values(devRepos),
      isRateLimited: true
    };
  }

  const allPassed = userFollow.following && orgFollow.following && starResult.success;

  return {
    success: allPassed,
    username,
    isFollowingUser: userFollow.following,
    isFollowingOrg: orgFollow.following,
    message: allPassed
      ? 'Verification complete! Thank you for supporting the project.'
      : starResult.message,
    unstarred: starResult.unstarred || [],
    isRateLimited: false
  };
}
