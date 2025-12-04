# pages/fonction_affine.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Visualisation interactive d'une fonction affine avec Streamlit")

try:
    st.header("Selectionner les paramètres de la fonction y=ax+b à l'aide des curseurs")
    # slider pour selectionner la valeur de a
    a = st.slider(
        'valeur de a',
        min_value=-10.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )

    # slider pour selectionner la valeur de b
    b = st.slider(
        'valeur de b',
        min_value=-10.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )

    # Option bonus: Faire choisir la couleur de la courbe 
    st.subheader("Personnalisation du graphique")
    curve_color = st.color_picker("Couleur de la courbe :", "#87CEEB")

    # Option Bonus: Proposer l'ajout d'un titre aux axes
    graph_title = st.text_input('Titre du graphique :', value='Representation graphique de la fonction affine y = a*x+b', help="Toutes modification de ce champ modifiera le titre du graphique")
    
    # Option bonus: Proposer l'ajout d'etiquettes aux axes
    x_label = st.text_input("Etiquette axe x:", value='x', help="Toute modification entrainera le changement du nom de l'axe x")
    y_label = st.text_input("Etiquette axe y:", value='y', help="Toute modification entrainera le changement du nom de l'axe y")
    
    # Option bonus modifications de l'intervalle des valeurs xaffichées
    x_min = -10
    x_max = 10
    nb_val_x = 10
    x_min_user = x_min
    x_max_user = x_max

    x_min_user = float(st.text_input("Modifier la valeur minimum de l'intervalle des valeurs de x", value=x_min))
    x_max_user = float(st.text_input("Modifier la valeur maximum de l'intervalle des valeurs de x", value=x_max))
    nb_val_x_user = st.text_input('Modifier le nombre de valeur de x', value=nb_val_x)
    #message_container = st.empty()
    if x_min_user < x_max_user:
        x_min = x_min_user
        x_max = x_max_user
        #message_container.success()
    #else:
        #message_container.error("Attention la borne minimale doit etre inferieure a la borne maximale")
    # Générer un ensemble de valeurs x sur un intervalle donné
    # entre -10 et 10 et 10 valeurs générées par defaut 
    
    x = np.linspace(x_min, x_max, 10)

    # on defini y
    y = a * x + b

    # Bonus afficher l'equation de la droite y = a*x + b avec val actuelles de a et b
    st.markdown(f"Equation de la droite : y = {a:.2f} * x + {b:.2f}")
    
    # on defini les parametres de l'affichage graphique
    fig, ax = plt.subplots()
    ax.plot(x, y,color = curve_color, lw=2)
    ax.set_title(graph_title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)

    st.pyplot(fig)
    # Bonus afficher l'equation de la droite y = a*x + b avec val actuelles de a et b
    st.markdown(f"Equation de la droite : y = {a:.2f} * x + {b:.2f}")

except Exception as e:
    print(f'Erreur : {e}')