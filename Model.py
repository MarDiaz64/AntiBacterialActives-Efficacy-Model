from sklearn.linear_model import LinearRegression
import pickle
from DatabaseManagement import DBManager
#import pandas 

class Model:
    def __init__(self):
        #set up data
        self.cleanedData=DBManager.getCleanedData()
        #load model
        try:
            self.model = pickle.load(open('efficacyModel.sav', 'rb')) #pickle used to save model for reuse
        except FileNotFoundError:
            self.model = LinearRegression()
            self.train()
            
    def train(self): 
        #input Set
        X=self.cleanedData.drop(columns=['Efficacy'])
        #output Set
        y=self.cleanedData['Efficacy']
        
        self.model.fit(X.values,y.values)
        filename = 'efficacyModel.sav'
        pickle.dump(self.model, open(filename, 'wb'))

    #update model 
    def updateModel(self,actives,dilution,hardness,dirty,ph,efficacy,idd):
        try:
            #actives[0]=DDAC, actives[1]=DKC,actives[2]=Citric
            self.cleanedData.loc[len(self.cleanedData.index)]=\
                [actives[0]*10000/dilution,actives[1]*10000/dilution,\
                 actives[2]*10000/dilution,hardness,dirty,ph,efficacy]
            DBManager.insert(actives,dilution,hardness,dirty,ph,efficacy,idd)
            self.train()
            return True
        except:
            return False
    #use model generated to give a prediction  
    def predict(self,actives,dilution,hardness,dirty,ph):
        #try:
            #actives[0]=DDAC, actives[1]=DKC,actives[2]=Citric
            DDAC_ppm=actives[0]*10000/dilution
            BKC_ppm=actives[1]*10000/dilution
            Citric_ppm=actives[2]*10000/dilution
            return self.model.predict([[DDAC_ppm,BKC_ppm,Citric_ppm,hardness,dirty,ph]])
        #except:
            #return -1
