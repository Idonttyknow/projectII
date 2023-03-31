import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np

labels = [(4, 4),(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(1, 4),(2, 4),(1, 3),(2, 3),(3, 3),(1, 2),(2, 2),(1, 1)]

x = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [2.931106786017412e-05, 0.00002670143311931838, 1.369069646647273e-05, 1.1907900193729218e-05, 2.108172880295414e-05, 0.0, 1.5753887790032183e-05, 1.895459910180473e-05, 2.5568515952197104e-05, 2.2979016753405363e-05, 2.416614094710922e-05, 1.9484012520595873e-05, 1.9761233840986816e-05, 2.257062369447041e-05]
# ax=plt.plot(x, y,"r")
fig, ax = plt.subplots(1, 1, figsize=(20, 12))
plt.plot(x,y)
plt.xlabel("nodes to be removed ", labelpad=20)
plt.ylabel("the entanglement rate after removing ")
plt.title("SP 9_9 grid plot of the entanglement rate after removing the repeater from a node when p=0.7")
plt.xticks(x, x)
x1 = 0.14
for i in labels:
    img = mpimg.imread(f'images2/9-9-{i[0]}-{i[1]}.png')
    #     img=mpimg.imread(f'images1/img.png')

    ax1 = fig.add_axes([x1, 0.082, 0.05, 0.05])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.0535
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
plt.savefig("SP_9_9_p=0.7.png", dpi=200)
