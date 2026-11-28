// 100 Days: Cat Apocalypse — original character rig v2 (inked storybook style, cel-shaded).
// Every episode draws the cast with these functions, so the characters look identical in every frame.
//
// cat(name, opts) / zombie(opts) return an SVG <g> string.
// Outline is a constant OUTLINE px on screen for every character at any size (pass the camera zoom as `cam`).
// opts: x, y, s (scale), face (neutral|scared|determined|happy|sleep), look (-1..1), blink (0..1),
//       tail (phase), breathe (phase), ear (0..1 ear swivel), flip, light ('warm'|'cool'|'red'), cam (camera zoom)

const INK = '#17131C';
const OUTLINE = 7;            // screen px — identical for every character
const PAL = {
  sky1: '#2B1B3F', sky2: '#B83B5E', sky3: '#F08A4B', ground: '#2E2A3B', shadow: '#1B1726',
  zombie: '#93B27F', zombieShade: '#5E7F55', cloth: '#6C4F8C', clothShade: '#46325E',
};
const LIGHT = { warm: '#FFC26B', cool: '#7FD1FF', red: '#FF5E5B' };

const CAST = {
  biscuit: { fur: '#FF9F43', shade: '#D2662A', hi: '#FFC58A', belly: '#FFE7C7', stripe: '#C85A22', eye: '#6BD66F', size: 1.12, chubby: 1.18,
             trait: 'DAD · scared of everything', acc: 'colander' },
  sage:    { fur: '#A3AFBD', shade: '#6F7C8E', hi: '#CBD4DE', belly: '#EEF1F4', eye: '#FFC93C', size: 1.0, chubby: 1.0,
             trait: 'MUM · the leader', acc: 'bandana', tornEar: true },
  pickles: { fur: '#2F2742', shade: '#19132A', hi: '#4E4470', belly: '#463C5E', eye: '#FFD93D', size: .86, chubby: .95,
             trait: 'KID · trouble magnet', acc: 'backpack' },
  bean:    { fur: '#FFFDF7', shade: '#E3D3BC', hi: '#FFFFFF', belly: '#FFFFFF', eye: '#4FC3F7', size: .62, chubby: 1.05,
             trait: 'BABY · accidental hero', acc: 'bell' },
};

let UID = 0;

