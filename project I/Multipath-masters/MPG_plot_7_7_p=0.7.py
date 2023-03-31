import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np

labels = [(3, 3),
          (0, 0),
(1, 0),

(1, 1),

(2, 2),

(2, 0),
(2, 1),(1, 3),

(0, 3)]

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [0.0785669390320553, 0.0638895987733197, 0.04460303300624442, 0.04791566842357451, 0.04720989519403267, 0.05755726948313572, 0.050226017076845805, 0.05114043162524292, 0.060496067755595885]
# ax=plt.plot(x, y,"r")
fig, ax = plt.subplots(1, 1, figsize=(20, 12))
plt.plot(x,y)
plt.xlabel("nodes to be removed ", labelpad=20)
plt.ylabel("the entanglement rate after removing ")
plt.title("MPG 7_7 grid plot of the entanglement rate after removing the repeater from a node when p=0.7")
plt.xticks(x, x)
x1 = 0.14
for i in labels:
    img = mpimg.imread(f'images1/7-7-{i[0]}-{i[1]}.png')
    #     img=mpimg.imread(f'images1/img.png')

    ax1 = fig.add_axes([x1, 0.082, 0.05, 0.05])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.087
'''
ax2 = fig.add_axes([0.14, 0.75
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

ax5 = fig.add_axes([0.72, 0.3
                       , 0.04, 0.04])
ax5.axison = False
plt.text(1, 0.055, "node inside grid", fontsize=15)
'''
plt.savefig("MPGplot_7_7_p=0.7.png", dpi=200)
