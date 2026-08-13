const fs = require("fs");
const path = require("path");
const { spawn, spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const themeCss = path.join(root, "css", "theme.css");

function rebuildRtl() {
  console.log("[watch] rebuilding RTL…");
  const r = spawnSync(process.execPath, [path.join(__dirname, "build-rtl.js")], {
    cwd: root,
    stdio: "inherit",
  });
  if (r.status !== 0) console.error("[watch] RTL build failed");
}

const sassCli = path.join(root, "node_modules", "sass", "sass.js");
const sassArgs = [
  sassCli,
  "scss/theme.scss",
  "css/theme.css",
  "--load-path=node_modules",
  "--style=compressed",
  "--source-map",
  "--quiet-deps",
  "--silence-deprecation=import",
  "--silence-deprecation=global-builtin",
  "--silence-deprecation=color-functions",
  "--watch",
];

const child = spawn(process.execPath, sassArgs, { cwd: root, stdio: "inherit" });

let timer = null;
fs.watch(path.join(root, "css"), (event, file) => {
  if (file !== "theme.css") return;
  clearTimeout(timer);
  timer = setTimeout(rebuildRtl, 400);
});

fs.watch(path.join(root, "scss"), { recursive: true }, (event, file) => {
  if (!file || !String(file).includes("rtl-overrides")) return;
  clearTimeout(timer);
  timer = setTimeout(rebuildRtl, 400);
});

rebuildRtl();

child.on("exit", (code) => process.exit(code || 0));
