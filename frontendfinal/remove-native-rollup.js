// Script pour supprimer le module natif Rollup problématique
import { rmSync } from 'fs';
import { join } from 'path';

const rollupNativePath = join(process.cwd(), 'node_modules', '@rollup', 'rollup-win32-arm64-msvc');

try {
  rmSync(rollupNativePath, { recursive: true, force: true });
  console.log('✓ Module natif Rollup supprimé - utilisation de la version JS');
} catch (error) {
  // Ignore si le dossier n'existe pas
}

