import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np

labels = [(4, 4),(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(1, 4),(2, 4),(1, 3),(2, 3),(3, 3),(1, 2),(2, 2),(1, 1),(4, 3)]

x = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [0.5186721991701245, 0.5112474437627812, 0.390625, 0.4537205081669691, 0.4340277777777778, 0.5107252298263534, 0.4424778761061947, 0.5117707267144319, 0.4549590536851683, 0.5336179295624333, 0.5405405405405406, 0.45454545454545453, 0.48638132295719844, 0.40387722132471726, 0.5213764337851929]
# ax=plt.plot(x, y,"r")
fig, ax = plt.subplots(1, 1, figsize=(20, 12))
plt.plot(x,y)
plt.xlabel("nodes to be removed ", labelpad=20)
plt.ylabel("the entanglement rate after removing ")
plt.title("MPG 9_9 grid plot of the entanglement rate after removing the repeater from a node when p=0.7")
plt.xticks(x, x)
x1 = 0.14
for i in labels:
    img = mpimg.imread(f'images2/9-9-{i[0]}-{i[1]}.png')
    #     img=mpimg.imread(f'images1/img.png')

    ax1 = fig.add_axes([x1, 0.082, 0.05, 0.05])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.0497
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
plt.savefig("MPCplot_9_9_p=0.7.png", dpi=200)
