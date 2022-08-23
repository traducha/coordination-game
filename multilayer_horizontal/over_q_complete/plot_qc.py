from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import constants as const
from constants import rules_names
from tools import rules_dicts

rule = const.BEST_RESPONSE
k = 499
N = 500
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
q_c_list = [0.9310344827586207, 0.9655172413793103, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
q_c_fit_list = [0.9469469469469469, 0.9719719719719719, 0.984984984984985, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999]

# rule = const.REPLICATOR
# k = 499
# N = 500
# ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
# q_c_list = [0.27586206896551724, 0.3448275862068966, 0.48275862068965514, 0.5172413793103449, 0.5172413793103449, 0.6206896551724138, 0.6551724137931034, 0.7241379310344828, 0.8275862068965517, 1.0]
# q_c_fit_list = [0.3203203203203203, 0.3133133133133133, 0.3833833833833834, 0.4894894894894895, 0.5025025025025025, 0.5715715715715716, 0.6456456456456456, 0.7087087087087087, 0.8858858858858859, 0.992992992992993]


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


fig = plt.figure(figsize=(4, 3))

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

plt.xlabel(r'$\Delta S$')
plt.ylabel(r'$q_c$')
plt.title(f'{rules_names[rule]}, $N$={N}, $k$={k}')

plt.tight_layout()
plt.savefig(f'plots/q_c_{rules_dicts[rule]}_k{k}.png')
plt.show()
plt.close()
