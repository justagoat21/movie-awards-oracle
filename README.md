
# Movie Awards Oracle

A desktop application that connects to a remote MySQL database and provides an interface to manage and analyze Oscar and nomination data related to movies and staff members.

## Features

- 🎬 Register a user account
- 🏆 Add a new user nomination for a staff member for a given movie
- 📜 View existing nominations for the user
- 🌟 View top nominated movies by system users (by category/year)
- 🎭 Show total nominations and Oscars for a given director, actor, and singer
- 🌍 Show top 5 birth countries for actors who won Best Actor
- 🗺️ Show all nominated staff from a given country
- 🎥 Dream Team: Best living cast (director, actors, producer, singer)
- 🏢 Top 5 production companies by Oscars won
- 🌐 List all non-English speaking Oscar-winning movies with year

## Requirements

- Python 3.7 or higher
- MySQL database connection
- Required Python packages:
  - pymysql
  - pyinstaller (for building the executable)

## Installation

### From Source

1. Clone this repository
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
python src/main.py
```

### From Executable

1. Download the latest release
2. Run the .exe file (Windows) or application bundle (macOS)

## Building the Executable

To build the executable yourself:

```
python build.py
```

This will create an executable in the `dist` folder.

## Database Connection

The application connects to a MySQL database with the following details:

- Host: sql7.freesqldatabase.com
- Database: sql7774986
- User: sql7774986
- Port: 3306

(Note: Password is stored in the application code)

## Project Structure

- `src/main.py`: Main application entry point
- `src/gui.py`: User interface components
- `src/database.py`: Database connection and query functions
- `src/models.py`: Data models
- `src/utils.py`: Utility functions
- `build.py`: Script for building the executable

## License

This project is open-source software.
