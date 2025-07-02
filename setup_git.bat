@echo off
echo 🚀 Configurando Git e enviando para GitHub...
echo.

REM Verificar se o Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git nao encontrado! Instale o Git primeiro.
    echo 📥 Download: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git encontrado!
echo.

REM Configurar Git (execute apenas uma vez)
echo 📝 Configure seu Git com suas informações:
set /p nome="Digite seu nome: "
set /p email="Digite seu email: "

git config --global user.name "%nome%"
git config --global user.email "%email%"

echo.
echo 🔧 Configuração concluída!
echo.

REM Inicializar repositório
echo 📂 Inicializando repositório Git...
git init

echo.
echo 📁 Adicionando arquivos...
git add .

echo.
echo 💾 Fazendo primeiro commit...
git commit -m "🌤️ Projeto inicial: Análise meteorológica Rio Grande vs Capão do Leão"

echo.
echo 🔗 Agora você precisa:
echo 1. Criar o repositório no GitHub
echo 2. Copiar a URL do repositório
echo 3. Executar: git remote add origin SUA_URL_AQUI
echo 4. Executar: git push -u origin main
echo.

pause
