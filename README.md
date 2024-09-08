<div align="center">
  <a href="https://twitter.com/shironappa_">
      <img src="https://cdn.discordapp.com/attachments/1255158843546271866/1277637460620480533/main.png?ex=66cde41b&is=66cc929b&hm=9a91acfc9e3f34f5946d59a4f6fbbed8486c98bf6b92e79635616287827d37ab&" alt="Illustration by Shironappa">
  </a>
  <p>Art by Shironappa</p>
  <h1>Ugoku-v2 Discord Bot</h1>
</div>
<b>A work in progress rework of <a href='https://github.com/Shewiiii/Ugoku-bot'>Ugoku !</a>, completely refactored and lightweight~</b>
<h2>Features/To do</h2>
<b>Unticked boxes are work in progress.</b>

- [X] Ping.
- [X] Echo messages (make the bot say any message).
- [X] Download stickers from LINE.
- [ ] Download songs, albums or playlists from Spotify.
- [X] Play songs in a voice channel.
  - [X] Skip, Show queue, Autodetect and add songs/albums, or playlists.
  - [X] Loop song, Loop queue, pause, resume...
  - [X] Bypass the channel's audio bitrate.
  - [X] Stream songs from Spotify.
  - [X] Play songs from a URL (custom source).
  - [X] Cache audio from custom sources.
  - [ ] Embed info messages with metadata (partially done).

> [!NOTE]
> Ugoku-v2 is only using Spotify or Youtube as streaming service sources, so the best audio chain (besides custom sources) is OGG 320kbps -> Opus 510kpbs. However the audio quality is extremely similar to FLAC -> Opus 510kpbs

- [X] Play 音声作品 (audio works) in a voice channel (because why not).
- [ ] Chat using GPT-4o Mini.
- [ ] And maybe more in the future~

<h2>Known bugs to fix</h2>

- Queue not showing when too many characters in the queue/loop section.
  ("In data.embeds.0.fields.1.value: Must be 1024 or fewer in length.").
- Can't play audio works without MP3 Files in it.