const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const path = require("path");
const { FiFileText, FiFile, FiGrid, FiEdit3, FiClock, FiStar, FiTool, FiCalendar } = require("react-icons/fi");
const OUT = path.join(__dirname, "icons");
const ICONS = [["ft-pdf", FiFileText], ["ft-doc", FiFile], ["ft-sheet", FiGrid], ["ft-form", FiEdit3],
               ["recent", FiClock], ["pinned", FiStar], ["tool", FiTool], ["calendar", FiCalendar]];
(async () => {
  for (const [name, Icon] of ICONS) {
    const svg = ReactDOMServer.renderToStaticMarkup(
      React.createElement(Icon, { size: 256, color: "#022049", strokeWidth: 1.6 }));
    await sharp(Buffer.from(svg), { density: 384 })
      .resize(256, 256, { fit: "contain", background: { r:0,g:0,b:0,alpha:0 } })
      .png().toFile(path.join(OUT, name + ".png"));
    console.log("wrote", name);
  }
})();
