from _lib import *

S = []

S.append(('sec-flowers', 'Meet the Flowers', (
    P('The last lessons gave us three models, each with the same recipe: <strong>model, loss, optimize</strong>. Today we ask a new question: is there a <em>better way to draw the line</em>?')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'Today: SVM'], [
        ['Output', 'a number', 'a probability', 'N probabilities', '?'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', '?'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', '?'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', '?']])
    + CALL('check', 'In every column the optimizer is the same walk downhill. The SVM changes the picture and the loss.')
    + H3('Our data: iris flowers')
    + P('The iris data has <strong>150 real flowers</strong>, 50 of each of 3 species. For every flower we measure the petal in centimeters: length and width. Today we take two species at a time, first <strong>setosa</strong> and <strong>versicolor</strong> (100 flowers). Virginica joins later.')
    + TBL(['Flower', 'Length', 'Width', 'Species'], [
        ['flower 1', '1.4 cm', '0.2 cm', 'setosa'], ['flower 2', '4.7 cm', '1.4 cm', 'versicolor']])
    + P('Setosa petals are $1.0$ to $1.9$ cm long, versicolor petals $3.0$ to $5.1$ cm. Each flower is one dot, and the two groups are easy to see.')
    + H3('Many lines work')
    + P('Take three different lines. All of them separate the 100 flowers with <strong>0 mistakes</strong>, so the training accuracy is the same: $100\\%$. Which line would you trust? Ask a different question: how close is the nearest flower to each line?')
    + TBL(['Line', 'Distance to the nearest flower'], [['line A', '0.04 cm'], ['line B', '0.32 cm'], ['line C', '0.65 cm']])
    + QA('Which line leaves the most room?', '<p>Line C: its closest flower is $0.65$ cm away. A line that leaves room on both sides is safer, and that is the idea of this lesson.</p>')
), True))

S.append(('sec-street', 'The Widest Street', (
    P('Build the widest empty street between the two groups of flowers. Three steps: draw an empty street between the groups, widen it until it touches the flowers, then take the line down the middle. That line is the SVM. The width of the street is the <strong>margin</strong>.')
    + P('For setosa against versicolor the margin is $1.30$ cm, and only <strong>2 flowers</strong> touch the edges. Those two are the <em>support vectors</em>.')
    + H3('Why the middle?')
    + P('A new flower arrives: a versicolor, a bit smaller than ours, with a petal of $3.8 \\times 0.8$ cm. A line squeezed against the data sits only $0.12$ cm from it and says <em>setosa</em>: wrong. The line in the middle of the widest street is $1.17$ cm away and says <em>versicolor</em>: right. The middle has room to spare for flowers we have not seen yet.')
    + H3('Support vectors: only the edge flowers matter')
    + P('The flowers on the edge of the street hold it in place. Remove all the other $98$ and nothing changes: the street keeps its width of $1.30$ cm. Remove one support vector and the street moves, to $1.41$ cm.')
    + CALL('check', 'The support vectors are the only flowers the SVM listens to.')
), True))

S.append(('sec-model', 'The Model', (
    P('The model is the same linear machine as before, now read as a <strong>ruler</strong>. Six symbols will follow us until the end.')
    + TBL(['Symbol', 'What it means', 'Our flowers'], [
        ['$x$', 'a flower: its measurements', '$(1.9, 0.4)$: length, width'],
        ['$d$', 'how many measurements a flower has', '$d = 2$'],
        ['$\\beta$', 'weights: numbers the machine learns', '$\\beta_0=-3.79,\\ \\beta_1=1.29,\\ \\beta_2=0.82$'],
        ['$f$', 'score: what the machine computes', '$f = -1.00$ for this flower'],
        ['$y$', 'truth: the real species, as a number', 'setosa $=-1$, versicolor $=+1$'],
        ['sign', 'keep only the sign of a number', '$\\text{sign}(-1.00) = -1$: setosa']])
    + P('The machine computes a <strong>score</strong> $f$ for every flower. The sign of the score gives the species.')
    + M(r'f(x) = \beta_0 + \sum_{j=1}^{d} \beta_j x_j, \qquad \hat{y} = \operatorname{sign}\big(f(x)\big)')
    + P('For a real flower of $3.0 \\times 1.1$ cm: $f = -3.79 + 1.29 \\cdot 3.0 + 0.82 \\cdot 1.1 = 0.98 \\approx 1$. This flower sits exactly on the edge of the street. Weights shown here are rounded.')
    + QA('The flower gets 1 cm longer. What happens to $f$?', '<p>$f$ grows by $1.29$, every time. A straight rule: that is what <em>linear</em> means.</p>')
    + H3('Score and sign: a ruler for flowers')
    + P('Every flower gets a score, a position on a ruler. The line is at $f = 0$, the street edges are at $f = -1$ and $f = +1$. Negative means the setosa side, positive the versicolor side. The farther from $0$, the surer the machine.')
    + QA('A flower has $f = -2.33$. What does the sign say?', '<p>$\\text{sign} = -1$, setosa. And it is far from the street, so the machine is very sure.</p>')
    + H3('The truth $y$ and the product $y \\cdot f$')
    + P('Multiply the truth by the score. The product $y \\cdot f$ is <em>positive exactly when the machine is right</em>, and it says how safely the flower sits on its own side.')
    + TBL(['Flower', 'Length', 'Width', '$f$', '$y$', '$y \\cdot f$'], [
        ['far setosa', '1.0', '0.2', '$-2.33$', '$-1$', '$2.33$'],
        ['setosa on the edge', '1.9', '0.4', '$-1.00$', '$-1$', '$1.00$'],
        ['versicolor on the edge', '3.0', '1.1', '$+1.00$', '$+1$', '$1.00$'],
        ['far versicolor', '5.1', '1.6', '$+4.13$', '$+1$', '$4.13$']])
    + UL(['$y \\cdot f \\ge 1$: safe, outside the street', '$0 \\le y \\cdot f \\lt 1$: right side, but inside the street', '$y \\cdot f \\lt 0$: a mistake'])
    + H3('Weights decide the width of the street')
    + P('Keep the same line but scale all the weights. The line stays put, only $f$ changes, so the street edges ($f = \\pm 1$) move. Try it.')
    + WIDGET('wsvm1', 'Figure 3.1 &mdash; Interactive. Weights times $s$: the line stays, the edges $f=\\pm1$ move. Dots: the two support vectors.', [('s', 'Weights &times;', 0.25, 3, 0.05, 1)], H=270)
    + M(r'\text{width} = \frac{2}{\|\beta\|}, \qquad \|\beta\| = \sqrt{\beta_1^2 + \beta_2^2} = \sqrt{1.29^2 + 0.82^2} = 1.53')
    + P('Halve the weights and the street doubles to $2.61$ cm. Double them and it shrinks to $0.65$ cm. <strong>Small weights mean a wide street.</strong>')
), True))

S.append(('sec-loss', 'The Loss', (
    P('<strong>The rule.</strong> A wide street needs small weights, but no flower is allowed inside the street. One rule per flower: stay outside the street, on your own side.')
    + M(r'\min_{\beta}\ \frac{1}{2}\sum_{j=1}^{d}\beta_j^2 \quad \text{such that} \quad y_i f(x_i) \ge 1 \ \text{ for every flower } i')
    + QA('What if the groups overlap and no empty street exists?', '<p>Then the rule cannot be satisfied. We need a softer rule.</p>')
    + H3('Versicolor against virginica: no empty street')
    + P('These two species look alike and their petals overlap: lengths of $4.5$ to $5.1$ cm appear in both. Label versicolor $=-1$ and virginica $=+1$. The best straight line still gets <strong>5 flowers wrong</strong>.')
    + H3('The fine is an arrow')
    + P('A flower outside the street on its own side pays nothing. Everybody else pays a <strong>fine</strong>: the way back to the safe edge, measured in $f$ (not in centimeters).')
    + TBL(['Flower', '$y \\cdot f$', 'Fine'], [
        ['1 versicolor (4.1, 1.3)', '2.54', '0.00'], ['2 virginica (4.9, 1.8)', '0.34', '0.66'],
        ['3 versicolor (5.1, 1.6)', '&minus;0.32', '1.32'], ['4 virginica (4.5, 1.7)', '&minus;0.76', '1.76']])
    + H3('Hinge loss: the fine as a curve')
    + M(r'\ell(y, f) = \max\big(0,\ 1 - y\,f\big)')
    + UL(['$y \\cdot f \\ge 1$: fine $0$, the flower is safe', '$0 \\le y \\cdot f \\lt 1$: small fine, right side but inside the street', '$y \\cdot f \\lt 0$: big fine, wrong side of the line'])
    + QA('Flower 4 has $y \\cdot f = -0.76$. What is its fine?', '<p>$1 - (-0.76) = 1.76$. The farther on the wrong side, the bigger the fine.</p>')
    + H3('The full SVM loss: two wishes')
    + P('The loss adds two wishes: a <em>wide street</em> (small weights) and <em>few fines</em>. $C$ is the price of one unit of fine.')
    + M(r'L(\beta) = \frac{1}{2}\sum_{j=1}^{d}\beta_j^2 \;+\; C\sum_{i=1}^{n}\max\big(0,\ 1 - y_i f(x_i)\big)')
    + P('Our case: $C=1$, $d=2$, $n=100$ flowers (versicolor against virginica). The street part is $4.92$ and the fine part $13.57$, so $L = 4.92 + 13.57 = 18.49$. This is the number gradient descent will push down.')
    + H3('$C$ is the price of a fine')
    + P('Small $C$: fines are cheap, the street grows wide and many flowers stay inside it. Big $C$: fines are expensive and the street shrinks until it is almost empty.')
    + TBL(['$C$', 'Street width', 'Inside the street or wrong', 'Mistakes'], [
        ['0.1', '1.31 cm', '50 flowers', '5'], ['1', '0.64 cm', '23 flowers', '5'], ['100', '0.22 cm', '10 flowers', '6']])
    + H3('Three fines for the same flower')
    + P('You know two fines already: squared error and log loss. The hinge is the new one. Move $y \\cdot f$ and compare.')
    + WIDGET('wsvm2', 'Figure 4.1 &mdash; Interactive. Fine against $y \\cdot f$. Squared error: $(1-yf)^2$. Log loss: $\\ln(1+e^{-yf})$. Hinge: exactly $0$ from $y \\cdot f = 1$.', [('m', '$y \\cdot f$', -2, 3, 0.05, 0.5)], H=270)
    + CALL('check', 'Hinge only cares about flowers near the street or on the wrong side. Safe flowers are ignored. It gives a side ($-1$ or $+1$), not a probability.')
), True))

S.append(('sec-opt', 'Optimize', (
    P('The same walk downhill as in every lesson. Imagine the loss as a bowl and one weight as a ball. The slope points uphill, so we step the opposite way, and the bowl has one bottom: no traps.')
    + M(r'\beta \leftarrow \beta - \eta\,\nabla L(\beta)')
    + P('Our case: $\\eta = 0.002$, starting at $\\beta_1 = -0.50$. Slope at step 0 on this slice: $-56$, so the loss falls to the right.')
    + H3('Who pushes the line?')
    + P('Only flowers inside the street or on the wrong side push the line. Safe flowers push with force $0$: they could vanish and the line would not care. After step 100, $27$ flowers push and $73$ do nothing.')
    + M(r'\frac{\partial L}{\partial \beta_j} = \beta_j \;-\; C\!\!\sum_{i:\ y_i f(x_i) \lt 1}\!\! y_i\, x_{ij}')
    + CALL('check', 'The sum runs only over the pushers. That is the whole gradient. The $\\beta_j$ term is the wish for a wide street.')
    + H3('One step, in numbers')
    + P('Start from a guess picked by hand: all $100$ flowers are inside the street or wrong, so all push. Petals are centered (minus their average).')
    + TBL(['', '$\\beta_1$ (length)', '$\\beta_2$ (width)', '$\\beta_0$'], [
        ['now', '&minus;0.50', '1.00', '0.00'], ['slope of $L$ (gradient)', '&minus;65.1', '&minus;34.0', '0.0'],
        ['step $=-\\eta \\times$ slope', '0.13', '0.07', '0.00'], ['after the step', '&minus;0.37', '1.07', '0.00']])
    + P('The loss goes from $97.9$ to $87.1$ after one step.')
    + QA('Why is the step so small?', '<p>$\\eta = 0.002$ keeps us from jumping over the bottom. Many small steps instead of one big one.</p>')
    + H3('1000 small steps and when to stop')
    + TBL(['Step', 'Loss', 'Inside or wrong', 'Mistakes'], [
        ['0', '97.9', '100', '39'], ['10', '31.4', '60', '6'], ['100', '19.2', '27', '6'], ['1000', '18.5', '23', '5']])
    + P('Nobody told the line where to go. It only followed the slope. The loss falls fast at first ($97.9 \\to 31.4$ in 10 steps), then slower ($31.4 \\to 19.2$), then barely moves ($19.2 \\to 18.5$). When the slope is almost $0$ we are at the bottom and we stop.')
    + QA('Why do the steps shrink by themselves?', '<p>$\\text{step} = \\eta \\times \\text{slope}$. Near the bottom the slope is almost $0$, so the step is too.</p>')
), True))

S.append(('sec-kernel', 'When a Line Is Not Enough', (
    H3('The temperature of tea')
    + P('Too cold: bad tea. Too hot: bad tea. Just right: good tea. On a line of temperatures no single cut separates good cups from bad ones. The best single cut, at $37.5\\,^\\circ$C, still gets $3$ of $11$ cups wrong.')
    + P('The idea: give every cup a <strong>second number</strong>, its distance from $55\\,^\\circ$C, squared. Now one straight cut at $162.5$ separates the cups. Move the slider.')
    + WIDGET('wsvm3', 'Figure 6.1 &mdash; Interactive. A cup at temperature $t$ gets the new number $(t-55)^2$. Below the cut: good tea.', [('t', 'Temperature $t$ (&deg;C)', 10, 90, 1, 30)], H=270)
    + P('In the old picture this horizontal cut is the zone <strong>$42.3$ to $67.7\\,^\\circ$C</strong>: a zone, not a line.')
    + CALL('check', 'The machine is still a straight cut. We only changed what we feed it.')
    + H3('The same problem in 2D: rings')
    + P('Two groups of dots: an inner ring and an outer ring. No straight line can cut a ring out of the middle. The best line gets $51\\%$ right on $200$ fresh dots: a coin flip.')
    + P('Same trick: give every dot a new number, $r^2 = x_1^2 + x_2^2$, its squared distance from the center. In the new picture one straight cut works: <strong>$100\\%$ right</strong>. A straight cut in the new picture is a circle in the old one.')
    + H3('The kernel idea: skip the building')
    + P('We invented $r^2$ and $(t-55)^2$ by hand, which needs a good guess every time. A <strong>kernel</strong> is a shortcut: do not build new numbers, only ask <em>how similar are two dots?</em> (from $0$ to $1$).')
    + QA('A hundred measurements per dot and no idea of the right formula. Which route?', '<p>The kernel. The RBF similarity only needs the distance between two dots.</p>')
    + H3('Similarity: from distance to a number')
    + M(r"K(x, x') = \exp\!\big(-\gamma\,\|x - x'\|^2\big)")
    + P('Take the distance between two dots, square it, multiply by $\\gamma$ and squeeze it into $0$ to $1$ with $\\exp$. Close dots are very similar (near $1$), far dots are not (near $0$). Play with it.')
    + WIDGET('wsvm4', 'Figure 6.2 &mdash; Interactive. RBF similarity against distance. $\\gamma$ sets how fast it falls.', [('g', '$\\gamma$', 0.1, 10, 0.1, 1), ('d', 'distance', 0, 3, 0.05, 1)], H=270)
    + TBL(['Pair with the star', 'Distance', 'Distance squared', '$K=\\exp(-\\gamma \\cdot d^2)$'], [['a close dot', '0.17', '0.03', '0.97'], ['a far dot', '1.32', '1.75', '0.17']])
    + H3('How similarity makes a boundary: votes')
    + P('Every support vector votes for its ring: its weight $\\alpha$ times its similarity to the new dot. The closer, the louder. Add the votes to the shift $b$: positive means inner ring, negative means outer ring.')
    + M(r'f(x) = b + \sum_{i \in SV} \alpha_i\, y_i\, K(x_i, x)')
    + TBL(['Support vector', '$\\alpha$', '$K$ to the star', 'vote $\\alpha \\cdot y \\cdot K$'], [
        ['(0.13, 0.54) inner', '9.94', '0.59', '+5.85'], ['(0.31, 0.81) outer', '8.01', '0.37', '&minus;2.95'],
        ['(&minus;0.44, &minus;0.30) inner', '2.83', '0.64', '+1.81'], ['(&minus;0.82, &minus;0.48) outer', '2.46', '0.31', '&minus;0.77']])
    + P('The other $6$ support vectors and $b$ add the rest. The total is $f = 1.90$, positive, so the machine says <strong>inner ring</strong>. (Outer-ring votes are negative because $y = -1$ for the outer ring.)')
    + H3('$\\gamma$: the size of one point\'s hill')
    + P('Each dot spreads similarity around itself, and $\\gamma$ sets how far. Small $\\gamma$: too smooth. Medium: just right. Huge: a loop around every dot. (Noisier dots than on the votes slide, 300 of them, so the numbers differ.)')
    + TBL(['$\\gamma$', 'Train', 'Test', 'Support vectors', 'Verdict'], [
        ['0.05', '68%', '64%', '120', 'too smooth'], ['1', '98%', '92%', '48', 'just right'], ['50', '100%', '87%', '101', 'memorized the noise']])
    + CARDS([('Kernel = similarity', 'A number from 0 to 1 for any two dots.'), ('Support vectors vote', 'Closer to the new dot, louder the vote.'),
             ('$\\gamma$ = size of the hill', 'Small: too smooth. Huge: memorizes noise.'), ('$C$ is still the price', 'The hinge loss and the fines did not change.')])
    + P('Other kernels exist: the <em>linear</em> kernel is our straight line from before, the <em>polynomial</em> kernel bends it by a fixed shape. RBF is the usual first try for curvy data. The kernel decides the shape of the boundary; the rest of the recipe is unchanged.')
), True))

S.append(('sec-iris', 'The Full Iris Problem', (
    P('Now all three species: the same $150$ flowers and the same two measurements, but $50$ flowers each of setosa, versicolor and virginica. Setosa is far from the others, versicolor and virginica touch, and versicolor sits in the middle.')
    + QA('How can a machine that splits two groups handle three?', '<p>One machine per species. Each asks: is it <em>my</em> species, or any other?</p>')
    + H3('One street per species')
    + P('Three machines on the $105$ training flowers. Setosa is easy. Versicolor sits in the middle, so one straight street cannot wrap it.')
    + TBL(['Machine', 'Mistakes on the 105 training flowers'], [['setosa vs the rest', '0'], ['versicolor vs the rest', '35'], ['virginica vs the rest', '7']])
    + H3('Train, then test on fresh flowers')
    + P('Split: $105$ flowers to train on and $45$ fresh ones to test (never seen in training). Two models with the same recipe: straight streets and bent streets (RBF kernel).')
    + TBL(['Model', 'Train', 'Test', 'Wrong on test'], [
        ['Linear SVM, 3 machines', '91.4%', '91.1%', '4 of 45'], ['RBF SVM, 3 machines ($\\gamma=1$, $C=1$)', '94.3%', '100.0%', '0 of 45']])
    + CALL('pit', 'Only $45$ test flowers. Test above train is luck of this split, not magic. Repeat with other splits (cross-validation) to be sure.')
    + P('The straight streets stumble where versicolor and virginica touch. The bent streets follow the curve between them.')
    + H3('The whole solution in sklearn')
    + CODE('X, y = load_iris(return_X_y=True)\nX = X[:, 2:4]\n\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.3, stratify=y, random_state=0)\n\nmodel = OneVsRestClassifier(SVC(kernel="rbf", gamma=1, C=1))\nmodel.fit(X_train, y_train)\n\nprint(model.score(X_test, y_test))   # 1.0\nprint(model.predict([[4.5, 1.5]]))   # [1] = versicolor')
    + QA('What changes if we use all 4 flower measurements?', '<p>Just drop the line <code>X = X[:, 2:4]</code>. Same model, more information.</p>')
    + H3('Same recipe, four models')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'SVM'], [
        ['Output', 'a number', 'a probability', 'N probabilities', 'a side: $-1$ or $+1$'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', 'line + sign (+ kernel)'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', 'hinge loss'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', 'gradient descent*']])
    + P('*Kernel SVMs in libraries use another solver. The SVM swaps the output and the loss, and adds a kernel.')
), True))

S.append(('sec-recap', 'What We Learned', (
    CARDS([('1 &middot; Widest street', 'The best line leaves the most room on both sides.'), ('2 &middot; Support vectors', 'Only the edge dots hold the line in place.'),
           ('3 &middot; Hinge loss + $C$', 'A fine for rule breakers; $C$ is the price.'), ('4 &middot; Kernel + similarity', 'Bends the line into a curve.')])
    + P('Thank you! Questions?')
), True))

S.append(('sec-glossary', 'Glossary &amp; Terminology', GLOSS([
    ('Weights $\\beta$', 'The numbers the machine learns.'), ('Score $f$', 'The machine\'s number for a dot.'),
    ('Sign', 'Keep only $+$ or $-$: the side.'), ('$y \\cdot f$', 'How safely a dot sits on its own side.'),
    ('Street / margin', 'The empty band around the line. Its width is $2/\\|\\beta\\|$.'), ('Support vector', 'A dot on the edge of the street: it holds the street.'),
    ('Hinge loss', 'Fine $=0$ if safe, grows as the dot gets near the street or crosses the line.'), ('$C$', 'The price of one unit of fine.'),
    ('Kernel', 'The similarity of two dots, from $0$ to $1$.'), ('$\\gamma$', 'How far one dot\'s similarity reaches.'),
    ('$\\eta$', 'The size of one step downhill.'), ('RBF', 'The usual kernel: $\\exp(-\\gamma \\cdot \\text{distance}^2)$.')]), False))

JS = r'''
        Wire('wsvm1', ['s'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 50, r: 20, t: 20, b: 34, x: [1, 7], y: [0, 2.5], xt: [1, 2, 3, 4, 5, 6, 7], yt: [0, 1, 2], xl: 'petal length (cm)', yl: 'petal width (cm)' });
            const w = (c) => (L) => (c - 1.29 * L) / 0.82;
            Curve(a, w(3.79 + 1 / v.s), 1, 7, AMBER, 1.8);
            Curve(a, w(3.79 - 1 / v.s), 1, 7, AMBER, 1.8);
            Curve(a, w(3.79), 1, 7, GREEN, 2.5);
            Dot(a, 1.9, 0.4, '#3b82f6', 6);
            Dot(a, 3.0, 1.1, '#ef4444', 6);
            return 'weights x ' + fmt(v.s) + ':  ||beta|| = ' + (1.53 * v.s).toFixed(2) + ',  street width = ' + (2 / (1.53 * v.s)).toFixed(2) + ' cm';
        });

        Wire('wsvm2', ['m'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 50, r: 20, t: 20, b: 34, x: [-2, 3], y: [0, 4], xt: [-2, -1, 0, 1, 2, 3], yt: [0, 1, 2, 3, 4], xl: 'y * f', yl: 'fine' });
            const hinge = (m) => Math.max(0, 1 - m), sq = (m) => (1 - m) * (1 - m), lg = (m) => Math.log(1 + Math.exp(-m));
            Curve(a, sq, -2, 3, AMBER, 2);
            Curve(a, lg, -2, 3, '#3b82f6', 2);
            Curve(a, hinge, -2, 3, GREEN, 3);
            Seg(a, v.m, 0, v.m, 4, 'currentColor', 1, '4 3');
            Dot(a, v.m, Math.min(sq(v.m), 4), AMBER, 5);
            Dot(a, v.m, lg(v.m), '#3b82f6', 5);
            Dot(a, v.m, hinge(v.m), GREEN, 6);
            Txt(a, -1.9, 3.7, 'hinge', GREEN, 13);
            Txt(a, -0.9, 3.7, 'squared', AMBER, 13);
            Txt(a, 0.1, 3.7, 'log loss', '#3b82f6', 13);
            return 'y*f = ' + fmt(v.m) + ':   hinge ' + hinge(v.m).toFixed(2) + '   squared ' + sq(v.m).toFixed(2) + '   log ' + lg(v.m).toFixed(2);
        });

        Wire('wsvm3', ['t'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 56, r: 20, t: 20, b: 34, x: [0, 100], y: [0, 2100], xt: [0, 20, 40, 60, 80, 100], yt: [0, 1000, 2000], xl: 'temperature (C)', yl: '(t - 55)^2' });
            Curve(a, (t) => (t - 55) * (t - 55), 0, 100, GREEN, 2.5);
            Seg(a, 0, 162.5, 100, 162.5, '#ef4444', 2, '5 4');
            const f = (v.t - 55) * (v.t - 55);
            Seg(a, v.t, 0, v.t, f, AMBER, 1.5, '4 3');
            Dot(a, v.t, f, AMBER, 6);
            return 't = ' + v.t + ' C:  (t - 55)^2 = ' + f + '  ->  ' + (f < 162.5 ? 'below the cut 162.5: good tea' : 'above the cut 162.5: bad tea');
        });

        Wire('wsvm4', ['g', 'd'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 50, r: 20, t: 20, b: 34, x: [0, 3], y: [0, 1], xt: [0, 1, 2, 3], yt: [0, 0.5, 1], xl: 'distance between two dots', yl: 'similarity K' });
            const K = (d) => Math.exp(-v.g * d * d);
            Curve(a, K, 0, 3, GREEN, 3);
            Seg(a, v.d, 0, v.d, K(v.d), AMBER, 1.5, '4 3');
            Dot(a, v.d, K(v.d), AMBER, 6);
            return 'gamma = ' + fmt(v.g) + ', distance = ' + fmt(v.d) + ', distance^2 = ' + (v.d * v.d).toFixed(2) + '  ->  K = ' + K(v.d).toFixed(3);
        });
'''

build('svmlesson2.html', 'Support Vector Machines: Lesson 2', 'Lesson 02 &middot; Turin Polytechnic University in Tashkent',
      'Support Vector Machines',
      'Which line is the best line? The one down the widest street. We keep the recipe (model, loss, optimize) and change the picture, the loss, and then bend the line with kernels.',
      S, JS)
