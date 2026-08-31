const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const {
  FiBookOpen, FiLayout, FiClipboard, FiShield, FiCheckSquare, FiBox, FiUsers
} = require("react-icons/fi");

const OUT_DIR = path.join(__dirname, "icons");
fs.mkdirSync(OUT_DIR, { recursive: true });

const NAVY = "#022049";

const ICONS = [
  ["standards", FiBookOpen],
  ["templates", FiLayout],
  ["forms", FiClipboard],
  ["policies", FiShield],
  ["sops", FiCheckSquare],
  ["revit", FiBox],
  ["learning", FiUsers]
];

async function run() {
  for (const [name, Icon] of ICONS) {
    const svgMarkup = ReactDOMServer.renderToStaticMarkup(
      React.createElement(Icon, { size: 256, color: NAVY, strokeWidth: 1.6 })
    );
    // Feather icons render without a fixed width/height root sometimes; ensure viewBox present
    const svg = svgMarkup.includes("<svg")
      ? svgMarkup
      : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">${svgMarkup}</svg>`;
    const pngPath = path.join(OUT_DIR, `${name}.png`);
    await sharp(Buffer.from(svg), { density: 384 })
      .resize(256, 256, { fit: "contain", background: { r:0,g:0,b:0,alpha:0 } })
      .png()
      .toFile(pngPath);
    console.log("wrote", pngPath);
  }
}

run().catch(e => { console.error(e); process.exit(1); });
