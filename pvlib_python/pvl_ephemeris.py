# Autogenerated with SMOP version 0.23
# /usr/local/bin/smop pvl_ephemeris.m -o python/pvl_ephemeris.py
from __future__ import division
import numpy as np
from scipy.io import loadmat,savemat
import os
import pdb
import pvl_tools
import pandas as pd
def pvl_ephemeris(**kwargs):

    Expect={'pressure': ('default','default=101325','array','num','x>=0'),
            'temperature': ('default','default=12','array', 'num', 'x>=-273.15'),
            'Time':'',
            'Location':''
            }
    var=pvl_tools.Parse(kwargs,Expect)


    Latitude=var.Location.latitude
    Longitude=- 1 * var.Location.longitude
    Year=var.Time.year
    Month=var.Time.month
    Day=var.Time.day
    Hour=var.Time.hour
    Minute=var.Time.minute
    Second=var.Time.second
    TZone=- 1 * var.Location.TZ
 

    DayOfYear=var.Time.dayofyear
    DecHours=Hour + Minute / 60 + Second / 3600
    Abber=20 / 3600
    LatR=np.radians(Latitude)
  

    UnivDate=DayOfYear + np.floor((DecHours + TZone) / 24)
    UnivHr=np.mod((DecHours + TZone),24)
    Yr=Year - 1900
    YrBegin=365 * Yr + np.floor((Yr - 1) / 4) - 0.5
    Ezero=YrBegin + UnivDate
    T=Ezero / 36525
    GMST0=6 / 24 + 38 / 1440 + (45.836 + 8640184.542 * T + 0.0929 * T ** 2) / 86400
    GMST0=360 * (GMST0 - np.floor(GMST0))
    GMSTi=np.mod(GMST0 + 360 * (1.0027379093 * UnivHr / 24),360)
    LocAST=np.mod((360 + GMSTi - Longitude),360)
    EpochDate=Ezero + UnivHr / 24
    T1=EpochDate / 36525
    ObliquityR=np.radians(23.452294 - 0.0130125 * T1 - 1.64e-06 * T1 ** 2 + 5.03e-07 * T1 ** 3)
    MlPerigee=281.22083 + 4.70684e-05 * EpochDate + 0.000453 * T1 ** 2 + 3e-06 * T1 ** 3
    MeanAnom=np.mod((358.47583 + 0.985600267 * EpochDate - 0.00015 * T1 ** 2 - 3e-06 * T1 ** 3),360)
    Eccen=0.01675104 - 4.18e-05 * T1 - 1.26e-07 * T1 ** 2
    EccenAnom=MeanAnom
    E=0
    
    while np.max(abs(EccenAnom - E)) > 0.0001:

         E=EccenAnom
         EccenAnom=MeanAnom + np.degrees(Eccen)*(np.sin(np.radians(E)))
    #pdb.set_trace()     
    TrueAnom=2 * np.mod(np.degrees(np.arctan2(((1 + Eccen) / (1 - Eccen)) ** 0.5*np.tan(np.radians(EccenAnom) / 2),1)),360)
    EcLon=np.mod(MlPerigee + TrueAnom,360) - Abber
    EcLonR=np.radians(EcLon)
    DecR=np.arcsin(np.sin(ObliquityR)*(np.sin(EcLonR)))
    Dec=np.degrees(DecR)
    #pdb.set_trace()
    RtAscen=np.degrees(np.arctan2(np.cos(ObliquityR)*((np.sin(EcLonR))),np.cos(EcLonR)))
    
    HrAngle=LocAST - RtAscen
    HrAngleR=np.radians(HrAngle)

    HrAngle=HrAngle - (360*((abs(HrAngle) > 180)))
    SunAz=np.degrees(np.arctan2(- 1 * np.sin(HrAngleR),np.cos(LatR)*(np.tan(DecR)) - np.sin(LatR)*(np.cos(HrAngleR))))
    SunAz=SunAz + (SunAz < 0) * 360
    SunEl=np.degrees(np.arcsin((np.cos(LatR)*(np.cos(DecR))*(np.cos(HrAngleR)) + np.sin(LatR)*(np.sin(DecR))))) #potential error
    SolarTime=(180 + HrAngle) / 15
    
    Refract=[]

    for Elevation in SunEl:
        TanEl=np.tan(np.radians(Elevation))
        if Elevation>5 and Elevation<=85:
            Refract.append((58.1 / TanEl - 0.07 / (TanEl ** 3) + 8.6e-05 / (TanEl ** 5)))
        elif Elevation > -0.575 and Elevation <=5:
            Refract.append((Elevation*((- 518.2 + Elevation*((103.4 + Elevation*((- 12.79 + Elevation*(0.711))))))) + 1735))
        elif Elevation> -1 and Elevation<= -0.575:
            Refract.append(- 20.774 / TanEl)
        else:
            Refract.append(0)


    Refract=np.array(Refract)*((283 / (273 + var.temperature)))*(var.pressure) / 101325 / 3600


    SunZen=90-SunEl
    SunZen[SunZen >= 90 ] = 0 

    ApparentSunEl=SunEl + Refract

    DFOut=pd.DataFrame({'SunEl':SunEl}, index=var.Time)
    DFOut['SunAz']=SunAz-180  #Changed RA Feb 18,2014 to match Duffe
    DFOut['SunZen']=SunZen
    DFOut['ApparentSunEl']=ApparentSunEl
    DFOut['SolarTime']=SolarTime

    return DFOut
    