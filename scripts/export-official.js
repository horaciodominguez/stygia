const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const destArg = process.argv[2];

if (!destArg) {
  console.error("Usage: node scripts/export-official.js <destination/stygia>");
  process.exit(1);
}

const dest = path.resolve(destArg);

// Match phpmyadmin/themes layout (see boodark): runtime + sources, no dev junk.
const include = [
  "css",
  "img",
  "fonts",
  "jquery",
  "scss",
  "theme.json",
  "screen.png",
  "README.md",
  "LICENSE",
  "CHANGELOG.md",
  "package.json",
];

if (fs.existsSync(dest)) {
  fs.rmSync(dest, { recursive: true, force: true });
}
fs.mkdirSync(dest, { recursive: true });

for (const item of include) {
  const src = path.join(root, item);
  if (!fs.existsSync(src)) {
    console.warn("skip missing:", item);
    continue;
  }
  fs.cpSync(src, path.join(dest, item), { recursive: true });
}

console.log("Exported official theme to", dest);
