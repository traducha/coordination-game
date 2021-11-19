from matplotlib import pyplot as plt

import constants as const
from constants import rules_names
from tools import rules_dicts

# !!!!!!!RD OLD (WRONG)!!!!!!!!!
# rule = const.REPLICATOR
# k = 8
# N = 1000
# ds_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# q_c_list = [0.10344827586206896, 0.10344827586206896, 0.13793103448275862, 0.1724137931034483, 0.24137931034482757, 0.7241379310344828, 0.7586206896551724, 0.9310344827586207, 1.0, 1.0]
# q_c_fit_list = [0.08108108108108109, 0.08208208208208208, 0.12312312312312312, 0.15715715715715717, 0.19019019019019018, 0.23123123123123124, 0.29429429429429427, 0.42342342342342343, 0.6286286286286287, 0.8848848848848849]

rule = const.REPLICATOR
k = 8
N = 1000
ds_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
q_c_list = [0.10344827586206896, 0.13793103448275862, 0.13793103448275862, 0.1724137931034483, 0.3103448275862069, 0.896551724137931, 0.9655172413793103, 0.9655172413793103, 1.0, 1.0]
q_c_fit_list = [0.08008008008008008, 0.1011011011011011, 0.12012012012012012, 0.15315315315315314, 0.1981981981981982, 0.24424424424424424, 0.3063063063063063, 0.4244244244244244, 0.5965965965965966, 0.8088088088088088]

# rule = const.BEST_RESPONSE
# k = 8
# N = 1000
# ds_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# q_c_list = [0.5517241379310345, 0.5517241379310345, 0.8620689655172413, 0.8620689655172413, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# q_c_fit_list = [0.5705705705705706, 0.5445445445445445, 0.8418418418418419, 0.8318318318318318, 0.9879879879879879, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999]

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

plt.scatter(ds_list, q_c_list, color=const.REDISH, label='first 0')
plt.plot(ds_list, q_c_list, color=const.REDISH)
plt.scatter(ds_list, q_c_fit_list, color=const.BLUE, label='fitted')
plt.plot(ds_list, q_c_fit_list, color=const.BLUE)
plt.legend()

# plt.xlim([0, 4])
# plt.ylim([0, 1])

plt.xlabel(r'$\Delta S$')
plt.ylabel(r'$q_c$')
plt.title(f'{rules_names[rule]}, T=-1, N={N}, k={k}')

plt.tight_layout()
plt.savefig(f'plots/q_c_{rules_dicts[rule]}_k{k}.png')
plt.show()
plt.close()
