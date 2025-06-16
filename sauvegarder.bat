
@echo off
setlocal enabledelayedexpansion

:: Change to the directory of the script
cd /d %~dp0

:: Display the current directory
echo Current directory: %cd%

:: Add all files to git
echo Adding files to git...
git add .

:: Commit with the current date and time
set "datetime=%date% %time%"
git commit -m "Sauvegarde automatique - !datetime!"

:: Push to the remote repository
echo Pushing to GitHub...
git push

:: Keep the window open
echo.
echo Sauvegarde terminée. Appuyez sur une touche pour fermer la fenêtre.
pause > nul