function cat(name, o = {}) {
  const c = CAST[name];
  const { x = 0, y = 0, s = 1, face = 'neutral', look = 0, blink = 0, tail = 0, breathe = 0, ear = 0,
          flip = false, light = 'warm', cam = 1 } = o;
  const id = 'c' + (UID++);
  const k = s * c.size, w = c.chubby;
  const ow = OUTLINE / (k * cam);                // outline width in local units -> constant on screen
  const st = `stroke="${INK}" stroke-width="${ow}" stroke-linejoin="round" stroke-linecap="round"`;
  const rim = LIGHT[light] || LIGHT.warm;
  const eyeOpen = face === 'sleep' ? 0.06 : Math.max(0.08, 1 - blink);
  const tailA = 22 * Math.sin(tail);
  const br = 1 + 0.025 * Math.sin(breathe);
  const hy = -205 - 4 * Math.sin(breathe);

  const bodyD = `M${-75 * w} 0 Q${-95 * w} -110 ${-40 * w} -150 L${40 * w} -150 Q${95 * w} -110 ${75 * w} 0 Z`;
  const tailD = `M${60 * w} -40 Q${150 * w} ${-60 + tailA} ${120 * w} ${-170 + tailA * 2}`;
  const earRotL = -25 * ear, earRotR = 35 * ear;
  const earLD = c.tornEar ? `M-80 ${hy - 20} L-70 ${hy - 105} L-52 ${hy - 82} L-40 ${hy - 95} L-20 ${hy - 62} Z` : `M-80 ${hy - 20} L-62 ${hy - 105} L-20 ${hy - 62} Z`;
  const earRD = `M80 ${hy - 20} L62 ${hy - 105} L20 ${hy - 62} Z`;

  let g = `<g transform="translate(${x} ${y}) scale(${flip ? -k : k} ${k})">
  <defs>
    <clipPath id="${id}b"><path d="${bodyD}"/></clipPath>
    <clipPath id="${id}h"><ellipse cx="0" cy="${hy}" rx="92" ry="78"/></clipPath>
    <radialGradient id="${id}g" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="${c.hi}"/><stop offset=".55" stop-color="${c.fur}"/><stop offset="1" stop-color="${c.fur}"/></radialGradient>
  </defs>
  <ellipse cx="0" cy="6" rx="${100 * w}" ry="16" fill="#000" opacity=".35"/>`;
  // tail (outline = fill width + 2 outlines, so it matches every other edge)
  g += `<path d="${tailD}" fill="none" stroke="${INK}" stroke-width="${18 + 2 * ow}" stroke-linecap="round"/>
        <path d="${tailD}" fill="none" stroke="${c.fur}" stroke-width="18" stroke-linecap="round"/>
        <path d="${tailD}" fill="none" stroke="${c.shade}" stroke-width="7" stroke-linecap="round" transform="translate(5 3)" opacity=".8"/>`;
  if (c.acc === 'backpack') g += `<rect x="${-102 * w}" y="-138" width="40" height="72" rx="12" fill="#F0662F" ${st}/><rect x="${-102 * w}" y="-104" width="40" height="34" rx="10" fill="#B9431C"/><path d="M${-94 * w} -128 h22" stroke="${INK}" stroke-width="${ow * .6}"/>`;
  // body: base gradient + cel shadow + rim light, all clipped to the silhouette
  g += `<g transform="scale(1 ${br}) "><path d="${bodyD}" fill="url(#${id}g)"/>
    <g clip-path="url(#${id}b)">
      <path d="M${-38 * w} -10 Q${-45 * w} -95 0 -110 Q${45 * w} -95 ${38 * w} -10 Z" fill="${c.belly}"/>
      ${name === 'biscuit' ? [-60, -95, -130].map(yy => `<path d="M${-82 * w} ${yy} q18 -6 30 4 M${82 * w} ${yy} q-18 -6 -30 4" fill="none" stroke="${c.stripe}" stroke-width="9" stroke-linecap="round"/>`).join('') : ''}
      <ellipse cx="${70 * w}" cy="-60" rx="${55 * w}" ry="120" fill="${c.shade}" opacity=".75"/>
      <ellipse cx="0" cy="8" rx="${110 * w}" ry="28" fill="${c.shade}" opacity=".55"/>
      <path d="${bodyD}" fill="none" stroke="${rim}" stroke-width="10" transform="translate(-6 -4)" opacity=".55"/>
    </g>
    <path d="${bodyD}" fill="none" ${st}/></g>`;
  g += `<ellipse cx="${-32 * w}" cy="-4" rx="25" ry="15" fill="${c.fur}" ${st}/><ellipse cx="${32 * w}" cy="-4" rx="25" ry="15" fill="${c.fur}" ${st}/>
        <path d="M${-38 * w} -6 v8 M${-26 * w} -6 v8 M${26 * w} -6 v8 M${38 * w} -6 v8" stroke="${INK}" stroke-width="${ow * .45}" stroke-linecap="round"/>`;
  // ears (swivel for the "cat fact" shot)
  g += `<g transform="rotate(${earRotL} -50 ${hy - 40})"><path d="${earLD}" fill="${c.fur}" ${st}/><path d="M-62 ${hy - 35} L-57 ${hy - 80} L-36 ${hy - 58} Z" fill="#FF8FA3"/></g>
        <g transform="rotate(${earRotR} 50 ${hy - 40})"><path d="${earRD}" fill="${c.fur}" ${st}/><path d="M62 ${hy - 35} L57 ${hy - 80} L36 ${hy - 58} Z" fill="#FF8FA3"/></g>`;
  // head
  g += `<ellipse cx="0" cy="${hy}" rx="92" ry="78" fill="url(#${id}g)"/>
    <g clip-path="url(#${id}h)">
      <ellipse cx="62" cy="${hy + 30}" rx="70" ry="90" fill="${c.shade}" opacity=".7"/>
      <ellipse cx="0" cy="${hy + 34}" rx="54" ry="34" fill="${c.belly}" opacity=".9"/>
      <ellipse cx="0" cy="${hy}" rx="92" ry="78" fill="none" stroke="${rim}" stroke-width="10" transform="translate(-7 -6)" opacity=".5"/>
      ${name === 'biscuit' ? `<path d="M-22 ${hy - 74} l8 26 M0 ${hy - 78} v28 M22 ${hy - 74} l-8 26" stroke="${c.stripe}" stroke-width="9" stroke-linecap="round"/>` : ''}
    </g>
    <ellipse cx="0" cy="${hy}" rx="92" ry="78" fill="none" ${st}/>`;
  // eyes
  const ex = 36, ey = hy - 6, er = name === 'bean' ? 26 : 21, lx = look * 8;
  for (const sx of [-1, 1]) {
    if (face === 'sleep') { g += `<path d="M${sx * ex - er} ${ey} q${er} ${er * .7} ${2 * er} 0" fill="none" stroke="${INK}" stroke-width="${ow}" stroke-linecap="round"/>`; continue; }
    g += `<ellipse cx="${sx * ex}" cy="${ey}" rx="${er}" ry="${er * 1.12 * eyeOpen}" fill="#fff" ${st}/>`;
    if (eyeOpen > .3) g += `<ellipse cx="${sx * ex + lx}" cy="${ey + 2}" rx="${er * .64}" ry="${er * .8 * eyeOpen}" fill="${c.eye}"/>
      <ellipse cx="${sx * ex + lx}" cy="${ey + 6}" rx="${er * .64}" ry="${er * .4 * eyeOpen}" fill="#000" opacity=".18"/>
      <ellipse cx="${sx * ex + lx}" cy="${ey + 3}" rx="${er * (face === 'scared' ? .14 : .28)}" ry="${er * .6 * eyeOpen}" fill="${INK}"/>
      <circle cx="${sx * ex + lx - 6}" cy="${ey - 8}" r="${er * .24}" fill="#fff"/><circle cx="${sx * ex + lx + 6}" cy="${ey + 7}" r="${er * .1}" fill="#fff"/>`;
  }
  const brow = { scared: [[-58, ey - 32, -18, ey - 44], [58, ey - 32, 18, ey - 44]],
                 determined: [[-58, ey - 44, -16, ey - 30], [58, ey - 44, 16, ey - 30]],
                 happy: [[-56, ey - 38, -18, ey - 41], [56, ey - 38, 18, ey - 41]],
                 neutral: [[-56, ey - 36, -18, ey - 36], [56, ey - 36, 18, ey - 36]], sleep: [] }[face] || [];
  g += brow.map(([a, b, cc, d]) => `<path d="M${a} ${b} L${cc} ${d}" stroke="${INK}" stroke-width="${ow * 1.1}" stroke-linecap="round"/>`).join('');
  g += `<ellipse cx="-58" cy="${hy + 26}" rx="14" ry="8" fill="#FF6F91" opacity=".45"/><ellipse cx="58" cy="${hy + 26}" rx="14" ry="8" fill="#FF6F91" opacity=".45"/>
        <path d="M-9 ${hy + 22} h18 l-9 10 z" fill="#E85D75" stroke="${INK}" stroke-width="${ow * .6}" stroke-linejoin="round"/>`;
  const mouth = { scared: `M-14 ${hy + 48} q14 -12 28 0 q-14 22 -28 0`, determined: `M-16 ${hy + 44} h32`,
                  happy: `M-20 ${hy + 38} q10 14 20 0 q10 14 20 0`, neutral: `M-14 ${hy + 40} q7 8 14 0 q7 8 14 0`,
                  sleep: `M-10 ${hy + 40} q10 6 20 0` }[face];
  g += `<path d="${mouth}" fill="${face === 'scared' ? '#5B1F2A' : 'none'}" stroke="${INK}" stroke-width="${ow * .75}" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M-40 ${hy + 28} l-50 -8 M-40 ${hy + 36} l-48 6 M40 ${hy + 28} l50 -8 M40 ${hy + 36} l48 6" stroke="${INK}" stroke-width="${ow * .4}" opacity=".75"/>`;
  // accessories
  if (c.acc === 'colander') g += `<path d="M-80 ${hy - 40} Q0 ${hy - 150} 80 ${hy - 40} Z" fill="#D5DBE3" ${st}/>
      <path d="M10 ${hy - 120} Q60 ${hy - 100} 72 ${hy - 46} L30 ${hy - 46}Z" fill="#9AA3B0" opacity=".7"/>
      <path d="M-50 ${hy - 90} q20 -20 40 -24" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".8"/>
      <path d="M-95 ${hy - 40} h190" stroke="${INK}" stroke-width="${ow * 1.5}" stroke-linecap="round"/>
      ${[-40, -10, 20, 50, -25, 5, 35].map((dx, i) => `<circle cx="${dx}" cy="${hy - 58 - (i > 3 ? 26 : 0)}" r="5" fill="${INK}"/>`).join('')}`;
  if (c.acc === 'bandana') g += `<path d="M-70 ${hy + 52} Q0 ${hy + 92} 70 ${hy + 52} L50 ${hy + 80} Q0 ${hy + 110} -50 ${hy + 80} Z" fill="#E63946" ${st}/>
      <path d="M-40 ${hy + 78} Q0 ${hy + 100} 40 ${hy + 78}" fill="none" stroke="#9E1B2A" stroke-width="6"/>
      <path d="M58 ${hy + 64} l38 26 l-6 -34 z" fill="#E63946" ${st}/>`;
  if (c.acc === 'bell') g += `<path d="M-50 ${hy + 62} Q0 ${hy + 82} 50 ${hy + 62}" fill="none" stroke="${INK}" stroke-width="${14 + 2 * ow}" stroke-linecap="round"/>
      <path d="M-50 ${hy + 62} Q0 ${hy + 82} 50 ${hy + 62}" fill="none" stroke="#3A86FF" stroke-width="14" stroke-linecap="round"/>
      <circle cx="0" cy="${hy + 88}" r="18" fill="#FFC300" ${st}/><circle cx="-6" cy="${hy + 82}" r="6" fill="#FFF3B0"/>
      <path d="M-9 ${hy + 94} h18" stroke="${INK}" stroke-width="${ow * .6}"/>`;
  if (c.acc === 'backpack') g += `<path d="M-70 ${hy + 60} L-90 -110" stroke="${INK}" stroke-width="${10 + 2 * ow}"/><path d="M-70 ${hy + 60} L-90 -110" stroke="#F0662F" stroke-width="10"/>`;
  return g + '</g>';
}

