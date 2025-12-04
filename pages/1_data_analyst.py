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
        st.dataframe(data_df, width='stretch')
        
        st.subheader('Affichage des 5 premieres lignes')
        st.dataframe(data_df.head(), width='stretch')
        
        st.subheader('Affichage des statistiques descriptives')
        st.dataframe(data_df.describe(), width='stretch')

        st.subheader('Selectionnez les colonnes à afficher')
        columns = st.multiselect("Colonnes sélectionnées", options=data_df.columns.tolist(), default=data_df.columns.tolist())
        if columns:
            # affiche data_df pour seulement les colonnes selectionnées
            st.dataframe(data_df[columns], width='stretch')

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
            if data_df[col_x].dtype in ['int64', 'float64', 'int32', 'float32'] and data_df[col_y].dtype in ['float64', 'int64', 'int32']:
                fig, ax = plt.subplots()
                sns.scatterplot(data=data_df, x=col_x, y=col_y,ax=ax)
                ax.set_title(f"{col_y} vs {col_x}")
                st.pyplot(fig)
            else:
                # st.error('❌ Colonnes numeriques uniquement {col_x}={data_df[col_x].dtype}, {col_y}={data_df[col_y].dtype}') # debug
                st.error('❌ Colonnes numeriques uniquement')

        # filtrage des données en fonction d'une colonne et d'une valeur specifique
        st.subheader('Selectionnez une colonne est une valeur spécifique pour filter les données')
        # selection de la colonne
        columns_filter = st.selectbox('Choisissez la colonne à filtrer', options=data_df.columns.tolist())

        st.subheader('Selectionnez la valeur à filtrer')
        # selection des valeurs uniques dans la colonne selectionnée
        unique_values = sorted(data_df[columns_filter].dropna().unique())
        # l'ajout de [-- Toutes __] permet de juste afficher tout si aps de saisie de valeur
        value_filter = st.selectbox(f"Sélectionnez une valeur dans {columns_filter}", options=['-- Toutes --'] + unique_values, index=0)

        # filtrage par bouton
        if st.button('Filtrer') and value_filter != '-- Toutes --':
            data_filtered = data_df[data_df[columns_filter] == value_filter]

            st.success(f"{len(data_filtered)} lignes trouvées pour {value_filter}")
            st.subheader(f'Colonne {columns_filter} filtrée avec {value_filter}')
            st.dataframe(data_filtered, width='stretch')

        # histogramme a partir d'une colonne numerique
        st.subheader("Création d'un histogramme à partir d'une colonne numerique")
        
        # selection d'une colonne numerique column_histo
        columns_numeric = data_df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        column_histo = st.selectbox("Choisissez une colonne", options=columns_numeric)

        # selection d'un nombre de bins avec un slider
        nb_bins = st.slider("Selectionnez le nombre de bacs pour l'histogramme", min_value=5, max_value=100, value=25, step=1)

        # histogramme sur la colonne choisie avec nombre de bins personnalisés par l'user
        fig, ax = plt.subplots()
        ax.hist(data_df[column_histo].dropna(), bins=nb_bins, color='skyblue')
        ax.set_title(f"Historigramme de {column_histo}")
        ax.set_xlabel(column_histo)
        ax.set_ylabel('Fréquence')
        ax.grid(True)
        st.pyplot(fig)

        st.subheader('Affichage des statistiques descriptives')
        st.dataframe(data_df.describe(), width='stretch')
        # a terminer valeur manquante st.dataframe(data_df) 

    except Exception as e:
        st.error(f"❌ Erreur innatendue : {e}")
    
