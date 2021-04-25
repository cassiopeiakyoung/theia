# theia
## Inspiration
We decided to do this project as we saw the failure in conventional moderation tools for Discord such as Dyno, which has auto-moderation settings but has many flaws that come with it. Especially as lockdowns kept people indoors, more people were able to stay anonymous allowing incentivizing them on posting more racist or sexist content.

## What it does
Theia is a bot that scans user uploaded attachments such as images, videos, gifs, and audio files. By using machine learning, we are able to moderate these attachments as we were actually looking at them. Theia is able to delete messages containing banned content within a few frames from looking at it.

## How we built it
We bootstrapped this project in discord.py, using a few libraries including opencv, moviepy, pytesseract, and speech_recognition to identify the content in attachments.

## Challenges we ran into
We ran into a lot of challenges while building Theia, one of the major ones, is that Discord embeds content is rendered locally so checking for message.embeds only worked half the time as the content didn't cache, this lead to the bot not responding to some attachments.

## Accomplishments that we're proud of
We are proud of Theia being able to detect and delete offensive content within milliseconds as it sees it. It only takes one frame to get a message flagged and deleted. Additionally, we have noticed no false positives with this system as of yet. 

## What we learned
We learned how to interact with object oriented python environment as well as interacting with the Discord api wrapper. Since discord.py is much smaller than discord.js, there were almost next to no resources to help us troubleshot.

## What's next for Theia
We plan to add a lot features for Theia if people are interested in the project, some features include sharding to expand on the performance of the bot.
