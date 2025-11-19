# Guide de dépannage - Erreur Rollup Windows ARM64

## Problème
```
Error: Failed to load module @rollup/rollup-win32-arm64-msvc. Required DLL was not found.
```

## Solutions

### Solution 1 : Installer Microsoft Visual C++ Redistributable (Recommandé)

1. Téléchargez le Visual C++ Redistributable pour ARM64 :
   - **Lien direct** : https://aka.ms/vs/17/release/vc_redist.arm64.exe

2. Exécutez l'installateur et suivez les instructions

3. Redémarrez votre terminal/PowerShell

4. Relancez le projet :
   ```powershell
   cd frontend
   npm run dev
   ```

### Solution 2 : Réinstaller les dépendances

Si le problème persiste après avoir installé le redistributable :

```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
npm run dev
```

### Solution 3 : Utiliser une version alternative de Node.js

Si vous utilisez Node.js v24, essayez de downgrader vers Node.js v20 LTS qui a une meilleure compatibilité avec les modules natifs Windows ARM64.

## Vérification

Pour vérifier si le problème est résolu, le serveur Vite devrait démarrer et afficher :
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

