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

12. **"The dashboard says 'API Connections'. Change it to 'YouTube Live Sync' and add a retry feature so it doesn't crash on bad internet."**
    *Result:* Updated the Streamlit UI and added a `try-except` retry block for fetching YouTube data.

13. **"Files aren't generating and the app keeps crashing because of emojis in the video titles."**
    *Result:* Forced the terminal to use UTF-8 encoding so emojis don't crash the app.

14. **"Gemini is throwing a `429 RESOURCE_EXHAUSTED` limit error. Add a cooldown."**
    *Result:* Added a 35-second sleep timer and a retry loop in `analyze_video()`.

15. **"It's still failing. I think my entire daily quota is gone. Let's test a different model."**
    *Result:* Tested `gemini-1.5-flash`, confirmed it's a hard daily limit, and switched back to wait for the reset.

16. **"Add a Troubleshooting section to the Readme explaining this Gemini quota error."**
    *Result:* Wrote the instructions at the bottom of `Readme.md`.

17. **"I keep getting a `RuntimeError: Event loop is closed` when I refresh the page. Fix it."**
    *Result:* Wrapped the UI updates in a `try-except` block so it shuts down quietly instead of throwing red errors.

18. **"How do I push all these updates to my GitHub repo if it says 'origin already exists'?"**
    *Result:* Ran `git pull origin main --rebase` to sync the changes, then pushed everything successfully.
