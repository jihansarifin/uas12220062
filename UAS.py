import streamlit as st
import pandas as pd
import json
import numpy as np
import csv

def a3df_to_namedf(df, countryList):
    for i in countryList:
        df['kode_negara'] = df['kode_negara'].replace([i[1]], i[0])
    return df
def addFullCountryName(df, countryList):
    df['Nama Negara'] = df['kode_negara']
    for i in countryList:
        df['Nama Negara'] = df['Nama Negara'].replace([i[1], i[0]])
    return df

def makeZeroDf(df, countryList):
    df['Nama Negara'] = 0
    for i in countryList:
        df['Nama Negara'] = df['Nama Negara'].replace([i[1], i[0]])
    return df

def noZeros(df):
    return df[df['produksi'] != 0]
def noZeros_cum(df):
    return df[df['kumulatif'] != 0]
def getZeros(df):
    return df[df['produksi'] == 0]
def getZeros_cum(df):
    return df[df['kumulatif'] == 0]

def addStatus(df, countryList):
    df['Nama Negara'] = df['kode_negara']
    df['Region'] = df['kode_negara']
    df['Sub Region'] = df['kode_negara']
    for i in countryList:
        df['Nama Negara'] = df['Nama Negara'].replace([i[1]], i[0])
        df['Region'] = df['Region'].replace([i[1]], i[3])
        df['Sub Region'] = df['Sub Region'].replace([i[1]], i[4])
    return df[['Nama Negara', 'Region', 'Sub Region']]



file = open('kode_negara_lengkap.json')
jfile = json.load(file)
file.close()
df = pd.read_csv("produksi_minyak_mentah.csv")




# JSON Dictionary
countryList = []
for elmt in jfile:
    name = elmt.get('name')
    alpha_3 = elmt.get('alpha-3')
    country_code = elmt.get('country-code')
    region = elmt.get('region')
    sub_region = elmt.get('sub-region')
    countryElmt = [name, alpha_3, country_code, region, region, sub_region]
    countryList.append(countryElmt)




# remove some country not in json
notInJSON = ["WLD", "G20", "EU28", "OECD"]
for x in notInJSON:
    df = df[df['kode_negara'] != x]

df = df[df['kode_negara'] != "WLD"]





# cumulative dataframe
df['kumulatif'] = df.groupby(['kode_negara'])['produksi'].cumsum()
df_cum = df.drop_duplicates('kode_negara', keep="last")
min_year = int(df.min(axis=0)['tahun'])
max_year = int(df.max(axis=0)['tahun'])
df_topcum = df_cum.sort_values(by='kumulatif', ascending=False, axis=0)

st.title("Data Produksi Minyak Mentah Dunia")
st.subheader("Informasi dan Grafik")
# informasi keseluruhan tahun
with st.expander("Rangkuman Informasi Keseluruhan Tahun: "):
    st.subheader("Negara Produksi Terbesar")
    maxIdx = (df_cum['kumulatif'].idxmax())
    for country in countryList:
        if country[1] == df_cum.loc[maxIdx, 'kode_negara']:
            break
    # searching di countryList
    st.write("Nama Negara: " + country[0])
    st.write("Kode Negara: " + country[1])
    st.write("Region: " + country[3])
    st.write("Subregion: " + country[4])
    st.write("Produksi terbesar keseluruhan tahun: " + str(df_cum.loc[maxIdx, 'kumulatif']))

    clean_cum = noZeros_cum(df_cum)
    st.subheader("Negara Produksi Terkecil")
    minIdx = (clean_cum['kumulatif'].idxmin())
    for country in countryList:
        if country[1] == clean_cum.loc[minIdx, 'kode_negara']:
            break
    # searching di countryList
    st.write("Nama Negara: " + country[0])
    st.write("Kode Negara: " + country[1])
    st.write("Region: " + country[3])
    st.write("Subregion: " + country[4])
    st.write("Produksi terkecilr keseluruhan tahun: " + str(clean_cum.loc[minIdx, 'kumulatif']))




    st.subheader("Negara-negara produksi nol")
    df_zero_cum = getZeros(df_cum).reset_index(drop=True)
    df_zero_cum.index += 1
    df_zero_cum2 = addStatus(df_zero_cum, countryList)
    st.table(df_zero_cum2)







