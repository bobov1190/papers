import re
D = 'C:/Users/bobov/Desktop/papers/'
SRC = open(D + 'linlesson1.html', encoding='utf-8').read()
HEAD_A = SRC[:SRC.index('<title>')]
HEAD_B = SRC[SRC.index('</title>') + 8:SRC.index('<main')]
_b = SRC.index('<div id="controlBar"')
BAR = SRC[_b:SRC.index('<script>', _b)]
JSC = SRC[SRC.index('<script>', _b):SRC.index('const loss =')]

JSLIB = r'''
        const fmt = (v) => (Number.isInteger(v) ? String(v) : String(+v.toFixed(3)));
        function Ax(svg, o) {
            const iw = o.W - o.l - o.r, ih = o.H - o.t - o.b;
            const sx = (v) => o.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * iw;
            const sy = (v) => o.H - o.b - (v - o.y[0]) / (o.y[1] - o.y[0]) * ih;
            const id = 'c' + Math.random().toString(36).slice(2);
            const defs = el(svg, 'defs', {});
            const cp = el(defs, 'clipPath', { id });
            el(cp, 'rect', { x: o.l, y: o.t, width: iw, height: ih });
            el(svg, 'path', { d: 'M' + o.l + ' ' + o.t + 'V' + (o.H - o.b) + 'H' + (o.W - o.r), fill: 'none', stroke: 'currentColor', 'stroke-width': 1, opacity: 0.6 });
            (o.xt || []).forEach(v => el(svg, 'text', { x: sx(v), y: o.H - o.b + 16, 'text-anchor': 'middle', 'font-size': 11, fill: 'currentColor' }, String(v)));
            (o.yt || []).forEach(v => el(svg, 'text', { x: o.l - 6, y: sy(v) + 4, 'text-anchor': 'end', 'font-size': 11, fill: 'currentColor' }, String(v)));
            if (o.xl) el(svg, 'text', { x: o.W - o.r, y: o.H - 3, 'text-anchor': 'end', 'font-size': 12, fill: 'currentColor' }, o.xl);
            if (o.yl) el(svg, 'text', { x: o.l + 4, y: o.t - 6, 'font-size': 12, fill: 'currentColor' }, o.yl);
            const g = el(svg, 'g', { 'clip-path': 'url(#' + id + ')' });
            return { sx, sy, g, svg };
        }
        function Curve(a, fn, x0, x1, col, w, n) {
            n = n || 140;
            let d = '';
            for (let i = 0; i <= n; i++) {
                const x = x0 + (x1 - x0) * i / n;
                d += (i ? 'L' : 'M') + a.sx(x).toFixed(1) + ' ' + a.sy(fn(x)).toFixed(1);
            }
            return el(a.g, 'path', { d, fill: 'none', stroke: col, 'stroke-width': w || 2.5 });
        }
        function Seg(a, x1, y1, x2, y2, col, w, dash) {
            const at = { x1: a.sx(x1), y1: a.sy(y1), x2: a.sx(x2), y2: a.sy(y2), stroke: col, 'stroke-width': w || 2, 'stroke-linecap': 'round' };
            if (dash) at['stroke-dasharray'] = dash;
            return el(a.g, 'line', at);
        }
        function Dot(a, x, y, col, r, ring) {
            const at = { cx: a.sx(x), cy: a.sy(y), r: r || 5.5, fill: ring ? 'none' : col };
            if (ring) { at.stroke = col; at['stroke-width'] = 2; }
            return el(a.svg, 'circle', at);
        }
        function Txt(a, x, y, t, col, size, anchor) {
            return el(a.svg, 'text', { x: a.sx(x), y: a.sy(y), fill: col || 'currentColor', 'font-size': size || 12, 'text-anchor': anchor || 'start' }, t);
        }
        function Wire(id, names, draw) {
            const svg = document.getElementById(id + '-svg');
            const ins = names.map(n => document.getElementById(id + '-' + n));
            function run() {
                const v = {};
                names.forEach((n, i) => {
                    v[n] = parseFloat(ins[i].value);
                    const s = document.getElementById(id + '-' + n + 'v');
                    if (s) s.textContent = fmt(v[n]);
                });
                svg.innerHTML = '';
                const out = draw(v, svg);
                const r = document.getElementById(id + '-readout');
                if (r && typeof out === 'string') r.textContent = out;
            }
            ins.forEach(i => i.addEventListener('input', run));
            run();
        }
'''

LI = 'menu-link block px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/10 transition-colors truncate'
AG = 'hover:text-emerald-600 dark:hover:text-emerald-400 inline-block transition-transform hover:translate-x-1'


