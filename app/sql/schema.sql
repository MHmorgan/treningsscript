
CREATE TABLE Exercises (
	name TEXT PRIMARY KEY,
    daytype TEXT,
    weighttype TEXT,
	object NOT NULL
) WITHOUT ROWID;

CREATE TABLE Sessions (
    date TEXT NOT NULL,  -- YYYY-MM-DD
    length INTEGER NOT NULL,
    daytype TEXT
);
