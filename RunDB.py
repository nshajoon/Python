import requests, mysql.connector
from bs4 import BeautifulSoup
import numpy as np

cnx =  mysql.connector.connect(user='root', password='Friendly20*')
cursor = cnx.cursor()
DB_NAME = 'CarDB'
#cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
cursor.execute("USE {}".format(DB_NAME))

#cursor.execute("CREATE TABLE info(name VARCHAR(30) NOT NULL, price INT(11) NOT NULL, mileAge INT(11) NOT NULL, color VARCHAR(20) NOT NULL)")

page = 1

while page<20:
    p = str(page)
    r = requests.get('https://www.truecar.com/used-cars-for-sale/listings/location-newton-falls-oh/?page={}'.format(p))
    soup = BeautifulSoup (r.content, 'html.parser')
    res = soup.find_all('li', attrs={"class":"margin-top-3 d-flex flex-grow col-md-6 col-xl-4"})
    for item in res:
        temp = item.find('span', attrs={'class':'vehicle-header-make-model'}).text
        temp = temp.split(' ') 
        name=temp[1]
        temp=[]
        #        
        temp = item.find('div', attrs={'data-test':'vehicleListingPriceAmount'}).text
        temp = temp[1:]
        price = int(temp.replace(',',''))
        temp = []
        temp = item.find('div', attrs={'data-test':'vehicleCardColors'}).text
        temp = temp.split(' ')
        color = temp[0]
        temp = []
        temp = item.find('div', attrs={'data-test':'vehicleMileage'}).text
        temp= temp.split(' ')
        mileAge = int (temp[0].replace(',',''))
        query= "SELECT * FROM info"
        vals=(name, price, mileAge, color)
        cursor.execute(query)
        records = cursor.fetchall()
        if np.where(records[0]==vals)[0].size==0:        
            query = "INSERT INTO info(name, price, mileAge, color) VALUES (%s, %s, %s, %s) "
            cursor.execute(query,vals)
            cnx.commit()
    page+=1 

    
    
