import requests
import json
import os, sys
from acrcloud.recognizer import ACRCloudRecognizer


"""user_id = "4a6e87a41d2045dbbb603d14b23192bd"
client_secret="678b6935100e4f329c78e23d929930c3"


request_body = json.dumps({
    "name": "testeeeeekkkkk",
    "description": "tche bro ganda teste",
    "public": True
})
query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
response=requests.post(
    query,
    data=request_body,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format()
    }
)"""

if __name__ == '__main__':

    if(len(sys.argv) != 2):
        print("usage: sudo python muic-identifier.py <path>")
    else:
        music = ""
        config = {
            #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
            'host':'identify-eu-west-1.acrcloud.com',
            'access_key':'c20267418e799f23a3f94b14baf3a790', 
            'access_secret':'aiwwg7KPELXaWt9AwvfYv6IclZSCTndEltCftKjJ',
            'timeout':10 # seconds
        }
        re = ACRCloudRecognizer(config)
        while(1):
            os.system('sudo ./ripper.sh')


            json_data = json.loads(re.recognize_by_file("/tmp/aaa.mp3", 0))
            print(json.dumps(json_data))
            if(json_data["status"]["msg"] == "Success"):
                current_music = json_data["metadata"]["music"][0]["title"]
                if current_music != music:
                    f = open(sys.argv[1], "a")
                    music = current_music
                    print("vou escrever crl")
                    f.write(json_data["metadata"]["music"][0]["artists"][0]["name"])
                    f.write (" - ")
                    f.write(music)
                    f.write ("\n")
                    f.close()

            os.remove("/tmp/aaa.mp3")
            os.remove("/tmp/aaa.cue")
