import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.image as mpimg
import pylab as pl
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
import numpy as np

labels = [(2, 2), (0, 0), (0, 4), (4, 4), (4, 0), (1, 0), (0, 1), (3, 0), (4, 1), (0, 3), (1, 4), (3, 4), (4, 3),
          (0, 2), (2, 0), (4, 2), (2, 4), (1, 1), (3, 1), (1, 3), (3, 3), (2, 1), (2, 3), (3, 2), (1, 2)]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
# y is the resultant entanglement rate when one repeater is removed from a node
y = [0.4921259842519685, 0.47664442326024786, 0.4616805170821791, 0.4508566275924256, 0.4821600771456123,
     0.32051282051282054, 0.3364737550471063, 0.3069367710251688, 0.3136762860727729, 0.36496350364963503,
     0.35410764872521244, 0.33266799733865604, 0.3162555344718533, 0.38109756097560976, 0.397456279809221,
     0.3834355828220859, 0.397456279809221, 0.3633720930232558, 0.37202380952380953, 0.3543586109142452,
     0.36683785766691124, 0.39184952978056425, 0.3943217665615142, 0.39588281868566905, 0.382262996941896]

y_2 = [0.012368889768454383, 0.011448983330280271, 0.011261007634963176, 0.012409103318194227, 0.011830959254176328,
       0.005875164504606129, 0.005859535221666217, 0.0062996094242156984, 0.005976071808478851, 0.0062402496099844,
       0.006233170439812506, 0.006141751627564181, 0.006109780536683122, 0.007546144674685703, 0.007564410959318598,
       0.007760721436664752, 0.007369196757553427, 0.005878549174063841, 0.006137303759712283, 0.00588914277637747,
       0.006064796283492838, 0.006241106423346731, 0.0063000856811652635, 0.006410749544836782, 0.005904303056067262]
fig, ax = plt.subplots(1, 1, figsize=(30, 12))
# ax=plt.plot(x, y,"r")
ax.plot(x[:5], y[:5], "r", label="central and corner p=0.7")
ax.plot(x[4:13], y[4:13], "b", label="node connected to corner user p=0.7")
ax.plot(x[12:17], y[12:17], "g", label="central position of edge p=0.7")
ax.plot(x[16:22], y[16:22], "c", label="node inside grid p=0.7")
ax.plot(x[21:], y[21:], '', label="node near the central node p=0.7")
ax.plot([1, 5], [np.mean(y[:5]),np.mean(y[:5])], "b", linewidth=6.0, label="original ER when p=0.7")

# ax.set_yticks([0.3, 0.4, 0.5, 0.6])
ax.set_ylim(0,0.6)
ax.set_yticklabels(["0","1*10⁻¹","2*10⁻¹","3*10⁻¹", '4*10⁻¹', '5*10⁻¹', '6*10⁻¹'])



ax1 = ax.twinx()
ax1.plot(x[:5], y_2[:5], "r", linestyle="-.", label="central and corner p=0.45")
ax1.plot(x[4:13], y_2[4:13], "b", linestyle="-.", label="node connected to corner user p=0.45")
ax1.plot(x[12:17], y_2[12:17], "g", linestyle="-.", label="central position of edge p=0.45")
ax1.plot(x[16:22], y_2[16:22], "c", linestyle="-.", label="node inside grid p=0.45")
ax1.plot(x[21:], y_2[21:], '', linestyle="-.", label="node near the central node p=0.45")
ax1.plot([1, 5], [np.mean(y_2[:5]),np.mean(y_2[:5])], "C2", linewidth=6.0, label="original ER when p=0.45")
ax1.set_yticklabels(['2*10⁻³', '4*10⁻³', '6*10⁻³', '8*10⁻³','1*10⁻²','1.2*10⁻²','1.4*10⁻²','1.6*10⁻²','1.8*10⁻²','2*10⁻²'])


ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0),prop={'family':'SimHei','size':18})
ax1.legend(loc='upper right', bbox_to_anchor=(0.75, 1.0),prop={'family':'SimHei','size':18})


ax.set_ylabel("p=0.7", size=20, rotation=360)
ax1.set_ylabel("p=0.45", size=20, rotation=360)
ax1.set_ylim(0.002,0.02)

plt.xlabel("nodes to be removed ", labelpad=20)
plt.title("MPC 5_5 grid plot of the entanglement rate after removing the repeater from a node when p=0.7 and p=0.45")
plt.xticks(x, x)

x1 = 0.14
for i in labels:
    img = mpimg.imread(f'project I/images/5-5-{i[0]}-{i[1]}.png')
    #     img=mpimg.imread(f'images/img.png')

    ax1 = fig.add_axes([x1, 0.082, 0.04, 0.04])

    ax1.axison = False
    imgplot = ax1.imshow(img)
    x1 += 0.0295
ax2 = fig.add_axes([0.14, 0.65
                       , 0.04, 0.04])
ax2.axison = False
plt.text(1, 0.055, "central and corner", fontsize=15)

ax3 = fig.add_axes([0.3, 0.35
                       , 0.04, 0.04])
ax3.axison = False
plt.text(1, 0.055, "node connected to corner user", fontsize=15)

ax4 = fig.add_axes([0.5, 0.45
                       , 0.04, 0.04])
ax4.axison = False
plt.text(1, 0.055, "central position of edge", fontsize=15)

ax5 = fig.add_axes([0.62, 0.42
                       , 0.04, 0.04])
ax5.axison = False
plt.text(1, 0.055, "node inside grid", fontsize=15)

ax6 = fig.add_axes([0.75, 0.38
                       , 0.04, 0.04])
ax6.axison = False
plt.text(1, 0.055, "node near the central node", fontsize=15)


plt.savefig("MPC_plot_5_5_p=0.7_and_p=0.45.png", dpi=200)
