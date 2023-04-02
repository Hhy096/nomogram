import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import gridspec
from matplotlib.transforms import (Bbox, TransformedBbox)
from mpl_toolkits.axes_grid1.inset_locator import (BboxConnector)


def generate_df_rank(path, total_point=100):
    
    df = pd.read_excel(path)
    
    df.index = df["feature"].values
    
    intercept = df.loc["intercept","coef"]
    threshold = df.loc["threshold","coef"]
    
    df = df.drop(index=["intercept", "threshold"])
    
    df = df.reset_index()
    
    df["sequence"] = list(range(0,df.shape[0]))
    
    df["range*coef"] = df["coef"]*(df["max"]-df["min"])
    df["abs_range*coef"] = abs(df["range*coef"])
    df = df.sort_values(by = "abs_range*coef", ascending = False)

    point = list(df["abs_range*coef"]/df["abs_range*coef"].shift(1))
    point[0] = 1
    point = total_point*np.cumprod(point)
    df["point"] = point
    
    df["negative_coef"] = np.minimum(df["coef"],0)
    df["positive_coef"] = np.maximum(df["coef"],0)
    
    df = df.sort_values(by = "sequence", ascending=True)
    
    return df, intercept, threshold


def compute_x(df, lm_intercept, total_point, maxi_point, mini_point=0):

    mini_score = sum(df["negative_coef"]*df["max"])+sum(df["positive_coef"]*df["min"])+lm_intercept
    maxi_score = sum(df["negative_coef"]*df["min"])+sum(df["positive_coef"]*df["max"])+lm_intercept
    
    coef = (maxi_score-mini_score)/maxi_point
    
    score = np.linspace(mini_score, maxi_score, 500)
    prob = 1/(1+np.exp(-score))

    x_point = np.linspace(0, 1, 500)
    
    label = np.linspace(mini_point, maxi_point, 500)
    
    flag = (prob<=0.99) & (prob>=0.01)

    
    mini_overallpoint = label[flag][0]//(total_point/2)*(total_point/2)
    maxi_overallpoint = (label[flag][-1]//(total_point/2)+1)*(total_point/2)
    
    score = np.linspace(coef*mini_overallpoint+mini_score, coef*maxi_overallpoint+mini_score, 500)
    prob = 1/(1+np.exp(-score))
      
    return mini_overallpoint, maxi_overallpoint, x_point+0.02, prob
    

def set_axis(ax, title, min_point, max_point, xticks, xticklabels, position, total_point, type_,
             ax_para = {"c":"black", "linewidth":1, "linestyle": "-"},
            #  tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             xtick_para = {"fontsize": 8,"fontfamily": "Times New Roman", 
                           "fontweight": "bold"},
             ylabel_para = {"fontsize": 10, "fontname": "Songti Sc", "labelpad":140,
                            "loc": "center", "color": "black", "rotation":"horizontal"}):
    ax.set_xlim(0, 1.1)

    ax.axhline(0.6, xmin=(min_point/total_point+0.02)/1.1, 
               xmax=(max_point/total_point+0.02)/1.1, **ax_para)

    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    for i in range(0,len(xticks)):
        ax.axvline(xticks[i]+0.02, ymin=0.6-0.2, ymax=0.6, **ax_para)
        
        if position[i] == "up":
            ax.annotate(xticklabels[i], xy=(xticks[i]+0.02, 0.75), horizontalalignment="center",
                       **xtick_para)
        else:
            ax.annotate(xticklabels[i], xy=(xticks[i]+0.02, 0), horizontalalignment="center",
                       **xtick_para)
        if i == len(xticks)-1:
            continue
        if type_ != 'continuous':
            continue
        if abs(xticks[i+1]-xticks[i]) > 0.07:
            for j in np.linspace(xticks[i], xticks[i+1], 6):
                ax.axvline(j+0.02, ymin=0.6-0.1, ymax=0.6, **ax_para)
        elif abs(xticks[i+1]-xticks[i]) > 0.025:
            for j in np.linspace(xticks[i], xticks[i+1], 3):
                ax.axvline(j+0.02, ymin=0.6-0.1, ymax=0.6, **ax_para)

    ax.set_ylabel(title, **ylabel_para)
    
    
