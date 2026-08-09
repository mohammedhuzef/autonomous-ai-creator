# Autonomous AI Video Agent — Prompt Log

## Prompts Used (Current Session)

1. **"I have an idea for an autonomous AI video agent — it looks at trending Shorts and turns them into new AI-generated content. Help me plan it out step by step."**
   *Result:* We planned the pipeline — first pull YouTube data, then send it to Gemini for analysis, then generate an image, then turn that into a video.

2. **"Let's start building — set up the YouTube API first."**
   *Result:* Made a Google Cloud project, turned on the YouTube Data API v3, and got an API key.

3. **"Write the code to fetch trending videos and send them to Gemini for analysis."**
   *Result:* Got the first version of `pipeline.py` working.

4. **Ran into a bunch of setup problems — wrong Python interpreter, missing modules, the app crashing because of emojis in the print statements, and YouTube search giving zero results.**
   *Result:* Fixed them one by one — pointed to the correct Python, installed what was missing, took out the emojis, and loosened the search filters so it could actually find videos.

5. **Got a `429 RESOURCE_EXHAUSTED` error from Gemini.**
   *Result:* Turned out `gemini-2.5-pro` had no free quota left. Switched to `gemini-2.5-flash`, then to `gemini-3.5-flash` after that one got deprecated too.

6. **"The image quality is bad, fix it."**
   *Result:* Switched to the `flux` model on Pollinations and turned on `enhance=true`, which made the images sharper.

7. **The image came out looking too realistic instead of cartoon-style, which wasn't the look we wanted.**
   *Result:* Changed both the Gemini prompt and the image prompt to force a cartoon style and stop it from making realistic people.

8. **Didn't want to pay for Kling for the video part, so decided to make our own zoom effect instead.**
   *Result:* Wrote a simple zoom animation using MoviePy and PIL that slowly zooms into the image over 5 seconds.

9. **Got a `moviepy.editor` import error because of a newer library version.**
   *Result:* Fixed the code so it works with both the old and new MoviePy versions.

10. **"Make this run on all 5 trending videos, not just one."**
    *Result:* Rewrote the code so it loops through all 5 videos automatically instead of just testing on one.

11. **Noticed the API keys were sitting directly in the code, which isn't safe if we're pushing to GitHub.**
    *Result:* Moved the keys into a separate `.env` file, and added `.gitignore` and `.env.example` so the real keys never get uploaded.

12. **Asked for a frontend so the results could be seen without using the terminal.**
    *Result:* Built a Streamlit app (`app.py`) that runs the pipeline and shows the generated images and videos on a webpage.

13. **Wasn't happy with how plain the first version of the frontend looked, and asked for something that felt more like a real, designed app.**
    *Result:* Redesigned it with a proper theme — a gold-and-black color scheme, custom fonts, and a "broadcast" concept, with a live "on air" indicator while the pipeline runs instead of a plain loading spinner.

14. **Asked for the app to be split into proper phases, like Welcome, Run, and Archive, instead of one long page.**
    *Result:* Rebuilt the frontend with three separate screens and navigation between them — a welcome/intro screen, a console screen to start a run, and an archive screen to browse all the generated results.

15. **Wanted a way to launch the app without typing commands every time.**
    *Result:* Created a `run_app.bat` file that starts the Streamlit app with a single double-click.

16. **"The project's name is Nova."**
    *Result:* Renamed the app and its branding from the placeholder name to Nova across the frontend, README, and documentation.