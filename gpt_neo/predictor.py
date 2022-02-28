from __future__ import print_function
import io
import os
import flask
import pandas as pd
import re
from transformers import GPT2Tokenizer, AutoModelForCausalLM

def predict_intent(model, tokenizer, text, max_length):

    prompt = f"<|startoftext|>Query: {text} Intent: "
    generated = tokenizer(f"<|startoftext|> {prompt}", return_tensors="pt").input_ids.cuda()
    sample_outputs = model.generate(generated, do_sample=False, top_k=50, max_length=max_length, top_p=0.90, 
            temperature=0, num_return_sequences=0)
    pred_text = tokenizer.decode(sample_outputs[0], skip_special_tokens=True)
    try:
        pred_intent = re.findall("(?<=Intent: ).*", pred_text)[-1]
    except:
        pred_intent = "None"

    return pred_text, pred_intent

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")

class ScoringService(object): 

    model = None 

    @classmethod
    def get_model(cls):

        if cls.model == None:
            cls.model = AutoModelForCausalLM.from_pretrained(model_path)
        return cls.model

    @classmethod
    def predict(cls, input):

        cls = cls.get_model()
        tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M", bos_token="<|startoftext|>",
                                          eos_token="<|endoftext|>", pad_token="<|pad|>")
                                  
        _, pred_intent = predict_intent(cls, tokenizer, input, 300)

        return pred_intent


# Flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():

    health = ScoringService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():

    data = None

    # Convert from CSV to pandas
    if flask.request.content_type == "text/csv":
        data = flask.request.data.decode("utf-8")
        s = io.StringIO(data)
        data = pd.read_csv(s, header=None)
    else:
        return flask.Response(
            response="This predictor only supports CSV data", status=415, mimetype="text/plain"
        )

    print("Invoked with {} records".format(data.shape[0]))

    # Do the prediction
    predictions = ScoringService.predict(data)

    out = io.StringIO()
    pd.DataFrame({"results": predictions}).to_csv(out, header=False, index=False)
    result = out.getvalue()

    return flask.Response(response=result, status=200, mimetype="text/csv")