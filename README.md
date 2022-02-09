# **CTTRPG**

#### *Console Table Top Role Playing Game*
A ncurses application to take notes for your table top rpg games. Notes are written on "cards", organized in "decks". A sample deck is available to explore.

This is not a database system however, no transaction logic, no undo either. Only direct editing of .txt files.

## **Known Problems**
- Only runs on linux for the moment
- Tags not implemented
- No way to add a description to a card yet
- Default configuration and sample deck are written in french, more language support to come
- Uncommented code :anxious_grin:

## **Planed features**
- More actions with tags
- Color assignment to tags, color themes
- Name completion using levenshtein distance
- Dice roll
- Random (encounter, loot, spell, poison ...) tables
- Hypertext references between cards


## Dependencies
Python3

## Usage
To install, download this github repository and get inside it :  
`git clone https://github.com/kalharko/cttrpg`  
`cd cttrpg`

To use, run the python file called `cttrpg.py` from inside the cttrpg folder:  
 `python cttrpg.py`

## Commands

Escape commands are `quit`, `q`, `exit` and will exit the application or the dialog currently opened.

### Commands that are always available

| Command                           | Description |
|-----------------------------------|-------------|
| `open <card name>`                | Opens the given card name. Saves the currently opened card. |
| `<card name>`                     | No command is a shortcut for `open`. |
| `new [card\|tag\|category]`       | Opens the dialog for creation. |
| `delete [card\|tag\|category]`    | Opens the dialog for deletion |
| `list`                            | Lists all the cards available to be opened. |
| `show <card tag or category name>`| Not implemented yet |
| `colors`                          | Shows the available colors. |
| `debug`                           | Displays informations about the application. |


### Commands available when a card is opened

| Command                              | Description |
|------------------------|-------------|
| `close [nosave]`                     | Closes the currently opened card. Will not save if passed `nosave`|
| `add [note\|tag]`                    | Opens the dialog to add a note or a tag. |
| `note [content]`                     | Shortcut for `add note`. If no `content` is give, will prompt a dialog for it.
| `tag [tagname]`                      | Shortcut for `add tag`. If no `tagname` is give, will prompt a dialog for it. |
| `remove [note\|tag]`                 | Opens the dialog to remove a note or a tag from the opened card. |
| `edit [name\|subtitle\|description]` | Opens the dialog to edit the name, subtitle or description of the opened card |
