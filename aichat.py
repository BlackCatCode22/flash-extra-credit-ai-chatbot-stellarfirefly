from flask import Flask, request, render_template
import openai
import config

#----
#   Need to create a file config.py and add a line defining
# OPENAI_API_KEY to your API key. Not included in github.
#
openai.api_key = config.OPENAI_API_KEY

app = Flask(__name__)

message_history = []

# this is what happens when someone starts at the root of the website "/"
@app.route("/", methods=["GET", "POST"])
def start_here():
    global message_history
    
    if request.method == "POST":
        if request.form.get("reset") != None:
            message_history = []
            return render_template("index.html", textQuestion="hello", textAnswer="(A new conversation has been started.)")

        if request.form.get("prompt") != None:
            # There is a <textarea> on the index.html webpage named "question"
            #   what the user types in the <textarea> named "question" will be used as the prompt for text-davinci-003 .
            text_question = request.form.get("question")

            # Choose the model from OpenAI that you want to use.
            model_name = "gpt-3.5-turbo"

            # Make a request to gpt-3.5-turbo.
            try:
                new_message_list = message_history
                new_message_list.append({
                    "role": "user",
                    "content": text_question,
                })
                
                # Call the method named create from the Completion class of the OpenAI Python client library.
                response = openai.ChatCompletion.create(
                    model = model_name,
                    messages = new_message_list,
                    max_tokens = 1000
                )

            except openai.error.OpenAIError as e:
                print(f"Something unexpected happened. Here is a debugging clue: {e}")

            text_answer = response["choices"][0]["message"]["content"]
            message_history.append({
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            })

            return render_template("index.html", textQuestion=text_question, textAnswer=text_answer)

    return render_template("index.html", textQuestion="", textAnswer="")

if __name__ == "__main__":
    app.run(debug=True)