def plot_prob(ax, title, x_point, prob, threshold=None,
             ax_para = {"c":"black", "linewidth":1, "linestyle": "-"},
             threshold_para = {"c":"g", "linewidth":1, "linestyle": "-."},
             tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             text_para = {"fontsize": 10,"fontfamily": "Songti Sc", "fontweight": "bold"},
             xtick_para = {"fontsize": 8,"fontfamily": "Times New Roman", "fontweight": "bold"},
             ylabel_para = {"fontsize": 10, "fontname": "Songti Sc", "labelpad":100,
                            "loc": "bottom", "color": "black", "rotation":"horizontal"},
             total_point=100):

    ax.spines['right'].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim([0,1.1])
    ax.set_ylim([-0.5, 0.5])
    
    ax.plot(x_point, -prob+0.5, **ax_para)
    
    if threshold != None:
        ax.axhline(-threshold+0.5, xmin=0, xmax=1, **threshold_para)
        ax.text(x=1.05, y=-threshold+0.5, s="threshold={}".format(threshold), **text_para,
                bbox=dict(facecolor='black', alpha=0.2))

    ax.tick_params(**tick_para)
    
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_xticklabels(['','','','','',''])
    ax.set_yticks([0.5, 0.3, 0.1, -0.1, -0.3, -0.5])  
    ax.set_yticklabels([0,0.2,0.4,0.6,0.8,1], **xtick_para)
    
    ax.set_ylabel(ylabel=title, **ylabel_para)
    
    
def grid_connect(ax1, ax2, xticks, 
                 prop_lines={"lw": 0.5, "color": "b", "linestyle": "-."}, **kwargs):
    
    for xtick in xticks:
        bbox = Bbox.from_extents(xtick+0.02, 0.02, xtick+0.02, 1.02)
        
        bbox1 = TransformedBbox(bbox, ax1.get_xaxis_transform())
        bbox2 = TransformedBbox(bbox, ax2.get_xaxis_transform())
    
        c = BboxConnector(
            bbox1, bbox2, loc1=3, loc2=3, clip_on=False, **prop_lines)
        
        ax2.add_patch(c)
        
    return c


