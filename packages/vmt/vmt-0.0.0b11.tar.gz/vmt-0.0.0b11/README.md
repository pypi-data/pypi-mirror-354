# vmt
Track, play, and browse your locally accessible media.

## Why use vmt?
Good question.

You've got plenty of ways to watch and track your media. Popular options are
jellyfin or plex. These are great both applications, but for me they are totally
overkill.

My needs:

  - [X] 100% offline functionality
  - [X] 100% local tracking
  - [X] Simple directory structure
  - [X] Tracks last watched episodes
  - [X] Tracks last watched shows
  - [X] Full mpv support

I made vmt to tick all of these boxes and it does just that in a simple way.

## Only for local files?
Not necessarily. You can mount a remote filesystem using NFS, sshfs, or SMB.
I'm sure there are tons of other ways to mount remote file systems so that they
are available on your local machine.

The only requirement is that you can cd into the directory that has the files
you want to add to your library. If you can do that you can use vmt to track and
watch these videos.

## 100% local? 100% offline?
Yep. But it doesn't have to be.

Feel free to setup `~/.config/vmt` as a syncthing share and keep your library
and progress synced across your laptop(s) and desktop(s), maybe even your phone
via termux (untested but maybe).

## Installation
Can install the usual way:

```bash
pip install vmt
```

Then run `vmt --build` and get taken through the setup process via a TUI interface.

### Dependencies
- dmenu, fzf, or rofi
- mpv

## Using vmt
Now that you've built your library you can start watching and tracking your anime.

As you've just built your library you don't have a log yet. Because of that you
are going to want to run this command, either through dmenu, a terminal, or via
some hot-key:

```bash
vmt -w
```

You will get prompted with a list of all the titles in your library. Select one
of the show titles and you will get another prompt displaying all the episodes
found for that show. Select an episode and watch some anime.

