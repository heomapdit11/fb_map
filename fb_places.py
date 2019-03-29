#!/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import json
import time

def find_places_fb(L, S, R):
    '''Tìm các địa điểm S trong bán kính R tại vị trí L
    '''
    with open('mapapi', 'r')  as f:
        API_KEY = f.read()
    # lấy lat và lng từ googlemap
    ses_location = requests.session()
    req_location = ses_location.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}'.format(L, API_KEY))
    location_json = json.loads(req_location.text)
    lat = location_json['candidates'][0]['geometry']['location']['lat']
    lng = location_json['candidates'][0]['geometry']['location']['lng']
    location = '{}, {}'.format(lat, lng)
    with open('facebooktoken', 'r') as f:
        TOKEN_FB = f.read()
    addr_final = ''
    tmp_1 = {'type': 'FeatureCollection', 'features': []}
    n = 1
    next_page_key = ['']
    i = 0
    while(i < len(next_page_key)):
        try:
            API_LINK = 'https://graph.facebook.com/v3.2'
            API_FIELD = '/search?type=place&q={}&center={}&distance={}&fields=name,link,location&access_token={}&after={}'.format(S, location, R, TOKEN_FB, (next_page_key[i]))
            SES_FB = requests.session()
            REQ_FB = SES_FB.get('{}{}'.format(API_LINK, API_FIELD))
            JSON_FB = json.loads(REQ_FB.text)
            for data in JSON_FB['data']:
                try:
                    name = data['name']
                    web = data['link']
                    location_lat = data['location']['latitude']
                    location_long = data['location']['latitude']
                    location_FB = location_lat + location_long
                    id_fb = data['id']
                    addr_fb = data['location']['street']
                    tmp_2 = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [data['location']['longitude'],data['location']['latitude']]}, 'properties': {'Address': addr_fb, 'name': name}}
                    tmp_1['features'].append(tmp_2)
                except KeyError:
                    addr_fb = None
                addr_final += "Đây là {} thứ {} có tên: {}\n\tID: {}\n\tWebsite: {}\n\tĐịa chỉ: {}\n".format(S, n, name, id_fb, web, addr_fb)
                n +=1
                
            after_key = JSON_FB['paging']['cursors']['after']
            next_page_key.append(after_key)
            time.sleep(5)
            i += 1
        except KeyError:
            break
    with open('mapfb.geojson', 'w', encoding='utf-8') as f:
        json.dump(tmp_1, f, ensure_ascii=False, indent= 4)
    return addr_final
def main():
    '''Xử lý import
    '''
    addr = input("Nhập địa chỉ tìm kiếm: ")
    search = input("Bạn muốn tìm gì từ địa chỉ trên: ")
    radius = input("Vùng tìm kiếm (m): ")
    print("Hệ thống đang tìm kiếm!!!")
    print(find_places_fb(addr, search, radius))
if __name__ == "__main__":
    main()