from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import constants as const
from constants import rules_names
from tools import rules_dicts

rule = const.BEST_RESPONSE
k = 8
N = 1000
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
q_c_list = [0.5517241379310345, 0.5517241379310345, 0.8620689655172413, 0.8620689655172413, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
q_c_fit_list = [0.5635635635635635, 0.5695695695695696, 0.8338338338338338, 0.8418418418418419, 0.9879879879879879, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999]


triple = []
for i in range(len(ds_list)):
    triple.append((ds_list[i], q_c_list[i], q_c_fit_list[i]))
triple.sort(key=lambda x: x[0])

ds_list = []
q_c_list = []
q_c_fit_list = []
for i in range(len(triple)):
    ds_list.append(triple[i][0])
    q_c_list.append(triple[i][1])
    q_c_fit_list.append(triple[i][2])

print('ds_list =', ds_list)
print('q_c_list =', q_c_list)
print('q_c_fit_list =', q_c_fit_list)


fig = plt.figure(figsize=(4.2, 3))

plt.scatter(ds_list, q_c_list, color=const.REDISH, label=r'$q_c$', marker='v')
plt.plot(ds_list, q_c_list, color=const.REDISH)
plt.scatter(ds_list, q_c_fit_list, color=const.BLUE, label=r'$q_c^{fit}$', marker='o')
plt.plot(ds_list, q_c_fit_list, color=const.BLUE)

legend_elements = [
        Line2D([0], [0], marker='v', color=const.REDISH, lw=1.3, label=r'$q_c$'),
        Line2D([0], [0], marker='o', color=const.BLUE, lw=1.3, label=r'$q_c^{fit}$')]
plt.legend(handles=legend_elements)

# plt.xlim([0, 4])
# plt.ylim([0, 1])

plt.xlabel(r'$\Delta S (= \Delta T)$')
plt.ylabel(r'$q_c$')
plt.title(f'{rules_names[rule]}')
plt.title("d", loc='left', fontweight='bold')

plt.tight_layout()
plt.savefig(f'plots/fig4_q_c_{rules_dicts[rule]}_k{k}.pdf')
plt.show()
plt.close()
