To compile your own executable.

Step 1: Clone the repository to an empty folder *example /desktop/LolChampionRandomizer

Step 2: Make sure you have pyinstaller

Step 3: Using a terminal of your choice, paste the following (making sure to adjust the paths of the data added to where it is located on your device)

      pyinstaller --name BlueshellChampionRandomizer --uac-admin --onefile --windowed --icon=icon.ico --add-data "C:\Users\***\***\sounds.wav";. --add-data "C:\***\***\icon.ico";. --add-data "C:\***\***\blueshellbitmap.png";. BlueshellChampionRandomizer.py

Step 4: Navigate to the executable within the /dist folder

BlueshellChampionRandomizer.exe should be ready and available to use. It will ask permission to make changes to your computer, but that is so that it can read/write to a .json folder so that win/loss data persists after program exit.

Please reach out if you need assistance!
