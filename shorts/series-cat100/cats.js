// 100 Days: Cat Apocalypse — original character rig (inked storybook style).
// Every episode draws the cast with these functions, so the characters look identical in every frame.
// cat(name, {x, y, s, face, look, blink, tail, flip}) returns an SVG <g> string.

const INK = '#1d1a22';
const PAL = {
  sky1: '#F2A65A', sky2: '#C8553D', ground: '#4A4E69', shadow: '#22223B',
  zombie: '#8DA47E', zombieDark: '#5C7253', cloth: '#6D597A', blood: '#7A1F2B',
};

const CAST = {
  biscuit: { // Dad — chubby orange tabby, nervous, colander helmet
    fur: '#F4A259', dark: '#C8733A', belly: '#FBE3C4', eye: '#7BC67E', size: 1.12, chubby: 1.18,
    trait: 'DAD · scared of everything', acc: 'colander',
  },
  sage: { // Mum — grey cat, leader, torn ear, red bandana
    fur: '#9AA0A8', dark: '#6B717A', belly: '#E3E5E8', eye: '#F2C14E', size: 1.0, chubby: 1.0,
    trait: 'MUM · the leader', acc: 'bandana', tornEar: true,
  },
  pickles: { // Kid — black cat, mischievous, tiny backpack
    fur: '#2E2A33', dark: '#18151C', belly: '#4A4452', eye: '#FFD23F', size: .86, chubby: .95,
    trait: 'KID · trouble magnet', acc: 'backpack',
  },
  bean: { // Baby — tiny white kitten, huge eyes, gold bell; the accidental hero
    fur: '#FBF7F0', dark: '#E2D9CB', belly: '#FFFFFF', eye: '#6EC1E4', size: .62, chubby: 1.05,
    trait: 'BABY · accidental hero', acc: 'bell',
  },
};

