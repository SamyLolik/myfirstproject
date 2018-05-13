import const
import requests



def main():
    print(get_places_info('ChIJg6pGoEtKtUYRUGCYdZWDin0'))



def get_places_info(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' \
          + str(place_id) + '&language=ru&key=' + const.GOOGLE_API_KEY
    info = requests.get(url).json()
    print(info)
    return {
        'name': info['result']['name'],
        'address': info['result']['formatted_address'],
        'phone': info['result']['international_phone_number'],
        'location': str(info['result']['geometry']['location']['lat'])\
                    + ',' \
                    + str(info['result']['geometry']['location']['lng']),
        'opening_hours': info['result']['opening_hours']['weekday_text'],
        'rating': info['result']['rating'],
        'website': info['result']['website']
    }


if __name__ == '__main__':
    main()
