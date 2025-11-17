# Script pour forcer Rollup à utiliser la version JavaScript
# Supprime le module natif problématique avant de lancer Vite

$rollupNativePath = "node_modules\@rollup\rollup-win32-arm64-msvc"

if (Test-Path $rollupNativePath) {
    Write-Host "Suppression du module natif Rollup pour forcer l'utilisation de la version JS..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $rollupNativePath -ErrorAction SilentlyContinue
}

Write-Host "Lancement de Vite..." -ForegroundColor Green
npm run vite

