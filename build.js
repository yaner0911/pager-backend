const fs = require("fs");
const path = require("path");

const dir = __dirname;
const js = fs
  .readFileSync(path.join(dir, "mqtt.min.js"), "utf8")
  .replace(/<\/script>/g, "<\\/script>")
  .replace(/<!--/g, "<\\!--");

const src = fs.readFileSync(path.join(dir, "index_src.html"), "utf8");
const tag = '<script src="https://cdn.jsdelivr.net/npm/mqtt@5/dist/mqtt.min.js"></script>';
if (!src.includes(tag)) {
  throw new Error("CDN script tag not found in index_src.html");
}

const out = src.replace(tag, "<script>" + js + "</script>");
fs.writeFileSync(path.join(dir, "index.html"), out, "utf8");
console.log("done, index.html 大小 =", Buffer.byteLength(out), "字节");
console.log("还引用 CDN 吗:", out.includes("cdn.jsdelivr.net"));
