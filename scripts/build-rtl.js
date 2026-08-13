const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const rtlcss = require("rtlcss");

const root = path.resolve(__dirname, "..");
const ltrPath = path.join(root, "css", "theme.css");
const rtlPath = path.join(root, "css", "theme.rtl.css");
const overridesScss = path.join(root, "scss", "_rtl-overrides.scss");
const overridesTmp = path.join(root, "css", ".rtl-overrides.tmp.css");
const sassCli = path.join(
  root,
  "node_modules",
  "sass",
  "sass.js"
);

if (!fs.existsSync(ltrPath)) {
  console.error("Missing css/theme.css — run build:ltr first");
  process.exit(1);
}

const ltr = fs.readFileSync(ltrPath, "utf8");
const flipped = rtlcss.process(ltr, { autoRename: false });
if (typeof flipped !== "string" || flipped.length < 1000) {
  console.error("rtlcss produced unexpectedly small output");
  process.exit(1);
}

const sass = spawnSync(
  process.execPath,
  [
    sassCli,
    overridesScss,
    overridesTmp,
    "--load-path=" + path.join(root, "node_modules"),
    "--style=compressed",
    "--quiet-deps",
    "--silence-deprecation=import",
    "--silence-deprecation=global-builtin",
    "--silence-deprecation=color-functions",
  ],
  { cwd: root, encoding: "utf8" }
);

if (sass.status !== 0) {
  console.error(sass.stderr || sass.stdout || "sass failed");
  process.exit(sass.status || 1);
}

const overrides = fs.existsSync(overridesTmp)
  ? fs.readFileSync(overridesTmp, "utf8")
  : "";

if (fs.existsSync(overridesTmp)) fs.unlinkSync(overridesTmp);

const banner =
  "/* Stygia RTL — generated via rtlcss(theme.css) + _rtl-overrides.scss */\n";
fs.writeFileSync(rtlPath, banner + flipped + "\n" + overrides);

fs.writeFileSync(
  path.join(root, "css", "theme.rtl.css.map"),
  JSON.stringify({
    version: 3,
    file: "theme.rtl.css",
    sources: ["theme.css", "../scss/_rtl-overrides.scss"],
    mappings: "",
    names: [],
  })
);

console.log(
  "Wrote css/theme.rtl.css (" + fs.statSync(rtlPath).size + " bytes)"
);
