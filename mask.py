import sys
import tensorflow as tf

from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, TFBertForMaskedLM
import os

# Pre-trained masked language model
MODEL = "bert-base-uncased"

# Number of predictions to generate
K = 3

# Constants for generating attention diagrams
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200
OUTPUT_FOLDER = "./output/"


def main():
    text = input("Text: ")

    # Tokenize input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="tf")
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Use model to process input
    model = TFBertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generate predictions
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = tf.math.top_k(mask_token_logits, K).indices.numpy()
    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualize attentions
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    Return the index of the token with the specified `mask_token_id`, or
    `None` if not present in the `inputs`.

    The function accepts the ID of the mask token (represented as an ) and the tokenizer-generated , which will be of type . It should return the index of the mask token in the input sequence of tokens. get_mask_token_indexintinputstransformers.BatchEncoding
        The index should be 0-indexed. For example, if the third input ID is the mask token ID, then your function should return .2
        If the mask token is not present in the input sequence at all, your function should return .None
        You may assume that there will not be more than one mask token in the input sequence.
        You may find it helpful to look at the documentation, in particular at the return value of calling a tokenizer, to see what fields the will have that you might want to access.transformersBatchEncoding
    """
    # If the mask token is not present in the input sequence at all, your function should return .None
    for i, token in enumerate(inputs.input_ids[0]):
        if token == mask_token_id:
            return i
    return None



def get_color_for_attention_score(attention_score):
    """
    Return a tuple of three integers representing a shade of gray for the
    given `attention_score`. Each value should be in the range [0, 255].
    """
    # TODO: Implement this function
    raise NotImplementedError



def visualize_attentions(tokens, attentions):
    """
    Produce a graphical representation of self-attention scores.

    For each attention layer, one diagram should be generated for each
    attention head in the layer. Each diagram should include the list of
    `tokens` in the sentence. The filename for each diagram should
    include both the layer number (starting count from 1) and head number
    (starting count from 1).
    """
    # TODO: Update this function to produce diagrams for all layers and heads.
    generate_diagram(
        1,
        1,
        tokens,
        attentions[0][0][0]
    )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Generate a diagram representing the self-attention scores for a single
    attention head. The diagram shows one row and column for each of the
    `tokens`, and cells are shaded based on `attention_weights`, with lighter
    cells corresponding to higher attention scores.

    The diagram is saved with a filename that includes both the `layer_number`
    and `head_number`.
    """
    # Create new image
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    # Draw each token onto the image
    for i, token in enumerate(tokens):
        # Draw token columns
        token_image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_image)
        token_draw.text(
            (image_size - PIXELS_PER_WORD, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )
        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        # Draw token rows
        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text(
            (PIXELS_PER_WORD - width, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    # Draw each word
    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle((x, y, x + GRID_SIZE, y + GRID_SIZE), fill=color)

    # Save image
    os.makedirs(OUTPUT_FOLDER + str(layer_number) + "/", exist_ok=True)
    img.save(f"{OUTPUT_FOLDER + str(layer_number) + "/"}{head_number}.png")


if __name__ == "__main__":
    main()
