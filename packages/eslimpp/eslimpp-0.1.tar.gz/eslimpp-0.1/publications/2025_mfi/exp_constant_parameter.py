import copy

import subjective_logic as sl
import random
import numpy as np

import matplotlib.pyplot as plt
from alive_progress import alive_bar

# plt.rcParams.update({
#     'font.size': 8,
#     'text.usetex': True,
#     'text.latex.preamble': " ".join([
#         r'\usepackage{amsmath}',
#         r'\usepackage{amssymb}',
#         r'\usepackage{amsfonts}',
#     ])
# })
# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')

test_uncertain = 0.2

num_agents = 5
num_runs = 1000
num_mc_runs = 50

switches = [
]

colors = ['tab:green', 'tab:blue', 'tab:orange', 'tab:olive', 'tab:red', 'tab:purple', 'tab:orange', 'tab:cyan']
draw_divider = 1
triangle_divider = 15

opinion_dimension = 10
default_opinions = []
for i in range(opinion_dimension):
    belief_masses = [0.0] * opinion_dimension
    belief_masses[i] = 0.9
    prior = [1 / opinion_dimension] * opinion_dimension
    prior[0] = prior[0] - 0.1
    prior[-1] = prior[-1] + 0.1
    default_opinions.append(sl.Opinion(belief_masses, prior))
uncertain_opinion = sl.Opinion(*[0.]*opinion_dimension)


reliabilities = [0.1, 0.4, 0.7, 0.9, 0.9]

weighted_types_cs_avg = [
    # (sl.TrustRevision.TrustRevisionType.REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.1),
    # (sl.TrustRevision.TrustRevisionType.HARMONY_REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.066),
    (sl.TrustRevision.TrustRevisionType.REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.1),
    (sl.TrustRevision.TrustRevisionType.HARMONY_REFERENCE_FUSION, sl.Conflict.ConflictType.BELIEF_AVERAGE, 0.09),
]

trusts = [[] for _ in range(num_agents)]

projections = np.zeros((num_mc_runs, num_agents, num_runs))
with alive_bar(num_mc_runs) as bar:
    for mc_run in range(num_mc_runs):
        trusted_opinions = [
            sl.TrustedOpinion(sl.Opinion([0, 0], [0.5, 0.5]), uncertain_opinion) for _ in range(num_agents)
        ]
        for run in range(num_runs):

            uncertainty_sum = 0
            possible_events = list(range(opinion_dimension))
            event = random.choice(possible_events)
            for idx in range(num_agents):
                if mc_run == 0:
                    trusts[idx].append(trusted_opinions[idx].trust_copy())

                projections[mc_run, idx, run] = trusted_opinions[idx].trust.getBinomialProjection()

                uncertainty_sum += trusted_opinions[idx].trust.uncertainty()

                if reliabilities[idx] > np.random.uniform():
                    trusted_opinions[idx].opinion = default_opinions[event]
                else:
                    # other_events = copy.copy(possible_events)
                    # other_events.remove(event)
                    # unreliable_event = random.choice(other_events)
                    # trusted_opinions[idx].opinion = default_opinions[unreliable_event]
                    # trusted_opinions[idx].opinion.trust_discount_(0.95)
                    trusted_opinions[idx].opinion = default_opinions[(event+1)%opinion_dimension]

                if np.random.uniform() < test_uncertain:
                    trusted_opinions[idx].opinion = uncertain_opinion
                    # trusted_opinions[idx].opinion = default_opinions[random.choice(possible_events)]

            avg_uncertainty = uncertainty_sum / num_agents
            updated_weights = []
            for entry in weighted_types_cs_avg:
                updated_weights.append((
                    entry[0],
                    entry[1],
                    entry[2] * avg_uncertainty,
                    # entry[2],
                ))

            fusion_result, trusted_opinions = sl.TrustedFusion.fuse_opinions_(sl.Fusion.FusionType.CUMULATIVE,
                                                                              updated_weights, trusted_opinions)
        bar()

median_projections = np.median(projections, axis=0)
print(median_projections[:,-1])
q25_projections = np.quantile(projections, 0.25, axis=0)
q75_projections = np.quantile(projections, 0.75, axis=0)

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

# fig2, ax2 = sl.create_triangle_plot(('distrust','trust'))
# for color, trust_list in zip(colors, trusts):
#     # sl.reset_plot()
#     # sl.create_triangle_plot()
#     for idx, trust in enumerate(trust_list):
#         if idx % triangle_divider != 0:
#             continue
#         sl.draw_point(trust, color=color, sizes=[100])
#
plt.show()

# export_args = {
#     "format": 'pdf',
#     "dpi": 500,
#     "transparent": True,
#     "bbox_inches": 'tight',
#     "pad_inches": 0,
# }
# fig2.savefig("04-constant_parameter_triangle.pdf", **export_args)
#
# import pandas as pd
#
# data = {'time': range(median_projections.shape[1])}
# for idx in range(num_agents):
#     data[str(idx) + '_median'] = median_projections[idx,:]
#     data[str(idx) + '_upper'] = q75_projections[idx, :]
#     data[str(idx) + '_lower'] = q25_projections[idx, :]
#
# df = pd.DataFrame(data)
# df.to_csv('04-exp_constant_parameter.csv', index=False)
#
