# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import plotly.express as px

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('C:/Users/PUddagiri/Desktop/Web_app/streamlit/background2.jpg')


# #st.write("Please enter the values for copper recovery")
# #col1,col2,col3,col4,col5=st.columns(5)
#
# #with col1:
#
#     val1=st.text_input("value1")
# #with col2:
#     val2=st.text_input("value2")
# with col3:
#     val3=st.text_input("value3")
# with col4:
#     val4=st.text_input("value4")
#
# result=st.button('submit')
#
#
#
#
#
#

def func(df,start_date, end_date,values_a,values_b):
        df=df.iloc[2:3]
        df_values=df.iloc[:,4:]
        df2=df_values.transpose()
        df2['date']=df2.index
        #df2['date']=np.datetime64
        mask=(df2['date']<end_date) & (df2['date']>start_date)
        
        df3=df2.loc[mask,2].to_numpy()
        len(df3)
         #basic model development
         #mill feed rate is the ore copper grade from the mine plan

        #a      b       c   d        formula
        #GRIND_P80	52.3	0.06	0	0		grind_p80 + a + bx + cx2 + dx3  x=mill rate
        #665	625 650 665 665 665 665 625 650 665 665 665 665 625 650 665 665 665 665 625 650 665 665 665 665 625 650 665 665 665 665 625 650 665 665 665 665 625 650 665 665 665 665 625 650	665	665	665	665	625	650	665	665	665	665	625	650	665	665	665

        average_millrate=655.8
        grindp80=52.3+0.06*average_millrate+0*(average_millrate**2)+0*(average_millrate**3)

            #a     b    c   d
        #GRIND_Cu=6.4 -0.07   0   0 a + bx + cx2 + dx3 x=GRIND_P80
        grind_cu=6.4-0.07*grindp80+0*grindp80**2+0*grindp80**2

         #formula for copper recovery
        #REC_Cu 91.5 1.00 0 0 Cu_rec + GRIND_Cu + a + bx + cx2 + dx3  x=mill feed grade
        cu=[]
        #count=0

        for i in df3:
            cu_recovery=grind_cu+values_a+values_b*i+0*(i**2)+0*(i**3)
            cu.append(cu_recovery)
            #count+=1
    
        return cu,df3



# +
col1,col2=st.columns(2)
with col1:    
    val_start=start_input=st.date_input("Start Date")
    val_st=val_start.strftime("%d/%m/%y")


with col2:
    val_end=end_input=st.date_input("End Date")
    val_en=val_end.strftime("%d/%m/%y")

# -

df_new=pd.DataFrame()
def file_upload(uploaded_file):
    if uploaded_file is not None:
        df_new = pd.read_excel(uploaded_file)
        st.write(df_new)
        st.dataframe(df_new)
    else:
        df_new=None
    return df_new


# +
col1,col2 =st.columns(2)
with col1:
    uploaded_file1 = st.file_uploader("Upload the Met Model")
    
    dfile1=file_upload(uploaded_file1)
with col2:
    uploaded_file2=st.file_uploader("Upload the Mine Plan")
    
    dfile2=pd.read_excel("C:/Users/PUddagiri/Desktop/Web_app/Carrapateena Python Model Interface/Mine Plan/Mine Plan.xlsx")

col3,col4=st.columns(2)
with col3:
    uploaded_file3=st.file_uploader("Upload the Mill Plan")
with col4:
     uploaded_file4=st.file_uploader("Upload general coeffecients")
#file_upload(uploaded_file3)
#with col4:
    #uploaded_file4=st.file_uploader("Upload the General Coeffecients")
#file_upload(uploaded_file4)





values_a = st.slider("Coeffecient a:",0.0, 100.0,step=0.5,key="a")
#st.session_state["a"] = values_a
#value_current_a=value_b.session_state.slider
values_b=st.slider("Coeffecient b:",0.0,100.0,key="b")

if values_a and values_b:
    cu_list,dfile3=func(dfile2,val_st,val_en, values_a, values_b)
   
    #fig.update_layout(xaxis_range=[2019,2028])
    plot= px.scatter(x=cu_list,y=dfile3)
    
    
    
    
    plot.update_layout(plot_bgcolor="rgba(1,1,1,1)")
    plot.update_traces(marker=dict(size=12.5,line=dict(width=2,color='DarkSlateGrey')),selector=dict(mode='markers'))
    st.plotly_chart(plot)

    
#cu_list,dfile3=func(dfile2,val_st, val_en,float(values_a),float(values_b)



#result=st.button('Run Model')

# -
# st.background("black")







