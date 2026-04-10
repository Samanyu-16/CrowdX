import geocoder

def get_location():

    try:
        g = geocoder.ip('me')

        if g.ok:
            lat, lng = g.latlng
            return lat, lng
        else:
            return None, None

    except:
        return None, None