// Script pour patcher Rollup afin d'utiliser la version JS si le module natif échoue
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const rollupNativePath = join(process.cwd(), 'node_modules', 'rollup', 'dist', 'native.js');

try {
  let content = readFileSync(rollupNativePath, 'utf8');
  
  // Remplacer le throw par un fallback vers la version JS
  const originalCode = `const { parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16 } = requireWithFriendlyError(
	existsSync(path.join(__dirname, localName)) ? localName : \`@rollup/rollup-\${packageBase}\`
);`;
  
  const patchedCode = `let parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16;
try {
	const native = requireWithFriendlyError(
		existsSync(path.join(__dirname, localName)) ? localName : \`@rollup/rollup-\${packageBase}\`
	);
	({ parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16 } = native);
} catch (error) {
	// Fallback vers la version JS si le module natif échoue
	const jsVersion = require('./native.es.js');
	({ parse, parseAsync, xxhashBase64Url, xxhashBase36, xxhashBase16 } = jsVersion);
}`;

  if (content.includes(originalCode)) {
    content = content.replace(originalCode, patchedCode);
    writeFileSync(rollupNativePath, content, 'utf8');
    console.log('✓ Rollup patché pour utiliser la version JS en cas d\'échec du module natif');
  } else {
    console.log('ℹ Rollup déjà patché ou structure différente');
  }
} catch (error) {
  console.error('Erreur lors du patch:', error.message);
  process.exit(1);
}

