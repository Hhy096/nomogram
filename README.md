## simpleNomo

simpleNomo is a python package for generating nomograms of logistic regression models with only model coefficients and variables ranges.  

#### Backgroud
Nomogram, a graphical calculator, has adequately solved the problem of inconvenient calculation. Nomogram is a chart consisting of several arranged lines for visualization of logistic regression model. With the development of the electronic calculators and computers, nomograms become less popular these days. However, they are still very prevalent in the condition without the computation sources. There are several tools for generating nomograms. They are available in SAS, Stata, as well as **rms** and **hdnom** packages in R language.

However, these tools either lack an integrated toolbox such as SAS or take input only from model trained within the programming language like hdnom and rms. In this case, it is difficult for converting existing works that established logistic regression models but not published the training data or developed nomograms. Therefore, plenty of works will stagnate into logistic regression models with good performance rather than meaningful clinical applications.  

simpleNomo is a straightforward framework for creating nomograms for logistic regression models. simpleNomo can accepts only the coefficients
and range of predictors in a logistic regression model as inputs.

#### Requirements
```txt
pandas==1.2.4
numpy==1.21.5
matplotlib==3.5.1
```

#### To install
```terminal
pip install simpleNomo
```

#### Function Introduction
```python
nomogram(path, result_title="Positive Risk", fig_width=10, single_height=0.45, dpi=300,
         ax_para = {"c":"black", "linewidth":1.3, "linestyle": "-"},
         tick_para = {"direction": 'in', "length": 3, "width": 1.5,},
         xtick_para = {"fontsize": 10, "fontfamily": "Songti Sc", "fontweight": "bold"},
         ylabel_para = {"fontsize": 12, "fontname": "Songti Sc", "labelpad":100, 
                        "loc": "center", "color": "black", "rotation":"horizontal"},
         total_point=100)
```
- **path:** Path of the excel that reserves the model coefficients and variabels range. The template of excel can be downloade at https://github.com/Hhy096/nomogram/blob/main/template.xlsx.
- **result_title:** Title for the predictive name. Default "Positive Risk".
- **fig_width:** Width for the figure. Default 10.
- **single_height:** Hight for each axis of the nomogram. Default 0.45.
- **dpi:** The resolution in dots per inch. Default 300.
- **ax_para:** The parameters for axises in the nomogram. You can find more from *Other Parameters* part in https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html.
- **tick_para:** The parameters for probability matching axis. You can find more in https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html.
- **xtick_para:** The parameters for x-ticklables of axises. You can find more paramters in https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text.
- **ytick_para:** The parameters for y-ticklabels of axises. You can find more paramters in https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text.
- **total_point:** The maximum point for aixes. Default 100.

The procedure for generating nomogram of a specific logisitic regression is shown below.

An example can be illustrated as follows. A logistic regression model to predict refractory/recurrent cytomegalovirus (CMV) infection after haploidentical donor (HID) hematopoietic stem cell transplantation (HSCT) was presented in work [1]. The model is presented as
$$\text{Probability (refractory/recurrent CMV infection)} = \dfrac{1}{1+exp(−Y)}$$
where Y = 0.0322 × (age) – 0.0696 × (gender) + 0.5492 × (underlying disease) + 0.0963 × (the cumulative dose of prednisone during pre- engraftment phase) – 0.0771 × (CD34+ cell counts in graft) – 1.2926. The threshold of probability was 0.5243, which separates patients into high- and low-risk groups.

#### Step 1. Construct excel file
According to the equation of logistic regression, fill the template file as follows:
<img width="652" alt="image" src="https://user-images.githubusercontent.com/105685749/210125549-5281415f-79d5-43ad-b956-ef4d1227a041.png">

<font color=red> **There can be several tricks when constructing excels for input, please check excel_construction.md for detials.** </font>

Rename the template file to be 'model.xlsx'.

#### Step 2. Run the following python code 
```python
'''
Use pip to install simpleNomo in advance
'''
import simpleNomo
path = "./model.xlsx"
nomo = simpleNomo.nomogram(path=path)
```

#### Step 3. Get the nomogram
Then we can get the nomogram for the logistic regression.
![image](https://user-images.githubusercontent.com/105685749/229339773-a6c1b4d1-03fd-4b0c-8165-d76607c7714d.png)

<!--![image](https://user-images.githubusercontent.com/105685749/210125610-5f55d5c4-c270-41e3-8f3c-8d9174cfda58.png)-->

### Reference
[1] Shen, M. Z., Hong, S. D., Wang, J., Zhang, X. H., Xu, L. P., Wang, Y., ... & Mo, X. D. (2022). A predicted model for refractory/recurrent cytomegalovirus infection in acute leukemia patients after haploidentical hematopoietic stem cell transplantation. Frontiers in Cellular and Infection Microbiology, 12, 862526.
