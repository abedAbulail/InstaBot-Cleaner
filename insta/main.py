from instagrapi import Client
import time
import random
import os
import google.generativeai as genai
from better_profanity import profanity
from instagrapi.exceptions import FeedbackRequired
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app=FastAPI()


class LoginRequest(BaseModel):
    username: str
    password: str


# This is a sample code to make react connect to fastapi.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/delete_comments")
def delete(request: LoginRequest):
    delete_comments = 0
    username = request.username
    password = request.password
    key = "Your Api Key Here"
    cl = Client()
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    def challenge_code_handler(username, choice):
        print(f"Instagram is sending a code to: {choice}")
        code = input("Enter the code: ")
        return code

    cl = Client()
    cl.challenge_code_handler = challenge_code_handler

    if os.path.exists("session.json"):
        try:
            cl.load_settings("session.json")
            cl.login(username, password)
            print("Logged in as:", cl.username)
        except Exception as e:
            print(f"⚠️ Failed to load or validate session: {e}")
            cl.login(username, password)
            cl.dump_settings("session.json")
    else:
        cl.login(username, password)
        print("Logged in as:", cl.username)
        cl.dump_settings("session.json")

    user_id = cl.user_id

    try:
        clips = cl.user_clips(user_id, amount=1)
        print("Fetched reel:", clips[0].id)
        for clip in clips:
            try:
                if clip is None:
                    continue
                allComments = cl.media_comments(clip.id)
                for comment in allComments:
                    oneComment_id = comment.pk
                    print(comment.text)
                    dirty = profanity.contains_profanity(comment.text)
                    if dirty:
                        print(f"Deleting comment {oneComment_id} by profanity.")
                        delete_comments += 1
                        cl.comment_bulk_delete(clip.id, [oneComment_id])
                        time.sleep(random.randint(1, 30))
                    else:
                        response = model.generate_content(
                            "just answer by yes or no to the following question: "
                            "Is this comment inappropriate or does this text contain bullying "
                            "(if it's emojis and not loving just answer yes)? "
                            + comment.text
                        )
                        answer = response.text.lower()
                        print(f"Answer: {answer}")
                        if "yes" in answer:
                            print(f"Deleting comment {oneComment_id} for being inappropriate by AI.")
                            cl.comment_bulk_delete(clip.id, [oneComment_id])
                            time.sleep(random.randint(1, 30))
                            delete_comments += 1
                        else:
                            print(f"Keeping comment {oneComment_id}.")
                        print(f"Keeping comment {oneComment_id}.")

            except FeedbackRequired:
                return(f"Rate limit reached. Skipping media {clip.id} for now.")
            except Exception as e:
                return(f"Unexpected error: {e}")
    except Exception as e:
        return("❌ Error fetching reel:", e)
    return{"number":{delete_comments}}


# how to run this code in terminal
# 1. Install the required packages:
# pip install instagrapi google-genai better-profanity fastapi uvicorn
# 2. Save this code in a file named main.py
# 3. Run the FastAPI server using uvicorn:
# uvicorn main:app --reload
