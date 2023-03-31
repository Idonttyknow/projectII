import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np

labels = [(2, 2), (0, 0), (0, 4), (4, 4), (4, 0), (1, 0), (0, 1), (3, 0), (4, 1), (0, 3), (1, 4), (3, 4), (4, 3),
          (0, 2), (2, 0), (4, 2), (2, 4), (1, 1), (3, 1), (1, 3), (3, 3)]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [0.05863288521199587, 0.054764512595837894, 0.05167424555601488, 0.05763024435223606, 0.058983130824584167,
     0.038358347876672484, 0.04161118508655127, 0.04000960230455309, 0.038916959988506574, 0.03525098702763677,
     0.04217985490129914, 0.036502750275027504, 0.03835238168290251, 0.043155532539271534, 0.04261847937265598,
     0.040796344647519585, 0.03783006733751986, 0.038998160073597055, 0.024108003857280617, 0.03208418891170431,
     0.03718854592785422]

y_2 = [0.0002035673136035893, 0.00019287953065980873, 0.0002095191535426197, 0.00020005268053920866,
       0.0002084317594419587, 0.00011439666698784746, 9.578577815052719e-05, 0.00010931463017288529,
       9.622955690840442e-05, 0.00010472828827431054, 0.00010816987461732185, 8.73563932714471e-05,
       0.00011421466684961455, 0.00012495652554215514, 0.00013723677414898333, 0.00014282755714887632,
       0.00013067462193952606, 0.00010132153680454164, 6.912936068362309e-05, 8.211184974536947e-05,
       8.696431300828005e-05]
fig, ax = plt.subplots(1, 1, figsize=(30, 12))
# ax=plt.plot(x, y,"r")
ax.plot(x[:5], y[:5], "r", linestyle='-', label="central and corner p=0.7")
ax.plot(x[4:13], y[4:13], "b", linestyle='-', label="node connected to corner user p=0.7")
ax.plot(x[12:17], y[12:17], "g", linestyle='-', label="central position of edge p=0.7")
ax.plot(x[16:], y[16:], "c", linestyle='-', label="node inside grid p=0.7")
ax.plot([1, 5], [np.mean(y[:5]), np.mean(y[:5])], "b", linewidth=6.0, label="original ER when p=0.7")

ax.set_yticks([0.02, 0.03, 0.04, 0.05, 0.06])
ax.set_ylabel("the entanglement rate after removing ")
ax.set_yticklabels(['2*10⁻²', '3*10⁻²', '4*10⁻²', '5*10⁻²', '6*10⁻²'])

ax1 = ax.twinx()

ax1.plot(x[:5], y_2[:5], "r", linestyle='-.', label="central and corner p=0.45")
ax1.plot(x[4:13], y_2[4:13], "b", linestyle='-.', label="node connected to corner user p=0.45")
ax1.plot(x[12:17], y_2[12:17], "g", linestyle='-.', label="central position of edge p=0.45")
ax1.plot(x[16:], y_2[16:], "c", linestyle='-.', label="node inside grid p=0.45")
ax1.set_yticklabels(['1*10⁻⁴', '2*10⁻⁴', '3*10⁻⁴', '4*10⁻⁴'])
ax1.plot([1, 5], [np.mean(y_2[:5]), np.mean(y_2[:5])], "C2", linewidth=6.0, label="original ER when p=0.45")
plt.yticks([0.0001, 0.0002, 0.0003, 0.0004])

ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), prop={'family': 'SimHei', 'size': 18})
ax1.legend(loc='upper right', bbox_to_anchor=(1.0, 0.78), prop={'family': 'SimHei', 'size': 18})

ax.set_ylabel("p=0.7", size=20, rotation=360)
ax1.set_ylabel("p=0.45", size=20, rotation=360)

plt.xlabel("nodes to be removed ", labelpad=20)

plt.title("MPG_5_5grid plot of the entanglement rate after removing the repeater from a node when p=0.7 and p=0.45")
plt.xticks(x, x)
x1 = 0.14
for i in labels:
    img = mpimg.imread(f'project I/images/5-5-{i[0]}-{i[1]}.png')

    ax1 = fig.add_axes([x1, 0.082, 0.04, 0.04])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.03525

ax2 = fig.add_axes([0.14, 0.6
                       , 0.04, 0.04])
ax2.axison = False
plt.text(1, 0.055, "central and corner", fontsize=15)

ax3 = fig.add_axes([0.3, 0.3
                       , 0.04, 0.04])
ax3.axison = False
plt.text(1, 0.055, "node connected to corner user", fontsize=15)

ax4 = fig.add_axes([0.55, 0.35
                       , 0.04, 0.04])
ax4.axison = False
plt.text(1, 0.055, "central position of edge", fontsize=15)

ax5 = fig.add_axes([0.72, 0.2
                       , 0.04, 0.04])
ax5.axison = False
plt.text(1, 0.055, "node inside grid", fontsize=15)

plt.savefig("MPG_plot_5_5_p=0.7_and_p=0.5.png", dpi=200)

