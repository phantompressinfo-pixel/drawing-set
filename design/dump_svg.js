const React = require("react");
const RDS = require("react-dom/server");
const fi = require("react-icons/fi");
const MAP = {
  home:"FiHome", announcements:"FiBell", standards:"FiBookOpen", templates:"FiLayout",
  forms:"FiClipboard", policies:"FiShield", sops:"FiCheckSquare", revit:"FiBox",
  learning:"FiUsers", directory:"FiUser", "ft-pdf":"FiFileText", "ft-doc":"FiFile",
  "ft-sheet":"FiGrid", "ft-form":"FiEdit3", recent:"FiClock", pinned:"FiStar",
  tool:"FiTool", calendar:"FiCalendar", search:"FiSearch", arrow:"FiArrowUpRight",
  download:"FiDownload", folder:"FiFolder"
};
const out = {};
for (const [name, comp] of Object.entries(MAP)) {
  const Icon = fi[comp];
  if (!Icon) { console.error("MISSING", comp); continue; }
  const html = RDS.renderToStaticMarkup(React.createElement(Icon, {}));
  // strip the outer <svg ...> wrapper, keep the inner geometry
  const inner = html.replace(/^<svg[^>]*>/, "").replace(/<\/svg>$/, "");
  out[name] = inner;
}
require("fs").writeFileSync("icon_svg.json", JSON.stringify(out, null, 1));
console.log("wrote", Object.keys(out).length, "icons");
