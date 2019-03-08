import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family']='simhei'
mpl.rcParams['axes.unicode_minus']=False # 处理负号问题
mpl.rcParams['font.size'] = 14.0



def make_bar_plot(x,y,title,color,xlabel,ylabel):
    def autolabel(rects, xpos='center'):
        xpos = xpos.lower()
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

    width=0.35
    fig, ax = plt.subplots(figsize=(20, 8), dpi=80)
    rects1 = ax.bar(range(len(x)), y, width, color=color)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)
    autolabel(rects1, "center")
    plt.show()

def bar_stack_plot(table,title,xlabel,ylabel):
    table.plot(kind='bar', stacked=True, figsize=(20, 8), fontsize=13, width=0.5, rot=0)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

#y,s 为位置
def show_normal_info(text,y,s):
    fig = plt.figure(figsize=(7.5,4.5),dpi=80)
    plt.axis([0, 30, 0, 75])
    plt.text(y,s,text, rotation=0, wrap=True, fontsize=18)
    plt.axis('off')
    plt.show()