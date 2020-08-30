# Fortuna

Command line note displayer and randomizer.

## Usage

Fortuna creates and displays a TODO list based on a global configuration. It caches the selections made (if configured to be stashed until a renewal date) and displays histories as required.

A typical note generated would look like so:

```
This is your Fortune for today, <date>:

Daily TODO:

1. <item_1>
2. <item_2>
...

Today's Chore: <random_item>
...
```

## Configurations

### Global Configuration Structure

The global configuration is stored in a file named `global.fortuna.json`:

```
{
    "<list_name>": {
        "type"    : "RANDOMIZE" | "RANDOMIZE_AND_CACHE" | "SELECT_ALL",
        "options" : ["<option>", ...],
        "renewal" : <renewal_period_in_days>
    }
    ...
}
```

### List Types

* `RANDOMIZE`           : This is the most basic list generation option. A single item form the list is returned at random. 
* `RANDOMIZE_AND_CACHE` : Return a single item from the list and cache it so it does not reappear until the `renewal` period has expired.
* `SELECT_ALL`          : Always return all items in the list. This option is recommended for portions of your TODO that you want to appear daily.

### Cache Structure

Generated notes are cached in files that are named after the date on which they are generated: `<YYYYMMDD>.fortuna.json`. The structure of a cached note is:

```
{
    "date": <date>,
    "<list_name>": [<selections>] | "<selection>"
}
```

To avoid searching all old notes to update renewals, an additonal file, `renewals.fortuna.json`, to save cache state is maintained:

```
{
    "<list_name>": {
        "cached_to_renew": [
            { "selection": "<option>", "date_cached": <date>, "renewal": <renewal_period_in_days>}
        ]
    }
}
```