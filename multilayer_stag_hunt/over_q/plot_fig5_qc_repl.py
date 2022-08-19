from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import constants as const
from constants import rules_names
from tools import rules_dicts

rule = const.REPLICATOR
k = 8
N = 1000
ds_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
q_c_list = [0.10344827586206896, 0.13793103448275862, 0.13793103448275862, 0.1724137931034483, 0.3103448275862069, 0.896551724137931, 0.9655172413793103, 0.9655172413793103, 1.0, 1.0]
q_c_fit_list = [0.08008008008008008, 0.1011011011011011, 0.12012012012012012, 0.15315315315315314, 0.1981981981981982, 0.24424424424424424, 0.3063063063063063, 0.4244244244244244, 0.5965965965965966, 0.8088088088088088]


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
plt.title("c", loc='left', fontweight='bold')

plt.tight_layout()
plt.savefig(f'plots/fig5_q_c_{rules_dicts[rule]}_k{k}.pdf')
plt.show()
plt.close()
