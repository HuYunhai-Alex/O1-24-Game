import json

def convert_to_sft_format(input_file, output_file):
    with open(input_file, "r") as f:
        raw = [json.loads(line) for line in f]

    new_data = []
    for item in raw:
        text = item["text"]
        instr = "Solve the sudoku puzzle based on the given input and provide your reasoning."
        try:
            input_part = text.split("<input>")[1].split("</input>")[0].strip()
            reasoning_part = text.split("<reasoning>")[1].split("</reasoning>")[0].strip()
            output_part = text.split("<output>")[1].split("</output>")[0].strip()

            new_data.append({
                "instruction": instr,
                "input": input_part,
                "output": "<think>" + reasoning_part + "</think>" + "\n\nFinal Solution:\n" + output_part
            })
        except:
            continue

    with open(output_file.replace(".jsonl", ".json"), "w") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)


convert_to_sft_format("sudoku_data.jsonl", "sudoku_sft.json")
