from flask import Flask, render_template, url_for, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from huggingface_hub import InferenceClient
import base64

app = Flask(__name__)

# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# --------------------------------------------------
# HUGGING FACE CLIENT
# --------------------------------------------------

hf_client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)

# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def hello_world():
    return render_template("index.html")

# ==================================================
# ASK ANYTHING
# ==================================================

@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.form.get("question") # "question" is the input name in index.html

        system_prompt = """
        You are a helpful personal assistant.
        
        Answer the user's query accurately, clearly, and concisely.
        
        Guidelines:
        - Understand the user's intent before answering.
        - Give a direct answer first.
        - Provide explanation or examples when useful.
        - If the query requires multiple steps, explain them in a logical order.
        - Do not invent facts, sources, or information.
        - If you are unsure about something, clearly say that you are unsure.
        - Use simple language unless the user asks for technical detail.
        - For technical questions, include code or examples when appropriate.
        - For calculations, show the important steps.
        - Stay focused on the user's query and avoid unnecessary information.
        - Ensure the response is complete, but stop once the user's question has been fully answered.
        """
        
        response = client.responses.create(
            model = "qwen/qwen3.8-27b",
            input = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature = 0.3, # To get facts-based answers
            max_output_tokens = 1000
        )

        answer = response.output_text.strip()
        return jsonify({"response": answer}), 200 # Status code: 200 => OK: Standard response signaling that a client's request was successful

    except Exception as e:
        print("ERROR IN /ask:", e)
        return jsonify({"error": str(e)}), 500 # Status code: 500 => Internal Server Error

# ==================================================
# SUMMARIZE TEXT
# ==================================================

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        text = request.form.get("summary-text")

        system_prompt = """
            Summarize the text as a personal assistant.

            Extract:
            - Main topic
            - Important facts
            - Dates and deadlines
            - Tasks and responsibilities
            - Decisions made
            - Meetings/events
            - Requirements
            - Next steps
            
            Organize the information using clear headings and bullet points.
            
            IMPORTANT RULES:
            - Do not invent information.
            - Do not make assumptions that are not explicitly stated.
            - Do not assign responsibilities that are not mentioned.
            - Preserve names, dates, times, numbers, and deadlines accurately.
            - Clearly distinguish between official requirements and suggestions.
            - Keep the summary concise but informative.
            - Do not unnecessarily over-explain.
            - Prioritize the most relevant information.
            - If the answer becomes long, summarize instead of adding additional sections.
            - Ensure the response is complete, but stop once the user's question has been fully answered.
            """

        response = client.responses.create(
            model = "qwen/qwen3.8-27b",
            input = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature = 0.3, # To get appropriate answers
            max_output_tokens = 800,
            reasoning={
                "effort": "none" # Don't spend extra tokens on deliberate reasoning; just answer the task directly
            }
        )

        summary = response.output_text.strip()
        return jsonify({"response": summary}), 200 # Status code: 200 => OK: Standard response signaling that a client's request was successful

    except Exception as e:
        print("ERROR IN /summarize:", e)
        return jsonify({"error": str(e)}), 500 # Status code: 500 => Internal Server Error

# ==================================================
# IMAGE ANALYSIS
# ==================================================

