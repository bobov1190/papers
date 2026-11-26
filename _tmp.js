
        const controlBar = document.getElementById('controlBar');
        const menuList = document.getElementById('menuList');
        const arrowIcon = document.getElementById('arrowIcon');
        const progressDisplay = document.getElementById('progressDisplay');
        const links = document.querySelectorAll('.menu-link');
        const themeToggle = document.getElementById('themeToggle');
        const htmlElement = document.documentElement;
        let isOpen = false;

        try {
            if (localStorage.getItem('theme') === 'light') htmlElement.classList.remove('dark');
        } catch (e) {}

        function toggleMenu() {
            isOpen = !isOpen;
            if (isOpen) {
                menuList.classList.remove('opacity-0', 'translate-y-2', 'scale-95', 'pointer-events-none');
                arrowIcon.classList.add('rotate-180');
            } else {
                menuList.classList.add('opacity-0', 'translate-y-2', 'scale-95', 'pointer-events-none');
                arrowIcon.classList.remove('rotate-180');
            }
        }

        controlBar.addEventListener('click', (e) => {
            if (e.target.closest('#themeToggle')) return;
            toggleMenu();
        });
        document.addEventListener('click', (e) => {
            if (!menuList.contains(e.target) && !controlBar.contains(e.target) && isOpen) toggleMenu();
        });
        links.forEach(link => link.addEventListener('click', () => { if (isOpen) toggleMenu(); }));

        themeToggle.addEventListener('click', () => {
            const dark = htmlElement.classList.toggle('dark');
            try { localStorage.setItem('theme', dark ? 'dark' : 'light'); } catch (e) {}
        });

        function updateProgress() {
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            let p = docHeight > 0 ? Math.round((window.scrollY / docHeight) * 100) : 0;
            progressDisplay.textContent = Math.max(0, Math.min(100, p)) + '%';
        }
        window.addEventListener('scroll', updateProgress);
        window.addEventListener('resize', updateProgress);

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => entry.target.classList.toggle('active', entry.isIntersecting));
        }, { root: null, rootMargin: '0px 0px -5% 0px', threshold: 0.05 });
        document.querySelectorAll('.reveal-section').forEach(s => revealObserver.observe(s));

        const menuObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const id = entry.target.getAttribute('id');
                links.forEach(link => {
                    const on = link.getAttribute('href') === '#' + id;
                    ['bg-gray-100', 'dark:bg-white/10', 'font-medium', 'text-gray-900', 'dark:text-white'].forEach(c => link.classList.toggle(c, on));
                });
            });
        }, { root: null, rootMargin: '-20% 0px -60% 0px', threshold: 0 });
        document.querySelectorAll('section[id]').forEach(s => menuObserver.observe(s));

        const NS = 'http://www.w3.org/2000/svg';
        const GREEN = '#10b981', RED = '#ef4444', AMBER = '#f59e0b';
        function el(parent, name, attrs, text) {
            const e = document.createElementNS(NS, name);
            for (const k in attrs) e.setAttribute(k, attrs[k]);
            if (text !== undefined) e.textContent = text;
            parent.appendChild(e);
            return e;
        }
        
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

        Wire('wknn1', ['k'], (v, svg) => {
            const nb = [['A', 33, 15.85, 1, 4.6], ['B', 30, 16.10, 0, 6.3], ['C', 36, 13.00, 1, 7.1], ['D', 28, 16.10, 0, 7.6], ['E', 43, 26.25, 0, 10.2]];
            const a = Ax(svg, { W: 640, H: 250, l: 50, r: 20, t: 20, b: 34, x: [24, 46], y: [10, 30], xt: [25, 30, 35, 40, 45], yt: [10, 15, 20, 25, 30], xl: 'age (years)', yl: 'fare' });
            let sv = 0, di = 0, ws = 0, wd = 0;
            nb.forEach((p, i) => {
                const on = i < v.k;
                if (on) { if (p[3]) { sv++; ws += 1 / p[4]; } else { di++; wd += 1 / p[4]; } }
                Dot(a, p[1], p[2], p[3] ? '#3b82f6' : AMBER, on ? 7 : 4);
                if (on) Dot(a, p[1], p[2], 'currentColor', 11, true);
                Txt(a, p[1] + 0.5, p[2] + 0.9, p[0], 'currentColor', 12);
            });
            const s = Dot(a, 35, 20, '#facc15', 8);
            Txt(a, 35.6, 20.9, 'you', 'currentColor', 12);
            return 'k = ' + v.k + ':  plain vote ' + sv + ' survived / ' + di + ' died -> ' + (sv === di ? 'tie' : sv > di ? 'survived' : 'died') + '     weighted ' + ws.toFixed(3) + ' vs ' + wd.toFixed(3) + ' -> ' + (ws > wd ? 'survived' : 'died');
        });

        Wire('wknn2', ['da', 'df'], (v, svg) => {
            const m = Math.max(v.da, v.df, 4) * 1.15;
            const a = Ax(svg, { W: 640, H: 250, l: 50, r: 20, t: 20, b: 34, x: [0, m * 2.2], y: [0, m], xt: [], yt: [], xl: 'age gap', yl: 'fare gap' });
            Seg(a, 0, 0, v.da, 0, '#3b82f6', 3);
            Seg(a, v.da, 0, v.da, v.df, '#3b82f6', 3);
            Seg(a, 0, 0, v.da, v.df, GREEN, 3);
            Dot(a, 0, 0, 'currentColor', 5);
            Dot(a, v.da, v.df, 'currentColor', 5);
            Txt(a, v.da / 2, -0.08 * m, 'taxi: ' + fmt(v.da) + ' + ' + fmt(v.df), '#3b82f6', 12, 'middle');
            return 'Euclid (ruler) = ' + Math.hypot(v.da, v.df).toFixed(1) + '     Manhattan (taxi) = ' + (v.da + v.df).toFixed(1);
        });

        Wire('wknn3', ['age', 'fare', 'sex'], (v, svg) => {
            const z = [(v.age - 30.15) / 14.32, (v.fare - 23.51) / 21.02, (v.sex - 0.35) / 0.48];
            const names = ['age', 'fare', 'sex'], cols = ['#3b82f6', GREEN, AMBER];
            const a = Ax(svg, { W: 640, H: 220, l: 70, r: 20, t: 20, b: 30, x: [-3, 3], y: [0, 3], xt: [-3, -2, -1, 0, 1, 2, 3], yt: [], xl: 'z', yl: '' });
            Seg(a, 0, 0, 0, 3, 'currentColor', 1, '3 3');
            z.forEach((zz, i) => {
                const y = 2.5 - i;
                Seg(a, 0, y, Math.max(-3, Math.min(3, zz)), y, cols[i], 12);
                Txt(a, -3.1, y - 0.12, names[i], cols[i], 13, 'end');
                Txt(a, Math.max(-3, Math.min(3, zz)) + (zz >= 0 ? 0.1 : -0.1), y - 0.12, (zz >= 0 ? '+' : '') + zz.toFixed(2), 'currentColor', 12, zz >= 0 ? 'start' : 'end');
            });
            return 'z-scores:  age ' + z[0].toFixed(2) + '   fare ' + z[1].toFixed(2) + '   sex ' + z[2].toFixed(2);
        });

        (function () {
            let st = 12345;
            const rnd = () => { st |= 0; st = st + 0x6D2B79F5 | 0; let t = Math.imul(st ^ st >>> 15, 1 | st); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
            const dims = [1, 2, 3, 5, 8, 12, 20, 30, 50, 75, 100];
            const ratio = (d) => {
                const n = 200, q = 15, P = [];
                for (let i = 0; i < n + q; i++) { const p = []; for (let j = 0; j < d; j++) p.push(rnd()); P.push(p); }
                let sum = 0;
                for (let i = n; i < n + q; i++) {
                    let mn = Infinity, tot = 0;
                    for (let j = 0; j < n; j++) {
                        let s = 0;
                        for (let c = 0; c < d; c++) { const dd = P[i][c] - P[j][c]; s += dd * dd; }
                        const r = Math.sqrt(s);
                        tot += r; if (r < mn) mn = r;
                    }
                    sum += mn / (tot / n);
                }
                return sum / q;
            };
            const vals = dims.map(ratio);
            const interp = (d) => {
                for (let i = 1; i < dims.length; i++) if (d <= dims[i]) { const t = (d - dims[i - 1]) / (dims[i] - dims[i - 1]); return vals[i - 1] + t * (vals[i] - vals[i - 1]); }
                return vals[vals.length - 1];
            };
            Wire('wknn4', ['d'], (v, svg) => {
                const a = Ax(svg, { W: 640, H: 250, l: 50, r: 20, t: 20, b: 34, x: [0, 100], y: [0, 1], xt: [0, 25, 50, 75, 100], yt: [0, 0.5, 1], xl: 'number of columns', yl: 'nearest / average distance' });
                let d = ''; dims.forEach((x, i) => { d += (i ? 'L' : 'M') + a.sx(x).toFixed(1) + ' ' + a.sy(vals[i]).toFixed(1); });
                el(a.g, 'path', { d, fill: 'none', stroke: GREEN, 'stroke-width': 2.5 });
                dims.forEach((x, i) => Dot(a, x, vals[i], GREEN, 3.5));
                Seg(a, v.d, 0, v.d, interp(v.d), AMBER, 1.5, '4 3');
                Dot(a, v.d, interp(v.d), AMBER, 6);
                return v.d + ' columns:  nearest / average distance = ' + interp(v.d).toFixed(2) + '  (1.00 means near and far look the same)';
            });
        })();

        updateProgress();
    