import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import gridspec
from matplotlib.transforms import (Bbox, TransformedBbox)
from mpl_toolkits.axes_grid1.inset_locator import (BboxConnector)


### Prepare dataframe from input data
def generate_df_rank(path, total_point=100):
    
    df = pd.read_excel(path)
    
    df["range*coef"] = df["coef"]*(df["max"]-df["min"])
    df["abs_range*coef"] = abs(df["range*coef"])
    df = df.sort_values(by = "abs_range*coef", ascending = False)

    point = list(df["abs_range*coef"]/df["abs_range*coef"].shift(1))
    point[0] = 1
    point = total_point*np.cumprod(point)
    df["point"] = point
    
    df["negative_coef"] = np.minimum(df["coef"],0)
    df["positive_coef"] = np.maximum(df["coef"],0)
    
    return df


def compute_x(df, lm_intercept, specific_maxi, maxi_point, mini_point=0):

    mini_score = sum(df["negative_coef"]*df["max"])+sum(df["positive_coef"]*df["min"])+lm_intercept
    maxi_score = sum(df["negative_coef"]*df["min"])+sum(df["positive_coef"]*df["max"])+lm_intercept
        
    score = np.linspace(mini_score, maxi_score, 500)
    prob = 1/(1+np.exp(-score))

    x_point = np.linspace(0, maxi_point/specific_maxi, 500)

    return x_point, prob

  
### Draw axis
def set_axis(ax, title, min_point, max_point, xticks, xticklabels,
             ax_para = {"c":"g", "linewidth":1.5, "linestyle": "-"},
             tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             xtick_para = {"fontsize": 8,"fontfamily": "Times New Roman", 
                           "fontweight": "bold", "wrap":True},
             ylabel_para = {"fontsize": 10, "fontname": "Songti Sc", "labelpad":150,
                            "loc": "bottom", "color": "black", "rotation":"horizontal"},
             total_point=100):
#              fontsize=12, labelsize=10, labelpad=120):
    
#     ax.axhline(0, xmin=min_point/total_point, xmax=max_point/total_point, c="black", linewidth=1.5)
    ax.axhline(0, xmin=min_point/total_point, xmax=max_point/total_point, **ax_para)

    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.tick_params(**tick_para)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, **xtick_para)
    ax.set_ylabel(ylabel=title, **ylabel_para)
    
### Assign probability to overall point
def plot_prob(ax, title, x_point, prob, threshold=None,
             ax_para = {"c":"black", "linewidth":1, "linestyle": "-"},
             threshold_para = {"c":"g", "linewidth":1, "linestyle": "-."},
             tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             text_para = {"fontsize": 10,"fontfamily": "Times New Roman", "fontweight": "bold"},
             xtick_para = {"fontsize": 8,"fontfamily": "Times New Roman", "fontweight": "bold"},
             ylabel_para = {"fontsize": 10, "fontname": "Songti Sc", "labelpad":100,
                            "loc": "bottom", "color": "black", "rotation":"horizontal"},
             total_point=100):

    ax.spines['right'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim([0,1])
    ax.set_ylim([-1,0])
    
    ax.plot(x_point, -prob, **ax_para)
    
    if threshold != None:
        ax.axhline(-threshold, xmin=0, xmax=1, **threshold_para)
        ax.text(x=1.05, y=-threshold, s="threshold={}".format(threshold), **text_para,
                bbox=dict(facecolor='black', alpha=0.2))

    ax.tick_params(**tick_para)
    
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_xticklabels(['','','','','',''])
    ax.set_yticks([0,-0.2,-0.4,-0.6,-0.8,-1])
    ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], **xtick_para)
    
#     ax.set_ylabel(ylabel=title, fontsize=labelsize, fontname="Songti Sc", labelpad=67, 
#                   loc="center", color="black", rotation="horizontal")
    ax.set_ylabel(ylabel=title, **ylabel_para)
    

### Draw grid between different axes
def grid_connect(ax1, ax2, xticks, 
                 prop_lines={"lw": 0.5, "color": "b", "linestyle": "-."}, **kwargs):
    
    for xtick in xticks:
        bbox = Bbox.from_extents(xtick, 0, xtick, 1)
        
        bbox1 = TransformedBbox(bbox, ax1.get_xaxis_transform())
        bbox2 = TransformedBbox(bbox, ax2.get_xaxis_transform())
    
        c = BboxConnector(
            bbox1, bbox2, loc1=3, loc2=3, clip_on=False, **prop_lines)
        
        ax2.add_patch(c)
        
    return c

### Generate xtick and corresponding labels
def generate_xtick(range_, type_, mini, maxi, point, total_point):
    ran = point/total_point
