### flower_boutique_bot


## Introduction
This Telegram bot allows users to browse and order different types of flowers from the flower shop.   
It also provides an admin panel for managing orders, users, prices, and sending announcements to users.

## Features
- **User Features**:
  - Browse and order flowers
  - Choose between Ukrainian and English languages
  - Receive help using the bot

- **Admin Features**:
  - Authentication for accessing admin panel
  - View orders and users
  - Modify prices or photos of bouquets
  - Send announcements to users
  

## Project Structure:
```
├── .github
│   ├── workflows
│       └── github-actions.yml
├── Flower_Bot
│   ├── database
│       └── __init__.py
│       └── sqlite_db_user.py
│   ├── handlers
│       └── admins
│           └── __init__.py
│           └── admin.py
│       └── eng_users
│           └── __init__.py
│           └── english_each_bouquet.py
│       └── ukr_users
│           └── __init__.py
│           └── backs.py
│           └── comment.py
│           └── each_bouquet.py
│           └── inline_handlers.py
│           └── purchase.py
│           └── states.py
│       └── __init__.py
│   ├── imgs
│   ├── keyboards
│       └── inline
│           └── __init__.py
│           └── callback_datas.py
│           └── choice_inline_buttons.py
│           └── english_choise_inline_buttons.py
│       └── reply
│           └── __init__.py
│           └── choise_reply_buttons.py
│           └── english_choise_reply_buttons.py
│       └── __init__.py
│   ├── prompts
│       └── __init__.py
│       └── generator.py
│   ├── tests
│       └── __init__.py
│   ├── app.py
│   ├── loader.py
│ 
├── .env.example
├── .gitignore
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── README.md
```
Flower_Bot: Main module or package for the flower shop bot.  
Handlers: Contains handlers for various user interactions.  
Keyboards: Holds definitions for different keyboard layouts used in the bot.  
Database: Likely contains database-related code or utilities.  
Tests: For testing your bot functionality.  
Img: Stores images used in the bot.  

## Code Style Tools
- **Black** (Version 23.9.1): Black is a Python code formatter that reformats your code to ensure a consistent style throughout your codebase.
- **Mypy** (Version 1.5.1): Mypy is an optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing.
- **Deptry** (Version 0.12.0): Deptry is a dependency management tool for Python that helps in managing and documenting your project's dependencies.


## Dependencies
- Python 3.7 or higher
- [Poetry](https://python-poetry.org/)
- aiogram
- sqlite3

## Getting Started

### Environment Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/oksanaaam/flower_boutique_bot.git

2. **Set up your environment variables:** 
   ``` 
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
   
Copy the values from the .env.example and fill in the required values:  

TOKEN= telegram token for using bot
PASSWORD= admin password for managing admin panel
ADMIN_ID= telegram id user which could manage orders and users

### Dependency Installation

1. Install Poetry:
   ```
   pip install poetry
   
2. Install project dependencies:
   ```
   poetry install

### Running the Server
1. Start the server:
   ```
   cd Flower_Bot
   poetry run python app.py

To use the bot, follow these steps:  
1. Start the bot by typing `/start`.
2. Choose your preferred language.
3. Browse the menu to select the type of bouquet.
4. Follow the prompts to complete the order process.

## Admin Panel
To access the admin panel:  
1. Type `/admin` to authenticate as an admin.
2. Use the provided commands to manage orders, users, and settings.

## Commands
- `/start`: Start the bot and select language.
- `/admin`: Access the admin panel.
- `/help`: Openai assistant get help with answers about the Flower Shop.
