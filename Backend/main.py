from server import app
import os


# Launch Server
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    app.run(debug=True)