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
if not exist "private_envs\KodeArrow" mkdir private_envs\KodeArrow
copy config\.env private_envs\KodeArrow\.env

echo Copying premium_Key_metadata.txt...
copy premium_Key_metadata.txt private_envs\KodeArrow\premium_Key_metadata.txt

cd private_envs
git add KodeArrow/.env
git add KodeArrow/premium_Key_metadata.txt
git commit -m "chore: backup KodeArrow config and key metadata"
git push origin main

echo ==================================================
echo Backup complete!
echo ==================================================
pause
