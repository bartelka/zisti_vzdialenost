import requests, re

fw = open("vzdialenosti_miest", "w", encoding="utf-8")
fr = open("hrany.txt", "r", encoding="utf-8")
hrany = [i.strip().split(";") for i in fr]


page = requests.get("http://www.kolko-km-je.ubytovaniesr.sk")
page.encoding = "windows-1250"

text = page.text
text = re.split("<option value=''>|</select>", text)
text = text[1].split("</option>")[1:-1]

obce = {}

for i in text:
    cislo = re.findall(r"(\d+)", i)
    obec = i.split(">")[1]
    obce[obec] = obce.get(obec, int(cislo[0]))

for i in hrany:
    data = {"obce1":obce[i[0]], "obce2":obce[i[1]]}
    vzdialenost = requests.post("http://www.kolko-km-je.ubytovaniesr.sk?a=a", data=data)
    vzdialenost.encoding = "windows-1250"
    fw.write(re.split("Odpoveď:|km,", vzdialenost.text)[1:-1][1].strip() + "\n")


