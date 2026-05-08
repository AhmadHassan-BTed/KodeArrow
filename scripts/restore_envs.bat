@echo off
echo ==================================================
echo Restoring private .env files from GitHub...
echo ==================================================

cd %~dp0\..

if not exist "private_envs" (
    echo Cloning private.envs repository...
    git clone https://github.com/AhmadHassan-BTed/private.envs.git private_envs
)

echo Updating private.envs repository...
cd private_envs
git pull origin main
cd ..

if not exist "config" mkdir config

echo Restoring .env...
copy private_envs\KodeArrow.env config\.env

echo ==================================================
echo Restore complete!
echo ==================================================
pause
