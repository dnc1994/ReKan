c:\python27\scripts\pyinstaller -c -F src\gen_couplets.py

mkdir submit
mkdir submit\src
mkdir submit\data
mkdir submit\corpus

copy src\*.py submit\src\
copy data\* submit\data\*
copy dist\gen_couplets.exe submit\ReKan.exe
copy corpus\corpus.zip submit\corpus\corpus.zip
copy report\report.pdf submit\

pause