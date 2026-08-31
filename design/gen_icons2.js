const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const path = require("path");
const { FiHome, FiBell, FiUser } = require("react-icons/fi");

const OUT = path.join(__dirname, "icons");
const NAVY = "#022049";
const ICONS = [["home", FiHome], ["announcements", FiBell], ["directory", FiUser]];

(async () => {
  for (const [name, Icon] of ICONS) {
    const svg = ReactDOMServer.renderToStaticMarkup(
      React.createElement(Icon, { size: 256, color: NAVY, strokeWidth: 1.6 })
    );
    await sharp(Buffer.from(svg), { density: 384 })
      .resize(256, 256, { fit: "contain", background: { r:0,g:0,b:0,alpha:0 } })
      .png().toFile(path.join(OUT, name + ".png"));
    console.log("wrote", name);
  }
})();
