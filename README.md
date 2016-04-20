err-karma
=========

Overview
--------

[Errbot](https://github.com/errbotio/errbot) karma plugin.

Listens to conversations in a chatroom and increases/decreases karma for random
strings. Example:

```
│13:56:19  br0ziliy | beer++
│13:56:19    errbot | br0ziliy: beer karma is now 3
│13:56:20  br0ziliy | some.things++
│13:56:20    errbot | br0ziliy: some.things karma is now 1
│13:56:20  br0ziliy | other.things--
│13:56:20    errbot | br0ziliy: other.things karma is now -5
```

Unicorns provided too!

Commands
--------

Plugin exposes following commands to a user:

- `srank` - shows top 10 list of strings with highest karma

Configuration
-------------

Bot can be configured to ignore some words, or some users:

```
!plugin configure Karma { 'blacklist': ["tea", "coffee"], 'ignore_users': ["foo", "bar"] }
```

In the example above, `tea++` or `coffee--` will not have effect.
Also messages from user **foo** and user **bar** will be ignored by plugin
completely.

License
-------

Released into public domain. Do with it as you wish!
