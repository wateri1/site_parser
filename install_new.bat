@echo off
chcp 65001 >nul
title LeadHunter - Полная автоматическая установка с 0
color 0b

echo ======================================================================
echo    LEADHUNTER: ПОЛНАЯ АВТОМАТИЧЕСКАЯ УСТАНОВКА С 0
echo ======================================================================
echo.
echo Этот скрипт проверит наличие необходимых программ (Python, Node.js),
echo при необходимости скачает и установит их, настроит виртуальное
echo окружение, установит все библиотеки и подготовит проект к запуску.
echo.
echo ======================================================================
echo.

:: ---------------------------------------------------------------------
:: ШАГ 1: Проверка и установка Python
:: ---------------------------------------------------------------------
echo [1/5] Проверка Python...

set "PY_CMD="
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python"
) else (
    py -3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_CMD=py -3"
    )
)

if defined PY_CMD (
    for /f "tokens=*" %%v in ('%PY_CMD% --version 2^>^&1') do echo [OK] Найден: %%v
) else (
    echo [!] Python не обнаружен в системе. Начинаем автоматическую скачку и установку...
    echo.
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Загрузка и установка Python через Windows Package Manager (winget)...
        winget install Python.Python.3.11 -e --accept-source-agreements --accept-package-agreements
    ) else (
        echo Загрузка официального установщика Python 3.11...
        curl.exe -L -o "%TEMP%\python_installer.exe" https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
        echo Установка Python (добавление в PATH)...
        "%TEMP%\python_installer.exe" /passive InstallAllUsers=0 PrependPath=1 Include_pip=1
        del /f /q "%TEMP%\python_installer.exe" >nul 2>&1
    )
    
    :: Проверка после установки
    set "PY_CMD="
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_CMD=python"
    ) else (
        py -3 --version >nul 2>&1
        if %errorlevel% equ 0 (
            set "PY_CMD=py -3"
        )
    )
    if not defined PY_CMD (
        echo.
        echo [ВНИМАНИЕ] Python был установлен, но командная строка пока не видит его PATH.
        echo Пожалуйста, перезапустите этот файл (install.bat) или добавьте Python в PATH.
        pause
        exit /b 1
    )
)
echo.

:: ---------------------------------------------------------------------
:: ШАГ 2: Проверка и установка Node.js
:: ---------------------------------------------------------------------
echo [2/5] Проверка Node.js и npm...

node --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('node --version 2^>^&1') do echo [OK] Найден Node.js: %%v
    for /f "tokens=*" %%v in ('call npm --version 2^>^&1') do echo [OK] Найден npm: v%%v
) else (
    echo [!] Node.js не обнаружен в системе. Начинаем автоматическую скачку и установку...
    echo.
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Загрузка и установка Node.js LTS через winget...
        winget install OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements
    ) else (
        echo Загрузка официального установщика Node.js LTS (msi)...
        curl.exe -L -o "%TEMP%\node_installer.msi" https://nodejs.org/dist/v20.18.0/node-v20.18.0-x64.msi
        echo Установка Node.js...
        msiexec /i "%TEMP%\node_installer.msi" /passive
        del /f /q "%TEMP%\node_installer.msi" >nul 2>&1
    )

    node --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [ВНИМАНИЕ] Node.js был установлен.
        echo Пожалуйста, закройте и снова откройте это окно,
        echo чтобы обновились переменные среды, затем запустите install.bat еще раз.
        pause
        exit /b 1
    )
)
echo.

:: ---------------------------------------------------------------------
:: ШАГ 3: Создание чистого виртуального окружения Python и установка зависимостей
:: ---------------------------------------------------------------------
echo [3/5] Настройка бэкенда (Python Virtual Environment)...

cd /d "%~dp0backend"

if exist "venv" (
    echo [i] Найдено существующее окружение venv. Проверяем библиотеки...
) else (
    echo [*] Создаем чистое изолированное окружение venv с 0...
    %PY_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ОШИБКА] Не удалось создать venv.
        pause
        exit /b 1
    )
)

echo [*] Обновление pip и установка библиотек из requirements.txt...
call venv\Scripts\python.exe -m pip install --upgrade pip --quiet
call venv\Scripts\pip.exe install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ОШИБКА] Ошибка при установке Python пакетов. Пробуем повторно без флага quiet:
    call venv\Scripts\pip.exe install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ОШИБКА] Не удалось установить зависимости бэкенда!
        pause
        exit /b 1
    )
)
echo [OK] Все библиотеки бэкенда успешно установлены.
echo.

:: ---------------------------------------------------------------------
:: ШАГ 4: Настройка конфигурации (.env)
:: ---------------------------------------------------------------------
echo [4/5] Проверка конфигурации .env...

if not exist ".env" (
    echo [*] Создаем файл конфигурации backend/.env...
    (
        echo # Файл конфигурации бэкенда
        echo # Введите сюда ваш OpenAI API Key для генерации B2B офферов
        echo OPENAI_API_KEY=
    ) > .env
    echo [OK] Файл backend/.env создан. Ключ OpenAI можно указать в нем или прямо в настройках сайта.
) else (
    echo [OK] Файл конфигурации backend/.env уже существует.
)
cd /d "%~dp0"
echo.

:: ---------------------------------------------------------------------
:: ШАГ 5: Установка фронтенд зависимостей (React / Vite / Tailwind)
:: ---------------------------------------------------------------------
echo [5/5] Установка зависимостей интерфейса (React / npm)...

cd /d "%~dp0frontend"
echo [*] Запуск npm install (скачивание пакетов фронтенда с 0)...
call npm install --no-audit --no-fund
if %errorlevel% neq 0 (
    echo [ОШИБКА] npm install завершился с ошибкой!
    pause
    exit /b 1
)
echo [OK] Все библиотеки фронтенда успешно установлены.

echo [*] Сборка интерфейса для быстрой работы (npm run build)...
call npm run build
if %errorlevel% neq 0 (
    echo [Предупреждение] Сборка dist завершилась с предупреждением, но dev-режим будет работать.
) else (
    echo [OK] Интерфейс успешно скомпилирован.
)
cd /d "%~dp0"
echo.

:: ---------------------------------------------------------------------
:: ФИНАЛ: Завершение установки
:: ---------------------------------------------------------------------
color 0a
echo ======================================================================
echo   🎉 УСТАНОВКА УСПЕШНО ЗАВЕРШЕНА!
echo ======================================================================
echo.
echo   Все компоненты готовы к работе:
echo   - Python + venv + FastAPI бэкенд
echo   - Node.js + React фронтенд
echo   - Готовая конфигурация с OpenAI ChatGPT
echo.
echo   Для запуска приложения используйте файл: start.bat
echo ======================================================================
echo.

set /p launch="Запустить LeadHunter прямо сейчас? (Y/N, по умолчанию Y): "
if /i "%launch%"=="N" goto finish

echo Запуск приложения через start.bat...
start "" start.bat

:finish
echo.
pause