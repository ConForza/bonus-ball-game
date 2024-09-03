# imports
from bs4 import BeautifulSoup
import requests
import json
import os


# National Lottery past results page
URL = "https://www.national-lottery.co.uk/results/lotto/draw-history"

# Initialise browser access
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
}

# Scrape all results from draw history page
response = requests.get(
    url=URL,
    headers=headers,
)
results_page = response.text
winners = []

# If the bonus ball json file has data in, load it, else load the template of user numbers and copy to file
if os.path.getsize("bonus_balls.json") > 0:
    with open("bonus_balls.json", mode="r") as file:
        data = json.load(file)
else:
    with open("bonus_ball_start.json", mode="r") as file:
        data = json.load(file)
    with open("bonus_balls.json", mode="w") as file:
        file.write(json.dumps(data))

# Parse latest bonus ball
soup = BeautifulSoup(results_page, "html.parser")
numbers = soup.select(selector=".table_cell_4 .table_cell_block")
for number in numbers[0:1]:
    bonus_ball = int(number.getText().replace(" ", "").strip())

# Log this week's bonus ball number
print("Bonus ball: " + str(bonus_ball))

# Iterate each player. If they have a matching bonus ball, delete this from the array
# If there are no numbers left, the player has won. Add them to the winners list
for player in data:
    for number in player["numbers"]:
        if bonus_ball == number:
            player["numbers"].remove(bonus_ball)
        if not player["numbers"]:
            winners.append(player)

# If there are winners, log the winning players. Copy the template file ready to restart the game
if winners:
    print("Winners this week: " + str(winners))
    with open("bonus_ball_start.json", mode="r") as file:
        copy_data = json.load(file)
    with open("bonus_balls.json", mode="w") as file:
        file.write(json.dumps(copy_data))
# If no winners, save updated list after this week's bonus ball removals
else:
    with open("bonus_balls.json", mode="w") as file:
        file.write(json.dumps(data))