@app.route("/analyze-image", methods=["POST"])
def analyze_image():

    try:

        # ---------------------------------------------------- 
        # GET QUESTION AND IMAGE
        # ----------------------------------------------------

        question = request.form.get("image-question")

        image_file = request.files.get("image")
        image_url = request.form.get("image-url")

        # ------------------------------------------
        # DEFAULT QUESTION
        # ------------------------------------------

        if not question or not question.strip():

            question = """
            Analyze this image carefully.

            Describe:
            - What is visible
            - Important objects
            - Text present in the image
            - Relevant details
            - Any useful observations

            If there is text in the image, accurately extract it.
            Do not invent information that is not visible.
            """

        # ------------------------------------------
        # CHECK WHETHER IMAGE WAS PROVIDED
        # ------------------------------------------

        if not image_file and not image_url:

            return jsonify({
                "error": "Please upload an image or provide an image URL."
            }), 400


        # ------------------------------------------
        # IMAGE CONTENT
        # ------------------------------------------

        if image_file:

            # Check file type
            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
                "image/gif"
            ]

            if image_file.mimetype not in allowed_types:

                return jsonify({
                    "error": "Unsupported image format. Use JPG, PNG, WEBP, or GIF."
                }), 400


            # Read image
            image_bytes = image_file.read()

            # 20 MB limit
            if len(image_bytes) > 20 * 1024 * 1024:

                return jsonify({
                    "error": "Image is too large. Maximum size is 20 MB."
                }), 400


            # Convert to Base64
            base64_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")


            image_source = (
                f"data:{image_file.mimetype};base64,{base64_image}"
            )

        else:

            # Use provided URL
            image_source = image_url.strip()

        # ------------------------------------------
        # VISION PROMPT
        # ------------------------------------------

        system_prompt = """
        You are an expert visual information assistant.

        Analyze the provided image carefully and answer the user's question
        using ONLY information that can be reasonably determined from the image.

        IMPORTANT RULES:

        - First understand exactly what the user is asking.
        - Answer the user's question directly.
        - Do not describe the entire image unless the user asks for a description.
        - Do not provide unnecessary visual details.
        - Do not invent, guess, or assume information that is not clearly visible.
        - If text is blurry, cropped, partially visible, or ambiguous, clearly say so.
        - Never turn an uncertain reading into a definite fact.
        - Preserve numbers, names, dates, prices, and quantities accurately.
        - If the user asks for a calculation, calculate only from clearly visible values.
        - If the image contains a bill/receipt, prioritize:
        - Items
        - Quantities
        - Individual prices
        - Subtotal
        - Tax/VAT
        - Discounts
        - Final total
        - If the user asks for a bill breakdown, organize the information clearly,
        preferably using a table when appropriate.
        - If some information cannot be determined from the image, explicitly mention it.
        - Do not speculate about cropped or unclear text.
        - Keep the response concise but complete.
        """


        # ------------------------------------------
        # GROQ VISION REQUEST
        # ------------------------------------------

        response = client.responses.create(

            model="qwen/qwen3.8-27b",

            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "input_text",
                            "text": question
                        },

                        {
                            "type": "input_image",
                            "detail": "auto",
                            "image_url": image_source
                        }

                    ]
                }
            ],

            temperature=0.3,
            max_output_tokens=1200
        )


        answer = response.output_text.strip()


        return jsonify({
            "response": answer
        }), 200


    except Exception as e:

        print("ERROR IN /analyze-image:", e)

        return jsonify({
            "error": str(e)
        }), 500

# ============================================================ 
# GENERATE IMAGE 
# ============================================================

@app.route("/generate-image", methods=["POST"]) 
def generate_image():
    try:

        # ----------------------------------------------------
        # GET PROMPT
        # ----------------------------------------------------

        prompt = request.form.get("prompt")

        if not prompt or not prompt.strip():
            return jsonify({
                "error": "Please enter an image prompt."
            }), 400

        prompt = prompt.strip()

        # ----------------------------------------------------
        # GET OPTIONAL REFERANCE IMAGE
        # ----------------------------------------------------

        reference_file = request.files.get("reference-image")
        reference_url = request.form.get("reference-url")

        reference_url = reference_url.strip() if reference_url else ""

        # ---------------------------------------------------- 
        # DON'T ALLOW BOTH #
        # ---------------------------------------------------- 

        if reference_file and reference_file.filename and reference_url: 
            return jsonify({
                "error": "Please provide either an uploaded reference image OR an image URL, not both."
            }), 400

        # ----------------------------------------------------
        # GENERATE IMAGE
        # ----------------------------------------------------

        if (
            not reference_file
            or not reference_file.filename
        ):

            # ----------------------------------------------
            # TEXT → IMAGE
            # ----------------------------------------------

            image = hf_client.text_to_image(

                prompt=prompt,

                model="black-forest-labs/FLUX.1-schnell"
            )

        elif reference_file:

            # ----------------------------------------------
            # UPLOADED IMAGE → IMAGE
            # ----------------------------------------------

            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp"
            ]

            if reference_file.mimetype not in allowed_types:

                return jsonify({
                    "error": "Unsupported reference image format. Use JPG, PNG, or WEBP."
                }), 400


            reference_bytes = reference_file.read()


            if len(reference_bytes) > 20 * 1024 * 1024:

                return jsonify({
                    "error": "Reference image is too large. Maximum size is 20 MB."
                }), 400


            image = hf_client.image_to_image(

                reference_bytes,

                prompt=prompt,

                model="black-forest-labs/FLUX.1-Kontext-dev"
            )
        
        else:

            # ----------------------------------------------
            # URL → IMAGE
            # ----------------------------------------------

            image = hf_client.image_to_image(

                reference_url,

                prompt=prompt,

                model="black-forest-labs/FLUX.1-Kontext-dev"
            )
        
        # ----------------------------------------------------
        # CONVERT IMAGE TO BASE64
        # ----------------------------------------------------

        from io import BytesIO

        image_buffer = BytesIO()

        image.save(
            image_buffer,
            format="PNG"
        )

        image_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode("utf-8")


        # ----------------------------------------------------
        # RETURN IMAGE DIRECTLY
        # ----------------------------------------------------

        return jsonify({

            "image": (
                "data:image/png;base64,"
                + image_base64
            )

        }), 200
    except Exception as e:

        print("ERROR IN /generate-image:", e)

        return jsonify({

            "error": str(e)

        }), 500

if __name__ == "__main__":
    app.run(debug=True)