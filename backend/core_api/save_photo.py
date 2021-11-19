from imgurpython import ImgurClient

client_id = '9272a9bd8cdeff3'
client_secret = '849aab6f299ab1183701cfba11f70a87bc2632fc'
access_token = 'a4d5e6f6aac81fac3804e67ffb5ce9a642534b15'
refresh_token = '2e9f1788610434401ca83eee84a40411d65a599c'

client = ImgurClient(client_id, client_secret, access_token, refresh_token)


def save_photo(byte):
    with open('temp', 'wb') as file:
        file.write(byte)
    url = client.upload_from_path('temp', config=None, anon=True)
    return url['link']

