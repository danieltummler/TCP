import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle

def main():
    
    df = pd.read_pickle(filepath_or_buffer = "all_fenix_2.pkl")

    df = df.explode("recipe").reset_index(drop = True)

    df["recipe"] = [" - ".join([str(y) for y in x]) for x in df["recipe"].values]

    st.title("Fenix Cocktail Bar")

    # st.dataframe(df)

    cocktail_name = st.selectbox(label = "Cocktail Name", options = df["name"].unique(), index = None)

    if cocktail_name:
        df_cocktail = df[df["name"] == cocktail_name]
        
        col1, col2 = st.columns([1, 2])
        col1.write(f"{cocktail_name}")
        
        col1.write("Ingredientes:")
        for ing in df_cocktail["recipe"].values:
            col1.write(f"{ing}")
            
        col2.write(f"\n")
        col2.write(f"\n")
        col2.write(f"\n")
        col2.write(f"Copa: {df_cocktail['glass'].unique()[0]}\n")
        col2.write(f"Decoración: {df_cocktail['garnish'].unique()[0]}\n")
        col2.write(f"Método: {df_cocktail['directions'].unique()[0]}")
if __name__ == "__main__":
    main()