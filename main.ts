import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

// gta6-meme-x-01-v4: reads the X post URL from POST.json in the bot dir and
// copies it (normalised) to $MAKEFUN_OUTPUT_DIR/POST.json.
// No dependencies, Node 22.

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const postPath = join(botDir, "POST.json");
let raw: string;
try {
  raw = readFileSync(postPath, "utf8");
} catch {
  fail(`POST.json not found at ${postPath}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(raw!);
} catch {
  fail(`POST.json at ${postPath} is not valid JSON`);
}

const url =
  typeof parsed === "object" &&
  parsed !== null &&
  "url" in parsed &&
  typeof (parsed as { url: unknown }).url === "string"
    ? (parsed as { url: string }).url
    : null;
if (url === null) {
  fail(`POST.json at ${postPath} has no "url" string`);
}

// Strip any query string or fragment, then validate the X post shape.
// Trim first: a copied URL can carry a trailing newline, which would
// otherwise make the regex below fail.
const clean = url.trim().split("?")[0].split("#")[0].replace(/\/+$/, "");
const match = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/(?:i\/web\/status\/|[^/]+\/status\/)(\d+)$/.exec(
  clean,
);
if (!match) {
  fail(`url is not an X post address: ${url}`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "POST.json"), JSON.stringify({ url: clean }) + "\n", "utf8");
console.log(`wrote ${join(outDir, "POST.json")}: ${clean}`);
