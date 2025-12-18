import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--add-data', 'icon1.ico;.',
    'KodeArrow.py'
])
