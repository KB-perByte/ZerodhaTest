import zipfile, requests, io, csv, redis
from datetime import date ,datetime , timedelta
from bs4 import BeautifulSoup
#import redis

def gen_fileName():
    ''' generates filename for url as well gives date for which file is fetched '''
    date_today = datetime.strftime(datetime.now() - timedelta(1), '%d%m%y')
    url_file_name = 'EQ'+str(date_today)+'_CSV'
    file_name = url_file_name.replace('_','.')
    return url_file_name, file_name , date_today

_name_url, _file_name , _date = gen_fileName()

print("Looking at yesterday's data: " , _date)
url = 'https://www.bseindia.com/download/BhavCopy/Equity/{}.ZIP'.format(_name_url)

resonse = requests.get(url)
zip_file = zipfile.ZipFile(io.BytesIO(resonse.content))
zip_file.extractall('csv_stored')

redisClient = redis.StrictRedis(host='localhost',
                                port=6379,
                                db=0)

with open('csv_stored/'+ _file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0 
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1 
        else:            
            redisClient.hmset(int(row[0]), {"Name": str(row[1]), "Open": float(row[4]), "High": float(row[5]), "Low": float(row[6]), "Close": float(row[7]) })
            #print(f'\t Code : {row[0]} Name : {row[1]} Open : {row[4]} High : {row[5]} Low : {row[6]} Close : {row[7]} ')
            line_count += 1
    print(f'Processed {line_count} lines.')

retrive_stocks = redisClient.keys(pattern='*')
print (retrive_stocks)

TARGET_URL = 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx'

def getBhavCopy():
    _page = requests.get(TARGET_URL)
    soup_obj = BeautifulSoup(_page.content,'lxml')
    zip_uri = soup_obj.find('li').contents[1].attrs.get('href')
    zip_file = requests.get(zip_uri)
    z = zipfile.ZipFile(io.BytesIO(zip_file.content))
    z.extractall('zips')
    return str('csv_stored' + '/' + z.namelist()[0])

def saveToRedis():
    #r = redis_conn()
    #r.flushall()
    csv_values = csv.DictReader(open(getBhavCopy(), 'r'))
    for row in csv_values:
        print (row['SC_NAME'].rstrip(), dict(row))
        #r.hmset(row['SC_NAME'].rstrip(), dict(row))
    #r.set('scrape_date',str(datetime.today().date().day))

saveToRedis()
### -- copy code ------------------------------------END