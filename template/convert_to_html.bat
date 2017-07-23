@echo off
if [%1]==[] goto usage
set name=%~n1
if exist .\html goto exists
mkdir html
goto process
:exists
echo y | del .\html\*
:process

htlatex %name%.tex html "" -dhtml "--interaction=nonstopmode"

:clean
del %name%.4tc > nul
del %name%.4ct > nul
del %name%.tmp > nul
del %name%.xref > nul
del %name%.idv > nul
del %name%.lg > nul
del %name%.html > nul
del %name%.css > nul
goto end

:usage

echo Usage: %0 file.tex
echo *** Caution *** If there is a html directory it will be deleted.
echo. 
:end