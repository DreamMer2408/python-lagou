import plotly
import plotly.graph_objs as go
import pymongo

client=pymongo.MongoClient('localhost',27017)
job=client['job']
table=job['jobs']

plotly.tools.set_credentials_file(username='dreamMER',api_key='XHhQzF9YtGeHKxFFzXqd')

def bar_data():
    cityList=[]
    for i in table.find():
        cityList.append(i['城市'])
    city_index=list(set(cityList))
    post_time=[]
    for i in city_index:
        post_time.append(cityList.count(i))
    trace=go.Bar(
        x=city_index,
        y=post_time,
        name='机器学习岗位'
    )

    data=[trace]
    fig=go.Figure(data=data)
    plotly.plotly.plot(fig,filename='机器学习城市分布')

def pie_data():
    education_list=['本科','硕士','博士','不限']
    under=0
    master=0
    doctor=0
    other=0
    for i in table.find():
        if i['学位']==education_list[0]:
            under+=1
        elif i['学位']==education_list[1]:
            master+=1
        elif i['学位']==education_list[2]:
            doctor+=1
        else:
            other+=1
    values=[under,master,doctor,other]
    trace=go.Pie(labels=education_list,values=values,
                 hoverinfo='label+percent',textinfo='value',
                 textfont=dict(size=20))
    plotly.plotly.plot([trace],filename='学历要求')
def bar_data_jingyan():
    cityList=[]
    for i in table.find():
        cityList.append(i['经验'])
    city_index=list(set(cityList))
    post_time=[]
    for i in city_index:
        post_time.append(cityList.count(i))
    trace=go.Bar(
        x=city_index,
        y=post_time,
        name='经验要求'
    )

    data=[trace]
    fig=go.Figure(data=data)
    plotly.plotly.plot(fig,filename='经验要求')
if __name__ == '__main__':
    #bar_data()
    #pie_data()
    bar_data_jingyan()