Please see [this](https://github.com/johndovern/vmt#Note-on-use-with-hot-keys)
section for more info on starting vmt via a hot-key or dmenu.

### Watching your last watched shows
At this point vmt is tracking the shows you watch in your library and history log. You can now run following command through dmenu, a terminal, or via a hot-key:

```bash
vmt -l
```

With this you will see a dmenu or fzf prompt showing you the titles of your last
watched shows. These shows are getting tracked which means once you select one mpv
will open and start playing your last watched episode.

It is advisable that you close mpv on the episode you wish to resume. You can
also use `Q` instead of `q` to save and quit (an mpv native feature which has
nothing to do with vmt). Then you'll start off exactly where you left off.

## vmt.lua
The secret sauce of vmt is the vmt.lua script. This script can work in two ways:

  1. Enable it by default via `script-opts/vmt.conf` by setting

      `enabled=yes`

  2. Enable it when you run mpv like so

      `mpv --script-opts=vmt-enabled=yes /path/to/file`

The full path to `script-opts/vmt.conf` is `~/.config/mpv/script-opts/vmt.conf`.

If you leave this file alone you must launch mpv with 
`mpv --script-opts=vmt-enabled=yes /path/to/file` to enable vmt.lua.

This is too long to type out. Instead you can use vmt as an mpv wrapper by
running `vmt -o /path/to/file` which will enable vmt.lua. Both `vmt -w` and `-l`
launch mpv in this way.

### How vmt.lua works
When enabled vmt.lua will get the currently playing file's path and set it to
the variable `trackPath`. After that it will run `vmt -s "$trackPath"`. The `-s,
--search` flag takes a file path and searches the shows in your library for the
given file. If the file gets found it will exit successfully. If it isn't found
vmt will exit with an error code.

If the search was successful vmt.lua will then run `vmt -t "$trackPath"`. The
`-t, --track` flag takes a file path. It repeats the same search as `-s` just to
be safe. If the search is successful your library and history log will be
updated appropriately.

## Updating your library
To update your library just run `vmt -u`. This will backup your current library
in case you don't like how the update went. You can use the `-c, --clean` flag
if you don't want to keep a backup.

When you update your library vmt will do it's best to detect any shows that
already exist in your library and still exist in your `base_dir`. If a show has
not changed locations then any episode progress will get carried over to the
updated library along with any title you may have set for the show.

If the shows directory has changed it will get treated as a new show and your
show progress will get lost. I do not have any simple way around this and I do
not consider this an issue.

Any new shows will get added with an automatically generated title.

### Updating interactively
If you wish to set the title yourself use the `-i, --interactive` flag. You should also use the `-d` flag and be sure to run vmt in a terminal.

Running `vmt -d -i -u` will give you a prompt asking you to set a title for the given show. It will also display either the previous title or an automatically generated title if the show is new. If you are using dmenu you can press ESC to accept the previous or automatic title. If you are using fzf this will be a read prompt in which case enter nothing to accept the previous or automatic title.

## Wrapping up
### Valid extensions
I mentioned earlier that only directories with valid file extensions are considered shows and added to your library. So what is a valid file extension? Well, here is a list of all file extensions that vmt considers valid:

  - mkv
  - mp4
  - mpg
  - mp2
  - mpeg
  - mpe
  - mpv
  - ogg
  - webm
  - m4p
  - m4v
  - avi
  - wmv
  - mov
  - qt
  - flv
  - swf
  - avchd

You might be thinking "Wow, that's a lot of extensions! The find command must be very long." Well, you're half right. That is a lot of extensions but the _find_ command is very short.

#### How vmt build's your library
This is the command that vmt uses to build your library:

```bash
  while read -r DIR ; do
    ...
  done < <(find "${BASE_DIR}" -type f -printf '%P\n' | \
    sed '/^.*\.\(mkv\|mp4\|mpg\|mp2\|mpeg\|mpe\|mpv\|ogg\|webm\|m4p\|m4v\|avi\|wmv\|mov\|qt\|flv\|swf\|avchd\)$/!d;s/\(^.*\)\/.*$/\1/g' | \
    sort -u)
```

Maybe it's just my system but when I give `find` a lot of flags it runs very slowly. For that reason I am using sed to filter find's results.

If a file path does not end in one of the given file extensions it is filtered from the results.

Any path that does end in a valid extension is then striped of the file leaving only the directory.

Finally we sort the directory results to ensure they are in alphabetical order and unique.

Pretty simple and most importantly fast. However, you want to make sure your `BASE_DIR` is as close to your videos as possible. Don't set it to `$HOME` if all your videos are in `~/Videos/Anime`.

### Automatically generated titles
I've mentioned these automatically generated titles a few times, but what the heck does that look like? Well, here is an example:

```bash
$ DIR="[Commie] Space Dandy - Volume 6 [BD 720p AAC]"
$ CLEAN_TITLE="$(printf '%s\n' "${DIR//\// - }" | sed 's/\s\+\?\[[^]]*\]\s\+\?//g')"
$ printf '%s\n' "${CLEAN_TITLE//[\!\\@#$%^&*\{\}\/<>?\'\":+\`|=]/-}"
Space Dandy - Volume 6
```

All the info that comes with a torrent is great but it doesn't look great. This it a pretty effective way of cleaning most directories and getting something that looks like a title.

Here is another example. This is a larger torrent with a path that is two directories deep:

```bash
$ DIR="[Anime Time] Little Busters! (S1+S2+S3+OVA) [BD][HEVC 10bit x265][AAC][Eng Sub]/Little Busters! Season 1"
$ CLEAN_TITLE="$(printf '%s\n' "${DIR//\// - }" | sed 's/\s\+\?\[[^]]*\]\s\+\?//g')"
$ printf '%s\n' "${CLEAN_TITLE//[\!\\@#$%^&*\{\}\/<>?\'\":+\`|=]/-}"
Little Busters- (S1-S2-S3-OVA) - Little Busters- Season 1
```

The output isn't perfect, but boy does it happen fast and looks a whole lot better.

When using vmt if you use the `-i` flag when updating or building your library you will get a chance to see a preview of what the title will look like if you enter nothing. So you can make the call on what you want your anime titles to be.

### Note on use with hot-keys
I use sxhkd to start vmt for most operations. I also use dmenu as my default prompt. If this is you then vmt will "just work".

If you use fzf you want to start vmt with a hot-key you will need to make sure you do this within a terminal. I use st which means I would put this in my sxhkdrc:

```bash
super + a
  st -e vmt -w
```

This ensures that vmt is running in a terminal and that you will be able to respond to the fzf or read prompts.

### Browsing your BASE_DIR
If you've set a `FILE_MANAGER` then you can run vmt with the `-B, --browse` flag. This will open your `BASE_DIR` in your chosen FILE_MANAGER.

## Disclaimer
This project is considered complete. The scope of features I set out to implement has been achieved. If you have a feature suggestion I will gladly hear and consider it. I may add new features but at present I can't think of anything I would add to this project. If anything I would like to strip it down more and make it more portable.

I have done a limited amount of testing relative to the possible directory names and structures that vmt may encounter. If you run into an error (my guess is that it has to do with sed) then please open an issue with as much relevant information as needed. I will do my best to come up with a solution or review any proposed solutions.
