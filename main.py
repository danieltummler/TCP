import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle
from datetime import datetime

def main():
    
    df = pd.read_pickle(filepath_or_buffer = "all_fenix_2.pkl")

    df = df.explode("recipe").reset_index(drop = True)

    df["recipe2"] = [" - ".join([str(y) for y in x]) for x in df["recipe"].values]

    st.title("Fenix Cocktail Bar")

    # st.dataframe(df)

    cocktail_name = st.selectbox(label = "Cocktail Name",
                                 options = df["name"].unique(),
                                 index = None)

    ingredient_name = st.selectbox(label = "Ingrediente",
                                   options = sorted(list(set([x[1].strip() for x in df["recipe"]]))),
                                   index = None)

    if cocktail_name:
        df_cocktail = df[df["name"] == cocktail_name]
        
        col1, col2 = st.columns([1, 2])
        col1.write(f"{cocktail_name}")
        
        col1.write("Ingredientes:")
        for ing in df_cocktail["recipe2"].values:
            col1.write(f"{ing}")
        
        col2.write(f"Copa: {df_cocktail['glass'].unique()[0]}\n")
        col2.write(f"Decoración: {df_cocktail['garnish'].unique()[0]}\n")
        col2.write(f"Método: {df_cocktail['directions'].unique()[0]}")

    if ingredient_name:
        col1, col2 = st.columns([1, 2])
        col1.write(f"{ingredient_name}")

        indices = list()
        for recipe, idx in zip(df["recipe"], df["recipe"].index):
            recipe = np.array(recipe)[1]
            if ingredient_name in recipe:
                indices.append(idx)
        df_ing = df.iloc[indices, :][["name", "glass", "directions"]].drop_duplicates().reset_index(drop = True)
        df_ing.columns = ["Nombre", "Copa", "Método"]
        st.dataframe(df_ing)

    with st.expander(label = "Añadir Cocktail 🍸", expanded = False):

        with st.form("new_cocktail"):
            col11, col22 = st.columns([1, 1])
            input_name = col11.text_input(label = "Nombre: ", placeholder = "Nombre").upper()
            input_directions = col22.selectbox(label = "Método", options = df["directions"].unique(), index = None, placeholder = "Método")
            input_glass = col11.selectbox(label = "Copa: ", options = df.replace({"nan" : np.nan}).dropna()["glass"].unique(), index = None, placeholder = "Copa")
            input_new_glass = col22.text_input(label = "¿Nueva copa?").upper()
            input_garnish = col11.text_input(label = "Decoración").upper()

            input_glass = input_new_glass if input_new_glass else input_glass
        
            ingredients = list()
            for i in range(10):
                col111, col222 = st.columns([1, 1])
                if i == 0:
                    input_unit = col111.text_input(label = "Unidad", key = i).upper()
                    input_ingredient_name = col222.text_input(label = "Ingrediente", key = (i + 1)*10).upper()

                    ingredients.append([input_unit, input_ingredient_name])

                else:
                    input_unit = col111.text_input(label = "Unidad", key = i, label_visibility = "hidden", ).upper()
                    input_ingredient_name = col222.text_input(label = "Ingrediente", key = (i + 1)*10, label_visibility = "hidden").upper()

                    if input_unit != "" and input_ingredient_name != "":
                        ingredients.append([input_unit, input_ingredient_name])

            input_password = col22.text_input(label = "Contraseña", type = "password")  
            submitted = st.form_submit_button("Añadir")

            if submitted and input_password.lower() == "pato":
                
                new_cocktail_info = {"name"       : input_name,
                                     "directions" : input_directions,
                                     "glass"      : input_glass,
                                     "recipe"     : ingredients,
                                     "garnish"    : input_garnish,
                                     "datetime"   : datetime.now()}

                fenix = pd.read_pickle(filepath_or_buffer = "all_fenix_2.pkl")
                new = pd.json_normalize(new_cocktail_info)

                fenix = pd.concat([fenix, new], ignore_index = True)

                fenix.to_pickle(path = "all_fenix_2.pkl")

                st.write("Añadido")

if __name__ == "__main__":
    main()
