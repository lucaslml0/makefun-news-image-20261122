// Entry point for the make.fun "news-image-20261122" bounty.
// Regenerates entry.png deterministically by running draw_entry.py
// (Python + Pillow, no network), then copies it to the output
// directory given by MAKEFUN_OUTPUT_DIR (default /output).

import { execFileSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const script = join(here, "draw_entry.py");
const png = join(here, "entry.png");

execFileSync("python3", [script], { stdio: "inherit" });

if (!existsSync(png)) {
  throw new Error(`draw_entry.py did not produce ${png}`);
}

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
mkdirSync(outDir, { recursive: true });
copyFileSync(png, join(outDir, "entry.png"));
console.log(`copied entry.png to ${join(outDir, "entry.png")}`);
