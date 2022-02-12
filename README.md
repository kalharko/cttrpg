# **CTTRPG**

#### *Console Table Top Role Playing Game*
A ncurses application to take notes for your table top rpg games. Notes are written on "cards", organized in "decks". A sample deck is available to explore.

This is not a database system however, no transaction logic, no undo either. Only direct editing of .txt files.

![Screenshot of the result of command list with a card opened](/ScreenShots/list_and_card.png)
Screenshot of the result of the `list` command with a card opened.

## **Known Problems**
- Only runs on linux for the moment
- Default configuration and sample deck are written in french, more language support to come
- Uncommented code :anxious_grin:
- No way to delete a color, change a tag's color

## **Planed features**
- More command shortcuts
- Name completion using levenshtein distance
- Dice roll
- Random (encounter, loot, spell, poison ...) tables
- Hypertext references between cards
- Not case sensitive tags and categories


## Dependencies
Python3

## Usage
To install, download this github repository and get inside it :  
`git clone https://github.com/kalharko/cttrpg`  
`cd cttrpg`

To use, run the python file called `cttrpg.py` from inside the cttrpg folder:  
 `python cttrpg.py`

 To update, simply pull from the github repository :  
 `git pull`  
 Your decks will not be discarded.

 To transfer your deck to another computer, you can copy your deck folder from `cttrpg/data/<your deck name>`

## Commands

Escape commands are `quit`, `q`, `exit` and will exit the application or the dialog currently opened.

### Commands that are always available

| Command                           | Description |
|-----------------------------------|-------------|
| `open <card name>`                | Opens the given card name. Saves the currently opened card. |
| `<card name>`                     | No command is a shortcut for `open`. |
| `new [card\|tag\|category\|color]`| Opens the dialog for creation. |
| `delete [card\|tag\|category]`    | Opens the dialog for deletion |
| `list [tag\|category]`            | Lists all the cards available to be opened ordered by tag or category, category by default.|
| `show <card tag or category name>`| Not implemented yet |
| `colors`                          | Shows the available colors. |
| `debug`                           | Displays informations about the application. |
| `reload`                          | Reloads the deck's configuration file. |


### Commands available when a card is opened

| Command                              | Description |
|------------------------|-------------|
| `close [nosave]`                     | Closes the currently opened card. Will not save if passed `nosave`|
| `add [note\|tag]`                    | Opens the dialog to add a note or a tag. |
| `note [content]`                     | Shortcut for `add note`. If no `content` is give, will prompt a dialog for it.
| `tag [tagname]`                      | Shortcut for `add tag`. If no `tagname` is give, will prompt a dialog for it. |
| `remove [note\|tag]`                 | Opens the dialog to remove a note or a tag from the opened card. |
| `edit [name\|subtitle\|description]` | Opens the dialog to edit the name, subtitle or description of the opened card |
