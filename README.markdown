I've been giving my data to Last.FM for years - it's time I cashed out on this
investment and got my data out, so I can make some pretty visualizations.

I hacked up this script to get all my scrobble information, and make a playlist
of each day.

After running it, you have a JSON representation of all your scrobbles in a big
array (containing all the information pulled form the Last.FM API), in `all_scrobbles.username.json`.

And you also get a text file for each day containing what you listened to that
day, named like `2010-12-14-username.txt`, and containing lines like 
`2011-03-23 17:48:43 - Passion Pit - Manners - Seaweed Song`.

Usage:

    ./get_lastfm.py --user=yourlastfmusername
