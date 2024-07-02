# -*- coding: utf-8 -*-
"""deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dxx0-7QpVv3jADs2RNccDoPB4uWL5Mhy
"""

#from google.colab import drive
#drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#!pip install pandas
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import numpy as np
from sklearn.linear_model import LinearRegression
# %matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('classic')
from pathlib import Path
 

def diss(op_rec,lati,longi ):
    var = 12
    def distance(lat1, lat2, lon1, lon2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 
        return(c * r)

    df = pd.read_excel('Shipdatabase.xlsx')

    operation = op_rec
    place_lat = float(lati)
    place_lon = float(longi)
    df.Lat = df.Lat.astype('float')
    df.Long = df.Long.astype('float')
    print('Testing Mradul /n/n/n')
    print (place_lat)
    print (place_lon)
    
    #type_of_oper = int(input('Please select the type of operation: \n1. Anti Piracy\n2. Refueling\n3. Relief\n\n'))
    '''if(type_of_oper == 1): 
        operation = 'Anti Piracy'
    elif(type_of_oper == 2):
        operation = 'Refueling'
    elif(type_of_oper == 3):
        operation = 'Relief Operation'
'''
    df = df[df['Best Suited for']==operation]
    ships = df[['Name ', 'Lat', 'Long']]
    range = df[['Range']]
    range_list = range.values.tolist()
    ships = ships.drop_duplicates(subset=['Name ']).dropna()
    ships.set_index('Name ', inplace = True)
    ship_ = []
    distance_ = []
    for i in ships.iterrows():
        ship_.append(i[0])
        
        distance_.append(distance(place_lat, i[1].Lat, place_lon, i[1].Long))
    distance_from_place = pd.DataFrame({'Distance From' : ship_ , 'Distance' : distance_ , 'Range': range_list})
    distance_from_place['new'] = np.where(np.less_equal(distance_from_place['Distance'][0] , distance_from_place['Range'][0]), distance_from_place['Distance'], np.nan)
    #distance_from_place['new'] = distance_from_place['Distance'][(distance_from_place['Distance'] <= distance_from_place['Range']) ]
    distance_from_place.sort_values(by='new', inplace=True)
    iter_df = df.set_index('Name ')
    distance_from_place= distance_from_place.dropna()
    print(distance_from_place)
    xyz = df[['Name ', 'WEAPONS','RADAR','ENGINE','COMM','Lat','Long']].reset_index()
    print(xyz)

    dataset = pd.read_csv('TEST1.csv')
    x = dataset.loc[:, ["WEAPONS", "RADAR", "ENGINE","COMM"]]
    y = dataset.loc[:, ["SUCCESSS"]]

    model = LinearRegression().fit(x, y)
    y_pred=[]

    for index, row in xyz.iterrows():
        modelOut = model.predict([[row['WEAPONS'], row["RADAR"], row["ENGINE"], row["COMM"]]])
        #print(modelOut[0])
        y_pred.append(modelOut[0])
        #xyz2 = xyz.assign(prediction=[y_pred])
        #print('predicted response:', y_pred, sep='\n')

    print(len(y_pred))
    tempDf = pd.DataFrame(y_pred)
    tempDf.columns = ['Predicted_Score']
    print(tempDf)
    out_Df = pd.concat([xyz, tempDf], axis=1)
    print(out_Df)
    final_df = out_Df.sort_values(by='Predicted_Score',ascending=False)
    print(final_df)
    #print(len(xyz))
    #print("Msg from Ajay to Bhardwaj :  out_Df is having Predicted_Score column,, Cheers")
    
    ship = final_df.reset_index(inplace=False).iloc[0]['Name ']
    ship_info = df.set_index('Name ').loc[ship]
    ship1 = final_df.reset_index(inplace=False).iloc[1]['Name ']
    ship_info1 = df.set_index('Name ').loc[ship1]
    ship2 = final_df.reset_index(inplace=False).iloc[2]['Name ']
    ship_info2 = df.set_index('Name ').loc[ship2]

    try:

        print_state = 'Best suited ship for ' + operation + ' is ' + str(ship) + ' of ' + str(df.set_index('Name ').loc[ship]['Type']) + ' type .' + '\n' + 'Next two best ships suited are ' + str(ship1)+ ' of ' + str(df.set_index('Name ').loc[ship1]['Type']) + ' type and ' + str(ship2)+ ' of ' + str(df.set_index('Name ').loc[ship2]['Type']) + ' type.' #+ '. It belongs to ' + str(df.set_index('Name ').loc[ship]['CLASS'])  +'and it\'s homeport is ' + str(df.set_index('Name ').loc[ship]['Homeport'])' class\nThis ship has displacement of ' + str(df.set_index('Name ').loc[ship]['Displacement']) + ' and it\'s length is ' + str(df.set_index('Name ').loc[ship]['Length']) + ' with the range of ' + str(df.set_index('Name ').loc[ship]['Range']) + '\nIt\'s speed is '+ str(df.set_index('Name ').loc[ship]['Speed']) + ' with armaments ' + str(df.set_index('Name ').loc[ship]['Armament']) + '\n\n'
        print(print_state.replace('nan', 'Not known'))
    except:
        print("No ship available for " + operation) 
      #  quit()
    op = print_state    
    print('\n\nAll other Ships available for ' + operation + ' are \n')
    #dataframe = df[df['Range']]
    #display(dataframe)
  #  for out in out_Df.iterrows():
   #   for iter in df[df['Name '] == out[1]['Name ']]['Name '].to_list():
  #        print(iter + ' is at ' + str(round(out[1].Distance)) + ' KM')
      
    return op ,final_df




# df.fillna(_, inplace=True)
'''
while(True):
    lat_flag = False
    lon_flag = False
    place_lat = float(input('Please enter latitude of the target location - '))
    place_lon = float(input('Please enter longitude of the target location - '))
    if(-90 <= place_lat <= 90):
        lat_flag = True
    if(-180 <= place_lon <= 180):
        lon_flag = True
    if(lat_flag and lon_flag):
      break
    
    if(lat_flag == False and lon_flag == False):
        print('Please enter correct values')
    if(lat_flag):
        print('Longitude value should lie between -180 to 180')
    if(lon_flag):
        print('Latitude value should lie between -90 to 90')
'''


'''
filepath = Path('content/drive/MyDrive/out.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
xyz.to_csv('/content/drive/MyDrive/out.csv')  
'''
    #xyz['prediction'] = y_pred    
      #  print(row["Name"], row["Age"])


#for i in range(len(xyz)):
 #   y_pred = model.predict([xyz.iloc[i, 1], xyz.iloc[i, 2], xyz.iloc[i, 3], xyz.iloc[i, 4]])
    # print(df.iloc[i, 0], df.iloc[i, 2])
    #y_pred = model.predict([[78,68,0,78]])
    # y_pred = model.intercept_ + model.coef_ * x
#    print('predicted response:', y_pred, sep='\n')