function cat(name, o = {}) {
  const c = CAST[name];
  const { x = 0, y = 0, s = 1, face = 'neutral', look = 0, blink = 0, tail = 0, flip = false } = o;
  const k = s * c.size, w = 1 * c.chubby;
  const st = `stroke="${INK}" stroke-width="${6 / k}" stroke-linejoin="round" stroke-linecap="round"`;
  const eyeOpen = Math.max(0.08, 1 - blink);
  const tailA = 20 * Math.sin(tail);
  let g = `<g transform="translate(${x} ${y}) scale(${flip ? -k : k} ${k})">`;
  // ground shadow
  g += `<ellipse cx="0" cy="4" rx="${95 * w}" ry="14" fill="#000" opacity=".25"/>`;
  // tail
  g += `<path d="M${60 * w} -40 Q${150 * w} ${-60 + tailA} ${120 * w} ${-170 + tailA * 2}" fill="none" stroke="${INK}" stroke-width="${30}" stroke-linecap="round"/>
        <path d="M${60 * w} -40 Q${150 * w} ${-60 + tailA} ${120 * w} ${-170 + tailA * 2}" fill="none" stroke="${c.fur}" stroke-width="${18}" stroke-linecap="round"/>`;
  // body
  g += `<path d="M${-75 * w} 0 Q${-95 * w} -110 ${-40 * w} -150 L${40 * w} -150 Q${95 * w} -110 ${75 * w} 0 Z" fill="${c.fur}" ${st}/>
        <path d="M${-38 * w} -10 Q${-45 * w} -95 0 -110 Q${45 * w} -95 ${38 * w} -10 Z" fill="${c.belly}"/>`;
  // tabby stripes for biscuit
  if (name === 'biscuit') g += [-60, -95, -130].map(yy => `<path d="M${-80 * w} ${yy} q18 -6 30 4 M${80 * w} ${yy} q-18 -6 -30 4" fill="none" stroke="${c.dark}" stroke-width="8" stroke-linecap="round"/>`).join('');
  // paws
  g += `<ellipse cx="${-32 * w}" cy="-4" rx="24" ry="14" fill="${c.fur}" ${st}/><ellipse cx="${32 * w}" cy="-4" rx="24" ry="14" fill="${c.fur}" ${st}/>`;
  // backpack (behind head side)
  if (c.acc === 'backpack') g += `<rect x="${-100 * w}" y="-135" width="38" height="70" rx="12" fill="#E4572E" ${st}/><path d="M${-92 * w} -128 h22" stroke="${INK}" stroke-width="5"/>`;
  // head
  const hy = -205;
  const earL = c.tornEar ? `M-80 ${hy - 20} L-70 ${hy - 105} L-52 ${hy - 82} L-40 ${hy - 95} L-20 ${hy - 62} Z` : `M-80 ${hy - 20} L-62 ${hy - 105} L-20 ${hy - 62} Z`;
  g += `<path d="${earL}" fill="${c.fur}" ${st}/><path d="M80 ${hy - 20} L62 ${hy - 105} L20 ${hy - 62} Z" fill="${c.fur}" ${st}/>
        <path d="M-60 ${hy - 35} L-55 ${hy - 78} L-34 ${hy - 58} Z M60 ${hy - 35} L55 ${hy - 78} L34 ${hy - 58} Z" fill="#F7A1B0"/>
        <ellipse cx="0" cy="${hy}" rx="92" ry="78" fill="${c.fur}" ${st}/>`;
  if (name === 'biscuit') g += `<path d="M-22 ${hy - 74} l8 26 M0 ${hy - 78} v28 M22 ${hy - 74} l-8 26" stroke="${c.dark}" stroke-width="8" stroke-linecap="round"/>`;
  // eyes
  const ex = 36, ey = hy - 6, er = name === 'bean' ? 26 : 21;
  const lx = look * 8;
  for (const sx of [-1, 1]) {
    g += `<ellipse cx="${sx * ex}" cy="${ey}" rx="${er}" ry="${er * 1.12 * eyeOpen}" fill="#fff" ${st}/>`;
    if (eyeOpen > .3) g += `<ellipse cx="${sx * ex + lx}" cy="${ey + 2}" rx="${er * .62}" ry="${er * .78 * eyeOpen}" fill="${c.eye}"/>
      <ellipse cx="${sx * ex + lx}" cy="${ey + 3}" rx="${er * .28}" ry="${er * .6 * eyeOpen}" fill="${INK}"/>
      <circle cx="${sx * ex + lx - 6}" cy="${ey - 8}" r="${er * .22}" fill="#fff"/>`;
  }
  // brows by expression
  const brow = { scared: [[-58, ey - 32, -18, ey - 42], [58, ey - 32, 18, ey - 42]],
                 determined: [[-58, ey - 42, -16, ey - 30], [58, ey - 42, 16, ey - 30]],
                 happy: [[-56, ey - 38, -18, ey - 40], [56, ey - 38, 18, ey - 40]],
                 neutral: [[-56, ey - 36, -18, ey - 36], [56, ey - 36, 18, ey - 36]] }[face] || [];
  g += brow.map(([a, b, cc, d]) => `<path d="M${a} ${b} L${cc} ${d}" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>`).join('');
  // nose + mouth
  g += `<path d="M-9 ${hy + 22} h18 l-9 10 z" fill="#E56B6F" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`;
  const mouth = { scared: `M-14 ${hy + 48} q14 -12 28 0 q-14 22 -28 0`, determined: `M-16 ${hy + 44} h32`,
                  happy: `M-20 ${hy + 38} q10 14 20 0 q10 14 20 0`, neutral: `M-14 ${hy + 40} q7 8 14 0 q7 8 14 0` }[face];
  g += `<path d="${mouth}" fill="${face === 'scared' ? '#5b1f2a' : 'none'}" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`;
  // whiskers
  g += `<path d="M-40 ${hy + 28} l-50 -8 M-40 ${hy + 36} l-48 6 M40 ${hy + 28} l50 -8 M40 ${hy + 36} l48 6" stroke="${INK}" stroke-width="3" opacity=".7"/>`;
  // accessories
  if (c.acc === 'colander') g += `<path d="M-80 ${hy - 40} Q0 ${hy - 150} 80 ${hy - 40} Z" fill="#C9CED6" ${st}/>
      <path d="M-95 ${hy - 40} h190" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>
      ${[-40, -10, 20, 50, -25, 5, 35].map((dx, i) => `<circle cx="${dx}" cy="${hy - 58 - (i > 3 ? 26 : 0)}" r="5" fill="${INK}"/>`).join('')}
      <path d="M-95 ${hy - 40} q-20 0 -22 -16 M95 ${hy - 40} q20 0 22 -16" fill="none" stroke="${INK}" stroke-width="7"/>`;
  if (c.acc === 'bandana') g += `<path d="M-70 ${hy + 52} Q0 ${hy + 92} 70 ${hy + 52} L50 ${hy + 80} Q0 ${hy + 110} -50 ${hy + 80} Z" fill="#D62839" ${st}/>
      <path d="M58 ${hy + 64} l38 26 l-6 -34 z" fill="#D62839" ${st}/>`;
  if (c.acc === 'bell') g += `<path d="M-50 ${hy + 62} Q0 ${hy + 82} 50 ${hy + 62}" fill="none" stroke="#3A86FF" stroke-width="14" stroke-linecap="round"/>
      <circle cx="0" cy="${hy + 86}" r="17" fill="#FFC300" ${st}/><path d="M-8 ${hy + 92} h16" stroke="${INK}" stroke-width="4"/>`;
  if (c.acc === 'backpack') g += `<path d="M-70 ${hy + 60} L-90 -110" stroke="#E4572E" stroke-width="10"/>`;
  return g + '</g>';
}

