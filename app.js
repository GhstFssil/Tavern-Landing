/* The Unassuming Tavern landing page. Plain JS, no build step. Search for the "---------- name ----------" markers to find a section. */
var APP_VERSION = '3';

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
    if (!url) el.addEventListener('click', function () { toast(site.label + ': Coming soon.'); });
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
// Whole-number pixel scale for the floor so every art pixel stays square and crisp.
function fitFloor() {
  var scale = Math.max(2, Math.ceil(Math.max(window.innerWidth, window.innerHeight) / 192));
  document.documentElement.style.setProperty('--floor-size', (192 * scale) + 'px');
}

/* ---------- boot ---------- */
document.getElementById('ver').textContent = 'v' + APP_VERSION;
buildDoors();
fitFloor();
window.addEventListener('resize', fitFloor);
