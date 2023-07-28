import requests
from bs4 import BeautifulSoup


URL = "https://gtahash.ru/?c=Doors%20and%20Gates&page="
doors = []

validPage = True
p=1
endmsg = ""
while validPage:
    r = requests.get(URL+str(p))
    soup = BeautifulSoup(r.text, 'html.parser')
    bod = soup.select(".card-body > table > tbody")
    validPage = len(bod) != 0
    print("CURRENT PAGE: %s (valid page? %s)" % (p, validPage))
    i=1
    for e in bod:
        try:
            doors.append(int(e.find_all("td")[3].text.rstrip()))
        except:
            endmsg += "[PAGE:%s;ENTITY:%s] > door has no hash [PROPNAME: %s]\n" % (p, i, e.find_all("td")[1].text.rstrip().lstrip())
        i+=1
    p+=1

i=1
lines = ""
for door in doors:
    lines += "\t[%s]= %s,\n" %(i, str(door))
    i+=1

print("\n\n"+endmsg+"\n\n")
print("amount of hashes: " + str(len(doors)))

with open("doors.lua", "w") as f:
    f.write("local doorhashes = {\n%s}" % lines)

print("hashes written to './doors.lua'")
