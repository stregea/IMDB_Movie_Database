# Command used to create the TitleBasics table.
CREATE_TITLE_BASICS_TABLE = '''CREATE TABLE IF NOT EXISTS TitleBasics(
                                tconst varchar PRIMARY KEY,
                                titleType varchar,
                                primaryTitle varchar,
                                originalTitle varchar,
                                isAdult integer,
                                startYear integer,
                                endYear integer,
                                runtimeMinutes integer,
                                genres varchar
                            );'''

# Command used to create the TitleAkas table.
CREATE_TITLE_AKAS_TABLE = '''CREATE TABLE IF NOT EXISTS TitleAkas(
                                id integer PRIMARY KEY AUTOINCREMENT,
                                titleId varchar NOT NULL,
                                ordering integer,
                                title varchar,
                                region varchar,
                                language varchar,
                                types varchar,
                                attributes varchar,
                                isOriginalTitle integer,
                                FOREIGN KEY(titleId) references TitleBasics(tconst)
                            );'''

# Command used to create the TitleRatings table.
CREATE_TITLE_RATINGS_TABLE = '''CREATE TABLE IF NOT EXISTS TitleAkas(
                                id integer PRIMARY KEY AUTOINCREMENT,
                                tconst varchar NOT NULL,
                                averageRating real,
                                numVotes integer,
                                FOREIGN KEY(tconst) references TitleBasics(tconst)
                            );'''

# Command used to create the NameBasics table.
CREATE_NAME_BASICS_TABLE = '''CREATE TABLE IF NOT EXISTS TitleAkas(
                                id integer PRIMARY KEY AUTOINCREMENT,
                                nconst varchar NOT NULL,
                                primaryName varchar,
                                birthYear integer,
                                deathYear integer,
                                primaryProfession varchar,
                                knownForTitles varchar
                            );'''

CREATE_TABLE_LIST = [
    CREATE_TITLE_BASICS_TABLE,
    CREATE_TITLE_AKAS_TABLE,
    CREATE_TITLE_RATINGS_TABLE,
    CREATE_NAME_BASICS_TABLE
]
