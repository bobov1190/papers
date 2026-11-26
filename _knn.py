from _lib import *

S = []

S.append(('sec-passengers', 'Meet the Passengers', (
    P('Four models, one recipe each time: <strong>model, loss, optimize</strong>. Today we ask a new question: <em>can a model work without any of these steps?</em>')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'SVM', 'Today: KNN'], [
        ['Output', 'a number', 'a probability', 'N probabilities', 'a side: $-1$ or $+1$', '?'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', 'line + sign (+ kernel)', '?'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', 'hinge loss', '?'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', 'gradient descent*', '?']])
    + CALL('check', 'In every column the optimizer is the same walk downhill. KNN will break that pattern.')
    + H3('Our data: Titanic passengers')
    + P('The Titanic data has <strong>891 real passengers</strong>. For every one we know the age and the ticket fare. Here we look at $22$ of them, a random sample: age, fare in pounds, and the fate. $9$ of the $22$ survived and $13$ died.')
    + TBL(['Passenger', 'Age', 'Fare', 'Fate'], [['passenger 1', '29 yrs', '&pound;7.05', 'died'], ['passenger 2', '19 yrs', '&pound;36.75', 'died']])
    + P('Each passenger is one dot on a map of age and fare. The two fates are mixed: there are no clean groups.')
    + H3('Intuition: ask the neighbors')
    + P('You are likely to share the fate of people with a similar age and a similar ticket. Put yourself on the map (a yellow star) and look at the $k$ closest passengers. Let them vote.')
    + UL(['find the passengers closest to you', 'keep the $k$ closest (here $k=3$)', 'the majority fate wins the vote'])
    + P('With $k=3$ the vote is $2$ survived against $1$ died: the answer is <strong>survived</strong>.')
), True))

S.append(('sec-model', 'The Model: Distance and a Vote', (
    P('There are no weights to learn. The only tool we need is the <strong>distance</strong> between two passengers. Close in age and in ticket price means a small distance.')
    + M(r'd(a, b) = \sqrt{\sum_{j=1}^{d} (a_j - b_j)^2}')
    + P('Our case, $d=2$: $d = \\sqrt{(\\text{age}_a-\\text{age}_b)^2 + (\\text{fare}_a-\\text{fare}_b)^2}$. A real pair: you $=(35\\text{ years}, \\pounds 20)$ and passenger A $=(33, \\pounds 15.85)$.')
    + M(r'd = \sqrt{2^2 + 4.15^2} = 4.6')
    + P('The age differs by $2$ years and the fare by $\\pounds 4.15$: the fare gap does most of the work here.')
    + QA('Two passengers have the same age and the same fare. What is $d$?', '<p>$d=0$. The closer two passengers are, the smaller $d$.</p>')
    + H3('Measure it to all 22, sort, keep the closest')
    + P('Step 1: the distance from you to every one of the $22$ passengers. Step 2: sort from smallest to largest. The top of the list are your neighbors.')
    + TBL(['Rank', 'Age', 'Fare', 'Distance', 'Fate'], [
        ['1', '33', '&pound;15.85', '4.6', 'survived'], ['2', '30', '&pound;16.10', '6.3', 'died'], ['3', '36', '&pound;13.00', '7.1', 'survived'],
        ['4', '28', '&pound;16.10', '7.6', 'died'], ['5', '43', '&pound;26.25', '10.2', 'died']])
    + P('The other $17$ passengers are farther away.')
    + QA('Where is the training step? Where are the weights?', '<p>There are none. The model <em>is</em> the passenger list, we just measure distances.</p>')
    + H3('$k$ is the number of voters')
    + P('Same star, different $k$. Small $k$ listens to a few passengers, large $k$ listens to a crowd. The neighbors vote with their fates and the most common fate is the answer: no formula to fit, just count.')
    + M(r'\hat{y}(x) = \operatorname{mode}\big\{\, y_i : i \in N_k(x) \,\big\}')
    + P('Use the slider below: the five nearest passengers from the table, a plain vote, and a <strong>weighted vote</strong> where each neighbor shouts with weight $w_i = 1/d_i$ (half the distance, double the voice).')
    + WIDGET('wknn1', 'Figure 2.1 &mdash; Interactive. The $k$ nearest passengers vote. Plain vote against weighted vote $1/d$.', [('k', '$k$', 1, 5, 1, 3)], H=250)
    + CALL('pit', 'With $k=4$ the vote can be 2 against 2, a tie. That is why we like an odd $k$.')
    + QA('You are the same person. Why does the answer flip at $k=5$?', '<p>Farther passengers join the vote and outvote the closest ones. $k$ is a setting we choose.</p>')
    + P('Table of the weights for $k=5$: survived gets $0.217+0.141=0.358$, died gets $0.158+0.132+0.099=0.388$. The plain vote says died ($2$ against $3$) and the weighted vote also says <strong>died</strong>, with a slim $52.0\\%$.')
    + M(r'w_i = \frac{1}{d_i}, \qquad \text{score}(c) = \sum_{i \in N_k(x)} w_i\,\mathbf{1}[y_i = c]')
    + H3('Other rulers: Euclid and Manhattan')
    + P('Distance has more than one recipe. The ruler goes straight, the taxi follows the streets.')
    + WIDGET('wknn2', 'Figure 2.2 &mdash; Interactive. The same two passengers, two different numbers. Start values: 6 years and &pound;5.9.', [('da', 'age gap', 0, 10, 0.1, 6), ('df', 'fare gap (&pound;)', 0, 10, 0.1, 5.9)], H=250)
    + M(r'd_2(a,b) = \sqrt{\sum_j (a_j - b_j)^2} = \sqrt{6^2 + 5.9^2} = 8.4, \qquad d_1(a,b) = \sum_j |a_j - b_j| = 6 + 5.9 = 11.9')
    + QA('Which distance is longer for the same pair?', '<p>The taxi: it cannot cut the corner. We use the Euclid ruler unless told otherwise.</p>')
    + H3('Categories: count the mismatches')
    + P('Sex, class and port are words, not numbers: a ruler cannot measure &ldquo;woman minus man&rdquo;. Instead count how many answers differ. This is the <strong>Hamming distance</strong>.')
    + M(r'd(a,b) = \sum_{j=1}^{p} \mathbf{1}\,[\,a_j \neq b_j\,]')
    + P('If you and passenger P differ in only one of three answers, $d=1$; passenger Q differs in two, $d=2$, so P is the closer neighbor. (The numbers are made up to show the idea.) Do not code classes $1,2,3$ and use the ordinary ruler: it would say 1st and 3rd are twice as far as 1st and 2nd, and we cannot back that up.')
    + H3('Regression: average instead of vote')
    + P('The same idea works for a number: how much did a passenger of age $35$ pay? Ask the closest ages. The prediction is the <strong>average</strong> of the $k$ closest passengers (distance in age only).')
    + M(r'\hat{y}(x) = \frac{1}{k}\sum_{i \in N_k(x)} y_i')
    + TBL(['$k$', 'Predicted fare'], [['1', '&pound;52.00'], ['15', '&pound;28.92'], ['101', '&pound;25.63']])
    + P('Small $k$ follows every dot, large $k$ gives a smooth curve.')
    + H3('A lazy learner: no training step')
    + P('Other models learn weights first and then answer fast. KNN does the opposite: all its work happens when a new passenger arrives.')
    + TBL(['', 'What happens', 'Cost'], [
        ['<code>fit()</code>', 'store the 466 training passengers, nothing is computed', '0 steps downhill'],
        ['<code>predict()</code>', 'measure 466 distances, sort them, count the votes', 'all the work is here']])
    + CALL('check', 'A lazy learner is cheap to build and expensive to ask: a million passengers means a million distances per question.')
), True))

S.append(('sec-loss', 'The Loss: Mistakes on Fresh Passengers', (
    P('KNN has nothing to push down, but we still must <em>score</em> it. Split all $666$ passengers (age and fare known): $466$ stay in the list and $200$ are fresh passengers the list never saw. The loss is the share of fresh passengers we get wrong.')
    + M(r'L = \frac{1}{n}\sum_{i=1}^{n} \mathbf{1}\,[\,\hat{y}_i \neq y_i\,]')
    + TBL(['Fresh passenger', 'Fare', 'Truth', 'Prediction', 'Loss'], [
        ['21 yrs', '&pound;8.66', 'died', 'died', '0'], ['27 yrs', '&pound;13.00', 'died', 'survived', '1'], ['23 yrs', '&pound;7.85', 'died', 'died', '0'],
        ['50 yrs', '&pound;26.00', 'survived', 'died', '1'], ['18 yrs', '&pound;13.00', 'survived', 'died', '1']])
    + P('Our case ($k=5$, age and fare): wrong on $79$ of $200$ fresh passengers, so $L = 79/200 = 0.395$.')
    + QA('So which number do we report?', '<p>The test one, on passengers the list has never seen.</p>')
    + H3('Why not score on the same passengers?')
    + P('Ask a passenger from the list: his nearest neighbor is himself, at distance $0$. With $k=1$ the answer is almost always right, and that tells us nothing about a new passenger.')
    + TBL(['$k=1$', 'Accuracy'], [['on the list (train)', '97.4%'], ['on fresh passengers (test)', '62.0%']])
    + P('Train is not exactly $100\\%$: two passengers with the same age and fare can have different fates. <strong>Train accuracy rewards memory. Test accuracy rewards understanding.</strong>')
    + H3('Beat the dumbest model first')
    + P('The dumbest model ignores the passenger and always says &ldquo;died&rdquo; ($62$ of $100$ died). Any real model must score above it on fresh passengers.')
    + TBL(['Model', 'Test accuracy'], [['always say &ldquo;died&rdquo;', '62.0%'], ['KNN, $k=1$', '62.0%'], ['KNN, $k=5$', '60.5%'], ['KNN, $k=19$', '70.5%']])
    + CALL('pit', 'Age and fare alone are weak signals: even the best $k$ beats the dumb model by only a few points. A score of $62\\%$ is not good by itself.')
), True))

S.append(('sec-opt', 'Optimize: Choosing k', (
    P('There is no walk downhill. We try several $k$ and compare them. Start with three maps of the same $466$ passengers: the background is what the list would answer there.')
    + TBL(['$k$', 'Map', 'Train', 'Test'], [['1', 'too jumpy', '97.4%', '62.0%'], ['19', 'just right', '71.9%', '70.5%'], ['101', 'too smooth', '66.3%', '59.5%']])
    + QA('Which map would you trust with a new passenger?', '<p>The middle one. $k=1$ memorizes noise, $k=101$ ignores the neighborhood.</p>')
    + P('We measure the accuracy on the list and on fresh passengers for every odd $k$ from $1$ to $101$. At $k=1$ every passenger votes for himself: train $97\\%$, test $62\\%$, memorizing. At $k=101$ both fall: too smooth, no details left.')
    + H3('Cross-validation: rotate the fresh passengers')
    + P('The test set is for the final exam only. To choose $k$ we need <em>practice exams</em>. Cut the $466$ training passengers into $5$ parts. Each part is the fresh part once (here $k=19$).')
    + TBL(['Round', '1', '2', '3', '4', '5', 'Mean'], [['Accuracy', '69.1%', '73.1%', '69.9%', '64.5%', '63.4%', '68.0%']])
    + QA('Why not just pick the $k$ with the best test accuracy?', '<p>Then the test set is no longer fresh. We would be fitting $k$ to the exam.</p>')
    + H3('Try, compare, keep the best')
    + P('Repeat the rotation for each candidate $k$. This is KNN&rsquo;s &ldquo;optimization&rdquo;: a <em>search</em>, not a walk. A rule of thumb: start near $\\sqrt{n}$ (here about $22$) and use an odd $k$.')
    + TBL(['$k$', '1', '5', '11', '19', '31', '61', '101'], [['CV accuracy', '64.4%', '66.1%', '67.4%', '68.0%', '66.1%', '67.0%', '67.2%']])
    + P('Winner: $k=19$ with CV $68.0\\%$. The final exam gives test $70.5\\%$.')
    + QA('How do we know the winner is not just luck?', '<p>We do not, fully. Nearby $k$ differ by about a point, which is within the noise.</p>')
), True))

S.append(('sec-scale', 'The Trap: Scale', (
    P('The ruler listens to the loudest number. Women and men survived very differently, so add a third measurement: woman $=1$, man $=0$. KNN just adds one more term under the square root.')
    + TBL(['', 'Age', 'Fare', 'Sex'], [['you', '35 yrs', '&pound;20', '1 (woman)'], ['passenger P', '41 yrs', '&pound;14.11', '0 (man)']])
    + M(r'd^2 = 6^2 + 5.9^2 + 1^2 = 71.7')
    + P('Share of $d^2$ for this pair: age $50\\%$, fare $48\\%$, sex $1.4\\%$. Over <em>all</em> pairs of passengers it is worse: age $33\\%$, fare $67\\%$, sex only $0.04\\%$.')
    + QA('Sex changes $d^2$ by only 1. Does KNN even notice it?', '<p>Almost never. Age and fare are measured in tens, so the $0/1$ column is a whisper.</p>')
    + H3('The fix: the same scale for every feature')
    + P('Subtract the average, divide by the spread. Every column gets mean $0$ and spread $1$. This is what <code>StandardScaler</code> does. The ruler then hears all features equally.')
    + M(r'z = \frac{x - \mu}{\sigma}')
    + WIDGET('wknn3', 'Figure 5.1 &mdash; Interactive. Scaling with the real averages and spreads of our passengers (age $30.15 \\pm 14.32$, fare $23.51 \\pm 21.02$, sex $0.35 \\pm 0.48$).',
             [('age', 'age', 1, 80, 1, 35), ('fare', 'fare (&pound;)', 0, 100, 1, 20), ('sex', 'sex (1 = woman)', 0, 1, 1, 1)], H=220)
    + P('For you: age $z = (35-30.15)/14.32 = +0.34$, fare $z=-0.17$, sex $z=+1.36$. After scaling, the average and the spread of every column are $0$ and $1$: age, fare and sex speak at the same volume.')
    + H3('Before and after scaling')
    + TBL(['', 'Raw numbers', 'Scaled numbers'], [
        ['share of age / fare / sex', '33% / 67% / 0.04%', '34% / 33% / 33%'], ['best $k$ (by CV)', '5', '23'], ['test accuracy', '65.5%', '76.0%']])
    + P('Only the ruler changed. Test accuracy went $65.5\\% \\to 76.0\\%$. One split of $200$ is noisy, but cross-validation agrees: $69.7\\% \\to 78.8\\%$.')
    + H3('Useless columns blur the neighbors')
    + P('Add columns of pure random noise to the real ones. Every extra column adds distance but no information, so the neighbors stop being close: accuracy falls and &ldquo;near&rdquo; and &ldquo;far&rdquo; start to look the same. This is the <strong>curse of dimensionality</strong>. Try a simulation: random points, how close is the nearest one compared with an average one?')
    + WIDGET('wknn4', 'Figure 5.2 &mdash; Live simulation (200 random points in the unit cube, 15 queries). Nearest distance divided by average distance, as the number of columns grows.', [('d', 'number of columns', 1, 100, 1, 3)], H=250)
    + QA('Why do the nearest neighbors stop being near?', '<p>With many columns every passenger is far from every other one.</p>')
    + H3('Speed: cut the map in halves')
    + P('Measuring all $n$ distances is slow for a big list. A <strong>KD-tree</strong> cuts the map into boxes first: cut by age at the middle passenger, cut each half by fare, and so on. To find your neighbors, look only in the boxes near the star. On our sample that is $13$ distances instead of $22$, and the gain grows with the list: roughly $\\log n$ boxes instead of $n$.')
    + QA('Does the tree change the answer?', '<p>No. Same neighbors, found faster. It works best with few columns, not hundreds.</p>')
    + H3('Strengths and weaknesses')
    + TBL(['Strengths', 'Weaknesses'], [
        ['No training step: new data is simply added to the list', '$k=1$ memorizes: train 97.4%, test only 62.0%'],
        ['One main setting, $k$, chosen by cross-validation', 'Raw numbers: the big scale shouts. Scaling lifted the test from 65.5% to 76.0%'],
        ['Bends around any shape of border', 'Every prediction measures all distances (22 here, 13 with a KD-tree)'],
        ['Works for classes (vote) and numbers (average)', 'Useless columns blur the neighbors']])
), True))

S.append(('sec-together', 'Putting It Together', (
    P('Same recipe, five models. KNN fills the &ldquo;?&rdquo; in a very different way: its &ldquo;model&rdquo; is the data, its &ldquo;loss&rdquo; is a count, its &ldquo;optimizer&rdquo; is a search over $k$.')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'SVM', 'KNN'], [
        ['Output', 'a number', 'a probability', 'N probabilities', 'a side: $-1$ or $+1$', 'a fate (vote)'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', 'line + sign (+ kernel)', 'the passenger list'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', 'hinge loss', 'mistakes on fresh data'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', 'gradient descent*', 'try $k$, compare (CV)']])
    + CALL('check', 'No weights and no walk downhill. The only &ldquo;learning&rdquo; is choosing $k$, and scaling the ruler.')
    + H3('All of it in five lines of sklearn')
    + P('The scaler and KNN live in one pipeline, so scaling is learned only from the training list. <code>cross_val_score</code> picks $k$, the $200$ fresh passengers give the final exam.')
    + CODE('from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\n\nmodel = make_pipeline(StandardScaler(), KNeighborsClassifier(23))\nmodel.fit(X_train, y_train)      # just stores the list\nmodel.score(X_test, y_test)      # distances happen here\n\n# test accuracy 76.0% (k = 23, age + fare + sex, scaled)')
    + QA('Why is the scaler inside the pipeline?', '<p>So the test passengers never influence the average and spread used for scaling.</p>')
), True))

S.append(('sec-recap', 'What We Learned', (
    CARDS([('1 &middot; The model is the data', 'No weights, no training: <code>fit()</code> only stores the list.'),
           ('2 &middot; $k$ is the one big setting', '$k=1$ memorizes (train 97%, test 62%), a huge $k$ forgets the details.'),
           ('3 &middot; Scale the ruler', 'Raw numbers: 65.5%. Scaled: 76.0%. Same data, same $k$ search.'),
           ('4 &middot; Beat the dumbest model', '&ldquo;Always died&rdquo; scores 62%. Compare every score with it.')])
    + P('Thank you! Questions?')
), True))

S.append(('sec-glossary', 'Glossary &amp; Terminology', GLOSS([
    ('Neighbor', 'One of the $k$ training examples closest to the new one.'), ('$k$', 'The number of voters. Our one big setting.'),
    ('Distance', 'How far apart two examples are. Euclid goes straight, Manhattan follows the streets.'), ('Hamming distance', 'For categories: count how many answers differ.'),
    ('Weighted vote', 'Closer neighbors count more: weight $1/d$.'), ('Lazy learner', 'No training step: all the work happens at prediction time.'),
    ('Fresh passengers / test set', 'Examples the list never saw. The honest exam.'), ('Cross-validation', 'Rotate which part of the training list is the fresh part. Used to choose $k$.'),
    ('StandardScaler', 'Subtract the average, divide by the spread, for every column.'), ('Curse of dimensionality', 'With many columns every point is far from every other one.'),
    ('KD-tree', 'Cut the map into boxes so we only search the boxes near the new point.')]), False))

JS = r'''
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
'''

build('knnlesson3.html', 'K-Nearest Neighbors: Lesson 3', 'Lesson 03 &middot; Turin Polytechnic University in Tashkent',
      'K-Nearest Neighbors',
      'Who is your neighbor? Ask the closest passengers. A model with no weights and no walk downhill: the model is the data, and the only things to choose are $k$ and the ruler.',
      S, JS)
