function newWarmupEntry(name, date, intervals) {
    return {
        name: name,
        date: new Date(date),
        intervals: splitValue(intervals).map(Number),
    }
}

/**
 * WarmupSheetBase implements the base functionality for an warmup sheet.
 *
 * It may be used directly when no special functionality is required.
 */
class WarmupSheetBase {
    constructor() {
        this.name = 'Oppvarming';
        this.sheet = SpreadsheetApp
            .getActiveSpreadsheet()
            .getSheetByName(this.name);
    }

    appendEntry(entry) {
        this.sheet.appendRow([
            entry.name,
            entry.date,
            entry.intervals.join(';'),
        ]);
    }

    allNames() {
        return this.sheet
            .getSheetValues(2, 1, this.sheet.getLastRow() - 1, 1)
            .map(row => row[0])
            .sort();
    }
}

/**
 * WarmupSheet implements more functionality for the warmup sheet
 * than WarmupSheetBase.
 *
 * This adds overhead upon construction by parsing the sheet values.
 */
class WarmupSheet extends WarmupSheetBase {
    constructor() {
        super();

        let nRows = this.sheet.getLastRow();
        let nCols = this.sheet.getLastColumn();

        this.warmups = {}
        this.sheet
            .getSheetValues(2, 1, nRows - 1, nCols)
            .map(row => newWarmupEntry(...row))
            .forEach(entry => this._addEntry(entry));
    }

    _addEntry(we) {
        if (!(we.name in this.warmups)) {
            this.warmups[we.name] = {
                history: []
            };
        }

        this.warmups[we.name].history.push({
            date: we.date,
            intervals: we.intervals,
        });
    }
}
