const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const zipPath = path.join(root, "stygia.zip");
const staging = path.join(root, ".pack-stygia");
const themeDir = path.join(staging, "stygia");

const include = [
  "css",
  "img",
  "fonts",
  "jquery",
  "scss",
  "docs",
  "theme.json",
  "screen.png",
  "README.md",
  "LICENSE",
  "CHANGELOG.md",
  "package.json",
];

if (fs.existsSync(zipPath)) fs.unlinkSync(zipPath);
if (fs.existsSync(staging)) fs.rmSync(staging, { recursive: true, force: true });
fs.mkdirSync(themeDir, { recursive: true });

for (const item of include) {
  const src = path.join(root, item);
  if (!fs.existsSync(src)) continue;
  fs.cpSync(src, path.join(themeDir, item), { recursive: true });
}

function zipWithZipCli() {
  return spawnSync("zip", ["-r", zipPath, "stygia"], {
    cwd: staging,
    stdio: "inherit",
    shell: false,
  });
}

function zipWithPowerShell() {
  return spawnSync(
    "powershell",
    [
      "-NoProfile",
      "-Command",
      `Compress-Archive -Path '${themeDir}' -DestinationPath '${zipPath}' -Force`,
    ],
    { stdio: "inherit" }
  );
}

let result;
if (process.platform === "win32") {
  result = zipWithPowerShell();
} else {
  result = zipWithZipCli();
  if (result.error || result.status !== 0) {
    console.error("zip CLI failed; install zip or run on a runner with it");
  }
}

fs.rmSync(staging, { recursive: true, force: true });
process.exit(result.status === null ? 1 : result.status);
