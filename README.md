# File Explorer
Browse, rename, delete, move and update files and directories on Windows.

## View
You can switch between two view modes (View → Toggle adjacent explorer):
* double (default) – view two directories in separate frames with a transport bar in the middle
* single – regular single directory frame
If you toggle the double mode off, every new open tab will be single until you toggle it back on again.

## Tabs
You can view directories in tabs. (View→ Open/Close (tab). There is no open tab upper limit. Keep in mind that I haven’t tested the behavior with let’s say 10000 tabs open.

## Functionality
### Browse
You can insert a directories path into the address bar to display it. Every tab you open displays the default directory (currently logged users „Documents” dir. C:\Users\current_user\Documents).
To display the currently viewed dir parent, click on the button on the left from the address bar.
To submit an address click button on the right or hit the „Enter” key. If you enter an invalid path, an error message will be displayed and the last valid path will replace the invalid one.

## Rightclick context menu
### Rename
rename one or multiple files/directories. When renaming files, skip their extension. It is omitted and can’t be changed.
* single object – display a rename entry. Rename if the new name is unique, display an error otherwise
* multiple objects – display a top-level with a prefix, name, and suffix entries. Object index will be added to the name. There are three predefined prefixes/suffixes:
  * %today%: today Format "%Y%m%d"
  * %creationd%: source file creation date. Format "%Y%m%d"
  * %creationdt%: source file creation DateTime. Format "%Y%m%d%H%M%S"
### Copy
store one or more objects to later paste their copies. Source objects are left unchanged.
### Cut
store one or more objects to later move them somewhere else. Source objects are deleted.
### Paste
paste or move object stored earlier (Copy/Cut). If an object with the same name exists in the destination directory – add a suffix „_copy_i” – i is the number of files named „src_copy_”.
Does nothing if there was no previously copied or cut object.
### Delete
permanently delete an object. ***The operation can’t be undone. Clears cache.***

## Transfer frame (only in double view)
Copy right (>) button – copy selected left to right
Move right (») button – move selected left to right
Copy left (<) button – copy right to left
Move left («) button – move right to left

## Undo/Redo
All actions except deletion can be undone and redone. (See keyboard shortcuts)

## Keyboard shortcuts
* CTRL+z – undo action
* CTRL+y – redo previously undone action
* CTRL+w – close tab
* CTRL+t – open a new tab
* CTRL+x – cut
* CTRL+c – copy
* CTRL+v – paste