with st.expander("Rangkuman Informasi Tahun T"):
    set_year = int(st.slider('Tahun (Y)', min_value=min_year, max_value=max_year, help="Masukkan tahun", key="rangkuman"))
    df_year = df.loc[df['tahun'] == set_year]
    st.subheader("Negara Produksi Terbesar")
    maxIdx = (df_year['produksi'].idxmax())
    for country in countryList:
        if country[1] == df_year.loc[maxIdx, 'kode_negara']:
            break
    # searching di countryList
    st.write("Nama Negara: " + country[0])
    st.write("Kode Negara: " + country[1])
    st.write("Region: " + country[3])
    st.write("Subregion: " + country[4])
    st.write("Produksi terbesar tahun " + str(set_year) + " : " + str(df_year.loc[maxIdx, 'produksi']))

    clean_year = noZeros(df_year)
    st.subheader("Negara Produksi Terkecil")
    minIdx = (clean_year['produksi'].idxmin())
    for country in countryList:
        if country[1] == clean_year.loc[minIdx, 'kode_negara']:
            break
    # searching di countryList
    st.write("Nama Negara: " + country[0])
    st.write("Kode Negara: " + country[1])
    st.write("Region: " + country[3])
    st.write("Subregion: " + country[4])
    st.write("Produksi terkecil tahun " + str(set_year) + " : " + str(clean_year.loc[minIdx, 'produksi']))

    st.subheader("Negara-negara produksi nol")
    df_zero_year = getZeros(df_year).reset_index(drop=True)
    df_zero_year.index += 1
    df_zero_year2 = addStatus(df_zero_year, countryList)
    st.table(df_zero_year2)
    




# dataframe top n production on year y (2)
with st.expander("Grafik produksi N negara terbesar pada tahun Y: "):
    set_year = int(st.slider('Masukkan tahun (Y)', min_value=min_year, max_value=max_year, help="Masukkan tahun"))
    set_n = int(st.number_input('Masukkan berapa negara terbesar (N):', min_value=1, max_value=len(countryList)-1, help="masukkan tahun", key="grafik2", value=3))
    df_year2 = df.loc[df['tahun'] == set_year]
    df_topn = df_year2.sort_values(by='produksi', ascending=False, axis=0)
    bar_topn = df_topn[['kode_negara', 'produksi']].head(set_n)
    st.write("Grafik produksi " + str(set_n) + " negara terbesar pada tahun" + str(set_year))
    st.bar_chart(bar_topn.set_index('kode_negara'))

# dataframe country x (1)
with st.expander("Grafik produksi minyak negara X"):
    ctry = st.selectbox("Negara: ", (i[0] for i in countryList))
    for x in countryList:
        if x[0] == ctry:
            set_country_code = x[1]
            break
    if not((df['kode_negara'] == set_country_code).any()):
        st.write("Tidak tersedia")
    else:
        st.write("Grafik produksi minyak " + str(ctry))
        df_country = df.loc[df['kode_negara'] == set_country_code]
        # grafik produksi suatu negara
        line_country = df_country[["tahun", "produksi"]]
        st.line_chart(line_country.set_index('tahun'))


# dataframe cumulative top n (3)
with st.expander("Grafik produksi kumulatif N negara terbesar"):
    set_n2 = int(st.number_input('Masukkan berapa negara terbesar (N)', min_value=1, max_value=len(countryList)-1, help="masukkan N", key='grafik3', value=3))
    bar_topcum = df_topcum[['kode_negara', 'produksi']].head(set_n2)
    st.write("Grafik produksi kumulatif " + str(set_n2) + " negara terbesar")
    st.bar_chart(bar_topcum.set_index('kode_negara'))





















