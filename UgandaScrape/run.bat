:: show the version of Window version ----------------------------------------------------------------------------------
@echo off
ver
:: This is a batch command that associates an extension with a file type (FTYPE), displays existing associations,
:: or deletes an association -------------------------------------------------------------------------------------------
:: @echo off
:: assoc > D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape\lists.txt
:: assoc | find “.py” > D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape\listsdoc.txt
:: The following example shows how the cd command can be used in a variety of ways. ------------------------------------
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
:: This batch command run the UgandaDemo.py ----------------------------------------------------------------------------
@echo off
python UgandaDemo.py
:: Copy the files-------------------------------------------------------------------------------------------------------
@echo off
cd
Rem Copies lists.txt to the present working directory. If there is no
Rem destination identified , it defaults to the present working directory.
:: copy c:\lists.txt
Rem The file lists.txt will be copied from C:\ to C:\tp location
copy D:\Kitty\NUS\Internship-PartTimeJob\RMI-CRI\Uganda-Scraping\UgandaScrape\smart_data.xlsx D:\Kitty\IT_Professionalism\Machine_Learning
Rem Quotation marks are required if the file name contains spaces
:: copy “C:\My File.txt”
Rem Copies all the files in F drive which have the txt file extension to the current working directory
:: copy F:\*.txt
Rem Copies all files from dirA to dirB. Note that directories nested in dirA will not be copied
:: copy C:\dirA dirB
