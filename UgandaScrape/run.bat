:: show the version of Window version
@echo off
ver

:: This is a batch command that associates an extension with a file type (FTYPE), displays existing associations,
:: or deletes an association
:: @echo off
:: assoc > D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape\lists.txt
:: assoc | find “.py” > D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape\listsdoc.txt

:: The following example shows how the cd command can be used in a variety of ways.
Rem The cd without any parameters is used to display the current working directory
@echo off
cd
Rem Changing the path to Program Files
cd\Program Files
cd
Rem Changing the path to Program Files
cd %USERPROFILE%
cd
Rem Changing to the parent directory
cd..
cd
Rem Changing to the parent directory two levels up
cd..\..
cd
Rem Changing back to the D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape
cd /d D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape
cd

:: This batch command run the UgandaDemo.py
@echo off
python UgandaDemo.py