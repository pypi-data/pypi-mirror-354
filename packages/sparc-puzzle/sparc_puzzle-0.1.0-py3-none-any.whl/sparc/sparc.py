from typing import Dict
from sparc.prompt import prompt
from sparc.validation import extract_solution_path, validate_solution, analyze_path
from datasets import load_dataset
from openai import OpenAI


def main() -> None:
    dataset = load_dataset("lkaesberg/SPaRC", "all", split="test")

    client = OpenAI(
        api_key="9c89c616-649e-4d77-a6ad-1b1e525f94b5",
        base_url="http://services.gipplab.org:8080/v1",
    )
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at solving puzzles games.",
            },
            {"role": "user", "content": prompt(dataset[0])},
        ],
        temperature=0.7,
    )
    message = response.choices[0].message.content
    extracted_path = extract_solution_path(message, dataset[0])

    solved = validate_solution(extracted_path, dataset[0])
    analysis = analyze_path(extracted_path, dataset[0])

    print(f"Extracted Path: {extracted_path}")
    print(f"Solved: {solved}")
    print(f"Analysis: {analysis}")


if __name__ == "__main__":
    main()
