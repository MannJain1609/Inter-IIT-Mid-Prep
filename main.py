'''Inter IIT Mid-Prep Problem Statement
    Copyright (C) 2021  AstroAnalyzer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from branca.element import Figure

#create a title on web
st.markdown("<h1 style='text-align: center; color: white;'>ASTROANALYZER </h1>", unsafe_allow_html=True)

#create a base map
fig3=Figure(width=550,height=350)
m3=folium.Map(location=[-8.907970, 33.433200],

                        zoom_start=2,
                        tiles='https://api.mapbox.com/v4/mapbox.mapbox-incidents-v1/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZS1rIiwiYSI6ImNrbWwycnY1aTA5OXQycXJ6b3piZmRjdjAifQ.4sci1n22WrZvWaQL_99mrA',
                        attr='Mapbox'     
)
fig3.add_child(m3)

st.sidebar.title('Map Legend:')
st.sidebar.header('High Mass Binaries - Red')
st.sidebar.header('Low Mass Binaries - Blue')
st.sidebar.write('')
st.sidebar.title('Radius for plotted dots:')

#radius for plotted points
r=st.sidebar.slider(label='Slide this-',min_value=1,max_value=15,value=5)


#reading catalog B csv file
f1=pd.read_csv('catalog_B.csv')
#making the list of all columns in catalog B
f1_ra=list(f1['RA'])
f1_dec=list(f1['Dec'])
f1_srcname=list(f1['Source_Name'])
f1_Obs_start_date=list(f1['Observation_start_date'])
f1_obs_start_time=list(f1['Observation_start_time'])
f1_proposal_id=list(f1['Proposal_ID'])
f1_target_id=list(f1['Target_ID'])
f1_obs_id=list(f1['Observation_ID'])
f1_proposal_title=list(f1['Proposal_Title'])
f1_abstract=list(f1['Abstract'])
f1_prime_instrument=list(f1['Prime_instrument'])


#reading csv file of low mass binary containg GLAN, GLOT,RA and Dec in hour format
df_l=pd.read_csv('loc_low.csv',index_col=0)
#making the lists of columns in the file
glat_l=list(df_l['GLAT'])
glong_l=list(df_l['GLON'])
#converting ra and dec in deg
df_l_ra = list((df_l['RAh']+(df_l['RAm']/60)+(df_l['RAs']/3600))*15)
df_l_dec=list(df_l['DE_sign']*(df_l['DEd']+(df_l['DEm']/60)+(df_l['DEs']/3600)))


#read csv file of high mass binary containing GLAN, GLOT, RA and Dec in hour format
df_h=pd.read_csv('loc_high.csv')
#making list of columns in file
glat_h=list(df_h['GLAT'])
glong_h=list(df_h['GLON'])
#converting ra and dec into deg
df_h_ra = list((df_h['RAh']+(df_h['RAm']/60)+(df_h['RAs']/3600))*15)
df_h_dec=list(df_h['DE_sign']*(df_h['DEd']+(df_h['DEm']/60)+(df_h['DEs']/3600)))

#creating lists for low binary mass for latitude, longitude and publication
lt_l = []
ln_l = []
nm_l = []

#creating a publication list
publication_list=[]

#appending the tuples of all publications in list
for i in range(len(f1_ra)):
	x=(f1_Obs_start_date[i],f1_obs_start_time[i],f1_proposal_id[i],f1_target_id[i],f1_ra[i],f1_dec[i],f1_obs_id[i],f1_proposal_title[i],f1_abstract[i],f1_srcname[i],f1_prime_instrument[i])
	publication_list.append(x)

#comparing ra, dec in range of 0.001 and appending in lists if found same.
for lt, ln, ra, dec in zip(glat_l,glong_l,df_l_ra,df_l_dec):
    for RA, DEC, publication in zip(f1_ra,f1_dec,publication_list):
        temp_diff_ra = ra-RA
        temp_diff_dec = dec-DEC
        if ((-0.001<=temp_diff_ra <= 0.001)  and (-0.001<=temp_diff_dec<=0.001)) :
            lt_l.append(lt)
            ln_l.append(ln)
            nm_l.append(publication)

#creating lists for high binary mass for latitude, longitude and publication
lt_h = []
ln_h = []
nm_h = []

#comparing ra, dec in range of 0.001 and appending in lists if found same.
for lt, ln, ra, dec in zip(glat_h,glong_h,df_h_ra,df_h_dec):
    for RA, DEC, publication in zip(f1_ra, f1_dec, publication_list):
        temp_diff_ra = ra-RA
        temp_diff_dec = dec-DEC
        if ((-0.001<=temp_diff_ra <= 0.001)  and (-0.001<=temp_diff_dec<=0.001)) :
            lt_h.append(lt)
            ln_h.append(ln)
            nm_h.append(publication)


#reading the publications of astrosat data
publication_file=pd.read_csv('publications.csv')
#making the lists of all columns in publication_file
Title=list(publication_file['Title'])
Abstract=list(publication_file['Abstract'])
Authors=list(publication_file['Authors'])
Bib_code=list(publication_file['Bibliographic Code'])
Keywords=list(publication_file['Keywords'])

#create an empty pub list
pub_list=[]

#append the columns lists tuples in pub_list
for i in range(len(Title)):
    x=(Title[i],Abstract[i],Authors[i],Bib_code[i],Keywords[i])
    pub_list.append(x)

#plot a map
fg = folium.FeatureGroup(name="Sample Map")

#comparing to the detected values and showing lists of publications
for lt, ln in zip(glat_l,glong_l):
    for clt, cln, csr in zip(lt_l,ln_l,nm_l):
        if lt == clt and ln == cln:
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius=r, popup=folium.Popup(
                '<b>Observation start date:</b> ' + str(csr[0]) + '<br><b>Observation start time:</b> ' + str(
                csr[1]) + '<br><b>Proposal Id:</b> ' + str(csr[2]) + '<br><b>Target Id:</b> ' + str(csr[3]) + '<br><b>RA:</b> ' + str(
                csr[4]) + '<br><b>Dec:</b> ' + str(csr[5]) + '<br><b>Observation Id:</b> ' + str(
                csr[6]) + '<br><b>Source Name:</b> ' + str(csr[9]) + '<br><b>Prime Instrument:</b> ' + str(csr[10]),
            min_width=300, max_width=300),
                                     color='green', fill_color='green', fill_opacity=0.5,
                                     tooltip='<strong>Click here for more information</strong>'))
            for values in pub_list:
                if(csr[9] in values[0] or csr[9] in values[1]):
                    demo = pd.DataFrame([[values[0], values[1], values[2], values[3], values[4]]])
                    demo.to_csv('Pub.csv', mode='a', header=False)
                    fg.add_child(folium.CircleMarker(location=[lt, ln], radius=r,tooltip='<strong>Click here for publication details</strong>', popup='<a href="https://drive.google.com/file/d/1PyE1N4c2bFMiOtHL0s6Hoe5CfWYKEcD0/view?usp=sharing" target="blank">Click Here</a>'))
                    break
        else:
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius = r, popup=folium.Popup('Source not detected by AstroSat', min_width=300, max_width=300),
            color = 'blue',fill_color='blue',fill_opacity=0.5, tooltip='<strong>Click here for more information</strong>'))

                
#to plot a map
m3.add_child(fg)
#comparing to the detected values and showing lists of publications
for lt, ln in zip(glat_h,glong_h):
    for clt, cln, csr in zip(lt_h,ln_h,nm_h):
        if lt == clt and ln == cln :
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius=r, popup=folium.Popup(
                '<b>Observation start date:</b> ' + str(csr[0]) + '<br><b>Observation start time:</b> ' + str(
                    csr[1]) + '<br><b>Proposal Id:</b> ' + str(csr[2]) + '<br><b>Target Id:</b> ' + str(csr[3]) + '<br><b>RA:</b> ' + str(
                    csr[4]) + '<br><b>Dec:</b> ' + str(csr[5]) + '<br><b>Observation Id:</b> ' + str(
                    csr[6]) + '<br><b>Source Name:</b> ' + str(csr[9]) + '<br><b>Prime Instrument:</b> ' + str(csr[10]),
                min_width=300, max_width=300),
                                             color='green', fill_color='green', fill_opacity=0.5,
                                             tooltip='<strong>Click here for more information</strong>'))
            for values in pub_list:
                if (csr[9] in values[0] or csr[9] in values[1]):
                    demo = pd.DataFrame([[values[0], values[1], values[2], values[3], values[4]]])
                    demo.to_csv('Pub.csv', mode='a', header=False)
                    fg.add_child(folium.CircleMarker(location=[lt, ln], radius=12,tooltip='<strong>Click here for publication details</strong>',
                                                     popup='<a href="https://drive.google.com/file/d/1PyE1N4c2bFMiOtHL0s6Hoe5CfWYKEcD0/view?usp=sharing" target="blank">Click here</a>'))
                    break
        else:
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius = r, popup=folium.Popup('Source not detected by AstroSat', min_width=300, max_width=300),
            color = 'red',fill_color='red',fill_opacity=0.5, tooltip='<strong>Click here for more information</strong>'))


m3.add_child(fg)

#for background image
page_bg_img = '''
<style>
body {
background-image: url('https://free4kwallpapers.com/uploads/wallpaper/whte-lights-in-space-4k-wallpaper-1024x768-wallpaper.jpg');
background-size: cover;
textColor: red
}

</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
#for sidebar background
st.markdown(
    """
<style>
.css-1aumxhk {
background-color: none;
background-image: url('https://cdn.pixabay.com/photo/2020/11/07/01/30/abstract-5719281_960_720.jpg');
color: black

}
</style>
""",
    unsafe_allow_html=True,
)

st.set_option('deprecation.showPyplotGlobalUse', False)

#to show folium map on webpage
folium_static(m3)
