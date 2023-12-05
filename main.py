import matplotlib.pyplot as plt
import numpy as np
from kmodes.kmodes import KModes
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


class DataSet:
    """ Represents a data set with a name and a dictionary of categories. A DataSet represents a single question in the
    survey."""

    def __init__(self, name: str, categories: dict[str, list[bool]]):
        self.name = name
        self.categories = categories

    def __str__(self):
        return f'{self.name}: {self.categories}'

    def __repr__(self):
        return f'{self.name}: {self.categories}'

    def name_pretty(self) -> str:
        """ The display name of the data set, used as the diagram title. """
        return self.name.replace('_', ' ')


def contains_name_in_data_sets(data_sets: list[DataSet], name: str) -> bool:
    for data_set_ in data_sets:
        if data_set_.name == name:
            return True
    return False


def create_diagram(data_set: DataSet, cluster_assignments: np.ndarray = None):
    """ Create a diagram for a data set. If cluster_assignments is not None, the data points will be clustered"""
    # plt.style.use('_mpl-gallery-nogrid')

    # make data
    x = []

    # 1. Calculate the number of data points in each cluster and answer possibility
    if len(data_set.categories) != 1:

        if cluster_assignments is None:
            x.append([sum(data_set.categories[category]) for category in data_set.categories])
        else:
            for cluster_label in set(cluster_assignments):
                cluster_data = []
                for category in data_set.categories:
                    cluster_data.append([x for (i, x) in enumerate(data_set.categories[category]) if
                                         cluster_assignments[i] == cluster_label])
                    # print(data_set.categories[category])
                x.append([sum(category) for category in cluster_data])
        labels = data_set.categories.keys()
    else:
        if cluster_assignments is None:
            yes = sum(data_set.categories[list(data_set.categories.keys())[0]])
            no = len(data_set.categories[list(data_set.categories.keys())[0]]) - yes
            x.append([yes, no])
        else:
            for cluster_label in set(cluster_assignments):
                cluster_data = []
                for category in data_set.categories:
                    cluster_data.append([x for (i, x) in enumerate(data_set.categories[category]) if
                                         cluster_assignments[i] == cluster_label])
                    # print(data_set.categories[category])
                yes = sum(cluster_data[0])
                no = len(cluster_data[0]) - yes
                x.append([yes, no])
        labels = ['Ja', 'Nein']
    # colors = plt.get_cmap('Spectral')(np.linspace(0.2, 0.7, len(x)))

    # 2. Generate the diagram
    # plot
    fig, ax = plt.subplots()
    bottom = [0 for _ in range(len(x[0]))]
    count_points = count_data_points_in_clusters(cluster_assignments)
    # print(bottom)
    # print(x)
    for (i, bar) in enumerate(x):
        ax.bar(labels, bar, bottom=bottom, label=f'Cluster {i + 1}, n={count_points[i + 1]}')
        bottom = [bottom[j] + bar[j] for j in range(len(bar))]
    # ax.bar(labels, x, color=colors, bottom=)
    ax.set_ylabel('Anzahl Personen')

    plt.suptitle(data_set.name_pretty())
    plt.legend()
    plt.tight_layout()
    plt.show()
    # plt.savefig(f'diagrams\\3_clusters\\{data_set.name}.png')


def count_data_points_in_clusters(cluster_assignments: np.ndarray):
    """
    Count the number of data points in each cluster.

    Parameters:
    - cluster_assignments: numpy array or list
        Array containing the cluster assignments for each data point.

    Returns:
    - dict
        A dictionary where keys are cluster labels and values are the counts
        of data points in each cluster.
    """
    cluster_counts = {}

    for cluster_label in set(cluster_assignments):
        count = sum(1 for x in cluster_assignments if x == cluster_label)
        cluster_counts[cluster_label] = count

    return cluster_counts


if __name__ == '__main__':
    # 1. Read data from file
    data = open('Umfrage_Ergebnis.csv', 'r')
    lines = data.readlines()
    data.close()
    lines = [line.replace('\n', '') for line in lines]

    array = [line.split(',') for line in lines]

    for line in array[1:]:
        for value in line:
            assert value in ['0', '1']
    categories: dict[str, list[bool]] = {category: [] for category in array[0]}

    for line in array[1:]:
        for i, value in enumerate(line):
            categories[array[0][i]].append(value == '1')

    # 2. Split data into data sets by question
    set_list: list[DataSet] = []
    for dict_key in categories:
        split = dict_key.split('=')
        name = split[0]
        subcategory = split[1] if len(split) > 1 else name
        if not contains_name_in_data_sets(set_list, name):
            set_list.append(DataSet(name, {subcategory: categories[dict_key]}))

        else:
            for data_set in set_list:
                if data_set.name == name:
                    data_set.categories[subcategory] = categories[dict_key]

    # print(set_list)

    # 3. Create array of data points, but only one column per question, not one per answer possibility as in the
    # original
    dimensions = []
    for s in set_list:
        l = []
        values_list = list(s.categories.values())
        for i in range(len(values_list[0])):
            x = []
            for j in values_list:
                x.append(j[i])

            val = None
            for k in range(len(x)):
                if x[k]:
                    val = k
            if val is None:
                val = -1
            l.append(val)
        dimensions.append(l)

    data = list(d for d in dimensions)
    persons = []
    for i in range(len(data[0])):
        p = []
        for j in range(len(data)):
            p.append(data[j][i])
        persons.append(p)

    print(len(persons))
    print(len(persons[0]))

    persons = np.array([np.array(xi) for xi in persons])

    # 4. Cluster data points with hierarchical clustering
    linkage_data = linkage(persons, method='ward', metric='euclidean', optimal_ordering=True)

    threshold = 10  # maximal variance within clusters
    # print(linkage_data)
    dendrogram(linkage_data, color_threshold=threshold)
    plt.tight_layout()
    plt.show()
    # plt.savefig('diagrams\\5_clusters\\dendrogram.png')

    # 5. Assign data points to clusters
    clusters = fcluster(linkage_data, criterion='distance', t=threshold)
    print("Data point assignments to clusters:")
    # print(clusters)

    print(count_data_points_in_clusters(clusters))

    for data_set in set_list:
        create_diagram(data_set, clusters)

    # biggest_cluster = max(count_data_points_in_clusters(clusters), key=count_data_points_in_clusters(clusters).get)
    # print(biggest_cluster)
    #
    # persons_biggest_cluster = np.array([p for (i, p) in enumerate(persons) if clusters[i] == biggest_cluster])
    # print(len(persons_biggest_cluster))
    #
    # km = KModes(n_clusters=1, init='Huang', n_init=5, verbose=1)
    #
    # clusters = km.fit_predict(persons_biggest_cluster)
    # km.labels_ = [i for i in persons]
    #
    # centroid = km.cluster_centroids_[0]
    # print(centroid)

    # for (i, p) in enumerate(persons):
    #     same = True
    #     canfail = True
    #     same_count = 0
    #     for j in range(len(p)):
    #         if p[j] != centroid[j]:
    #             if canfail:
    #                 canfail = False
    #             else:
    #                 same = False
    #         else:
    #             same_count += 1
    #     if same:
    #         print(i)