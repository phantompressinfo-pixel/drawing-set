/**
 * Builds the IT Help form, its response sheet, and the three columns IT
 * works out of. Run buildITForm() once; everything after that is automatic.
 *
 * script.google.com -> New project -> paste -> Run -> authorise.
 */
function buildITForm() {
  var form = FormApp.create('IT Help — Report an Issue');

  form.setDescription(
    'Tell IT what broke. The more specific the last two answers are, the ' +
    'faster it gets fixed — "Revit crashed" takes three emails to diagnose, ' +
    '"Revit closes when I open the linked file in 2431-ARCH-Central" takes none.');

  // Who and what machine ------------------------------------------------
  form.addTextItem()
      .setTitle('Your name')
      .setRequired(true);

  form.addTextItem()
      .setTitle('Computer or device')
      .setHelpText('The label on the machine, e.g. EAD-WS-14. If you do not ' +
                   'know it, say where it sits — "desk by the plotter".')
      .setRequired(true);

  // The problem ---------------------------------------------------------
  form.addTextItem()
      .setTitle('What is the problem?')
      .setHelpText('One line.')
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('What were you doing when it happened?')
      .setHelpText('Which file, which program, roughly what time, and whether ' +
                   'it has happened before. This is the answer that saves the ' +
                   'back-and-forth.')
      .setRequired(true);

  form.addMultipleChoiceItem()
      .setTitle('How urgent is it?')
      .setChoiceValues(['Blocked — I cannot work',
                        'Slowing me down',
                        'Whenever you get a chance'])
      .setRequired(true);

  form.addParagraphTextItem()
      .setTitle('Anything else IT should know?')
      .setRequired(false);

  // Settings ------------------------------------------------------------
  form.setProgressBar(false);
  form.setConfirmationMessage(
    'Logged. IT can see it now — no need to email as well.');

  // Both of these are Workspace-only, so they are allowed to fail on a
  // personal account without taking the rest of the script down.
  try { form.setRequireLogin(true); } catch (e) {}
  try { form.setCollectEmail(true); } catch (e) {}

  // Response sheet, plus the columns IT fills in -------------------------
  var ss = SpreadsheetApp.create('IT Help — Issue Log');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  SpreadsheetApp.flush();
  ss = SpreadsheetApp.openById(form.getDestinationId());
  var sheet = ss.getSheets()[0];
  var col = sheet.getLastColumn() + 1;

  sheet.getRange(1, col, 1, 3)
       .setValues([['Status', 'IT notes', 'Date fixed']])
       .setFontWeight('bold');

  sheet.getRange(2, col, sheet.getMaxRows() - 1, 1).setDataValidation(
    SpreadsheetApp.newDataValidation()
      .requireValueInList(['New', 'In progress', 'Waiting on you', 'Done'], true)
      .setAllowInvalid(false)
      .build());

  styleHeader_(sheet);
  sheet.setFrozenRows(1);
  sheet.setColumnWidth(col, 120);
  sheet.setColumnWidth(col + 1, 300);
  sheet.setColumnWidth(col + 2, 110);

  Logger.log('Form (share this):  ' + form.getPublishedUrl());
  Logger.log('Form (edit):        ' + form.getEditUrl());
  Logger.log('Issue log:          ' + ss.getUrl());
}

/** Navy header band, matching the hub. */
function styleHeader_(sheet) {
  sheet.getRange(1, 1, 1, sheet.getLastColumn())
       .setBackground('#022049')
       .setFontColor('#ffffff')
       .setFontFamily('Montserrat')
       .setFontWeight('bold')
       .setVerticalAlignment('middle')
       .setWrap(true);
  sheet.setRowHeight(1, 42);
}
