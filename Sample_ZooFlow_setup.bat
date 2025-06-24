@echo off
:: === Prompt password using PowerShell and store as plain string (no echo)
for /f "delims=" %%P in ('powershell -Command "$p = Read-Host -AsSecureString 'Enter your MySQL root password to download the resources, sample database and users for ZooFlow Setup'; [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($p))"') do set MYSQLPASS=%%P

:: === Run mysql commands with password, suppressing warnings
mysql -u root -p%MYSQLPASS% -e "CREATE DATABASE IF NOT EXISTS pawcache;" 2>nul
mysql -u root -p%MYSQLPASS% pawcache < "%~dp0PawCache.sql" 2>nul
mysql -u root -p%MYSQLPASS% mysql < "%~dp0sampleuseraccounts.sql" 2>nul

