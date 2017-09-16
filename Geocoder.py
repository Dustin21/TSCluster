import numpy as np
import requests
import json
import csv


class Geocoder:

    def __init__(self, x):
        self.x = x

    def submit_request(self):

        def as_complex(dct):
            if '__complex__' in dct:
                return complex(dct['real'], dct['imag'])
            return dct

        def create_url(address):
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
            comp_url = base_url + str(address)
            return comp_url

        def send_request(url):
            resp = requests.get(url).text
            _data = json.loads(resp, object_hook=as_complex)
            return _data

        def extract_geocoordinates(_id, data):
            geom = data['results'][0]['geometry']
            loc_type = geom['location_type']
            lat = geom['location']['lat']
            lng = geom['location']['lng']
            return [_id, lat, lng, loc_type]

        def is_okay(_id, request):
            coords = extract_geocoordinates(_id, request)
            return coords

        def is_denied():
            print("Request has been declined.")
            exit(1)

        def is_zero(_id, _request, iterator):
            _url = create_url(self.x.ADDRESS_DROP_PC[iterator])
            _request = send_request(_url)
            if _request['status'] == 'OK':
                return is_okay(_id, _request)
            elif _request['status'] == 'ZERO_RESULTS':
                _url = create_url(self.x.ADDRESS_DROP_CITY[iterator])
                _request = send_request(_url)
                if _request['status'] == 'OK':
                    return is_okay(_id, _request)
                elif _request['status'] == 'ZERO_RESULTS':
                    _url = create_url(self.x.ADDRESS_DROP_ST[iterator])
                    _request = send_request(_url)
                    if _request['status'] == 'OK':
                        return is_okay(_id, _request)
                    elif _request['status'] == 'ZERO_RESULTS':
                        return [_id, np.nan, np.nan, np.nan]
                    elif _request['status'] == 'OVER_QUERY_LIMIT' or _request['status'] == 'REQUEST_DENIED':
                        return is_denied()
                elif _request['status'] == 'OVER_QUERY_LIMIT' or _request['status'] == 'REQUEST_DENIED':
                    return is_denied()
            elif _request['status'] == 'OVER_QUERY_LIMIT' or _request['status'] == 'REQUEST_DENIED':
                return is_denied()

        # initialie csv file to append to
        f = open('data/geocode_batches/geocode_batch_0.csv', 'a')
        ff = csv.writer(f, delimiter=',', lineterminator='\n')
        counter = 0

        for i in range(self.x.shape[0]):
            # if i=1000 then re-initialize new file to append to
            if (i % 5) == 0 and i > 0:
                counter += 1
                f.close()
                f = open('data/geocode_batches/geocode_batch_' + str(counter) + '.csv', 'a')
                ff = csv.writer(f, delimiter=',', lineterminator='\n')

            # create url
            __url = create_url(self.x.FULL_ADDRESS[i])
            __id = self.x.USDPID[i]

            # send request to api
            __request = send_request(__url)

            # extract data
            if __request['status'] == 'OK':
                temp = is_okay(__id, __request)
                # foo.append(temp)
                ff.writerow(temp)
                print(temp)

            elif __request['status'] == 'ZERO_RESULTS':
                temp = is_zero(__id, __request, i)
                # foo.append(temp)
                ff.writerow(temp)
                print(temp)

            elif __request['status'] == 'OVER_QUERY_LIMIT' or __request['status'] == 'REQUEST_DENIED':
                is_denied()
