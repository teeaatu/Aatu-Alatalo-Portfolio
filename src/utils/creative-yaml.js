import fs from 'node:fs';
import path from 'node:path';
import YAML from 'yaml';

const DATA_DIR = path.resolve(process.cwd(), 'src/data');
const BACKUP_DIR = path.resolve(DATA_DIR, '.backup');

// Map category slug to YAML filename
const SLUG_TO_FILE = {
  'recent': 'recent.yml',
  'work1': 'work1.yml',
  'work2': 'work2.yml',
  'work3': 'work3.yml',
  'work4': 'work4.yml',
  'masters-2026': 'masters-2026.yml',
  'kuvaprojekti-ajasta-v365': 'kuvaprojekti_ajasta_v365.yml',
  'tapahtumat': 'tapahtumat.yml',
  'vari-ja-muoto': 'vari-ja-muoto.yml',
  'raw': 'raw.yml',
  'mustavalkoinen-sarja': 'mustavalkoinen-sarja.yml',
  'sisatilan-valo': 'sisatilan-valo.yml',
  'kiehtovat-rakennukset': 'kiehtovat-rakennukset.yml',
  'luonto-ja-ymparisto': 'luonto-ja-ymparisto.yml',
  'still-life': 'still-life.yml',
  'elaimet': 'elaimet.yml',
  'categories': 'categories.yml',
};

export function getYamlFilePath(categorySlug) {
  const fileName = SLUG_TO_FILE[categorySlug] || `${categorySlug}.yml`;
  return path.join(DATA_DIR, fileName);
}

export function ensureBackupDir() {
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
}

export function backupYaml(categorySlug) {
  ensureBackupDir();
  const filePath = getYamlFilePath(categorySlug);
  if (!fs.existsSync(filePath)) return null;

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFileName = `${timestamp}_${path.basename(filePath)}`;
  const backupFilePath = path.join(BACKUP_DIR, backupFileName);

  fs.copyFileSync(filePath, backupFilePath);
  return backupFilePath;
}

export function readYaml(categorySlug) {
  const filePath = getYamlFilePath(categorySlug);
  if (!fs.existsSync(filePath)) return null;
  const content = fs.readFileSync(filePath, 'utf8');
  return YAML.parse(content);
}

export function writeYaml(categorySlug, data) {
  backupYaml(categorySlug);
  const filePath = getYamlFilePath(categorySlug);
  const doc = new YAML.Document(data);
  const yamlString = doc.toString({ indent: 2 });
  fs.writeFileSync(filePath, yamlString, 'utf8');
  return true;
}

export function getAvailableBackups() {
  ensureBackupDir();
  return fs.readdirSync(BACKUP_DIR)
    .filter(file => file.endsWith('.yml'))
    .sort()
    .reverse();
}

export function restoreLatestBackup(categorySlug) {
  ensureBackupDir();
  const fileName = SLUG_TO_FILE[categorySlug] || `${categorySlug}.yml`;
  const backups = getAvailableBackups().filter(b => b.endsWith(`_${fileName}`));
  if (backups.length === 0) return false;

  const latestBackup = path.join(BACKUP_DIR, backups[0]);
  const targetPath = getYamlFilePath(categorySlug);
  fs.copyFileSync(latestBackup, targetPath);
  return true;
}
