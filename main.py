import pandas as pd
import streamlit as st

def normalize(df):
    for col in df.columns:
        df[col] = df[col]/df[col].sum()
    return df

def get_weights(df):
    weights = df.mean(axis=1).round(4)
    return weights

def get_consistency_ratio(df):
    weights = get_weights(df)
    n = len(weights)
    ci = (weights.mean() - n)/(n-1)
    ri = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49]
    cr = ci/ri[n-1]
    return cr

st.write("""
         # Performs AHP on a given dataset
         ***
         """)

st.write("""
         ### Instructions
            1. Enter the names of the alternatives separated by commas.
            2. Enter the conditions separated by commas.
            3. Press Enter, changes will be reflected in the table.
            4. Enter the values in the table.
         """)
alternative_names = st.text_input('Names of Alternatives (comma separated)',value="A,B,C,D").split(',')
conditions = st.text_input('Conditions (comma separated)',value='Price,Distance,Air Quality').split(',')

st.write(" ##### Input pairwise comparison matrices for each condition.")
pairwise_matrices = {}

for condition in conditions:
    st.write(f"##### {condition}")
    pairwise_matrices[condition] = pd.DataFrame(1.0,columns=alternative_names, index=alternative_names)
    pairwise_matrices[condition] = st.data_editor(pairwise_matrices[condition],key=condition)

for condition,matrix in pairwise_matrices.items():
    pairwise_matrices[condition] = normalize(matrix)

weights = pd.DataFrame(columns=conditions,index=alternative_names)
for condition,matrix in pairwise_matrices.items():
    weights[condition] = get_weights(matrix)

st.write('##### Weights')
st.write(weights)

st.write("##### Enter pairwise comparison matrix for conditions")
pairwise_condition_matrix = pd.DataFrame(1.0,columns=conditions, index=conditions)
pairwise_condition_matrix = st.data_editor(pairwise_condition_matrix,key='condition_matrix')

pairwise_condition_matrix = normalize(pairwise_condition_matrix)
condition_weights = get_weights(pairwise_condition_matrix)
condition_weights = pd.DataFrame(condition_weights,columns=['Weights'])

st.write('##### Condition Weights')
st.write(condition_weights)

weights = weights.to_numpy()
condition_weights = condition_weights.to_numpy()

final_weights = weights @ condition_weights

final_weights = pd.DataFrame(final_weights,columns=['Weights'],index=alternative_names)

st.write('##### Final Weights')
st.write(final_weights)