#     print(ran)
#     print(type_)
    
    if type_=="nominal":
        range_ = int(range_)
        xticks = list(np.linspace(0, point/total_point, range_+1))
        xticklabels = list(range(int(mini), int(maxi)+1, 1))
    elif (0.1<=ran<0.25) or (range_<2):
        xticks = list(np.linspace(0, point/total_point, 5))
        xticklabels = list(np.linspace(mini, maxi, 5))
    elif (ran<0.1):
        xticks = list(np.linspace(0, point/total_point, 3))
        xticklabels = list(np.linspace(mini, maxi, 3))
    elif (range_<= 11):
        range_ = int(range_)
        xticks = list(np.linspace(0, point/total_point, range_+1))
        xticklabels = list(range(int(mini), int(maxi)+1, 1))
    elif range_ <= 150:
        xticks = list(np.linspace(0, point/total_point, 6))
        xticklabels = list(np.linspace(int(mini), int(maxi), 6))
    elif range_ <= 200:
        num = int((maxi-mini)//10+1)
        xticks = list(np.linspace(0, point/total_point, num))
        xticklabels = list(np.linspace(mini, maxi, num))
    else:
        num = int((maxi-mini)//50+1)
        xticks = list(np.linspace(0, point/total_point, num))
        xticklabels = [int(i) for i in list(np.linspace(mini, maxi, num))]
        
    return xticks, xticklabels

  
### Draw nomogram
def nomogram(path, result_title, lm_intercept, 
             threshold=None, fig_width=10, single_height=0.35, specific_maxi="default", dpi=150,
             ax_para = {"c":"black", "linewidth":1.5, "linestyle": "-"},
             tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             xtick_para = {"fontsize": 8,"fontfamily": "Times New Roman", "fontweight": "bold"},
             ylabel_para = {"fontsize": 10, "fontname": "Songti Sc", "labelpad":100,
                            "loc": "bottom", "color": "black", "rotation":"horizontal"},
             total_point=100):
    
    df = generate_df_rank(path=path, total_point=total_point)
    new = df["feature"].str.split(pat="_", expand=True)
    
    if new.shape[1] == 1:
        df["main_feature"] = new[0]
    else:
        df["main_feature"] = new[0]
        df["sub_feature"] = new[1]
        
    group = df.groupby(["main_feature"])
    num = len(group)
    
    maxi_point = sum(df["point"])
    if (specific_maxi=="default") or (specific_maxi<maxi_point):
        specific_maxi = 50*(maxi_point//50+1)
        
    x_point, prob = compute_x(df=df, lm_intercept=lm_intercept, 
                              maxi_point=maxi_point, specific_maxi=specific_maxi)

    fig = plt.figure(figsize=(fig_width, single_height*(num+2+7)), dpi=dpi)  # 创建画布
    gs = gridspec.GridSpec(num+5, 1)
    
    xticklabels = []
    for i in np.linspace(0,total_point,51):
        if int(i) == i:
            xticklabels.append(int(i))
        else:
            xticklabels.append("")
    ax0 = fig.add_subplot(gs[0,:])
    set_axis(ax0, title="Point", min_point=0, max_point=total_point, total_point=total_point,
            xticks=np.linspace(0,1,51), xticklabels=xticklabels, ax_para=ax_para)

    feature = list(set(df["main_feature"]))
    
    for i in range(0, len(feature)):
        ax = fig.add_subplot(gs[i+1,:])
        title = str(feature[i]).replace("\\n","\n")
        
        d = group.get_group(feature[i])

        if d.shape[0] > 1:
            min_point = min(d["point"])
            max_point = max(d["point"])

            xticks = [point/total_point for point in d["point"].values]
            xticklabels = [str(i).replace("\\n", "\n") for i in d["sub_feature"]]

        elif d.shape[0] == 1:

#             maxi = int(d["max"])
#             mini = int(d["min"])
            maxi = float(d["max"])
            mini = float(d["min"])
            point = d["point"].values[0]
            range_ = maxi-mini
            
            xticks, xticklabels=generate_xtick(range_, type_=list(set(d["type"].values))[0],
                                               mini=mini, maxi=maxi,
                                               point=point, total_point=total_point)
            
            if d["coef"].values < 0:
                xticklabels.sort(reverse=True)
                
            if range_ > 10:
                xticklabels = [int(i) for i in xticklabels]
            else:
                xticklabels = [round(i,2) for i in xticklabels]
                
            min_point = 0
            max_point = d["point"].values[0]
            
        if list(set(d["type"].values))[0] == "nominal":
            ax_para["linestyle"] = "-."
        elif list(set(d["type"].values))[0] == "continuous":
            ax_para["linestyle"] = "-"
        elif list(set(d["type"].values))[0] == "ordinal":
            ax_para["linestyle"] = "-"

        set_axis(ax, title=title, min_point=min_point, max_point=max_point, 
             xticks=xticks, xticklabels=xticklabels, total_point=total_point, ax_para=ax_para)

        tick_num = int(np.ceil(max(xticks)/0.1))
        grid_connect(ax0, ax, xticks=np.linspace(0,0.1*tick_num,tick_num+1))
        
    ax_overallpoint = fig.add_subplot(gs[num+1, :])
    xticks, xticklabels = generate_xtick(range_=specific_maxi, type_="continuous",
                                         mini=0, maxi=specific_maxi,
                                         point=total_point, total_point=total_point)
    ax_para["linestyle"] = "-"
    xticklabels = [int(i) for i in xticklabels]
    set_axis(ax_overallpoint, title="Overall Point", min_point=0, max_point=specific_maxi,
            xticks=xticks, xticklabels=xticklabels, total_point=total_point, ax_para=ax_para)

    ax_prob = fig.add_subplot(gs[num+2:, :])
    plot_prob(ax_prob, title=result_title, x_point=x_point, prob=prob, 
              threshold=threshold, total_point=total_point)
    ax_prob.grid(color='b', ls = '-.', lw = 0.25, axis="both")

    fig.tight_layout()
    
    return fig