// Shambler — simple, non-graphic cartoon zombie silhouette.
function zombie(o = {}) {
  const { x = 0, y = 0, s = 1, sway = 0, flip = false } = o;
  const st = `stroke="${INK}" stroke-width="${6 / s}" stroke-linejoin="round" stroke-linecap="round"`;
  const a = 8 * Math.sin(sway);
  return `<g transform="translate(${x} ${y}) scale(${flip ? -s : s} ${s}) rotate(${a / 3})">
    <ellipse cx="0" cy="4" rx="70" ry="12" fill="#000" opacity=".25"/>
    <path d="M-30 0 L-22 -150 M30 0 L22 -150" stroke="${INK}" stroke-width="30" stroke-linecap="round"/>
    <path d="M-30 0 L-22 -150 M30 0 L22 -150" stroke="#3D405B" stroke-width="18" stroke-linecap="round"/>
    <path d="M-55 -140 L-48 -300 Q0 -320 48 -300 L55 -140 Z" fill="${PAL.cloth}" ${st}/>
    <path d="M-40 -290 L${-150} ${-280 + a} M40 -290 L${150} ${-270 - a}" stroke="${INK}" stroke-width="28" stroke-linecap="round"/>
    <path d="M-40 -290 L${-150} ${-280 + a} M40 -290 L${150} ${-270 - a}" stroke="${PAL.zombie}" stroke-width="16" stroke-linecap="round"/>
    <ellipse cx="0" cy="-360" rx="58" ry="66" fill="${PAL.zombie}" ${st}/>
    <circle cx="-22" cy="-370" r="15" fill="#F6F7D7" ${st}/><circle cx="24" cy="-366" r="11" fill="#F6F7D7" ${st}/>
    <circle cx="-22" cy="-370" r="4" fill="${INK}"/><circle cx="24" cy="-366" r="3" fill="${INK}"/>
    <path d="M-26 -322 q14 -10 26 0 q14 10 26 0" fill="none" stroke="${INK}" stroke-width="6"/>
    <path d="M-50 -405 q20 -30 40 -8 q16 -26 40 -4" fill="none" stroke="${PAL.zombieDark}" stroke-width="10" stroke-linecap="round"/>
  </g>`;
}

if (typeof module !== 'undefined') module.exports = { cat, zombie, CAST, PAL, INK };
