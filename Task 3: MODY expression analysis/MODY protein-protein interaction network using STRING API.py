import pandas as pd
import networkx as nx
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Import MD gene file and convert to list format
Input_df = pd.read_table('MD_genes_new.txt', header=None)
Input_df_to_List = Input_df.values.tolist()
protein_list = [item for sublist in Input_df_to_List for item in sublist]

# first get list of mody target and interactive proteins
MODY_genes = []
def MODY_NETWORK(MODY_List):
    Interaction_DF = []
    for protein in MODY_List:
        proteins = '%0d'.join(protein)
        url = 'https://string-db.org/api/tsv/network?identifiers=' + proteins + '&species=9606'
        r = requests.get(url)
        lines = r.text.split('\n')
        data = [l.split('\t') for l in lines]
        df2 = pd.DataFrame(data[1:-1], columns=data[0])
        interactions = df2[['preferredName_A', 'preferredName_B', 'score']]
        Interaction_DF.append(interactions)

    # Build network with weights using Networkx
    G = nx.Graph(name='Protein Interaction Graph')
    Network_DF = pd.concat(Interaction_DF)
    Neonatal_and_MODY_Network_DF = np.array(Network_DF)
    for i in range(len(Neonatal_and_MODY_Network_DF)):
        interaction = Neonatal_and_MODY_Network_DF[i]
        a = interaction[0]  # protein a node
        b = interaction[1]  # protein b node
        w = float(interaction[2])  # score
        G.add_weighted_edges_from([(a, b, w)])

    print('nodes: ', len(G.nodes))

    return G.nodes

def Decoy_Network_with_MODY_network(Decoy_Variant_Files):
    mody = MODY_NETWORK(Input_df_to_List)
    stem_cells = Decoy_Variant_Files
    similarity = [x for x in stem_cells if x in mody]
    print('similarity: ', similarity)
    print(len(similarity))
    print(mody)
    print(len(mody))
    print(stem_cells)
    print(len(stem_cells))
    with open(r'RFProteinIDs', 'w') as fp:
        for item in similarity:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')

    Interaction_DF = []

    proteins = '%0d'.join(similarity)
    url = 'https://string-db.org/api/tsv/network?identifiers=' + proteins + '&species=9606'
    r = requests.get(url)
    lines = r.text.split('\n')
    data = [l.split('\t') for l in lines]
    df2 = pd.DataFrame(data[1:-1], columns=data[0])
    interactions = df2[['preferredName_A', 'preferredName_B', 'score']]
    Interaction_DF.append(interactions)

    # Build network with weights using Networkx
    G = nx.Graph(name='Protein Interaction Graph')
    Network_DF = pd.concat(Interaction_DF)
    Neonatal_and_MODY_Network_DF = np.array(Network_DF)
    for i in range(len(Neonatal_and_MODY_Network_DF)):
        interaction = Neonatal_and_MODY_Network_DF[i]
        a = interaction[0]  # protein a node
        b = interaction[1]  # protein b node
        w = float(interaction[2])  # score
        G.add_weighted_edges_from([(a, b, w)])

    # Generate colour map for each gene. Red indicates the Target gene, Blue indicate the Interactive gene
    colour_map = []
    for node in G.nodes:
        if not node in protein_list:
            colour_map.append('indigo')
        else:
            colour_map.append('orange')

    # Generate plots using Matplotlib and Networkx
    # Plot of Target and Interactive proteins
    plt.figure(figsize=(20, 20), facecolor=[0.7, 0.7, 0.7, 0.4])
    pos = nx.spring_layout(G, k=0.08)
    nx.draw(G, node_color=colour_map, with_labels=True, pos=pos, node_size=2000, font_size=10, font_color='white',
            font_weight='bold')
    plt.axis('off')
    plt.savefig("finalNetwork.png")
    plt.savefig("finalNetwork.pdf")


Decoy_Network_with_MODY_network(protein_list)

# Call STRING at iterate each gene ID to generate list of interactive genes then append to Interaction DF

Interaction_DF = []
for i in Input_df_to_List:
    print(i)
    proteins = '%0d'.join(i)
    url = 'https://string-db.org/api/tsv/network?identifiers=' + proteins + '&species=9606'
    r = requests.get(url)
    lines = r.text.split('\n')
    data = [l.split('\t') for l in lines]
    df2 = pd.DataFrame(data[1:-1], columns = data[0])
    interactions = df2[['preferredName_A', 'preferredName_B', 'score']]
    print(len(interactions))
    Interaction_DF.append(interactions)


# Build network with weights using Networkx
G = nx.Graph(name='Protein Interaction Graph')
Network_DF = pd.concat(Interaction_DF)
Neonatal_and_MODY_Network_DF = np.array(Network_DF)
for i in range(len(Neonatal_and_MODY_Network_DF)):
    interaction = Neonatal_and_MODY_Network_DF[i]
    a = interaction[0] # protein a node
    b = interaction[1] # protein b node
    w = float(interaction[2]) # score
    G.add_weighted_edges_from([(a,b,w)])

# Generate colour map for each gene. Red indicates the Target gene, Blue indicate the Interactive gene
colour_map = []
for node in G.nodes:
    if not node in protein_list:
        colour_map.append('indigo')
    else:
        colour_map.append('orange')

# Generate plots using Matplotlib and Networkx
# Plot of Target and Interactive proteins
plt.figure(figsize=(20, 20), facecolor=[0.7, 0.7, 0.7, 0.4])
pos = nx.spring_layout(G, k=0.08)
nx.draw(G, node_color=colour_map, with_labels=True, pos=pos, node_size= 2000, font_size=10, font_color= 'white', font_weight = 'bold')
plt.axis('off')
plt.savefig("TargetandInteractiveProteinNetwork.png")
plt.savefig("TargetandInteractiveProteinNetwork.pdf")

# Plot of all genes, colour coded according to relevancy of interaction partners and edge thickness indicating weights
def rescale(l,newmin,newmax):
    arr = list(l)
    return [(x-min(arr))/(max(arr)-min(arr)+1)*(newmax-newmin)+newmin for x in arr]

graph_colormap = cm.get_cmap('plasma', 12)
c = rescale([G.degree(v) for v in G],0.0,0.9)
c = [graph_colormap(i) for i in c]
bc = nx.betweenness_centrality(G)
s = rescale([v for v in bc.values()],1500,7000)
ew = rescale([float(G[u][v]['weight']) for u,v in G.edges],0.1,4)
ec = rescale([float(G[u][v]['weight']) for u,v in G.edges],0.1,1)
ec = [graph_colormap(i) for i in ec]

pos = nx.spring_layout(G, k=0.2)
plt.figure(figsize=(90,80),facecolor=[0.7,0.7,0.7,0.4])
nx.draw_networkx(G, pos=pos, with_labels=True, node_color=c, node_size=s,edge_color= ec,width=ew,
                         font_color='white',font_weight='bold',font_size='9')
plt.axis('off')
plt.savefig("WeightedColourNetwork.pdf")
plt.savefig("WeightedColourNetwork.png")
# Simplified colour graph
T = nx.minimum_spanning_tree(G)
pos = nx.spring_layout(T)
plt.figure(figsize=(19,6),facecolor=[0.7,0.7,0.7,0.1])
nx.draw_networkx(T, pos=pos, with_labels=True,node_color=c,node_size=s,edge_color= ec,width=ew,
                font_color='white',font_weight='bold',font_size='8')
plt.axis('off')
plt.show()
