from matplotlib import pyplot as plt

import constants as const
from constants import rules_names
from tools import rules_dicts

# rule = const.REPLICATOR
# k = 8
# N = 1000
# ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
# q_c_list = [0.20689655172413793, 0.20689655172413793, 0.20689655172413793, 0.24137931034482757, 0.24137931034482757, 0.24137931034482757, 0.27586206896551724, 0.27586206896551724, 0.27586206896551724, 0.3103448275862069]
# q_c_fit_list = [0.17217217217217218, 0.20020020020020018, 0.2012012012012012, 0.21921921921921922, 0.23923923923923923, 0.23323323323323322, 0.25325325325325326, 0.26726726726726724, 0.2602602602602603, 0.28428428428428426]

rule = const.BEST_RESPONSE
k = 8
N = 1000
ds_list = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
q_c_list = [0.5517241379310345, 0.5517241379310345, 0.5517241379310345, 0.5517241379310345, 0.48275862068965514, 0.48275862068965514, 0.8275862068965517, 0.8275862068965517, 0.8275862068965517, 0.8275862068965517]
q_c_fit_list = [0.5725725725725725, 0.5665665665665666, 0.5625625625625625, 0.48848848848848847, 0.42042042042042044, 0.4624624624624625, 0.8078078078078078, 0.8078078078078078, 0.8088088088088088, 0.8078078078078078]

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