def P(t):
    return '<p class="mb-6">\n' + t + '\n</p>\n'


def H3(t):
    return '<h3 class="font-sans text-lg font-semibold mt-12 mb-4 text-gray-900 dark:text-gray-100">' + t + '</h3>\n'


def M(tex):
    return ('<div class="my-8 w-full overflow-x-auto no-scrollbar py-2"><div class="text-center text-sm sm:text-base '
            'max-w-full text-gray-900 dark:text-gray-100">$$' + tex + '$$</div></div>\n')


def UL(items):
    return '<ul class="list-disc pl-5 mb-6 space-y-1">' + ''.join('<li>' + i + '</li>' for i in items) + '</ul>\n'


def TBL(head, rows):
    h = ''.join('<th class="py-3 %s">%s</th>' % ('pr-4' if i == 0 else 'px-4', c) for i, c in enumerate(head))
    b = ''
    for r in rows:
        b += '<tr class="hover:bg-gray-50/50 dark:hover:bg-white/[0.02]">'
        for i, c in enumerate(r):
            cls = 'py-3 pr-4 font-medium text-gray-800 dark:text-gray-200' if i == 0 else 'py-3 px-4'
            b += '<td class="%s">%s</td>' % (cls, c)
        b += '</tr>\n'
    return ('<div class="my-8 overflow-x-auto no-scrollbar font-sans text-sm"><table class="w-full text-left border-collapse">'
            '<thead><tr class="border-b border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100 font-medium">'
            + h + '</tr></thead><tbody class="divide-y divide-gray-100 dark:divide-gray-900 text-gray-600 dark:text-gray-400">'
            + b + '</tbody></table></div>\n')


def CALL(kind, t):
    if kind == 'pit':
        return ('<div class="my-6 pl-4 border-l border-amber-500/60 font-sans text-sm sm:text-base text-gray-500 dark:text-gray-400 '
                'transition-colors hover:border-amber-500"><span class="font-medium text-gray-800 dark:text-gray-200">Common Pitfall:</span> '
                + t + '</div>\n')
    return ('<div class="my-6 pl-4 border-l border-gray-300 dark:border-gray-700 font-sans text-sm sm:text-base text-gray-500 '
            'dark:text-gray-400 transition-colors hover:border-gray-500"><span class="font-medium text-gray-800 dark:text-gray-200">'
            'Intuition Check:</span> ' + t + '</div>\n')


def QA(q, a):
    return ('<details class="group my-8 py-3 border-y border-gray-200 dark:border-gray-800/80 font-sans transition-colors">'
            '<summary class="cursor-pointer font-medium text-gray-800 dark:text-gray-200 flex items-center justify-between select-none '
            'hover:text-gray-900 dark:hover:text-white transition-colors text-base"><span>' + q +
            '</span><svg class="w-4 h-4 text-gray-400 transition-transform duration-300 group-open:rotate-180" fill="none" '
            'stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
            'd="M19 9l-7 7-7-7"></path></svg></summary><div class="accordion-content"><div>'
            '<div class="mt-4 pt-2 text-base space-y-4 font-serif text-gray-700 dark:text-gray-300">' + a +
            '</div></div></div></details>\n')


def FIG(inner, cap):
    return ('<figure class="my-8"><div class="flex flex-col items-center">' + inner + '</div>'
            '<figcaption class="mt-3 text-center font-sans text-xs text-gray-400 dark:text-gray-500">' + cap + '</figcaption></figure>\n')


def WIDGET(i, cap, sliders, H=260, W=640, buttons=None):
    rows = ''
    for n, lab, mn, mx, st, val in sliders:
        rows += ('<div><label for="%s-%s" class="whitespace-nowrap">%s = <span id="%s-%sv" class="font-medium text-gray-900 '
                 'dark:text-gray-100 tabular-nums">%s</span></label><input id="%s-%s" type="range" min="%s" max="%s" step="%s" '
                 'value="%s" class="lesson-range mt-2"></div>') % (i, n, lab, i, n, val, i, n, mn, mx, st, val)
    return ('<figure class="my-8 font-sans" id="%s"><div class="grid gap-3 mb-3 text-sm text-gray-600 dark:text-gray-400 sm:grid-cols-2">%s</div>'
            '<svg id="%s-svg" viewBox="0 0 %d %d" class="w-full h-auto text-gray-500 dark:text-gray-400" role="img"></svg>'
            '<div class="mt-3 text-sm text-gray-600 dark:text-gray-400 tabular-nums" id="%s-readout"></div>'
            '<figcaption class="mt-3 text-center text-xs text-gray-400 dark:text-gray-500">%s</figcaption></figure>\n') % (i, rows, i, W, H, i, cap)


