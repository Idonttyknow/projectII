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
y =[0.0033756641619238584, 0.0035873924679107744, 0.003360011827241632, 0.003757562093713599, 0.0032831018746511706, 0.0032414280435388615, 0.003300308248790437, 0.003327631990522904, 0.003551741774166051, 0.003382034632034632, 0.003455329500221141, 0.003430084585885888, 0.0035044927597179584, 0.003316485586553641, 0.003470896532574364, 0.0032054569699456353, 0.003349881749174254, 0.003061830607283483, 0.0031916251755393847, 0.0032631111807241496, 0.0033259497249439576] 
fig, ax = plt.subplots(1, 1, figsize=(20, 12))
# ax=plt.plot(x, y,"r")
plt.plot(x[:5], y[:5], "r")
plt.plot(x[4:13], y[4:13], "b")
plt.plot(x[12:17], y[12:17], "g")
plt.plot(x[16:], y[16:], "c")
plt.xlabel("nodes to be removed ", labelpad=20)
plt.ylabel("the entanglement rate after removing ")
plt.title("SP 5_5 grid plot of the entanglement rate after removing the repeater from a node when p=0.7")
plt.xticks(x, x)
plt.ylim(0.002,0.006)
x1 = 0.14
for i in labels:
    img = mpimg.imread(f'images/5-5-{i[0]}-{i[1]}.png')
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

ax5 = fig.add_axes([0.72, 0.3
                       , 0.04, 0.04])
ax5.axison = False
plt.text(1, 0.055, "node inside grid", fontsize=15)

plt.savefig("SP_5_5_p=0.7.png", dpi=200)