// Shambler — cartoon zombie, cel-shaded, non-graphic. turn: 0 = facing camera, 1 = looking toward +x.
function zombie(o = {}) {
  const { x = 0, y = 0, s = 1, sway = 0, flip = false, turn = 0, cam = 1, light = 'red', glow = 0 } = o;
  const ow = OUTLINE / (s * cam);
  const st = `stroke="${INK}" stroke-width="${ow}" stroke-linejoin="round" stroke-linecap="round"`;
  const rim = LIGHT[light] || LIGHT.red;
  const a = 8 * Math.sin(sway), hx = 18 * turn;
  const limb = (d, col, wdt) => `<path d="${d}" stroke="${INK}" stroke-width="${wdt + 2 * ow}" stroke-linecap="round" fill="none"/><path d="${d}" stroke="${col}" stroke-width="${wdt}" stroke-linecap="round" fill="none"/>`;
  return `<g transform="translate(${x} ${y}) scale(${flip ? -s : s} ${s}) rotate(${a / 3})">
    <ellipse cx="0" cy="6" rx="80" ry="14" fill="#000" opacity=".4"/>
    ${limb('M-30 0 L-22 -150', '#3D405B', 20)}${limb('M30 0 L22 -150', '#2B2D42', 20)}
    <path d="M-55 -140 L-48 -300 Q0 -320 48 -300 L55 -140 Z" fill="${PAL.cloth}"/>
    <path d="M10 -310 Q48 -300 55 -140 L20 -140 Z" fill="${PAL.clothShade}"/>
    <path d="M-55 -140 L-48 -300 Q0 -320 48 -300 L55 -140 Z" fill="none" stroke="${rim}" stroke-width="8" transform="translate(-5 -3)" opacity=".45"/>
    <path d="M-30 -230 l20 14 l-8 22 M20 -180 l18 -10" stroke="${PAL.clothShade}" stroke-width="6" fill="none"/>
    <path d="M-55 -140 L-48 -300 Q0 -320 48 -300 L55 -140 Z" fill="none" ${st}/>
    ${limb(`M-40 -290 L-150 ${-280 + a}`, PAL.zombie, 17)}${limb(`M40 -290 L150 ${-270 - a}`, PAL.zombieShade, 17)}
    <g transform="translate(${hx} 0)">
      <ellipse cx="0" cy="-360" rx="58" ry="66" fill="${PAL.zombie}"/>
      <ellipse cx="${30 - hx}" cy="-340" rx="40" ry="62" fill="${PAL.zombieShade}" opacity=".8"/>
      <ellipse cx="0" cy="-360" rx="58" ry="66" fill="none" ${st}/>
      <circle cx="${-22 + hx}" cy="-370" r="15" fill="#F6F7D7" ${st}/><circle cx="${24 + hx}" cy="-366" r="11" fill="#F6F7D7" ${st}/>
      ${glow ? `<circle cx="${-22 + hx}" cy="-370" r="26" fill="#E9FF70" opacity="${.35 * glow}"/><circle cx="${24 + hx}" cy="-366" r="20" fill="#E9FF70" opacity="${.35 * glow}"/>` : ''}
      <circle cx="${-22 + hx * 1.4}" cy="-370" r="4" fill="${INK}"/><circle cx="${24 + hx * 1.4}" cy="-366" r="3" fill="${INK}"/>
      <path d="M${-26 + hx} -322 q14 -10 26 0 q14 10 26 0" fill="none" stroke="${INK}" stroke-width="${ow * .8}"/>
      <path d="M-50 -405 q20 -30 40 -8 q16 -26 40 -4" fill="none" stroke="${PAL.zombieShade}" stroke-width="10" stroke-linecap="round"/>
    </g>
  </g>`;
}

if (typeof module !== 'undefined') module.exports = { cat, zombie, CAST, PAL, INK, OUTLINE, LIGHT };
