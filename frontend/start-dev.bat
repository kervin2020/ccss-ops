@echo off
cd /d "%~dp0"
node check-dependencies.js
node remove-native-rollup.js
npx vite

