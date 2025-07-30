import copy

import subjective_logic as sl
import random
import numpy as np

import matplotlib.pyplot as plt
from alive_progress import alive_bar

plt.rcParams.update({
    'font.size': 8,
    'text.usetex': True,
    'text.latex.preamble': " ".join([
        r'\usepackage{amsmath}',
        r'\usepackage{amssymb}',
        r'\usepackage{amsfonts}',
    ])
})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


num_agents = 5
num_runs = 400
num_mc_runs = 100

switches = [
    num_runs // 4,
    num_runs * 2 // 4
]

colors = ['tab:green', 'tab:blue', 'tab:orange', 'tab:olive', 'tab:red', 'tab:purple', 'tab:orange', 'tab:cyan']
draw_divider = 1
triangle_divider = 15

default_true = sl.Opinion([0.9, 0.0], [0.5, 0.5])
default_false = sl.Opinion([0.0, 0.9], [0.5, 0.5])

reliabilities_start = [0.1, 0.1, 0.1, 0.9, 0.9]
# reliabilities_start = [0.1, 0.9, 0.9, 0.9, 0.9]
reliabilities_mid = [0.1, 0.1, 0.9, 0.9, 0.9]
reliabilities_end = [0.1, 0.1, 0.1, 0.9, 0.9]
# reliabilities_end = [0.7, 0.1, 0.7, 0.9, 0.9]

weighted_types_cs_avg = [
    (sl.TrustRevision.TrustRevisionType.REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.1),
    (sl.TrustRevision.TrustRevisionType.HARMONY_REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.08),
]

trusts = [[] for _ in range(num_agents)]

projections = np.zeros((num_mc_runs, num_agents, num_runs))
uncertainties = np.zeros((num_mc_runs, num_runs))
with alive_bar(num_mc_runs) as bar:
    for mc_run in range(num_mc_runs):
        trusted_opinions = [
            sl.TrustedOpinion(sl.Opinion([0.0, 0.0], [0.5, 0.5]), sl.Opinion(0, 0)) for _ in range(num_agents)
        ]
        for run in range(num_runs):

            if run < switches[0]:
                reliabilities = reliabilities_start
            elif run < switches[1]:
                reliabilities = reliabilities_mid
            else:
                reliabilities = reliabilities_end

            uncertainty_sum = 0
            event = random.choice([True, False])
            for idx in range(num_agents):
                if mc_run == 0:
                    trusts[idx].append(trusted_opinions[idx].trust_copy())

                projections[mc_run, idx, run] = trusted_opinions[idx].trust.getBinomialProjection()
                # projections[mc_run, idx, run] = trusted_opinions[idx].trust.getProbability()

                uncertainty_sum += trusted_opinions[idx].trust.uncertainty()

                trusted_opinions[idx].opinion = default_true
                if (reliabilities[idx] > np.random.uniform()) != event:
                    trusted_opinions[idx].opinion = default_false

            avg_uncertainty = uncertainty_sum / num_agents
            uncertainties[mc_run, run] = avg_uncertainty
            updated_weights = []
            for entry in weighted_types_cs_avg:
                updated_weights.append((
                    entry[0],
                    entry[1],
                    entry[2]
                    # entry[2] * avg_uncertainty,
                ))

            fusion_result, trusted_opinions = sl.TrustedFusion.fuse_opinions_(sl.Fusion.FusionType.CUMULATIVE,
                                                                              updated_weights, trusted_opinions)
            for t_op in trusted_opinions:
                t_op.trust.trust_discount_(0.995)
        bar()

median_projections = np.median(projections, axis=0)
q25_projections = np.quantile(projections, 0.25, axis=0)
q75_projections = np.quantile(projections, 0.75, axis=0)
print('median prob:',median_projections[:,-1])
median_avg_uncert_last = np.median(uncertainties[:,-1])
print('median avg uncert:',median_avg_uncert_last)

print('test:', (median_projections[:,-1] - 0.5 * median_avg_uncert_last) / (1 - median_avg_uncert_last))

plt.ylim(0,1)
for color, idx in zip(colors, range(num_agents)):
    # gt = [reliabilities_start[idx] for i in range(0, idx_switch, draw_divider)] + [reliabilities_switched[idx] for i in
    #                                                                                range(0, num_runs - idx_switch,
    #                                                                                      draw_divider)]
    # plt.plot(gt, color='tab:gray')
    # plt.plot(mean_projections[idx, ::draw_divider], color=color)
    plt.plot(median_projections[idx, ::draw_divider], color=color)
    plt.fill_between(
        range(0, num_runs // draw_divider),
        q75_projections[idx, ::draw_divider],
        q25_projections[idx, ::draw_divider],
        color='gray', alpha=0.5)

fig2, ax2 = sl.create_triangle_plot(('distrust','trust'))
for color, trust_list in zip(colors, trusts):
    # sl.reset_plot()
    # sl.create_triangle_plot()
    for idx, trust in enumerate(trust_list):
        if idx % triangle_divider != 0:
            continue
        sl.draw_point(trust, color=color, sizes=[100])

plt.show()

define_opinion_tikz_string = "\\defineOpinion[{prior}]{{{name}}}{{{belief}}}{{{disbelief}}}{{{uncertainty}}}"
tikz_filename_trust = "52-opinion_definitions_changing_rel.tex"
trust_file = open(tikz_filename_trust, 'w')

for s_idx, trust_list in enumerate(trusts):
    for idx, trust in enumerate(trust_list):
        if idx % triangle_divider != 0:
            continue
        name = 'T' + str(s_idx) + '_' + str(idx)
        trust_file.write(define_opinion_tikz_string.format(prior=0.5, name=name, belief=trust.belief(), disbelief=trust.disbelief(), uncertainty=trust.uncertainty()))
        trust_file.write('\n')
trust_file.close()

import pandas as pd

data = {'time': range(median_projections.shape[1])}
for idx in range(num_agents):
    data[str(idx) + '_median'] = median_projections[idx,:]
    data[str(idx) + '_upper'] = q75_projections[idx, :]
    data[str(idx) + '_lower'] = q25_projections[idx, :]

df = pd.DataFrame(data)
df.to_csv('52-exp_changing_parameter.csv', index=False)

