# pages/data_analyst.py
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

st.title("Créaition d'un outil d'analyse de données interactif avec streamlit")

# affichage d'un widget permettant d'upload un fichier depuis son ordinateur
uploaded_file = st.file_uploader('Choisissez un fichier CSV', type='csv')

if uploaded_file is not None:
    try:    
        data_df = pd.read_csv(uploaded_file)

        st.subheader('Affichage du fichier CSV en entier')
        st.dataframe(data_df)
        
        st.subheader('Affichage des 5 premieres lignes')
        st.dataframe(data_df.head())
        
        st.subheader('Affichage des statistiques descriptives')
        st.dataframe(data_df.describe(), use_container_width=True)

        st.subheader('Selectionnez les colonnes à afficher')
        columns = st.multiselect("Colonnes sélectionnées", options=data_df.columns.tolist(), default=data_df.columns.tolist())
        if columns:
            # affiche data_df pour seulement les colonnes selectionnées
            st.dataframe(data_df[columns])

        st.subheader('Sélectionner deux colonnes pour générer un graphique interactif')
        # par defaut les deux premiers colonnes numeriques
        columns_graph = st.multiselect('Colonnes sélectionnées ', options=data_df.columns.tolist(), default=data_df.select_dtypes(include=[np.number]).columns.tolist()[:2])

        if columns_graph is None or len(columns_graph) == 0:
            st.error('❌ Selectionner deux colonnes')
        elif len(columns_graph) > 2:
            st.warning('⚠️ Si plus de 2 colonnes selectionnées par defaut les 2 premières seront utilisées')
            cols_to_plot = columns_graph[:2]
        else:
            cols_to_plot = columns_graph

        # création du graphique
        st.subheader(f'Graphique nuage de points avec les colonnes selectionnées: {columns_graph[:2]}')
        if len(cols_to_plot) == 2:
            col_x, col_y = cols_to_plot

            # st.write(f"Debug: X={col_x} (type: {data_df[col_x].dtype}), Y={col_y} (type: {data_df[col_y].dtype})") # debug
            
            # verification que ce sont bien des valeurs numeriques dans ces colonnes
            if data_df[col_x].dtype in ['float64', 'int64', 'int32'] and data_df[col_y].dtype in ['float64', 'int64', 'int32']:
                fig, ax = plt.subplots()
                sns.scatterplot(data=data_df, x=col_x, y=col_y,ax=ax)
                ax.set_title(f"{col_y} vs {col_x}")
                st.pyplot(fig)
            else:
                # st.error('❌ Colonnes numeriques uniquement {col_x}={data_df[col_x].dtype}, {col_y}={data_df[col_y].dtype}') # debug
                st.error('❌ Colonnes numeriques uniquement')
    except Exception as e:
        st.error(f"Erreur innatendue : {e}")
    
