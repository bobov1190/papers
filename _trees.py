from _lib import *

S = []

S.append(('sec-patients', 'Meet the Patients', (
    P('Five models, one recipe each time: <strong>model, loss, optimize</strong>. Today a new question: <em>can a model just ask yes/no questions?</em>')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'SVM', 'KNN', 'Today: Tree', 'Today: Forest'], [
        ['Output', 'a number', 'a probability', 'N probabilities', '$-1$ / $+1$', 'a fate (vote)', '?', '?'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', 'line + sign', 'the patient list', '?', '?'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', 'hinge loss', 'test mistakes', '?', '?'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', 'gradient descent*', 'try $k$ (CV)', '?', '?']])
    + CALL('check', 'In every column the optimizer was a walk downhill. Trees break that pattern.')
    + H3('Our data: breast tumor cells')
    + P('The breast-cancer data has <strong>569 real patients</strong>. For each we measure the cell nuclei on a biopsy image. Here are $24$ of them: the size of the nucleus (<em>radius</em>) and the dents on its outline (<em>concave points</em>). $14$ are benign and $10$ malignant (in all $569$: $357$ and $212$).')
    + TBL(['Patient', 'Radius', 'Dents', 'Diagnosis'], [['patient 1', '23.3', '0.190', 'malignant'], ['patient 2', '9.5', '0.085', 'benign']])
    + P('Big nuclei with many dents: malignant. But the groups overlap.')
    + H3('Intuition: twenty questions')
    + P('A doctor does not measure everything at once. She asks short yes/no questions, and every answer sends the patient to a smaller, cleaner group. She stops when the group is (almost) one diagnosis.')
    + P('Question 1: <em>radius $\\le 16.8$?</em> The left group has $16$ patients, $2$ malignant. The right group has $8$ patients, all malignant.')
    + QA('The star patient has radius $14.1$. Which side of the cut?', '<p>Left ($\\le 16.8$), the mostly benign side. One more question will settle it.</p>')
), True))

S.append(('sec-model', 'The Tree Model', (
    P('A <strong>stack of yes/no questions</strong>. Seven symbols follow us to the end.')
    + TBL(['Symbol', 'What it means', 'Our patients'], [
        ['$x$', 'a patient: his measurements', '$(14.1, 0.098)$: radius, dents'],
        ['$j, t$', 'a question: feature $j$ and threshold $t$', '$j$ = radius, $t=16.8$: &ldquo;radius $\\le 16.8$?&rdquo;'],
        ['$R$', 'a box on the map: a group of patients', '$R$ = patients with radius $\\le 16.8$ (16 of 24)'],
        ['$p$', 'share of one class inside a box', 'benign share of all 24: $14/24 = 0.58$'],
        ['$G$', 'Gini: how mixed a box is (0 = pure)', '$G=0.49$ for all 24 patients'],
        ['$c$', 'the answer a box gives (its majority)', 'left-left box: $c$ = benign'],
        ['$\\hat{y}$', 'the tree\'s answer for a patient', 'benign $=1$, malignant $=0$']])
    + CALL('check', 'The tree learns $j$ and $t$. The depth and the crowd size are settings we choose.')
    + H3('One question cuts the map')
    + P('A question is a rule &ldquo;$x_j \\le t$?&rdquo;. Its answer splits the patients into two boxes: one straight cut, parallel to an axis.')
    + M(r'R_L = \{x : x_j \le t\}, \qquad R_R = \{x : x_j \gt t\}')
    + P('Our case, $j$ = radius, $t=16.8$: the left box has $16$ patients ($2$ malignant, $14$ benign), the right box has $8$ ($8$ malignant, $0$ benign). The right box is pure: no more questions needed. The left box is still mixed: ask again.')
    + QA('Why is a cut always parallel to an axis?', '<p>A question mentions one measurement only: &ldquo;radius $\\le t$&rdquo; or &ldquo;dents $\\le t$&rdquo;.</p>')
    + H3('A stack of questions')
    + P('Ask again inside the left box. The cuts form boxes and the questions form a <strong>tree</strong>. Every box is a leaf. Counts are (malignant : benign).')
    + CODE('radius &le; 16.8 ?\n |-- no  : malignant (8 : 0)\n |-- yes : dents &le; 0.142 ?\n           |-- yes : benign    (0 : 13)\n           |-- no  : malignant (2 : 1)')
    + QA('How many questions does the deepest patient answer?', '<p>Two. The tree is as deep as the longest path from the top box to a leaf.</p>')
    + H3('The prediction: walk down the tree')
    + P('A new patient walks from the top box down. Each answer picks a branch and a leaf gives the answer. No formula to fit: only comparisons.')
    + M(r'\hat{y}(x) = \sum_{m=1}^{M} c_m\,\mathbf{1}\,[\,x \in R_m\,]')
    + P('$M$ leaves are $M$ boxes $R_m$. A patient falls in exactly one box and gets that box\'s answer $c_m$. Our case, $M=3$: radius $14.1 \\le 16.8$? yes, go left. Dents $0.098 \\le 0.142$? yes, go left. Leaf $(0:13)$: all benign, so $\\hat{y}=1$.')
    + QA('A patient has radius 20. How many questions?', '<p>One. Radius $\\gt 16.8$ sends him straight to a malignant leaf.</p>')
    + H3('A leaf answers by majority')
    + P('A leaf holds the training patients that landed in it. Its answer is the most common diagnosis, and the share inside is a probability-like score.')
    + M(r'c_m = \arg\max_k\, p_{mk}, \qquad p_{mk} = \frac{1}{n_m}\sum_{i \in R_m}\mathbf{1}[y_i = k]')
    + TBL(['Leaf', 'Malignant : benign', '$p(\\text{benign})$', 'Answer'], [
        ['left-left', '0 : 13', '13/13 = 1.00', 'benign'], ['left-right', '2 : 1', '1/3 = 0.33', 'malignant'], ['right', '8 : 0', '0/8 = 0.00', 'malignant']])
    + QA('The middle leaf has 2 malignant and 1 benign. What does it say?', '<p>Malignant (2 of 3). The leaf is not pure, so the tree is wrong for 1 patient here.</p>')
), True))

S.append(('sec-loss', 'The Loss: How Mixed Is a Box?', (
    P('The tree needs a score for a box. A pure box scores $0$, a fifty-fifty box is the worst. <strong>Gini</strong> is the chance that two random patients of the box have different diagnoses.')
    + M(r'G(R) = 1 - \sum_{k=1}^{K} p_k^2')
    + P('Here $p_k$ is the share of class $k$ in the box. Our case, $K=2$: $G = 1 - p_{\\text{ben}}^2 - p_{\\text{mal}}^2$. Play with the counts.')
    + WIDGET('wtree1', 'Figure 3.1 &mdash; Interactive. Gini (green) and entropy (amber) against the benign share $p$. Both are $0$ for a pure box and largest at $50:50$.', [('p', 'share of benign $p$', 0, 1, 0.01, 0.58)], H=270)
    + TBL(['Box (M : B)', 'Gini'], [['0 : 10', '0.00'], ['2 : 8', '0.32'], ['5 : 5', '0.50'], ['10 : 14', '0.49']])
    + QA('Which box is the easiest for the tree?', '<p>The first one, $G=0$. Everyone in it has the same diagnosis.</p>')
    + H3('Gini by hand: the top box')
    + P('The top box holds all $24$ patients: $10$ malignant and $14$ benign. Count, divide, square, subtract from $1$.')
    + TBL(['Class', 'Count $n_k$', 'Share $p_k$', '$p_k^2$'], [['malignant', '10', '10/24 = 0.417', '0.174'], ['benign', '14', '14/24 = 0.583', '0.340']])
    + M(r'G = 1 - 0.174 - 0.340 = 0.486')
    + P('Close to the worst possible value for two classes, $0.5$. If all $24$ were benign, $G = 1 - 1^2 = 0$.')
    + H3('Scoring a question: weighted Gini')
    + P('A question makes two boxes. Its score is the Gini of each box, <em>weighted by its size</em>. Lower is better: we want the cleanest children.')
    + M(r'J(j, t) = \frac{n_L}{n}\,G(R_L) + \frac{n_R}{n}\,G(R_R)')
    + TBL(['Question', 'Left (M : B)', 'Right (M : B)', 'Weighted sum', '$J$'], [
        ['radius $\\le 16.8$', '2 : 14', '8 : 0', '0.67&middot;0.22 + 0.33&middot;0.00', '0.146'],
        ['dents $\\le 0.14$', '1 : 12', '9 : 2', '0.54&middot;0.14 + 0.46&middot;0.30', '0.213'],
        ['radius $\\le 12$', '0 : 5', '10 : 9', '0.21&middot;0.00 + 0.79&middot;0.50', '0.395']])
    + P('The first question gives the lowest $J$: it makes the cleanest boxes. Try your own split, and compare Gini with entropy.')
    + WIDGET('wtree2', 'Figure 3.2 &mdash; Interactive. Set the counts of the two boxes. Start values: the split &ldquo;radius $\\le 16.8$&rdquo;.',
             [('ml', 'left: malignant', 0, 20, 1, 2), ('bl', 'left: benign', 0, 20, 1, 14), ('mr', 'right: malignant', 0, 20, 1, 8), ('br', 'right: benign', 0, 20, 1, 0)], H=170)
    + QA('Why weight by size and not just add $G(R_L) + G(R_R)$?', '<p>A tiny pure box would otherwise look as important as a big messy one.</p>')
    + H3('Try every threshold')
    + P('For one measurement, sort the patients and test a cut between every two neighbors: $23$ cuts for our $24$ radii. Score each cut by $J$. The lowest point is the best question for this measurement: $t=16.8$ with $J=0.146$.')
    + QA('How many cuts does the tree test for a measurement with $n$ patients?', '<p>At most $n-1$. It is a search, not a walk downhill.</p>')
    + H3('Gini and entropy: two ways to say &ldquo;mixed&rdquo;')
    + M(r'H(R) = -\sum_{k=1}^{K} p_k \log_2 p_k \qquad (0 \cdot \log 0 = 0)')
    + P('Top box, $p=(0.417, 0.583)$: $H = -0.417\\log_2 0.417 - 0.583\\log_2 0.583 = 0.980$ (and $G=0.486$). In practice both pick almost the same questions. sklearn uses Gini by default: no logarithm, only squares, so it is cheaper.')
    + H3('Information gain by hand')
    + P('With entropy, a question is scored by how much it lowers the entropy: the <strong>information gain</strong>. Bigger is better.')
    + M(r'\mathrm{IG} = H(\text{parent}) - \Big(\frac{n_L}{n}H(L) + \frac{n_R}{n}H(R)\Big)')
    + TBL(['Box', 'M : B', 'Patients', 'Entropy $H$'], [['top box (all)', '10 : 14', '24', '0.980'], ['left: radius $\\le 16.8$', '2 : 14', '16', '0.544'], ['right: radius $\\gt 16.8$', '8 : 0', '8', '0.000']])
    + M(r'\mathrm{IG} = 0.980 - (0.67 \times 0.544 + 0.33 \times 0) = 0.617')
    + P('Your turn with the two other questions: dents $\\le 0.14$ gives $\\mathrm{IG} = 0.454$ and radius $\\le 12$ gives $\\mathrm{IG} = 0.190$. The ranking matches the weighted Gini scores. Radius $\\le 12$ isolates $5$ benign patients perfectly, but it only cleans a small box: the big box stays almost $50:50$.')
), True))

S.append(('sec-opt', 'Optimize: Grow the Tree', (
    P('No walk downhill: we grow the tree <strong>greedily</strong>. Start with one box (all training patients). Find the question with the lowest $J$, split, repeat in each child. Each box takes the best question for itself and never looks back.')
    + M(r'(j^*, t^*) = \arg\min_{j,\,t}\ J(j, t)')
    + P('This recipe is called ID3 (with entropy) or CART (with Gini). The loop is the same: look at the box (pure, too small or too deep? then it becomes a leaf), score every question, ask the best one, repeat on both children.')
    + P('Our case: the top box has $398$ training patients. Best cut per measurement:')
    + TBL(['Measurement', 'Best question', 'Score $J$'], [['worst radius', '$\\le 16.80$', '0.131'], ['worst concave points', '$\\le 0.142$', '0.135']])
    + P('Radius wins (lower $J$), so it is the top question of the tree.')
    + QA('Greedy never revisits a choice. Is the tree then the best possible?', '<p>Not always. A weak first question may allow two strong ones later, but greedy never sees that. It is a good tree found fast. Looking for the best one is far too slow.</p>')
    + H3('Growing deeper')
    + P('Same $398$ training patients, three depths. Each extra level cuts the boxes finer.')
    + TBL(['Depth', 'Train', 'Test'], [['1: one cut', '93.0%', '90.6%'], ['3', '97.0%', '91.8%'], ['no limit: every box pure', '100.0%', '91.2%']])
    + P('Training keeps climbing, test stops early: depth $2$ gives the best test ($92.4\\%$), while a full tree at depth $15$ has train $100\\%$ and test $91.2\\%$: memorized. When every leaf is pure the tree has memorized every patient.')
    + H3('Stopping rules: keep the tree short')
    + P('<strong>Overfitting</strong> means the tree memorizes. We stop it with simple rules, or cut branches afterwards. Every rule is a setting we choose, not a weight the tree learns.')
    + TBL(['Rule', 'Leaves', 'Train', 'Test'], [
        ['no rule (grow to the end)', '24', '100.0%', '91.2%'], ['<code>max_depth = 3</code>', '7', '97.0%', '91.8%'],
        ['<code>min_samples_leaf = 10</code>', '9', '96.0%', '91.8%'], ['<code>min_impurity_decrease = 0.01</code>', '3', '95.5%', '92.4%'],
        ['pruning: <code>ccp_alpha = 0.01</code>', '5', '96.5%', '91.2%']])
    + QA('What is pruning?', '<p>Grow the full tree first, then cut away the branches that add little. A smaller tree, a steadier test score.</p>')
    + H3('Choosing the depth: cross-validation')
    + P('We pick the setting like we picked $k$: rotate the fresh part inside the training list and keep the test list for the final exam.')
    + TBL(['Depth', '1', '2', '3', '4', '6', '8', '12'], [['CV accuracy', '90.2%', '94.0%', '94.7%', '93.2%', '92.7%', '92.5%', '92.2%']])
    + P('Winner: depth $3$ with CV $94.7\\%$, final exam test $91.8\\%$. Depths $2$ to $6$ differ by about two points, so the exact depth is within the noise: a short tree is enough.')
    + H3('Regression tree: average instead of vote')
    + P('Same boxes, but the target is a number (here: how many dents a nucleus of a given radius has). A leaf answers with the <strong>average</strong> of its training patients.')
    + M(r'c_m = \frac{1}{n_m}\sum_{i \in R_m} y_i, \qquad \mathrm{MSE}(R_m) = \frac{1}{n_m}\sum_{i \in R_m}(y_i - c_m)^2')
    + P('Depth $1$ gives $2$ leaves, depth $3$ gives $8$ leaves, depth $8$ gives $136$ leaves: more and more steps, and finally one step per dot.')
    + H3('One tree is unstable')
    + P('Resample the $398$ training patients a few times (all $30$ measurements) and grow a full tree on each. Small changes in the data change the top question and the score.')
    + TBL(['Tree', 'Top question', 'Depth', 'Test'], [
        ['resample 1', 'worst perimeter $\\le 113.75$', '5', '93.6%'], ['resample 2', 'worst perimeter $\\le 114.45$', '5', '93.0%'],
        ['resample 3', 'mean concave points $\\le 0.06$', '5', '90.1%'], ['resample 4', 'worst concave points $\\le 0.15$', '7', '91.8%'],
        ['resample 5', 'worst concave points $\\le 0.14$', '6', '91.2%'], ['resample 6', 'worst perimeter $\\le 106.10$', '5', '93.0%'],
        ['resample 7', 'mean concave points $\\le 0.05$', '4', '93.0%']])
    + QA('Seven trees, the same kind of data. Are they the same tree?', '<p>No. The test score moves between $90.1\\%$ and $93.6\\%$ and the top question changes. One tree is a nervous judge.</p>')
), True))

S.append(('sec-forest', 'Random Forest', (
    P('Many different trees, one vote.')
    + H3('Bootstrap: resample with replacement')
    + P('Every tree gets its own list: draw $n$ patients from the $n$ we have, <em>putting each one back after the draw</em>. Some patients are drawn twice or more, others never. The never-drawn ones are <strong>out of bag</strong>.')
    + M(r'P(\text{never drawn}) = \Big(1 - \frac{1}{n}\Big)^{n} \longrightarrow e^{-1} \approx 0.368')
    + WIDGET('wtree3', 'Figure 5.1 &mdash; Live simulation. Draw $n$ patients with replacement from $n$ and count how many were never drawn.', [('n', 'patients $n$', 10, 1000, 10, 398)], H=200)
    + P('Our case, $n=398$: one resample keeps $64.3\\%$ of the patients and $35.7\\%$ are out of bag. Each tree trains on its own resample, so each tree is a little different.')
    + H3('Random features: each split sees a few')
    + P('Resampling is not enough: trees would still all start with the same top question. So at every split the tree may only look at $m$ randomly chosen measurements.')
    + M(r'm = \lfloor \sqrt{M} \rfloor')
    + P('$M$ is the number of measurements. Our case: $M=30$, so $m=5$ at every split.')
    + QA('Why forbid a tree to use the best measurement?', '<p>A strong measurement would win every top split and all trees would look alike. Different trees make a better crowd.</p>')
    + H3('The forest votes')
    + P('Ask all $B$ trees about the same patient. The majority wins, and the share of votes is a score. Wrong trees are scattered, right trees agree.')
    + M(r'\hat{y}(x) = \operatorname{mode}\{T_b(x)\}_{b=1}^{B}, \qquad \hat{p}_k(x) = \frac{1}{B}\sum_{b=1}^{B}\mathbf{1}[T_b(x) = k]')
    + P('Our case: $B=100$ trees, one test patient. $82$ trees say benign and $18$ say malignant: the forest says <strong>benign</strong> (share $0.82$). One single tree said malignant, the truth is benign. Most trees see the patient differently than the one wrong tree, and the errors cancel in the vote.')
    + H3('Why does averaging help?')
    + P('Each tree makes mistakes of its own. Averaging cancels the mistakes that are not shared. What is left is the mistake they all make together: the more alike the trees, the less help. Here $\\sigma^2$ is the variance of one tree and $\\rho$ says how alike two trees are.')
    + M(r'\operatorname{Var}(\bar{f}) = \rho\,\sigma^{2} + \frac{1-\rho}{B}\,\sigma^{2}')
    + WIDGET('wtree4', 'Figure 5.2 &mdash; Interactive. Variance of the average of $B$ trees (one tree $=1$). Different trees (small $\\rho$) gain much more.', [('rho', '$\\rho$', 0, 1, 0.05, 0.5), ('B', 'trees $B$', 1, 100, 1, 25)], H=270)
    + P('On our $30$ splits the spread of the test score went from $\\pm 2.1$ (one tree) to $\\pm 1.5$ (forest).')
    + H3('How many trees?')
    + P('Test accuracy of the forest as it grows from $1$ tree to $300$: $1$ tree gives $88.9\\%$, $100$ trees $95.3\\%$, $300$ trees $95.3\\%$. The first trees help a lot, later ones barely change the score. More trees cost time but cannot overfit more.')
    + H3('Out-of-bag: a free exam')
    + P('A patient who is out of bag for a tree was never seen by that tree. Let only those trees vote for him: an honest exam without a test list.')
    + M(r'\text{OOB error} = \frac{1}{n}\sum_{i=1}^{n}\mathbf{1}\big[\hat{y}_i^{\text{oob}} \neq y_i\big]')
    + P('Our forest, $B=100$: OOB accuracy $97.0\\%$, test accuracy $95.3\\%$. Two exams, nearly the same. You get a test estimate for free, using only training patients. Handy when data is scarce.')
    + H3('Tree against forest')
    + P('Same two measurements, $398$ training patients. One full tree has jagged boxes: train $100.0\\%$, test $91.2\\%$. A forest of $100$ trees has a smoother border: train $100.0\\%$, test $93.6\\%$. Both reach $100\\%$ on train, but the forest border follows the trend, not each single dot.')
    + H3('Thirty different splits')
    + P('We repeat the whole experiment on $30$ random train/test splits (all $30$ measurements):')
    + TBL(['Model', 'Mean test accuracy', 'Spread'], [['one tree', '92.6%', '$\\pm 2.1$'], ['forest of 100', '95.6%', '$\\pm 1.5$']])
    + P('The forest wins in $27$ of $30$ splits: higher on average and less spread. It is the steadier model, not a magic one.')
    + H3('Which measurements matter?')
    + TBL(['By impurity (Gini lowered)', '', 'By shuffling (test drop)', ''], [
        ['worst perimeter', '0.171', 'worst radius', '0.018'], ['worst radius', '0.128', 'worst concave points', '0.017'],
        ['worst concave points', '0.108', 'worst area', '0.016'], ['mean concave points', '0.094', 'worst texture', '0.013'],
        ['mean perimeter', '0.076', 'mean texture', '0.009'], ['mean concavity', '0.068', 'worst perimeter', '0.008'],
        ['worst area', '0.066', 'mean concave points', '0.008'], ['mean area', '0.049', 'mean concavity', '0.008']])
    + CALL('pit', 'The two lists differ. Correlated measurements share the credit, so read it as a hint, not a proof. Shuffling a column checks the real damage.')
    + H3('The settings of a forest')
    + P('The forest learns its trees. We choose how many, how random and how deep. Most defaults work; check with OOB or cross-validation.')
    + TBL(['Setting', 'What it does'], [
        ['<code>n_estimators</code>', 'number of trees $B$: more = steadier and slower. Default 100'],
        ['<code>max_features</code>', 'measurements a split may see: $\\sqrt{M}$ for classification. Smaller = more different trees'],
        ['<code>max_depth</code>, <code>min_samples_leaf</code>', 'how far each tree may memorize (by default trees grow to pure leaves)'],
        ['<code>bootstrap</code>', 'resample the patients for each tree (True by default, creates the out-of-bag patients)'],
        ['<code>oob_score</code>', 'free exam on out-of-bag patients: read <code>forest.oob_score_</code>'],
        ['<code>random_state</code>', 'fixes the dice: same number = same forest every run']])
    + H3('Beyond accuracy: the confusion matrix')
    + P('Forest of $100$ trees, all $30$ measurements, the same $171$ test patients: accuracy $95.3\\%$. Accuracy hides which kind of mistake we make. The matrix counts each kind (positive class = malignant).')
    + TBL(['', 'Forest says malignant', 'Forest says benign'], [['truly malignant', 'TP = 59 (caught)', 'FN = 5 (missed!)'], ['truly benign', 'FP = 3 (false alarm)', 'TN = 104 (cleared)']])
    + TBL(['Score', 'Formula', 'Our case', 'Value'], [
        ['accuracy', '$\\frac{TP+TN}{n}$', '(59+104) / 171', '95.3%'], ['precision', '$\\frac{TP}{TP+FP}$', '59 / (59+3)', '95.2%'],
        ['recall', '$\\frac{TP}{TP+FN}$', '59 / (59+5)', '92.2%'], ['F1', '$\\frac{2PR}{P+R}$', '2&middot;0.952&middot;0.922 / (0.952+0.922)', '93.7%']])
    + QA('For a doctor, which mistake is worse, FN or FP?', '<p>FN. A missed tumor goes untreated. A false alarm costs a second test. We watch FN closely.</p>')
    + QA('A lazy model says &ldquo;benign&rdquo; for everybody. What are its accuracy and recall?', '<p>Accuracy about $62.6\\%$ (the benign share, $107$ of $171$) but recall $0\\%$. This is why accuracy alone can fool us.</p>')
    + H3('Strengths and weaknesses')
    + TBL(['Strengths', 'Weaknesses'], [
        ['Questions you can read and explain to a doctor', 'One full tree memorizes: 100% train, about 91% test'],
        ['No scaling needed: a cut on radius ignores its units', 'One tree is unstable: small data change, new top question'],
        ['Mixes numbers and categories, bends to any border', 'Cuts are parallel to the axes: diagonal borders need many steps'],
        ['Forest: 95.6% &plusmn; 1.5 against 92.6% &plusmn; 2.1 for one tree', 'A forest of 100 trees is no longer readable'],
        ['Forest: a free exam, the out-of-bag score (97.0%)', 'Importance lists can mislead when columns are correlated']])
), True))

S.append(('sec-together', 'Putting It Together', (
    P('Same recipe, seven models. Trees fill the &ldquo;?&rdquo; with questions and counting. There is no gradient anywhere: the &ldquo;optimizer&rdquo; is a search over splits, then a crowd of trees.')
    + TBL(['', 'Linear', 'Logistic', 'Softmax', 'SVM', 'KNN', 'Tree', 'Forest'], [
        ['Output', 'a number', 'a probability', 'N probabilities', '$-1$ / $+1$', 'a fate (vote)', 'a class (leaf)', 'a vote of trees'],
        ['1. Model', 'line', 'line + sigmoid', 'N lines + softmax', 'line + sign', 'the patient list', 'stack of questions', 'many trees'],
        ['2. Loss', 'squared error', 'log loss', 'cross-entropy', 'hinge loss', 'test mistakes', 'Gini impurity', 'Gini + OOB error'],
        ['3. Optimize', 'gradient descent', 'gradient descent', 'gradient descent', 'gradient descent*', 'try $k$ (CV)', 'greedy split search', 'resample, grow, vote']])
    + CALL('check', 'Trees ask, counting scores, search grows. Forests average many noisy trees.')
    + H3('All of it in a few lines of sklearn')
    + P('A tree and a forest share the same interface: fit, score, predict. No scaling needed. The forest also hands us a free OOB score.')
    + CODE('X, y = load_breast_cancer(return_X_y=True)\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.3, stratify=y, random_state=0)\n\ntree = DecisionTreeClassifier(max_depth=3, random_state=0)\ntree.fit(X_train, y_train)\nforest = RandomForestClassifier(n_estimators=100, oob_score=True,\n                                random_state=0).fit(X_train, y_train)\n\nprint(tree.score(X_test, y_test))     # 0.901\nprint(forest.score(X_test, y_test))   # 0.953\nprint(forest.oob_score_)              # 0.970')
    + QA('Why does the tree not need a scaler, unlike KNN?', '<p>A question compares one measurement with a threshold. Units do not matter, only the order of the values.</p>')
), True))

S.append(('sec-recap', 'What We Learned', (
    CARDS([('1 &middot; Questions cut the map', 'Each yes/no question is one straight cut. A leaf answers by majority.'),
           ('2 &middot; Gini + greedy search', 'Pick the cut with the cleanest boxes, again and again. No gradient.'),
           ('3 &middot; One tree memorizes', 'Grown to the end: train 100%, test about 91%. Stop it early.'),
           ('4 &middot; A forest of random trees', 'Resample, random features, vote: 95.6% against 92.6% over 30 splits.')])
    + P('Thank you! Questions?')
), True))

S.append(('sec-glossary', 'Glossary &amp; Terminology', GLOSS([
    ('Question', '&ldquo;Is $x_j \\le t$?&rdquo;: one cut of the map.'), ('Leaf', 'A final box: it gives the answer.'),
    ('Gini $G$', 'How mixed a box is: $0$ = pure.'), ('Split score $J$', 'Weighted Gini of the two children.'),
    ('Entropy, information gain', 'Another way to measure mixing; the gain is how much a question lowers it.'), ('Depth', 'The longest chain of questions.'),
    ('Pruning', 'Cut away branches that add little.'), ('Greedy', 'Best question now, no looking back.'),
    ('Overfitting', 'Memorizing the training list.'), ('Bootstrap', 'A resample with replacement.'),
    ('<code>max_features</code> $m$', 'How many measurements a split may see.'), ('Out-of-bag', 'Patients a tree never saw: a free exam.'),
    ('Vote', 'The majority of trees is the answer.'), ('Precision / recall / F1', 'Scores built from the confusion matrix: alarms that were real, tumors that were caught, and their balance.')]), False))

JS = r'''
        Wire('wtree1', ['p'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 50, r: 20, t: 20, b: 34, x: [0, 1], y: [0, 1], xt: [0, 0.25, 0.5, 0.75, 1], yt: [0, 0.5, 1], xl: 'share of benign p', yl: 'mixedness' });
            const G = (p) => 1 - p * p - (1 - p) * (1 - p);
            const H = (p) => (p <= 0 || p >= 1 ? 0 : -p * Math.log2(p) - (1 - p) * Math.log2(1 - p));
            Curve(a, G, 0, 1, GREEN, 3);
            Curve(a, H, 0, 1, AMBER, 3);
            Seg(a, v.p, 0, v.p, 1, 'currentColor', 1, '4 3');
            Dot(a, v.p, G(v.p), GREEN, 6);
            Dot(a, v.p, H(v.p), AMBER, 6);
            Txt(a, 0.03, 0.95, 'Gini (peak 0.5)', GREEN, 13);
            Txt(a, 0.03, 0.88, 'entropy (peak 1.0)', AMBER, 13);
            return 'p = ' + fmt(v.p) + ':   Gini = ' + G(v.p).toFixed(3) + '     entropy = ' + H(v.p).toFixed(3);
        });

        Wire('wtree2', ['ml', 'bl', 'mr', 'br'], (v, svg) => {
            const Hh = (m, b) => { const n = m + b; if (!n || !m || !b) return 0; const p = m / n, q = b / n; return -p * Math.log2(p) - q * Math.log2(q); };
            const Gg = (m, b) => { const n = m + b; if (!n) return 0; const p = m / n, q = b / n; return 1 - p * p - q * q; };
            const nl = v.ml + v.bl, nr = v.mr + v.br, n = nl + nr;
            if (!n) return 'add some patients';
            const gl = Gg(v.ml, v.bl), gr = Gg(v.mr, v.br);
            const J = (nl / n) * gl + (nr / n) * gr;
            const Hp = Hh(v.ml + v.mr, v.bl + v.br);
            const IG = Hp - ((nl / n) * Hh(v.ml, v.bl) + (nr / n) * Hh(v.mr, v.br));
            return 'left G = ' + gl.toFixed(3) + ', right G = ' + gr.toFixed(3) + '  ->  J = ' + J.toFixed(3) + '     parent H = ' + Hp.toFixed(3) + ',  information gain = ' + IG.toFixed(3);
        });

        Wire('wtree3', ['n'], (v, svg) => {
            const n = v.n, seen = new Uint8Array(n);
            for (let i = 0; i < n; i++) seen[Math.floor(Math.random() * n)] = 1;
            let kept = 0; for (let i = 0; i < n; i++) kept += seen[i];
            const a = Ax(svg, { W: 640, H: 200, l: 50, r: 20, t: 20, b: 30, x: [0, 100], y: [0, 1], xt: [0, 25, 50, 75, 100], yt: [], xl: '% of patients', yl: '' });
            Seg(a, 0, 0.7, 100 * kept / n, 0.7, GREEN, 26);
            Seg(a, 100 * kept / n, 0.7, 100, 0.7, AMBER, 26);
            Txt(a, 1, 0.52, 'drawn: ' + (100 * kept / n).toFixed(1) + '%', GREEN, 13);
            Txt(a, 99, 0.52, 'out of bag: ' + (100 - 100 * kept / n).toFixed(1) + '%', AMBER, 13, 'end');
            return 'n = ' + n + ':  one resample kept ' + kept + ' distinct patients, ' + (n - kept) + ' out of bag.  Theory: (1 - 1/n)^n = ' + (100 * Math.pow(1 - 1 / n, n)).toFixed(1) + '%  (moves a little each time you touch the slider)';
        });

        Wire('wtree4', ['rho', 'B'], (v, svg) => {
            const a = Ax(svg, { W: 640, H: 270, l: 50, r: 20, t: 20, b: 34, x: [0, 100], y: [0, 1.05], xt: [0, 25, 50, 75, 100], yt: [0, 0.5, 1], xl: 'number of trees B', yl: 'variance of the average' });
            const f = (r) => (B) => r + (1 - r) / Math.max(B, 1);
            Curve(a, f(0.9), 1, 100, '#ef4444', 1.8);
            Curve(a, f(0.1), 1, 100, '#3b82f6', 1.8);
            Curve(a, f(v.rho), 1, 100, GREEN, 3);
            const val = f(v.rho)(v.B);
            Seg(a, v.B, 0, v.B, val, AMBER, 1.5, '4 3');
            Dot(a, v.B, val, AMBER, 6);
            Txt(a, 60, 0.98, 'red: rho 0.9   blue: rho 0.1', 'currentColor', 12);
            return 'rho = ' + fmt(v.rho) + ', B = ' + v.B + ':  variance = ' + val.toFixed(3) + ' (one tree = 1.000, floor = rho = ' + fmt(v.rho) + ')';
        });
'''

build('treeslesson4.html', 'Decision Trees and Random Forests: Lesson 4', 'Lesson 04 &middot; Turin Polytechnic University in Tashkent',
      'Decision Trees &amp; Random Forests',
      'Benign or malignant? Ask a list of questions, then ask a whole forest. No gradient anywhere: the model is a stack of yes/no questions, and the optimizer is a greedy search.',
      S, JS)
