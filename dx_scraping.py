import requests
from bs4 import BeautifulSoup
import os
import logging
import constants

logging. basicConfig(filename="draft.log")
logger = logging.getLogger("DX_STATS")

file_name = 'dx_stats.csv'


def get_player_specs(player_url):
    page = requests.get(player_url)
    soup = BeautifulSoup(page.text)
    player_dict = dict()

    return player_dict


def format_for_csv(player_data_dict):
    csv_row_list = []
    for player in player_data_dict:
        row_str = ""
        row_str = "2017,,"
        row_str += player + ","
        player_row = player_data_dict[player]

        # Get player specs
        player_specs_dict = get_player_specs(player_row['url'])

        #TODO: stuff that I don't have yet
        for i in range(6):
            row_str += ","

        # Actual data
        row_str += player_row['gp'] + ","
        row_str += player_row['min'] + ","
        fgm = float(player_row['2pm']) + float(player_row['3pm'])
        fga = float(player_row['2pa']) + float(player_row['3pa'])
        row_str += str(fgm) + ","
        row_str += str(fga) + ","
        row_str += str(round(fgm/fga, 3)) + ","
        row_str += player_row['2pm'] + ","
        row_str += player_row['2pa'] + ","
        row_str += str(round(float(player_row['2p%'].rstrip("%"))/100, 3)) + ","
        row_str += player_row['3pm'] + ","
        row_str += player_row['3pa'] + ","
        row_str += str(round(float(player_row['3p%'].rstrip("%"))/100, 3)) + ","
        row_str += player_row['ftm'] + ","
        row_str += player_row['fta'] + ","
        row_str += str(round(float(player_row['ft%'].rstrip("%"))/100, 3)) + ","
        row_str += player_row['treb'] + ","
        row_str += player_row['ast'] + ","
        row_str += player_row['stl'] + ","
        row_str += player_row['blk'] + ","
        row_str += player_row['to'] + ","
        row_str += player_row['pf'] + ","
        row_str += player_row['pts'] + ","
        #row_str +=

        # End of row
        row_str += "\n"
        csv_row_list.append(row_str)

        # print blank nba stats
        #TODO: figure out right number of columns
        for i in range(28):
            row_str += ","

    return csv_row_list


def get_dx_stats():

    # Get page soup
    page = requests.get(constants.dx_url.format(constants.dx_versions[0]))
    soup = BeautifulSoup(page.text, 'lxml')

    # Get table
    try:
        table = soup.find('table')
        rows = table.find('tbody').find_all('tr')

    except Exception as e:
        logger.error("Exception getting rows from page: {0}".format(e))
        raise(e)

    player_data_dict = dict()
    for row in rows:
        player_name = row.find("td", class_="text key").text
        columns = row.find_all("td")
        player_dict = {
            "tm": columns[3].text.strip(),
            "gp":  columns[4].text,
            "min": columns[5].text,
            "pts": columns[6].text,
            "2pm": columns[7].text,
            "2pa": columns[8].text,
            "2p%": columns[9].text,
            "3pm": columns[10].text,
            "3pa": columns[11].text,
            "3p%": columns[12].text,
            "ftm": columns[13].text,
            "fta": columns[14].text,
            "ft%": columns[15].text,
            "oreb": columns[16].text,
            "dreb": columns[17].text,
            "treb": columns[18].text,
            "ast": columns[19].text,
            "stl": columns[20].text,
            "blk": columns[21].text,
            "to": columns[22].text,
            "pf": columns[23].text,
        }
        player_data_dict[player_name] = player_dict

    # Format for writing
    output_rows = format_for_csv(player_data_dict)

    # Write to file
    with open(file_name, 'w') as file:
        for header in constants.stats_header:
            file.write(header)
            file.write(',')
        file.write('\n')
        for row in output_rows:
            file.write(row)
        file.close()
    return None

if __name__ == "__main__":
    if file_name in os.listdir(os.getcwd()):
        os.remove(os.getcwd() + "/" + file_name)

    get_dx_stats()