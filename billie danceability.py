import requests
import pandas as pd

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQArjS-7LXj0niEbH0A0ICnJy1kAjqboEt9wJyVsIABzwO4ZasOJk7UBgIj-n7068EM_ICdosl5741eXZZQwLAMio1bFLX3kcfI0RUpC2TnRLPa5NOT-Nr_3bLC1BFbiIe8cbv3QSXia7PfCDDd_qBDlmauuffgKhVNwv83s0crR2ALDo64X4hzIVIfovaGkrrY',
}
        

searchBillieID = str("https://api.spotify.com/v1/search?q=Billie%20Eilish&type=artist&market=AR&limit=1")
billieIDPageResponse = requests.get(searchBillieID,headers=headers)
billieIDResponseJSON = billieIDPageResponse.json()
billiesID = billieIDResponseJSON['artists']['items'][0]['id']


getBilliesAlbums = str(f"https://api.spotify.com/v1/artists/{billiesID}/albums?include_groups=album,single&market=AR&limit=50")
billieAlbumsPageResponse = requests.get(getBilliesAlbums,headers=headers)
billieAlbumsIDResponseJSON = billieAlbumsPageResponse.json()
billieAlbumsList = []
for album in range(len(billieAlbumsIDResponseJSON['items'])):
    billieAlbumsDict = {}
    billieAlbumsDict['id'] = billieAlbumsIDResponseJSON['items'][album]['id']
    billieAlbumsDict['name'] = billieAlbumsIDResponseJSON['items'][album]['name']
    billieAlbumsDict['type'] = billieAlbumsIDResponseJSON['items'][album]['type']

    billieAlbumsList.append(billieAlbumsDict)

"""
billieAlbumsListImproved = []
for x in range(len(billieAlbumsList)):
    if billieAlbumsList[x]['id'] == '0JGOiO34nwfUdDrD612dOp' or billieAlbumsList[x]['id'] == '0S0KGZnfBGSIssfF54WSJh' or billieAlbumsList[x]['id'] == '1YPWxMpQEC8kcOuefgXbhj' or billieAlbumsList[x]['id'] == '2kzPJWrTjVKEYWWhowXLnz' or billieAlbumsList[x]['id'] == '4i3rAwPw7Ln2YrKDusaWyT' or billieAlbumsList[x]['id'] == '7fRrTyKvE4Skh93v97gtcU' or billieAlbumsList[x]['id'] == '4iyJ8i3eKbez8JXDbsHIdZ':
        billieAlbumsListImproved.append(billieAlbumsList[x])
"""

billieAlbumsIDS = [billieAlbumsList[x]['id'] for x in range(len(billieAlbumsList))]

billieAlbumsTracksList = []
for id in billieAlbumsIDS:
    getBilliesAlbumsTracks = str(f"https://api.spotify.com/v1/albums/{id}/tracks?market=AR&limit=50")
    billieAlbumsTracksPageResponse = requests.get(getBilliesAlbumsTracks,headers=headers)
    billieAlbumsTracksResponseJSON = billieAlbumsTracksPageResponse.json()

    for track in range(len(billieAlbumsTracksResponseJSON['items'])):
        billieTracksDict = {}
        billieTracksDict['id'] = billieAlbumsTracksResponseJSON['items'][track]['id']
        billieTracksDict['name'] = billieAlbumsTracksResponseJSON['items'][track]['name']
        billieTracksDict['type'] = billieAlbumsTracksResponseJSON['items'][track]['type']

        billieAlbumsTracksList.append(billieTracksDict)

billieTracksIDS = [billieAlbumsTracksList[x]['id'] for x in range(len(billieAlbumsTracksList))]

getBilliesTracksInfo = str(f"https://api.spotify.com/v1/audio-features?ids={','.join(billieTracksIDS[:100])}")
billieTracksInfoPageResponse = requests.get(getBilliesTracksInfo,headers=headers)
billieTracksInfoResponseJSON = billieTracksInfoPageResponse.json()

billieTracksInfoList = []
for track in range(len(billieTracksInfoResponseJSON['audio_features'])):
        billieTracksInfoDict = {}
        billieTracksInfoDict['id'] = billieTracksInfoResponseJSON['audio_features'][track]['id']
        billieTracksInfoDict['danceability'] = billieTracksInfoResponseJSON['audio_features'][track]['danceability']
        billieTracksInfoDict['energy'] = billieTracksInfoResponseJSON['audio_features'][track]['energy']
        billieTracksInfoDict['tempo'] = billieTracksInfoResponseJSON['audio_features'][track]['tempo']



        billieTracksInfoList.append(billieTracksInfoDict)

for track in range(len(billieAlbumsTracksList)):
    for info in range(len(billieTracksInfoList)):
        if billieAlbumsTracksList[track]['id'] == billieTracksInfoList[info]['id']:
            billieAlbumsTracksList[track]['danceability'] = billieTracksInfoList[info]['danceability']
            billieAlbumsTracksList[track]['energy'] = billieTracksInfoList[info]['energy']

for x in range(len(billieAlbumsTracksList)):
    billieAlbumsTracksList[x]["(energy + danceability)/ 2"] = (billieAlbumsTracksList[x]["energy"] + billieAlbumsTracksList[x]["danceability"]) / 2


pdRawFromJSON = pd.DataFrame(billieAlbumsTracksList)


finalDataFrame = pdRawFromJSON.loc[:,["name","type",
    "danceability","energy","(energy + danceability)/ 2"]] \
    .where(pdRawFromJSON["(energy + danceability)/ 2"] > 0.5) \
    .dropna() \
    .sample(frac=1) \
    .reset_index(drop=True)

print(finalDataFrame)