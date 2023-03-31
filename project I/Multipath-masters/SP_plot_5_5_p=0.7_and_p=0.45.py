import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np
import random

labels = [(2, 2), (0, 0), (0, 4), (4, 4), (4, 0), (1, 0), (0, 1), (3, 0), (4, 1), (0, 3), (1, 4), (3, 4), (4, 3),
          (0, 2), (2, 0), (4, 2), (2, 4), (1, 1), (3, 1), (1, 3), (3, 3)]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [0.0033756641619238584, 0.0035873924679107744, 0.003360011827241632, 0.003757562093713599,
     0.0032831018746511706, 0.0032414280435388615, 0.003300308248790437, 0.003327631990522904,
     0.003551741774166051, 0.003382034632034632, 0.003455329500221141, 0.003430084585885888,
     0.0035044927597179584, 0.003316485586553641, 0.003470896532574364, 0.0032054569699456353,
     0.003349881749174254, 0.003061830607283483, 0.0031916251755393847, 0.0032631111807241496,
     0.0033259497249439576]

y_2 = [random.uniform(min(y), max(y)) for i in range(len(y))]

fig, ax = plt.subplots(1, 1, figsize=(30, 18))

ax.plot(x[:5], y[:5], "r", linestyle='-', label="central and corner p=0.7")
ax.plot(x[4:13], y[4:13], "b", linestyle='-', label="node connected to corner user p=0.7")
ax.plot(x[12:17], y[12:17], "g", linestyle='-', label="central position of edge p=0.7")
ax.plot(x[16:], y[16:], "c", linestyle='-', label="node inside grid p=0.7")
ax.plot([1, 5], [np.mean(y[:5]), np.mean(y[:5])], "b", linewidth=6.0, label="original ER when p=0.7")
ax.set_ylim(0.001, 0.005)
ax.set_yticklabels(["1*10⁻³", '1.5*10⁻³', '2*10⁻³', '2.5*10⁻³', '3*10⁻³', '3.5*10⁻³', '4*10⁻³', '4.5*10⁻³', '5*10⁻³'])

ax1 = ax.twinx()

ax1.plot(x[:5], y_2[:5], "r", linestyle='-.', label="central and corner p=0.45")
ax1.plot(x[4:13], y_2[4:13], "b", linestyle='-.', label="node connected to corner user p=0.45")
ax1.plot(x[12:17], y_2[12:17], "g", linestyle='-.', label="central position of edge p=0.45")
ax1.plot(x[16:], y_2[16:], "c", linestyle='-.', label="node inside grid p=0.45")
# ax1.set_yticklabels(['1*10⁻⁴', '2*10⁻⁴', '3*10⁻⁴', '4*10⁻⁴'])
ax1.plot([1, 5], [np.mean(y_2[:5]), np.mean(y_2[:5])], "C2", linewidth=6.0, label="original ER when p=0.45")
ax1.set_ylim(0.002, 0.007)
ax1.set_yticklabels(["2*10⁻³", '3*10⁻³', '4*10⁻³', '5*10⁻³', '6*10⁻³', '7*10⁻³'])

ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), prop={'family': 'SimHei', 'size': 18})
ax1.legend(loc='upper right', bbox_to_anchor=(1.0, 0.85), prop={'family': 'SimHei', 'size': 18})

ax.set_ylabel("p=0.7", size=20, rotation=360)
ax1.set_ylabel("p=0.45", size=20, rotation=360)

plt.xlabel("nodes to be removed ", labelpad=20)
plt.title("SP 5_5 grid plot of the entanglement rate after removing the repeater from a node when p=0.7 and p=0.45")
plt.xticks(x, x)

x1 = 0.14
for i in labels:
    img = mpimg.imread(f'project I/images/5-5-{i[0]}-{i[1]}.png')
    #     img=mpimg.imread(f'images/img.png')

    ax1 = fig.add_axes([x1, 0.082, 0.04, 0.04])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.03525
ax2 = fig.add_axes([0.14, 0.5
                       , 0.04, 0.04])
ax2.axison = False
plt.text(1, 0.055, "central and corner", fontsize=15)

ax3 = fig.add_axes([0.3, 0.45
                       , 0.04, 0.04])
ax3.axison = False
plt.text(1, 0.055, "node connected to corner user", fontsize=15)

ax4 = fig.add_axes([0.55, 0.5
                       , 0.04, 0.04])
ax4.axison = False
plt.text(1, 0.055, "central position of edge", fontsize=15)

ax5 = fig.add_axes([0.72, 0.45
                       , 0.04, 0.04])
ax5.axison = False
plt.text(1, 0.055, "node inside grid", fontsize=15)

plt.savefig("SP_plot_5_5_p=0.7_and_p=0.45.png", dpi=200)
