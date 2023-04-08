const spawn = require('cross-spawn');
const fs = require('fs');
var base_url = "/";

if (process.env.CF_PAGES_BRANCH === 'main') {
    base_url = "https://blog.nathanv.me/";
} else if (process.env.CF_PAGES_URL) {
    base_url = process.env.CF_PAGES_URL;
}

console.log(`Using base url "${base_url}"`);
cmd = spawn.sync("npx.cmd", ["hugo", "--cleanDestinationDir", "--minify", "-b", base_url], { encoding : 'utf8' });

if (cmd.error) {
    console.log("ERROR: ", cmd.error);
}

console.log(cmd.stdout);
console.error(cmd.stderr);

fs.unlinkSync("public/style.css");

process.exit(cmd.status);
