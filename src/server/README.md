# Server

## Database Configuration

### Bins
```sql
CREATE TABLE "Bins" (
	"sensor_id"	TEXT NOT NULL,
	"lat"	FLOAT NOT NULL,
	"long"	FLOAT NOT NULL,
	"fall_status"	BOOLEAN,
	"battery"	FLOAT,
	"time_online"	INTEGER NOT NULL,
	"entry_id"	TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL,
	"fill_level"	FLOAT,
	"temperature"	FLOAT,
	"fire_status"	BOOLEAN,
	"orientation"	TEXT,
	PRIMARY KEY("entry_id"),
	UNIQUE("entry_id")
);
```

### Bounty
```sql
CREATE TABLE "Bounty" (
	"id"	INTEGER NOT NULL,
	"timestamp"	TEXT NOT NULL,
	"bin_id"	TEXT,
	"message"	TEXT NOT NULL,
	"points"	INTEGER NOT NULL,
	"type"	TEXT,
	"assigned_usr_id"	INTEGER,
	"time_assigned"	TEXT,
	"completed"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("id")
);
```

### Regression
```sql
CREATE TABLE "Regression" (
	"sensor_id"	TEXT NOT NULL,
	"angle"	FLOAT NOT NULL,
	"timestamp"	TEXT NOT NULL,
	PRIMARY KEY("sensor_id"),
	UNIQUE("sensor_id")
);
```

### Reports
```sql
CREATE TABLE "Reports" (
	"report_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"details"	TEXT,
	"status"	TEXT NOT NULL,
	"updated"	DATETIME NOT NULL,
	PRIMARY KEY("report_id")
);
```

### Trucks
```sql
CREATE TABLE "Trucks" (
	"id"	INTEGER NOT NULL,
	"status"	INTEGER NOT NULL,
	"fullness"	INTEGER NOT NULL,
	"lat"	FLOAT NOT NULL,
	"long"	FLOAT NOT NULL,
	"updated"	DATETIME NOT NULL,
	PRIMARY KEY("id")
);
```

### Users
```sql
CREATE TABLE "Users" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"password"	VARCHAR(64) NOT NULL,
	"email"	VARCHAR(80) NOT NULL,
	"created"	DATETIME NOT NULL,
	"role"	TEXT,
	"points"	INTEGER NOT NULL,
	"admin"	BOOLEAN NOT NULL,
	UNIQUE("username"),
	PRIMARY KEY("id")
);
```

## Miscellaneous Utilities

src.utils.utils is a package containing various functions used over the project

### `rand_perc(inc: bool = False, neg: bool = False, center: bool = False) -> float`

Returns a random percentage in range [0, 1]

#### Flags
- inc: changes the range to [1, 2]
- neg: changes the range to [-1, 0]
- center: changes the range to [-1, 1]

### `is_perc(perc: float) -> bool)`

Returns `True` if `perc` is a percentage (between 0 and 1)

### `rand_check(chance: float) -> bool`

Makes a random check that has `chance` chances to succeed. Returns `True` on success and `False` in failure.
