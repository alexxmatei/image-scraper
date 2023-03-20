import os


def mkDirAtCwdIfNoExist(folderName: str):
    folderPath = os.path.join(os.getcwd(), folderName)
    # Check if the folder exists
    if not os.path.exists(folderPath):
        # Create the folder
        os.mkdir(folderPath)
    return folderPath
