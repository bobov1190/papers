# The Start of ML and Linear Models


Hi everybody
Today we are going to go through topics like Linear Regression and Logistic Regression. And that is not only thing about but also it is about Likelihood, Loss Functions, Gradient Descent Optimizer, Adam Optimizer, Softmax Regression, Simple NN and so on. So as you can see it is really huge topic to talk about cause it gathers the first beginner's ideas and solves fundamental questions.

So let's start from agenda of this big introduction topic:
1. Data and Likelihood
2. Log Negative Likelihood
3. Optimizer
4. Model Families: Linear models and some Classification models
5. Loss functions and difference between each of them
6. Linear Regression Explained fully
7. Logistic Regression Explained fully


## Data and Likelihood

So let's start from the roots of our models. How they have been created and etc. There is also one more really interesting question: how a model can learn the pattern of data and predict some info from it? And the answer is actually simple: Likelihood.

So imagine that we have some data and we have have target element to predict. So firstly, we are going talk about only tabular datasets. So let's say that we can predict either numbers or classes.

The example with the number can be the temperature prediction made on wind speed and humidity and etc. And example with the class can be within spam/not spam problem in your email or tg.
