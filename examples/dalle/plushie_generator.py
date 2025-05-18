"""Simple script to generate plushie images using the DALL·E API.

This script demonstrates how to combine descriptors from the command line
into a prompt for DALL·E and save the returned image locally.

Example usage:
    python plushie_generator.py dragon --color purple --style "kawaii" --output my_plushie.png
"""

import argparse
import os
import requests
from openai import OpenAI


def build_prompt(subject: str, color: str, style: str) -> str:
    """Compose a short prompt describing the plushie."""
    bits = ["plush toy"]
    if color:
        bits.append(color)
    bits.append(subject)
    if style:
        bits.append(f"in {style} style")
    return " ".join(bits)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a plushie image")
    parser.add_argument("subject", help="animal or object for the plushie")
    parser.add_argument(
        "--color", default="", help="optional color for the plushie, e.g. blue"
    )
    parser.add_argument(
        "--style",
        default="cute",
        help="style descriptor like kawaii, realistic, or cartoonish",
    )
    parser.add_argument(
        "--size", default="1024x1024", help="image size accepted by the API"
    )
    parser.add_argument(
        "--output", default="plushie.png", help="filename for the generated image"
    )
    args = parser.parse_args()

    prompt = build_prompt(args.subject, args.color, args.style)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size=args.size,
        quality="standard",
    )

    image_url = response.data[0].url
    image = requests.get(image_url).content
    with open(args.output, "wb") as f:
        f.write(image)
    print(f"Plushie saved to {args.output}")


if __name__ == "__main__":
    main()
