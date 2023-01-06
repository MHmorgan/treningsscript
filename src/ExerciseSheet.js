function newExerciseEntry(name, date, reps, weight, weight_type, tags) {
    return {
        name: name,
        date: new Date(date),
        reps: splitValue(reps).map(Number),
        weight: splitValue(weight).map(Number),
        weight_type: weight_type,
        tags: tags.split(';'),
    }
}

function verifyExerciseEntry(entry) {
    let issues = [];
    if (!entry.name)
        issues.push('name is missing');
    if (!entry.date)
        issues.push('date is missing');
    if (!entry.reps)
        issues.push('reps is missing');
    if (!entry.weight_type)
        issues.push('weight_type is missing');
    return issues.join('; ') || null;
}

/**
 * ExerciseSheetBase implements the base functionality for an exercise sheet.
 *
 * It may be used directly when no special functionality is required.
 */
class ExerciseSheetBase {
    constructor() {
        this.name = 'Øvelser';
        this.sheet = SpreadsheetApp
            .getActiveSpreadsheet()
            .getSheetByName(this.name);
    }

    appendEntry(entry) {
        this.sheet.appendRow([
            entry.name,
            entry.date,
            entry.reps.join(';'),
            entry.weight.join(';'),
            entry.weight_type,
            entry.tags.join(';'),
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
 * ExerciseSheet implements more functionality for the exercise sheet
 * than ExerciseSheetBase.
 *
 * This adds overhead upon construction by parsing the sheet values.
 */
class ExerciseSheet extends ExerciseSheetBase {
    constructor() {
        super();

        let nRows = this.sheet.getLastRow();
        let nCols = this.sheet.getLastColumn();

        this.warmups = {}
        this.sheet
            .getSheetValues(2, 1, nRows - 1, nCols)
            .map(row => newExerciseEntry(...row))
            .forEach(entry => this._addEntry(entry));
    }

    _addEntry(ex) {
        if (!(ex.name in this.warmups)) {
            this.warmups[ex.name] = {
                weight_type: ex.weight_type,
                tags: ex.tags,
                history: []
            };
        }

        this.warmups[ex.name].history.push({
            date: ex.date,
            reps: ex.reps,
            weight: ex.weight
        });
    }
}
