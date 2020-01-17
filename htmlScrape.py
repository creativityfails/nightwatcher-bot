import requests
from bs4 import BeautifulSoup


def wotlabs_scrape(server, name, mod=None):
    url = 'https://wotlabs.net/' + server + '/player/' + name
    html = requests.get(url)

    soup = BeautifulSoup(html.content)

    table = soup.find(id="tankerStats")
    if table:
        table = table.find("tbody").find_all("tr")
        battles = table[0].find_all("td")[1].text.strip()
        if mod == '-r':
            wr = table[2].find_all("td")[12].text.strip()
            wn8 = table[13].find_all("td")[6].text.strip()
            return '*' + name + '* - battles: ' + battles + ', rWR: ' + wr + ', rWN8: ' + wn8 + ' - <' + url + '>'
        elif mod == "-d":
            wr = table[2].find_all("td")[4].text.strip()
            wn8 = table[13].find_all("td")[2].text.strip()
            if wr == "-":
                return 'no 24 hour stats for ' + name + ' - <' + url + '>'
            return '*' + name + '* - battles: ' + battles + ', 24hWR: ' + wr + ', 24hWN8: ' + wn8 + ' - <' + url + '>'
        else:
            wr = table[2].find_all("td")[2].text.strip()
            wn8 = table[13].find_all("td")[1].text.strip()
            return '*' + name + '* - battles: ' + battles + ', WR: ' + wr + ', WN8: ' + wn8 + ' - <' + url + '>'

    else:
        return 'Player not found - ' + name
