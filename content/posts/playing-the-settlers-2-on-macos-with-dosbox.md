---
title: Playing The Settlers 2 on macOS with DOSBox
date: 2024-10-06T20:09:12+02:00
draft: false
---
[DOSBox] emulates an old Intel x86 PC for running old MS-DOS games on modern computers – including the original [The Settlers 2], the first computer game I've ever played, but which unfortunately no longer runs on modern computers and operating systems.

The German edition of The Settlers 2 is freely available [here](https://www.chip.de/downloads/Die-Siedler-2-Gold-Edition_116251848.html).
Simply download and extract the content into a folder, for example: `/Applications/Siedler2/`.

After installing DOSBox:

1. Open DOSBox application
2. Mount folder where game is installed: `mount C /Applications/Siedler2/`
3. Navigate into mounted folder: `C:`
4. Launch the game: `S2.EXE`

You can press `Option-Enter` to enter full-screen mode in DOSBox.
Press it again to switch back to windowed mode.

You can also configure DOSBox to automatically mount folders on start-up.
In the `[autoexec]` section of the DOSBox settings file `/Library/Preferences/DOSBox 0.74-3-3 Preferences`, add:

```bash
mount C ~/Applications/Siedler2/
```

For more details, see the DOSBox [wiki].

There is also a community-developed addon, called [Return To The Roots], including new game settings, maps and buildings.

[DOSBox]: https://www.dosbox.com/
[The Settlers 2]: https://settlers2.net/
[wiki]: https://www.dosbox.com/wiki/DOSBox_and_Mac_OS_X
[Return To The Roots]: https://www.siedler25.org/
