from matplotlib import pyplot as plt

import constants as const
from constants import rules_names
from tools import rules_dicts

# rule = const.BEST_RESPONSE
# k = 8
# N = 1000
# ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
# q_c_list = [0.5517241379310345, 0.5517241379310345, 0.8620689655172413, 0.8620689655172413, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# q_c_fit_list = [0.5635635635635635, 0.5695695695695696, 0.8338338338338338, 0.8418418418418419, 0.9879879879879879, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999, 0.98998998998999]

rule = const.REPLICATOR
k = 8
N = 1000
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
q_c_list = [0.20689655172413793, 0.24137931034482757, 0.27586206896551724, 0.3448275862068966, 0.3793103448275862, 0.4482758620689655, 0.7586206896551724, 0.9310344827586207, 1.0, 1.0]
q_c_fit_list = [0.19519519519519518, 0.22322322322322322, 0.25725725725725723, 0.3353353353353353, 0.36236236236236236, 0.42842842842842843, 0.49149149149149146, 0.6046046046046046, 0.8398398398398398, 1.0]


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

plt.xlabel(r'$\Delta T$')
plt.ylabel(r'$q_c$')
plt.title(f'{rules_names[rule]}, S=-2, N={N}, k={k}')

plt.tight_layout()
plt.savefig(f'plots/q_c_{rules_dicts[rule]}_k{k}.png')
plt.show()
plt.close()
