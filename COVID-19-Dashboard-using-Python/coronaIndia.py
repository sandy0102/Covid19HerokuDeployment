import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.figure_factory as ff 
import plotly.express as px
import plotly.graph_objects as go

def scrape ():
    url="https://www.mohfw.gov.in/"
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response=requests.get(url, headers=headers)
    soup= BeautifulSoup(response.content,'html.parser')
    coronatable_in= soup.find_all("table")
    corona1=coronatable_in[0]
    states=[]
    total_cases=[] #confirmed_cases
    cmd=[] #cured_migrated_discharged
    deaths=[]
    rows=corona1.find_all('tr')[1:34]
    for row in rows[:-5]:
    
        col=row.find_all('td')
        states.append(col[1].text.strip())
        total_cases.append(col[2].text.strip())
        cmd.append(col[3].text.strip())
        deaths.append(col[4].text.strip())
    df = pd.DataFrame(list(zip(states, total_cases, cmd, deaths)), 
               columns =['States', 'Total_Cases',"Cured", "Deaths"]) 
    df.replace({"Uttarakhand": "Uttaranchal", 
                                  "Odisha":"Orissa"}, inplace=True) 
    df['Total_Cases'] = df['Total_Cases'].astype(int)
    df['Cured']=df['Cured'].astype(int)
    df['Deaths']=df['Deaths'].astype(int)
    df.loc[:,'variance'] = df.loc[:,'Cured'].add(df.loc[:,'Deaths'])
    df['Active_Cases'] = df["Total_Cases"]-df["variance"]
    df.drop(["variance"],axis=1, inplace=True)
    df.sort_values(["Total_Cases"], inplace=True, ascending=False)
    df.reset_index(drop=True,inplace=True)
    return df

def table():
    df=scrape()
    
    df3 = ff.create_table(df)
    return plotly.offline.plot(df3,output_type='div')  
def total():
    df=scrape()
    Total_Cases=df["Total_Cases"].sum()
    Total_Cured=df["Cured"].sum()
    Total_Deaths=df["Deaths"].sum()
    Active_Cases=df["Active_Cases"].sum()
    return [Total_Cases,Total_Cured,Total_Deaths,Active_Cases]


def plot1():
    df=scrape()
    fig = px.bar(df, x='States', y='Total_Cases', color='Total_Cases', height=600)
    return plotly.offline.plot(fig,output_type='div')
    
def plot2():
    df=scrape()
    fig = px.bar(df, x='States', y='Deaths', color='Deaths', height=600)
    return plotly.offline.plot(fig,output_type='div')
def plot3():
    df=scrape()
    fig = px.bar(df, x='States', y='Active_Cases', color='Active_Cases', height=600)
    return plotly.offline.plot(fig,output_type='div')  
    
def top20():
    df=scrape()
    df_latest=df.sort_values("Total_Cases", ascending=False)
    df_latest.reset_index(drop=True,inplace=True)

    data=df_latest.iloc[0:20,:]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["States"],
                    y=data["Cured"],
                    name='Recovered/Migrated',
                    marker_color='indianred'
                    ))
    fig.add_trace(go.Bar(x=data["States"],
                    y=data["Deaths"],
                    name='Deaths',
                    marker_color='lightsalmon'
                    ))

    fig.update_layout(
        title='Recovered v/s deaths ratio in top 20 states',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor="rgba(255, 255, 255, 0)",
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return plotly.offline.plot(fig,output_type='div')


def bedslowest():
    df_f1=pd.read_csv("bedspermn.csv")
    df_final=df_f1.drop([9,17])
    df_l=df_final.sort_values('Beds per mn', ascending=True)
    df_lowest=df_l[0:15]
    df_lowest.reset_index(drop=True,inplace=True)
    fig = px.scatter(df_lowest, x="State / Union Territory", y="Beds per mn", color="Beds per mn",
               color_continuous_scale=px.colors.sequential.Agsunset, render_mode="webgl")
    
    return plotly.offline.plot(fig,output_type='div')


def datewise():
    df=pd.read_csv(r"covid_19_india (1).csv")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Total Confirmed"], 
                    mode='lines+markers',
                    name='Corona Virus Cases with date'))
    return plotly.offline.plot(fig,output_type='div')

def ageWise():
    df=pd.read_csv(r"AgeGroupDetails.csv")
    df1= df.rename(index = {"Oct-19": "10-19"}) 
    fig = px.pie(df1, values='Percentage', names='AgeGroup', title="Age-wise distribution of COVID19 cases in India",color_discrete_sequence=px.colors.sequential.RdBu)
    return plotly.offline.plot(fig,output_type='div')

def malefemaleratio():
    df=pd.read_csv(r"AgeGroupDetails.csv")
    df1= df.rename(index = {"Oct-19": "10-19"}) 
    
    fig = px.pie(df1, values='Percentage', names='AgeGroup', title="Age-wise distribution of COVID19 cases in India",color_discrete_sequence=px.colors.sequential.RdBu)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["AgeGroup"],
                    y=df["M"],
                    name='Male infected',
                    marker_color='midnightblue'
                    ))
    fig.add_trace(go.Bar(x=df["AgeGroup"],
                    y=df["F"],
                    name='Female infected',
                    marker_color='hotpink'
                    ))

    fig.update_layout(
        title='Male v/s Female cases',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Number of cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor="rgba(255, 255, 255, 0)",
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, 
        bargroupgap=0.1
    )
    return plotly.offline.plot(fig,output_type='div')

def icmr():
    df=pd.read_csv("ICMR.csv")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["TotalSamplesTested"], 
                    mode='lines+markers',
                    name='ICMR tests done everyday'))
    return plotly.offline.plot(fig,output_type='div')

def positive():
    df=pd.read_csv("ICMR.csv")
    fig = px.bar(df, x='Date', y='Increase per day', color='Increase per day', height=600, title="New positive cases everyday")
    return plotly.offline.plot(fig,output_type='div')

def icmrlabs():
    df=pd.read_csv("ICMRTestingLabs.csv")
    values = list(df['state'].value_counts())
    states = list(df['state'].value_counts().index)
    labs = pd.DataFrame(list(zip(values, states)),columns =['values', 'states'])
    fig = px.bar(labs, x='values', y='states', height=600,title='Statewise Labs for testing',color='states')
    return plotly.offline.plot(fig,output_type='div')