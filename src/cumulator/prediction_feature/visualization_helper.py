import matplotlib.pyplot as plt


def scatterplot(consumption_costs, scores):
    """
    Show the results of the prediction tool.
    Order of algorithms in the 4 lists: Linear, Decision tree, Random forest, Neural network
    Parameters
    ----------
    computation_costs List of estimated consumption costs.
    scores List of estimated f1 scores.
    """
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)

    colors = ['r', 'g', 'b', 'y']
    algorithms = ['Linear', 'Decision tree', 'Random forest', 'Neural network']
    for i in range(4):
        ax.scatter(x=consumption_costs[i], y=scores[i], label=algorithms[i], color=colors[i])


    # set the limit of the axes to -3,3 both on x and y
    ax.set_xlim(0, 1.1 * max(consumption_costs))
    ax.set_ylim(0, 1)
    ax.set_xlabel('Consumption (mgCO2eq)')
    ax.set_ylabel('F1')
    ax.legend(loc='lower right')
    plt.show()