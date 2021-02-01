#    Copyright (C) Midhun KM 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import os
import time

import wget
from telethon.tl.types import DocumentAttributeAudio
from uniborg.util import edit_or_reply, friday_on_cmd, sudo_cmd
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos

from virtualuserbot import CMD_HELP
from virtualuserbot.Configs import Config
from virtualuserbot.function import progress
from virtualuserbot.function.FastTelethon import upload_file
from virtualuserbot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


@friday.on(friday_on_cmd(pattern="ytmusic ?(.*)"))
@friday.on(sudo_cmd(pattern="ytmusic ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    urlissed = event.pattern_match.group(1)
    myself_stark = await edit_or_reply(
        event, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    if not os.path.isdir("./music/"):
        os.makedirs("./music/")
    path = Config.TMP_DOWNLOAD_DIRECTORY
    url = mo
    sedlyf = wget.download(kekme, out=path)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "480",
            }
        ],
        "outtmpl": "%(title)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except Exception as e:
        await event.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    await asyncio.sleep(20)
    c_time = time.time()
    file_stark = f"{ytdl_data['title']}.mp3"
    lol_m = await upload_file(
        file_name=file_stark,
        client=borg,
        file=open(file_stark, "rb"),
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading Your Song!", file_stark)
        ),
    )
    capy = f"**Song Name ➠** `{thum}` \n**Requested For ➠** `{urlissed}` \n**Channel ➠** `{thums}` \n**Link ➠** `{mo}`"
    await event.delete()
    await borg.send_file(
        event.chat_id,
        lol_m,
        force_document=False,
        allow_cache=False,
        caption=capy,
        thumb=sedlyf,
        attributes=[
            DocumentAttributeAudio(
                duration=int(ytdl_data["duration"]),
                title=str(ytdl_data["title"]),
                performer=str(ytdl_data["uploader"]),
            )
        ],
        supports_streaming=True,
    )
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@friday.on(friday_on_cmd(pattern="utubevid ?(.*)"))
@friday.on(sudo_cmd(pattern="utubevid ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    urlissed = event.pattern_match.group(1)
    myself_stark = await edit_or_reply(
        event, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    if not os.path.isdir("./music/"):
        os.makedirs("./music/")
    path = Config.TMP_DOWNLOAD_DIRECTORY
    url = mo
    sedlyf = wget.download(kekme, out=path)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(title)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except Exception as e:
        await event.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['title']}.mp4"
    lol_m = await upload_file(
        file_name=file_stark,
        client=borg,
        file=open(file_stark, "rb"),
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading Your Video!", file_stark)
        ),
    )
    capy = f"**Video Name ➠** `{thum}` \n**Requested For ➠** `{urlissed}` \n**Channel ➠** `{thums}` \n**Link ➠** `{mo}`"
    await event.delete()
    await borg.send_file(
        event.chat_id,
        lol_m,
        force_document=False,
        allow_cache=False,
        caption=capy,
        thumb=sedlyf,
        attributes=[
            DocumentAttributeAudio(
                duration=int(ytdl_data["duration"]),
            )
        ],
        supports_streaming=True,
    )
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "ytmusic": "**Ytmusic**\
\n\n**Syntax : **`.ytmusic <song name>`\
\n**Usage :** Downloads songs from ytmusic"
    }
)