def GLOSS(items):
    return ('<dl class="font-sans text-sm sm:text-base space-y-5">' + ''.join(
        '<div><dt class="font-medium text-gray-900 dark:text-gray-100">%s</dt><dd class="text-gray-600 dark:text-gray-400">%s</dd></div>' % (a, b)
        for a, b in items) + '</dl>\n')


def CARDS(items):
    return ('<div class="my-8 grid gap-4 font-sans sm:grid-cols-2">' + ''.join(
        '<div class="p-5 rounded-xl border border-gray-200 dark:border-gray-800"><div class="text-xs uppercase tracking-widest '
        'text-emerald-600 dark:text-emerald-400 mb-2">%s</div><div class="text-sm text-gray-600 dark:text-gray-400">%s</div></div>' % (a, b)
        for a, b in items) + '</div>\n')


def CODE(t):
    return ('<pre class="my-8 p-4 rounded-lg bg-gray-100 dark:bg-white/5 overflow-x-auto no-scrollbar font-mono text-sm leading-relaxed '
            'text-gray-800 dark:text-gray-200">' + t + '</pre>\n')


def build(fname, title, kicker, h1, lead, sections, js=''):
    agenda = ''.join('<li><a href="#%s" class="%s">%s</a></li>' % (s[0], AG, s[1]) for s in sections)
    menu = '<li><a href="#sec-agenda" class="%s">Agenda</a></li>' % LI
    body = ''
    n = 0
    for sid, name, html, numbered in sections:
        if numbered:
            n += 1
            tag = '<span class="font-sans text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 block">Chapter %02d</span>' % n
            menu += '<li><a href="#%s" class="%s">%d. %s</a></li>' % (sid, LI, n, name)
        else:
            tag = ''
            menu += '<li><a href="#%s" class="%s">%s</a></li>' % (sid, LI, name)
        body += ('<section id="%s" class="scroll-mt-28 w-full reveal-section">%s<h2 class="font-sans text-2xl sm:text-3xl font-semibold mb-6 '
                 'text-gray-900 dark:text-gray-100 tracking-tight">%s</h2>\n%s</section>\n\n') % (sid, tag, name, html)
    out = HEAD_A + '<title>' + title + '</title>' + HEAD_B
    out += '<main class="max-w-2xl mx-auto px-5 sm:px-6 py-16 sm:py-28 min-h-[200vh] w-full">\n'
    out += ('<header class="mb-16 sm:mb-24 reveal-section"><span class="font-sans text-xs font-medium text-gray-400 dark:text-gray-500 uppercase '
            'tracking-widest mb-4 block">' + kicker + '</span><h1 class="font-sans text-3xl sm:text-5xl font-bold tracking-tight mb-6 '
            'text-gray-900 dark:text-gray-100 leading-tight">' + h1 + '</h1><p class="font-sans text-lg sm:text-xl text-gray-500 '
            'dark:text-gray-400 font-normal leading-relaxed">' + lead + '</p></header>\n')
    out += '<div class="space-y-16 sm:space-y-24 w-full">\n'
    out += ('<section id="sec-agenda" class="scroll-mt-28 reveal-section"><h2 class="font-sans text-xl font-semibold mb-4 text-gray-900 '
            'dark:text-gray-100">Agenda</h2><ol class="font-sans list-decimal pl-5 space-y-2.5 text-gray-600 dark:text-gray-400 text-sm '
            'sm:text-base">' + agenda + '</ol></section>\n\n')
    out += body + '</div>\n</main>\n\n'
    out += ('<div class="fixed bottom-4 left-4 sm:bottom-6 sm:left-6 z-50 font-sans max-w-[calc(100vw-2rem)]">'
            '<nav id="menuList" class="absolute bottom-full left-0 mb-3 w-[280px] max-w-[calc(100vw-2rem)] max-h-[50vh] overflow-y-auto '
            'bg-white/95 dark:bg-darkCard/95 backdrop-blur-md text-gray-700 dark:text-gray-300 rounded-xl p-2 transition-all duration-300 '
            'ease-out opacity-0 translate-y-2 scale-95 pointer-events-none shadow-2xl border border-gray-200/60 dark:border-gray-800/80">'
            '<ul class="flex flex-col space-y-1 text-sm font-normal">' + menu + '</ul></nav>\n')
    out += BAR + JSC + JSLIB + js + '\n        updateProgress();\n    </script>\n</body>\n</html>\n'
    open(D + fname, 'w', encoding='utf-8').write(out)
    print(fname, len(out))
