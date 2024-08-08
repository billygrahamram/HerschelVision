import os

history_path = os.path.join('resources/history', 'img_dir_record.txt')
recent_file_path = os.path.join('resources/history', 'recentFiles.txt')
lightThemeImgPath = 'resources/images/welcomeLight.png'  #this image is showed where a hsi image will be showed.
darkThemeImgPath = 'resources/images/welcomeDark.png'
aboutImgpath= 'resources/images/about.png'

# we can make this values to read from specific file
noOfBandsEMR = 224
firstBandEMR = 300
lastBandEMR =  1000
spectralResolution = 5