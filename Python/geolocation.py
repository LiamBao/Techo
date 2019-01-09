
# from geopy.geocoders import Nominatim


# geolocator = Nominatim(user_agent="huhuserver")
# location = geolocator.reverse("31.23211587946230, 121.47525873664082")
# print(location.address)

import urllib
import hashlib

AK='cseItsSwPiOe7GVnrRvi50mcHWkSaAmx'
SK='KwhxcA4OhGIioOKPDBLV4fQFbzuSLfsm'

import requests
def area2coor(area):
    try:
        address = area
        url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address  + '&output=json&ak=' + AK
        # url = urllib.quote(url, safe="/:=&?#+!$,;'@()*[]")
        json_data = requests.get(url=url).json()
        coor_loc = json_data['result']
        print(coor_loc)
    except Exception as e:
        print(e)
        pass # 不换ak多半都是 'nocoor'

area2coor('上海市,徐汇区,天钥桥路93-2号大龙火锅')