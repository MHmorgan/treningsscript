function test() {
    let ex = new ExerciseSheet();
    console.info(ex.warmups);
}

/**
 * Get the training website or data.
 *
 * When called with the /api path, it will return the training data.
 *
 * Training data:
 *
 * {
 *  "data": [
 * }
 *
 * @param e {GoogleAppsScript.Events.AppsScriptHttpRequestEvent}
 * @returns {any}
 */
function doGet(e) {
    switch (e.pathInfo) {
        case 'api/exercises':
            let ex = new ExerciseSheet();
            return ContentService
                .createTextOutput(JSON.stringify(ex.data))
                .setMimeType(ContentService.MimeType.JSON);
        case 'api/warmups':
            let w = new WarmupSheet();
            return ContentService
                .createTextOutput(JSON.stringify(w.warmups))
                .setMimeType(ContentService.MimeType.JSON);
    }
    return HtmlService.createHtmlOutputFromFile('index.html');
}

/**
 * Add new training data.
 *
 * @param e {GoogleAppsScript.Events.AppsScriptHttpRequestEvent}
 * @returns {any}
 */
function doPost(e) {
    switch (e.pathInfo) {
        case 'api/exercises':
            let exercise = JSON.parse(e.postData.contents);
            let errMsg = verifyExerciseEntry(exercise);
            if (errMsg) {
                return ContentService
                    .createTextOutput(errMsg)
                    .setMimeType(ContentService.MimeType.TEXT);
            }

            let ex = new ExerciseSheetBase();
            ex.appendEntry(exercise);
            break;
        case 'api/warmups':
            let w = new WarmupSheetBase();
            w.appendEntry(JSON.parse(e.postData.contents));
            break;
    }
}

/**
 * Split a string on a delimiter. Then the empty parts of the
 * resulting array is filled in with the prior value.
 *
 * Example:
 *  '2;;' -> ['2', '2', '2']
 */
function splitValue(s, delim = ';') {
    let arr = s.split(delim);
    if (arr.length <= 1)
        return arr[0] === '' ? [] : arr;

    let last = arr[0]
    for (let i = 1; i < arr.length; i++) {
        if (!arr[i])
            arr[i] = last;
        else
            last = arr[i];
    }
    return arr;
}