// Script pour vérifier les dépendances système requises
import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

console.log('🔍 Vérification des dépendances système...\n');

// Vérifier si le module natif Rollup existe
const rollupNativePath = join(process.cwd(), 'node_modules', '@rollup', 'rollup-win32-arm64-msvc');
const rollupExists = existsSync(rollupNativePath);

if (rollupExists) {
  console.log('⚠️  Module natif Rollup détecté');
  console.log('⚠️  Ce module nécessite Microsoft Visual C++ Redistributable pour Windows ARM64\n');
  
  // Vérifier si le redistributable est installé (approximation)
  try {
    const vcRedistPath = 'C:\\Program Files\\Microsoft Visual C++ Redistributable';
    const vcRedistExists = existsSync(vcRedistPath);
    
    if (!vcRedistExists) {
      console.log('❌ Microsoft Visual C++ Redistributable non détecté\n');
      console.log('📥 Pour installer :');
      console.log('   1. Téléchargez : https://aka.ms/vs/17/release/vc_redist.arm64.exe');
      console.log('   2. Exécutez l\'installateur');
      console.log('   3. Redémarrez votre terminal');
      console.log('   4. Relancez npm run dev\n');
      console.log('💡 Solution temporaire : Le script supprimera automatiquement le module natif');
      console.log('   et utilisera la version JavaScript (plus lente mais fonctionnelle)\n');
    } else {
      console.log('✅ Microsoft Visual C++ Redistributable détecté\n');
    }
  } catch (error) {
    console.log('⚠️  Impossible de vérifier le Visual C++ Redistributable\n');
  }
} else {
  console.log('✅ Module natif Rollup non présent - utilisation de la version JS\n');
}

console.log('🚀 Tentative de démarrage du serveur...\n');

