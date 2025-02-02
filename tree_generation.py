import pandas as pd
import numpy as np
from graphviz import Digraph

def generate_tree():
    # Load the CSV file
    rawdf = pd.read_csv('family_tree.csv', sep=";", keep_default_na=False)

    # Normalize IDs by removing the decimal point
    rawdf['ID'] = rawdf['ID'].astype(str).str.replace('.0', '', regex=False)
    rawdf['ID Spouse'] = rawdf['ID Spouse'].astype(str).str.replace('.0', '', regex=False)
    rawdf['ID Mother'] = rawdf['ID Mother'].astype(str).str.replace('.0', '', regex=False)
    rawdf['ID Father'] = rawdf['ID Father'].astype(str).str.replace('.0', '', regex=False)

    # Prepare parent-child relationships
    el1 = rawdf[['ID', 'ID Mother']]  # Mother-child relationships
    el2 = rawdf[['ID', 'ID Father']]  # Father-child relationships
    el1.columns = ['Child', 'ParentID']
    el2.columns = el1.columns
    el = pd.concat([el1, el2])
    el.replace('', np.nan, regex=True, inplace=True)
    t = pd.DataFrame({'tmp': ['no_entry' + str(i) for i in range(el.shape[0])]})
    el['ParentID'].fillna(t['tmp'], inplace=True)

    # Merge with main data
    df = el.merge(rawdf, left_index=True, right_index=True, how='left')

    # Create the Merge column
    df['Merge'] = df.apply(lambda x: ' '.join(x[['Surname', 'Name']].dropna().astype(str)), axis=1)

    # Clean up unnecessary columns
    df = df.drop(['Child', 'ID Father', 'ID Mother', 'Surname', 'Name'], axis=1)
    df = df[['ID', 'Merge', 'Gender', 'Date of Birth', 'Date of Death', 'Birthplace', 'Job', 'ParentID', 'ID Spouse', 'No Gen']]
    df.fillna('Inconnu', inplace=True)

    # Create the graph
    f = Digraph('dot', format='svg', encoding='utf8', filename='family_tree',
                node_attr={'style': 'filled'}, graph_attr={"concentrate": "true"})
    f.attr('node', shape='box')

    # Add nodes with conditional cross symbol for deceased individuals
    for index, row in df.iterrows():
        # Check if the person is deceased (DdD is not 'Inconnu')
        if row['Date of Death'] != 'Unknown':
            # Construct the label for deceased individuals
            label = (str(row['Merge']) + '\n' +
                     str(row['Date of Birth']) +
                     ' † ' + str(row['Date of Death']) + '\n' +
                     str(row['Job']) + '\n' +
                     ("Born in " + str(row["Birthplace"])))
        else:
            # Construct the label for living individuals
            label = (str(row['Merge']) + '\n' +
                     str(row['Date of Birth']) + '\n' +
                     str(row['Job']) + '\n' +
                     ("Born in " + str(row["Birthplace"])))
        
        # Add the node to the graph
        f.node(str(row['ID']),
               label=label,
               _attributes={'color': 'lightpink' if row['Gender'] == 'Female' else 'lightblue' if row['Gender'] == 'Male' else 'lightgray'})

    # Track processed spouse pairs to avoid duplicates
    processed_pairs = set()

    # Create intermediary nodes for spouses
    for index, row in df.iterrows():
        if row['ID Spouse'] != 'nan' and row['ID'] != row['ID Spouse'] and row['ID'] < row['ID Spouse']:  # Ensure valid pairs
            spouse1 = str(row['ID'])
            spouse2 = str(row['ID Spouse'])
            intermediary_node = f'spouse_{spouse1}_{spouse2}'
            f.node(intermediary_node, label='', shape='point', width='0.1', height='0.1')
            f.edge(spouse1, intermediary_node, dir='none')
            f.edge(spouse2, intermediary_node, dir='none')
            processed_pairs.add((spouse1, spouse2))  # Mark this pair as processed

    # Add edges for parent-child relationships
    for index, row in df.iterrows():
        if row['ParentID'] not in t['tmp'].values:
            # Find the intermediary node for the parents
            parent_spouse_pair = df[(df['ID'] == row['ParentID']) | (df['ID Spouse'] == row['ParentID'])]
            if not parent_spouse_pair.empty:
                parent_id = str(row['ParentID'])
                spouse_id = str(parent_spouse_pair.iloc[0]['ID Spouse'])
                if parent_id != spouse_id:  # Ensure valid spouse pair
                    intermediary_node = f'spouse_{parent_id}_{spouse_id}' if parent_id < spouse_id else f'spouse_{spouse_id}_{parent_id}'
                    f.edge(intermediary_node, str(row['ID']), label='')

    # Enforce generational levels using the "No Gen" column
    generations = df['No Gen'].unique()
    for gen in generations:
        with f.subgraph() as s:
            s.attr(rank='same')
            for index, row in df[df['No Gen'] == gen].iterrows():
                s.node(str(row['ID']))

    # Save and display the graph
    f.render()
    f.view()