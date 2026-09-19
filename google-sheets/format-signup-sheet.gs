/**
 * Formats the Learning Sessions sign-up sheet: title bar, navy header,
 * dropdowns, and colour that shows at a glance which Fridays are still open.
 *
 * Safe to re-run — it rebuilds the formatting from scratch each time and
 * never touches what people have typed.
 */
var SHEET_ID = '1kezUdZavOkIlFe96_a6GJu5bKDkVSB49no-MgYUD3xI';

var NAVY  = '#022049';
var RULE  = '#d5dce4';
var OPEN  = '#f4f6f9';   // nobody has claimed it
var CLAIM = '#fff4d6';   // name in, topic maybe not
var CONF  = '#e7f4ea';   // locked in
var DONE  = '#eeeeee';   // in the past

var FORMATS  = ['Demo', 'Walkthrough', 'Lessons learned',
                'Project story', 'Guest speaker'];
var STATUSES = ['Open', 'Claimed', 'Confirmed', 'Done'];

function formatSignupSheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheets()[0];
  sh.setName('Schedule');

  // A title bar above the headers, so the sheet explains itself ----------
  // The title bar is merged, so A1 holds the whole sentence -- test the
  // prefix, or a re-run inserts a second title row every time.
  if (String(sh.getRange('A1').getValue()).indexOf('LEARNING SESSIONS') !== 0) {
    sh.insertRowBefore(1);
  }
  sh.getRange(1, 1, 1, 6).merge()
    .setValue('LEARNING SESSIONS   ·   Find an Open Friday, put your name ' +
              'and topic in, set Status to Claimed. That is the whole process.')
    .setBackground(NAVY).setFontColor('#ffffff').setFontFamily('Montserrat')
    .setFontSize(11).setFontWeight('bold').setVerticalAlignment('middle')
    .setHorizontalAlignment('left');
  sh.setRowHeight(1, 46);

  var head = 2;
  var firstRow = head + 1;
  var rows = sh.getLastRow() - head;

  // Header row ----------------------------------------------------------
  sh.getRange(head, 1, 1, 6)
    .setValues([['Date', 'Presenter', 'Topic', 'Format',
                 'Notes for attendees', 'Status']])
    .setBackground('#ffffff').setFontColor(NAVY).setFontFamily('Montserrat')
    .setFontWeight('bold').setFontSize(10).setVerticalAlignment('middle')
    .setBorder(null, null, true, null, null, null, NAVY,
               SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
  sh.setRowHeight(head, 34);
  sh.setFrozenRows(head);

  // Body ----------------------------------------------------------------
  var body = sh.getRange(firstRow, 1, rows, 6);
  body.setFontFamily('Montserrat').setFontSize(10)
      .setVerticalAlignment('middle')
      .setBorder(null, null, null, null, null, true, RULE,
                 SpreadsheetApp.BorderStyle.SOLID);
  sh.setRowHeights(firstRow, rows, 30);

  sh.getRange(firstRow, 1, rows, 1).setFontWeight('bold').setFontColor(NAVY);
  sh.getRange(firstRow, 5, rows, 1).setWrap(true);
  sh.getRange(firstRow, 4, rows, 1).setHorizontalAlignment('center');
  sh.getRange(firstRow, 6, rows, 1).setHorizontalAlignment('center');

  [130, 150, 260, 140, 300, 110].forEach(function (w, i) {
    sh.setColumnWidth(i + 1, w);
  });

  // Dropdowns -----------------------------------------------------------
  sh.getRange(firstRow, 4, rows, 1).setDataValidation(listRule_(FORMATS));
  sh.getRange(firstRow, 6, rows, 1).setDataValidation(listRule_(STATUSES));

  // Colour the row by status -------------------------------------------
  sh.clearConditionalFormatRules();
  sh.setConditionalFormatRules([
    statusRule_(sh, firstRow, rows, 'Open',      OPEN,  '#6b7280'),
    statusRule_(sh, firstRow, rows, 'Claimed',   CLAIM, NAVY),
    statusRule_(sh, firstRow, rows, 'Confirmed', CONF,  NAVY),
    statusRule_(sh, firstRow, rows, 'Done',      DONE,  '#9aa3ae')
  ]);

  // Nobody needs to edit the two header rows ----------------------------
  sh.getProtections(SpreadsheetApp.ProtectionType.RANGE)
    .forEach(function (p) { p.remove(); });
  sh.getRange(1, 1, head, 6).protect()
    .setDescription('Headers').setWarningOnly(true);

  sh.getRange('B' + firstRow).activate();
  Logger.log('Formatted: ' + ss.getUrl());
}

function listRule_(values) {
  return SpreadsheetApp.newDataValidation()
    .requireValueInList(values, true).setAllowInvalid(false).build();
}

/** Paint the whole row from the value in the Status column. */
function statusRule_(sh, firstRow, rows, value, bg, fg) {
  return SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=$F' + firstRow + '="' + value + '"')
    .setBackground(bg).setFontColor(fg)
    .setRanges([sh.getRange(firstRow, 1, rows, 6)])
    .build();
}
