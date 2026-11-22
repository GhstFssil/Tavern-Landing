/* The Unassuming Tavern landing page. Plain JS, no build step. Search for the "---------- name ----------" markers to find a section. */
var APP_VERSION = '1';

/* ---------- sprites ---------- */
// 32-bit style pixel art drawn as SVG rects from ASCII maps. '.' is transparent.
var SPRITE_COLORS = {
  k: '#1a0b05', o: '#ff8a1c', O: '#ffc247', r: '#d6342b', t: '#17d6c0', T: '#8ffbea',
  w: '#fff6e0', b: '#7a4a2b', B: '#a9683a'
};
var SPRITES = {
  torchA: [
    '....r...',
    '..rOr...',
    '.rOOOr..',
    '.rOOOOr.',
    '.rOwwOr.',
    '..rOOr..',
    '.kbBBbk.',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '.kkkkkk.'
  ],
  torchB: [
    '...r....',
    '..rOr...',
    '..rOOr..',
    '.rOOOOr.',
    '.rOwwOr.',
    '..rOOr..',
    '.kbBBbk.',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '..kbbk..',
    '.kkkkkk.'
  ]
};

function spriteSVG(rows) {
  var h = rows.length, w = rows[0].length, out = '';
  for (var y = 0; y < h; y++) {
    var x = 0;
    while (x < w) {
      var c = rows[y][x];
      if (c === '.' || !SPRITE_COLORS[c]) { x++; continue; }
      var x2 = x;
      while (x2 + 1 < w && rows[y][x2 + 1] === c) x2++;
      out += '<rect x="' + x + '" y="' + y + '" width="' + (x2 - x + 1) + '" height="1" fill="' + SPRITE_COLORS[c] + '"/>';
      x = x2 + 1;
    }
  }
  return '<svg viewBox="0 0 ' + w + ' ' + h + '" shape-rendering="crispEdges" focusable="false" aria-hidden="true">' + out + '</svg>';
}

/* ---------- doors (links from config.js) ---------- */
function doorUrl(site, domain) {
  var sub = (site.subdomain || '').trim(), dom = (domain || '').trim();
  var raw = '';
  if (dom && sub) raw = 'https://' + (sub.indexOf('.') > -1 ? sub : sub + '.' + dom) + '/';
  else if ((site.githubPage || '').trim()) raw = site.githubPage.trim();
  if (!raw) return '';
  try {
    var u = new URL(raw);
    return u.protocol === 'https:' ? u.href : '';
  } catch (e) { return ''; }
}

function buildDoors() {
  var cfg = window.TAVERN_CONFIG || { domain: '', sites: [] };
  var list = document.getElementById('doors');
  cfg.sites.forEach(function (site) {
    var url = doorUrl(site, cfg.domain);
    var li = document.createElement('li');
    var el = document.createElement(url ? 'a' : 'button');
    el.className = 'btn' + (url ? '' : ' locked');
    el.setAttribute('data-site', site.id);
    if (url) { el.href = url; el.rel = 'noopener'; }
    else { el.type = 'button'; el.setAttribute('aria-disabled', 'true'); }
    el.innerHTML = '<span class="face"><span class="label"></span></span>';
    el.querySelector('.label').textContent = site.label;
    if (!url) el.addEventListener('click', function () { toast('The door to ' + site.label + ' is barred for now.'); });
    li.appendChild(el);
    list.appendChild(li);
  });
}

/* ---------- toast ---------- */
var toastTimer = 0;
function toast(msg) {
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function () { t.hidden = true; }, 2600);
}

/* ---------- scene ---------- */
function buildTorches() {
  var els = document.querySelectorAll('[data-sprite="torch"]');
  for (var i = 0; i < els.length; i++) {
    els[i].innerHTML = '<span class="fa">' + spriteSVG(SPRITES.torchA) + '</span><span class="fb">' + spriteSVG(SPRITES.torchB) + '</span>';
  }
}

// Whole-number pixel scale for the floor so every art pixel stays square and crisp.
function fitFloor() {
  var scale = Math.max(2, Math.ceil(Math.max(window.innerWidth, window.innerHeight) / 192));
  document.documentElement.style.setProperty('--floor-size', (192 * scale) + 'px');
}

/* ---------- boot ---------- */
document.getElementById('ver').textContent = 'v' + APP_VERSION;
buildDoors();
buildTorches();
fitFloor();
window.addEventListener('resize', fitFloor);
