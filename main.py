import pandas as pd
import streamlit as st

class AHPAnalyzer:
    def __init__(self, alternative_names, conditions):
        self.alternative_names = alternative_names
        self.conditions = conditions
        self.pairwise_matrices = {}
        self.weights = pd.DataFrame(columns=conditions, index=alternative_names)
        self.pairwise_condition_matrix = pd.DataFrame(1.0, columns=conditions, index=conditions)

    def normalize(self, df):
        for col in df.columns:
            df[col] = df[col] / df[col].sum()
        return df

    def get_weights(self, df):
        weights = df.mean(axis=1).round(4)
        return weights

    def get_consistency_ratio(self, df):
        weights = self.get_weights(df)
        n = len(weights)
        ci = (weights.mean() - n) / (n - 1)
        ri = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        cr = ci / ri[n - 1]
        return cr

    def perform_ahp_analysis(self):
        for condition in self.conditions:
            st.write(f"##### {condition}")
            self.pairwise_matrices[condition] = pd.DataFrame(1.0, columns=self.alternative_names,
                                                             index=self.alternative_names)
            self.pairwise_matrices[condition] = st.data_editor(self.pairwise_matrices[condition], key=condition)

            self.pairwise_matrices[condition] = self.normalize(self.pairwise_matrices[condition])

        for condition, matrix in self.pairwise_matrices.items():
            self.weights[condition] = self.get_weights(matrix)

        st.write('##### Weights')
        st.write(self.weights)

        st.write("##### Enter pairwise comparison matrix for conditions")
        self.pairwise_condition_matrix = st.data_editor(self.pairwise_condition_matrix, key='condition_matrix')

        self.pairwise_condition_matrix = self.normalize(self.pairwise_condition_matrix)
        condition_weights = self.get_weights(self.pairwise_condition_matrix)
        condition_weights = pd.DataFrame(condition_weights, columns=['Weights'])

        st.write('##### Condition Weights')
        st.write(condition_weights)

        weights = self.weights.to_numpy()
        condition_weights = condition_weights.to_numpy()

        final_weights = weights @ condition_weights

        final_weights = pd.DataFrame(final_weights, columns=['Weights'], index=self.alternative_names)

        st.write('##### Final Weights')
        st.write(final_weights)


# Create an instance of the AHPAnalyzer class
alternative_names_input = st.text_input('Names of Alternatives (comma separated)', value="A,B,C,D").split(',')
conditions_input = st.text_input('Conditions (comma separated)', value='Price,Distance,Air Quality').split(',')

ahp_analyzer = AHPAnalyzer(alternative_names=alternative_names_input, conditions=conditions_input)

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

# Perform AHP analysis
ahp_analyzer.perform_ahp_analysis()