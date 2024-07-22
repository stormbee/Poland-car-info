**Telegram Bot for Vehicle History Reports (Polish)**

This Telegram bot automates the process of generating vehicle history reports from the Polish government website historiapojazdu.gov.pl. It interacts with users through a user-friendly interface and provides generated reports in PDF format.

### Features:

- **User-friendly interface with inline keyboard buttons for easy interaction.**
- **Secure data handling:** user credentials are not stored by the bot.
- **Supports searching by vehicle registration plate, VIN, and registration date.**
- **Generates reports in PDF format for easy sharing and record-keeping.**
- **Written in Python using the aiogram library.**

### Prerequisites:

- **A Telegram account**
- **Python 3.x installed**
- **Telegram bot token** (see "Installation" section)

### Dependencies:

- aiogram
- bs4
- selenium
- reportlab

### Installation:

#### Create a Telegram Bot:

1. Visit the BotFather in Telegram (@BotFather) and create a new bot.
2. Follow the instructions to obtain your bot's token.

#### Install Dependencies:

```bash
pip install -r requirements.txt
```
### Clone or Download the Repository:

```bash
git clone https://github.com/stormbee/Poland-car-info.git
```

### Configure the Bot:

Create the `.env` file in a text editor.
Add `YOUR_BOT_TOKEN` with your actual bot token obtained from BotFather to variable `TOKEN` in `.env`.
`TOKEN = "YOUR_BOT_TOKEN"`
Optionally, adjust other settings in the code (e.g., language strings).

### Run the Bot:

```bash
python bot.py
```

### Usage:

Open Telegram and start a chat with your bot.
You'll receive a welcome message with instructions.
Follow the prompts to enter the vehicle's registration plate, VIN, and registration date (DD.MM.YYYY format).
Once you confirm, the bot will search for the vehicle history and generate a PDF report.
If successful, the bot will send you the generated PDF report as a downloadable document.

### Security:

The bot does not store any user credentials, including vehicle data, on its servers.
It interacts with the Polish government website directly using Selenium and parses the response using BeautifulSoup.
Exercise caution when sharing generated reports, as they may contain sensitive information about the vehicle.

### Disclaimer:

This bot is provided for informational purposes only. The accuracy and completeness of the data retrieved from the government website cannot be guaranteed. It's recommended to double-check the information with official sources.

### Contributing:

We welcome contributions to improve this bot. Please feel free to fork the repository, make changes, and submit pull requests.

### License:

This bot is licensed under the MIT License. See the LICENSE file for details.


