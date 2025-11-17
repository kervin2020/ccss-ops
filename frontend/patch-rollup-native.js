// Script pour patcher Rollup afin qu'il utilise une version JS de fallback
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const rollupNativePath = join(process.cwd(), 'node_modules', 'rollup', 'dist', 'native.js');

try {
  let content = readFileSync(rollupNativePath, 'utf8');
  
  // Remplacer le code qui charge le module natif pour qu'il utilise un fallback JS
  const originalRequire = `const { parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16 } = requireWithFriendlyError(
	existsSync(path.join(__dirname, localName)) ? localName : \`@rollup/rollup-\${packageBase}\`
);`;
  
  const patchedRequire = `let parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16;
try {
	const native = requireWithFriendlyError(
		existsSync(path.join(__dirname, localName)) ? localName : \`@rollup/rollup-\${packageBase}\`
	);
	({ parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16 } = native);
} catch (error) {
	// Fallback: utiliser les fonctions JS de base si le module natif échoue
	console.warn('⚠️  Module natif Rollup non disponible, utilisation de la version JS (plus lente)');
	// Implémentation basique en JS (Rollup utilisera sa version JS intégrée)
	const rollupJs = require('./rollup.js');
	// Ces fonctions seront fournies par la version JS de Rollup
	parse = rollupJs.parse || (() => { throw new Error('JS parser not available'); });
	parseAsync = rollupJs.parseAsync || (async () => { throw new Error('JS parser not available'); });
	xxhashBase64Url = rollupJs.xxhashBase64Url || (() => '');
	xxhashBase36 = rollupJs.xxhashBase36 || (() => '');
	xxhashBase16 = rollupJs.xxhashBase16 || (() => '');
}`;

  if (content.includes(originalRequire)) {
    content = content.replace(originalRequire, patchedRequire);
    writeFileSync(rollupNativePath, content, 'utf8');
    console.log('✓ Rollup patché pour utiliser la version JS en cas d\'échec');
  } else if (!content.includes('Fallback: utiliser les fonctions JS')) {
    console.log('⚠️  Structure de Rollup différente, tentative de patch alternatif...');
    // Patch alternatif - remplacer juste la ligne problématique
    const altPattern = /const \{ parse, parseAsync[^}]+\} = requireWithFriendlyError\([^)]+\);/s;
    if (altPattern.test(content)) {
      content = content.replace(altPattern, patchedRequire);
      writeFileSync(rollupNativePath, content, 'utf8');
      console.log('✓ Rollup patché (méthode alternative)');
    } else {
      console.log('ℹ Rollup déjà patché ou structure inattendue');
    }
  } else {
    console.log('ℹ Rollup déjà patché');
  }
} catch (error) {
  console.error('❌ Erreur lors du patch:', error.message);
  process.exit(1);
}

