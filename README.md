# **CTTRPG**

#### *Console Table Top Role Playing Game*
A ncurses application to take notes for your table top rpg games. Notes are written on "cards", organized in "decks". A sample deck is available to explore.

## **Known Problems**
- Only runs on linux for the moment
- Tags not implemented
- No way to add a description to a card yet

## **Planed features**
- More actions with tags
- Color assignment to tags, color themes
- Name completion using levenshtein distance
- Dice roll
- Random encounter tables


## Dependencies
Python3

## Install
Download this github repository, get inside it and run `python cttrpg.py`

## Commands

Escape commands are `quit`, `q`, `exit` and will exit the application or the dialog currently opened.

### Commands that are always available

| Command                        | Description |
|--------------------------------|-------------|
| `open <card name>`             | Opens the given card name. Saves the currently opened card. |
| `<card name>`                  | No command is a shortcut for `open`. |
| `new [card\|tag\|category]`    | Opens the dialog for creation. |
| `delete [card\|tag\|category]` | Opens the dialog for deletion |
| `list`                         | Lists all the cards available to be opened. |
| `show [category\|card\|tag]`   | Not implemented yet |
| `colors`                       | Shows the available colors. |
| `debug`                        | Displays informations about the application. |


### Commands available when a card is opened

| Command                | Description |
|------------------------|-------------|
| `close [nosave]`       | Closes the currently opened card. Will not save if passed `nosave`|
| `add [note\|tag]`      | Opens the dialog to add a note or a tag. |
| `note [ \|content]`    | Shortcut for `add note`. If no `content` is give, will prompt a dialog for it.
| `tag [ \|tagname]`     | Shortcut for `add tag`. If no `tagname` is give, will prompt a dialog for it. |
| `remove [note\|tag]`   | Opens the dialog to remove a note or a tag. |
