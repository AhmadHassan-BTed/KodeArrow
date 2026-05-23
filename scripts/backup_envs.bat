@echo off
echo ==================================================
echo Backing up private .env files to GitHub...
echo ==================================================

cd %~dp0\..

if not exist "private_envs" (
    echo Cloning private.envs repository...
    git clone https://github.com/AhmadHassan-BTed/private.envs.git private_envs
) else (
    echo Updating private.envs repository...
    cd private_envs
    git pull origin main
    cd ..
)

echo Copying .env...
copy config\.env private_envs\KodeArrow.env

cd private_envs
git add KodeArrow.env
git commit -m "chore: backup KodeArrow .env file"
git push origin main

echo ==================================================
echo Backup complete!
echo ==================================================
pause