def generate_xtick(range_, type_, mini, maxi, point, total_point):
    ran = point/total_point
    
    if type_ in ["nominal", "ordinal"]:
        range_ = int(range_)
        if (ran<=0.1) and (range_>=3):
            xticks = list(np.linspace(0, point/total_point, 3))
            xticklabels = list(np.linspace(mini, maxi, 3))
            xticklabels = [int(i) for i in xticklabels]
        else:
            xticks = list(np.linspace(0, point/total_point, range_+1))
            xticklabels = list(range(int(mini), int(maxi)+1, 1))
    elif (0.1<=ran<0.25) or (range_<2):
        xticks = list(np.linspace(0, point/total_point, 5))
        xticklabels = list(np.linspace(mini, maxi, 5))
    elif (ran<0.1):
        xticks = list(np.linspace(0, point/total_point, 2))
        xticklabels = list(np.linspace(mini, maxi, 2))
    elif (range_<= 11):
        range_ = int(range_)
        xticks = list(np.linspace(0, point/total_point, range_+1))
        xticklabels = list(range(int(mini), int(maxi)+1, 1))
    elif range_ <= 150:
        if (range_%10 == 0) and (ran/(range_/5+1) < 0.07):
            num = int(range_/10)
            xticks = list(np.linspace(0, point/total_point, num+1))
            xticklabels = list(np.linspace(int(mini), int(maxi), num+1))
        elif range_%5 == 0:
            num = int(range_/5)
            xticks = list(np.linspace(0, point/total_point, num+1))
            xticklabels = list(np.linspace(int(mini), int(maxi), num+1))
        else:
            xticks = list(np.linspace(0, point/total_point, 6))
            xticklabels = list(np.linspace(int(mini), int(maxi), 6))
    elif range_ <= 200:
        if range_%10 == 0:
            num = range_/10
            xticks = list(np.linspace(0, point/total_point, num))
            xticklabels = list(np.linspace(int(mini), int(maxi), num))
        else:
            num = int((maxi-mini)//10+1)
            xticks = list(np.linspace(0, point/total_point, num))
            xticklabels = list(np.linspace(mini, maxi, num))
    else:
        num = int((maxi-mini)//50+1)
        xticks = list(np.linspace(0, point/total_point, num))
        xticklabels = [int(i) for i in list(np.linspace(mini, maxi, num))]
    
    position = ['down' for i in xticks]
        
    return xticks, xticklabels, position



def nomogram(path, result_title="Positive Risk", fig_width=10, single_height=0.45, dpi=100,
             ax_para = {"c":"black", "linewidth":1.3, "linestyle": "-"},
             tick_para = {"direction": 'in',"length": 3, "width": 1.5,},
             xtick_para = {"fontsize": 10,"fontfamily": "Songti Sc", "fontweight": "bold"},
             ylabel_para = {"fontsize": 12, "fontname": "Songti Sc", "labelpad":100,
                            "loc": "center", "color": "black", "rotation":"horizontal"},
             total_point=100):
    
    df, lm_intercept, threshold = generate_df_rank(path=path, total_point=total_point)
    new = df["feature"].str.split(pat="_", expand=True)
    
    if new.shape[1] == 1:
        df["main_feature"] = new[0]
    else:
        df["main_feature"] = new[0]
        df["sub_feature"] = new[1]
        
    group = df.groupby(["main_feature"], sort=False)
    num = len(group)
    
    maxi_point = sum(df["point"])
    # if (specific_maxi=="default") or (specific_maxi<maxi_point):
    #     specific_maxi = (total_point/2)*(maxi_point//(total_point/2)+1)
        
    mini_overallpoint, maxi_overallpoint, x_point, prob = compute_x(df=df, lm_intercept=lm_intercept, 
                                                                    total_point=total_point,
                              maxi_point=maxi_point)

    fig = plt.figure(figsize=(fig_width, single_height*(num+2+7)), dpi=dpi)  # 创建画布
    gs = gridspec.GridSpec(num+5, 1)
    
    xticklabels = []
    labels = np.linspace(0, total_point, 11)
    for i in range(0,11):
        if i%1 == 0:
            xticklabels.append(int(labels[i]))
        else:
            xticklabels.append("")
            
    position = ["done" for i in xticklabels]

    ax0 = fig.add_subplot(gs[0,:])
    set_axis(ax0, title="Point", min_point=0, max_point=total_point, position=position, 
             total_point=total_point, xticks=np.linspace(0,1,11), xticklabels=xticklabels, 
             type_='continuous', ax_para=ax_para, xtick_para=xtick_para, ylabel_para=ylabel_para)
    
    main_feature = list(df["main_feature"])
    feature = list(set(main_feature))
    feature.sort(key=main_feature.index)
    
    for i in range(0, len(feature)):
        ax = fig.add_subplot(gs[i+1,:])
        title = str(feature[i]).replace("\\n","\n")
        
        d = group.get_group(feature[i])

        if d.shape[0] > 1:
            min_point = min(d["point"])
            max_point = max(d["point"])

            xticks = [point/total_point for point in d["point"].values]
            xticklabels = [str(i).replace("\\n", "\n") for i in d["sub_feature"]]
            position = [i for i in d["position"].values]

        elif d.shape[0] == 1:

            maxi = float(d["max"])
            mini = float(d["min"])
            point = d["point"].values[0]
            range_ = maxi-mini
            
            xticks, xticklabels, position=generate_xtick(range_, type_=list(set(d["type"].values))[0],
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
        elif list(set(d["type"].values))[0] == "ordinal":
            ax_para["linestyle"] = "-"
        elif list(set(d["type"].values))[0] == "continuous":
             ax_para["linestyle"] = "-"
        elif list(set(d["type"].values))[0] == "discrete":
             ax_para["linestyle"] = "-"

        set_axis(ax, title=title, min_point=min_point, max_point=max_point, 
             xticks=xticks, xticklabels=xticklabels, position=position,
             total_point=total_point, ax_para=ax_para, type_= list(set(d["type"].values))[0],
             xtick_para=xtick_para, ylabel_para=ylabel_para)

        tick_num = int(np.ceil(max(xticks)/0.1))
        grid_connect(ax0, ax, xticks=np.linspace(0,0.1*tick_num,tick_num+1))
        
    ax_overallpoint = fig.add_subplot(gs[num+1, :])
    
    xticklabels = []
    
    xticks, xticklabels, position=generate_xtick(maxi_overallpoint-mini_overallpoint,
                                       type_="continuous",
                                       mini=mini_overallpoint, 
                                       maxi=maxi_overallpoint,
                                       point=maxi_overallpoint, 
                                       total_point=maxi_overallpoint)

    ax_para["linestyle"] = "-"

    set_axis(ax_overallpoint, title="Overall point", min_point=0, 
            max_point=maxi_overallpoint, position=position, type_="continuous",
            xticks=xticks, xticklabels=xticklabels, 
            total_point=maxi_overallpoint, ax_para=ax_para, xtick_para=xtick_para, ylabel_para=ylabel_para)

    ax_prob = fig.add_subplot(gs[num+2:, :])
    ylabel_para["loc"] = "center"
    plot_prob(ax_prob, title=result_title, x_point=x_point, prob=prob, tick_para=tick_para,
              threshold=threshold, total_point=total_point,ylabel_para=ylabel_para)
    ax_prob.grid(color='b', ls = '-.', lw = 0.25, axis="both")

    fig.tight_layout()
    
    return fig
