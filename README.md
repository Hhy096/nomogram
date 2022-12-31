## Nomogram

Logistic regression model is commonly used in clinical prediction. However, when there is no computational resources or no internet access, especially in underdeveloped regions, it is demanding to take the model into practice by hand. As a visualization tool, nomogram can tremendously speed up the calculation procedure. However, existing tools for generating nomograms cannot be applied to the established logistic regression models providing only coefficients, which makes abundant works hard to transfer into clinical use. We designed and developed PyNG, a Python toolbox for making nomograms of logistic regression models. Uniquely, it provides a short-cut way to construct nomograms utilizing only the coefficients of the models. PyNG properly maintains the predictive ability of the original logistic regression model and easy to follow.

The procedure for generating nomogram of a specific logisitic regression is shown below.

An example can be illustrated as follows. A logistic regression model to predict refractory/recurrent cytomegalovirus (CMV) infection after haploidentical donor (HID) hematopoietic stem cell transplantation (HSCT) was presented in . The model is presented as
$$\text{Probability (refractory/recurrent CMV infection)} = \dfrac{1}{1+exp(−Y)}$$
where Y = 0.0322 × (age) – 0.0696 × (gender) + 0.5492 × (underlying disease) + 0.0963 × (the cumulative dose of prednisone during pre- engraftment phase) – 0.0771 × (CD34+ cell counts in graft) – 1.2926. The threshold of probability was 0.5243, which separates patients into high- and low-risk groups.

#### Step 1. Construct excel file
According to the equation of logistic regression, fill the template file as follows:
<img width="652" alt="image" src="https://user-images.githubusercontent.com/105685749/210125549-5281415f-79d5-43ad-b956-ef4d1227a041.png">

Rename the template file to be 'model.xlsx'.

#### Step 2. Run the following python code 
```python
'''
Download nomogram.py to certain path
'''
import sys
sys.path.append(path)
from nomogram import nomogram

path = "./example/model.xlsx"
nomogram(path=path, result_title="High Risk")
```

#### Step 3. Get the nomogram
Then we can get the nomogram for the logistic regression.
![image](https://user-images.githubusercontent.com/105685749/210125610-5f55d5c4-c270-41e3-8f3c-8d9174cfda58.png)
