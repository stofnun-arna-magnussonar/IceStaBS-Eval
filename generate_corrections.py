import pandas as pd

import torch
import yaml
import requests
import os

from typing import List, Dict
from datasets import Dataset
from collections import namedtuple
from dataclasses import dataclass
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
from tqdm import tqdm
from tokenizer import split_into_sentences, correct_spaces

tqdm.pandas()

from evaluation import get_original_set, get_standardized_set, rule_classes, CONFIG


def save_corrections(corrections: pd.DataFrame) -> None:
    corrections.to_csv(
        os.path.join(CONFIG["FILE_FOLDERS"]["base_dir"], "data", "corrections.tsv"),
        sep="\t",
        index=True,
    )


def load_config(config_filepath: str) -> dict:
    with open(config_filepath, "r") as f:
        config = yaml.safe_load(f)
    return config


def add_output_to_corrections(
    corrections: pd.DataFrame, output: pd.DataFrame, column_name: str
) -> pd.DataFrame:
    corrections[column_name] = output
    return corrections


def join_split_sentences(input: List[str], output: List[str]):
    if len(input) == len(output):
        return output

    split_sent_indexes = []

    i = 0
    for sent in input:
        # Split the sentence into sub-sentences
        sub_sents = list(split_into_sentences(sent))
        num_sub_sents = len(sub_sents)

        # If there are multiple sub-sentences, mark their index for merging
        if num_sub_sents > 1:
            split_sent_indexes.append((i, i + num_sub_sents - 1))
            i += num_sub_sents  # Move the index forward by the number of sub-sentences
        else:
            split_sent_indexes.append((i, i))
            i += 1  # Move forward by one for single sentences

    # Now we combine the sentences in the output based on the split indexes
    new_output = []
    output_len = len(
        output
    )  # Cache the length of the output to avoid accessing out of bounds

    for pair in split_sent_indexes:
        start_idx, end_idx = pair

        # Ensure that indexes are within the valid range of output
        if start_idx >= output_len:
            break  # If the start index exceeds the output length, exit the loop

        if end_idx >= output_len:
            end_idx = output_len - 1  # Ensure end index does not exceed bounds

        if start_idx == end_idx:
            new_output.append(output[start_idx])
        else:
            # Merge sentences from output[start_idx] to output[end_idx]
            merged_sentence = " ".join(output[start_idx : end_idx + 1])
            new_output.append(merged_sentence)

    for i, j in zip(new_output, input):
        print(f"Input: {j}")
        print(f"Output: {i}")
        print("\n")

    return new_output


def apply_greynir_correct(example_set: List[str], example_set_index: int) -> List[str]:
    from reynir_correct import check_errors

    all_results = []

    options = {
        "annotations": False,  # Viljum hafa þetta false hér, því okkur vantar bara textann
        "format": "text",  # text, json, csv, m2
        "all_errors": True,  # Viljum allar villur
        "annotate_unparsed_sentences": True,  # Viljum vita hvaða setningar þáttast ekki
        "one_sent": True,  # Inntakið hér er að nafninu til ein setning í einu
    }

    tq = tqdm(total=len(example_set), desc="GreynirCorrect", position=0)

    for sent in example_set:
        # sent = [text.strip().strip("\n") for text in example_set]
        sent = sent.strip().strip("\n")
        # Create a new dictionary with all the options and the dynamic text field
        desc_string = f"Correcting ex_{example_set_index} with GreynirCorrect"
        updated_options = {**options, "input": sent}
        result = check_errors(**updated_options)
        result = result.replace("\n", " ")
        all_results.append(result)
        tq.update(1)
        # results = results.split("\n")
        # results = join_split_sentences(example_set, results)
    return all_results


@dataclass
class SkrambiAnnotation:
    charStart: int
    charEnd: int
    targetWord: str
    suggestions: List[str]
    errorClass: str


def apply_skrambi_corrections(sentences: List[str], annotations):
    # Initialize the corrected sentences list
    corrected_sentences = sentences[:]  # A copy of the original sentences

    # Step 1: Process each annotation
    for annotation in annotations:
        # Extract annotation details
        char_start = annotation.charStart
        char_end = annotation.charEnd
        target_word = annotation.targetWord
        suggestions = annotation.suggestions

        # Find out which sentence contains the current annotation based on char_start
        sentence_index, sentence_start_index = find_sentence_index(
            sentences, char_start
        )
        if sentence_index is None:
            # print(f"Could not find sentence for annotation: {annotation}")
            continue

        sentence = corrected_sentences[sentence_index]
        # print(f"Annotation target word: '{target_word}'")
        # print(f"Matched sentence: '{sentence}'")

        # Step 2: Tokenize the sentence into words
        tokens = " ".join(
            [sent for sent in split_into_sentences(sentence, normalize=False)]
        ).split()

        # Step 3: Find the token corresponding to the target word using a simple match
        for i, token in enumerate(tokens):
            # Naive matching: If the token matches the target word, replace it with the first suggestion
            if token == target_word and len(suggestions) > 0:
                # print(
                #     f"Replacing '{token}' with '{suggestions[0]}' in sentence {sentence_index}"
                # )
                tokens[i] = suggestions[0]  # Replace with the first suggestion

        # Step 4: Reassemble the sentence and store the corrected version
        corrected_sentences[sentence_index] = correct_spaces(" ".join(tokens))
        # print(f"Corrected sentence: '{corrected_sentences[sentence_index]}'")
        # print()

    return corrected_sentences


def find_sentence_index(sentences, char_start):
    """Find the index of the sentence containing the character at char_start"""
    total_chars = 0  # Cumulative length of sentences

    for i, sentence in enumerate(sentences):
        sentence_length = len(sentence) + 1  # +1 for the invisible break '\uefff'
        if total_chars <= char_start < total_chars + sentence_length:
            return i, total_chars
        total_chars += sentence_length

    return None, None  # Return None if char_start is out of bounds


def get_skrambi_correction_bulk(text_list: List[str]):

    url = "https://skrambi.arnastofnun.is/checkDocument"

    # maintain unicode
    break_symbol = "\\uefff".encode("utf-8").decode("unicode-escape")

    # Concatenate the entire column values into one payload
    # payload = f"{break_symbol}".join(text_list)
    payload = " ".join(text_list)

    headers = {"Content-Type": "text/plain"}

    # print("Sending request to Skrambi...")

    # Send the payload with the entire column's text
    # add a tqdm loading bar to the request
    response = requests.post(url, headers=headers, data=payload.encode("utf-8"))

    # Parse the response, assuming it's a list of annotations for the concatenated text
    annotations: List[SkrambiAnnotation] = [
        SkrambiAnnotation(**ann) for ann in response.json()
    ]

    return annotations


def load_model(model_name: str, max_length: int = None) -> pipeline:
    model_dir = CONFIG["FILE_FOLDERS"]["model_dir"]
    corr = namedtuple(
        "correction",
        ["pipe", "prompt_start", "prompt_end", "line_start", "line_end"],
    )
    if model_name.startswith("byt5"):
        model_path = os.path.join(model_dir, model_name)
        device = 0
        pipe = pipeline(
            "text2text-generation",
            model=model_path,
            tokenizer="google/byt5-base",
            device=device,  # use the GPU (0) or CPU (-1)
            batch_size=8,
            max_length=max_length,
        )
        return corr(pipe, "", "", "", "")
    if model_name.startswith("ice-gpt-sw3"):
        START_PROMPT = "Hér er texti sem ég vil að þú skoðir vel og vandlega. Þú skalt skoða hvert einasta orð, orðasamband, og setningu og meta hvort þér finnist eitthvað athugavert, til dæmis hvað varðar málfræði, stafsetningu, skringilega merkingu og svo framvegis.\nHér er textinn:\n\n"
        END_PROMPT = "\n\nReyndu nú að laga textann þannig að hann líti betur út, eins og þér finnst best við hæfi.\n"
        pipe = pipeline(
            "text-generation",
            model=os.path.join(model_dir, "icelandic-gpt-sw3-6.7b-gec"),
            max_new_tokens=1024,
            device_map="auto",
            tokenizer="AI-Sweden-Models/gpt-sw3-6.7b",
            return_full_text=False,
        )
        # return a named tuple

        return corr(pipe, START_PROMPT, END_PROMPT, '"\n', '\n\n"')
    else:
        raise ValueError(f"Model '{model_name}' not found.")


def apply_correction_model(
    model_name: str,
    example_set: List[str],
    example_set_index: int = None,
    max_length: int = None,
) -> str:

    total_length = len(example_set)
    correction = load_model(model_name, max_length=max_length)
    example_set = [
        f"{correction.prompt_start}{ex}{correction.prompt_end}" for ex in example_set
    ]
    example_set_name = f"ex_{example_set_index}" if example_set_index else "example_set"
    example_set = {example_set_name: example_set}

    dataset = Dataset.from_dict(example_set)

    corrected = tqdm(
        correction.pipe(KeyDataset(dataset, key=example_set_name)),
        desc=f"Correcting {example_set_name} with {model_name}",
        total=total_length,
    )
    # due to the batch size being n, the corrected is list of 245/n nested lists
    # we need to flatten the list
    corrected = [out[0]["generated_text"] for out in corrected]
    line_start, line_end = correction.line_start, correction.line_end
    corrected = [
        out.strip().strip(line_start).strip(line_end).strip() for out in corrected
    ]

    # free the memory used by the correction_pipe
    with torch.no_grad():
        correction_pipe = None
        torch.cuda.empty_cache()

    return corrected


def initiate_corrections(overwrite: bool = False) -> pd.DataFrame:
    if overwrite:
        if isinstance(overwrite, bool):
            corrections = pd.DataFrame(
                columns=[
                    "Ritregla",
                    "ex_1_standardized",
                    "ex_2_standardized",
                    "ex_3_standardized",
                    "ex_1_original",
                    "ex_2_original",
                    "ex_3_original",
                ]
            )

            corrections["Ritregla"] = rule_classes
            for i in range(1, 4):
                corrections[f"ex_{i}_standardized"] = get_standardized_set(i)
                corrections[f"ex_{i}_original"] = get_original_set(i)
        elif isinstance(overwrite, list):
            # If a list of tools is provided, overwrite only those columns
            corrections = pd.read_csv(
                os.path.join(
                    CONFIG["FILE_FOLDERS"]["base_dir"], "data", "corrections.tsv"
                ),
                sep="\t",
            )
            if "Unnamed: 0" in corrections.columns:
                corrections = corrections.drop(columns=["Unnamed: 0"])
            for tool in overwrite:
                if tool not in CONFIG["GLOBALS"]["tools"]:
                    print(f"Tool {tool} not found. Skipping...")
                    continue
                for i in range(1, 4):
                    column_name = f"ex_{i}_{tool}"
                    if column_name in corrections.columns:
                        corrections = corrections.drop(columns=[column_name])
    else:
        CORRECTIONS_PATH = os.path.join(
            CONFIG["FILE_FOLDERS"]["base_dir"], "data", "corrections.tsv"
        )
        if os.path.exists(CORRECTIONS_PATH):
            corrections = pd.read_csv(CORRECTIONS_PATH, sep="\t")
            if "Unnamed: 0" in corrections.columns:
                corrections = corrections.drop(columns=["Unnamed: 0"])
        else:
            corrections = pd.DataFrame(
                columns=[
                    "Ritregla",
                    "ex_1_standardized",
                    "ex_2_standardized",
                    "ex_3_standardized",
                    "ex_1_original",
                    "ex_2_original",
                    "ex_3_original",
                ]
            )

            corrections["Ritregla"] = rule_classes
            for i in range(1, 4):
                corrections[f"ex_{i}_standardized"] = get_standardized_set(i)
                corrections[f"ex_{i}_original"] = get_original_set(i)
    return corrections


def apply_all_corrections(corrections: pd.DataFrame, tools: Dict[str, dict]) -> None:
    for tool in tools:
        for i in range(1, 4):
            example_set = get_original_set(i)
            max_length = max([len(ex) for ex in example_set])
            match tool:
                case "greynir":
                    column_name = f"ex_{i}_greynir"
                    if not column_name in corrections.columns:
                        greynir_corrected = apply_greynir_correct(example_set, i)
                        add_output_to_corrections(
                            corrections, greynir_corrected, f"ex_{i}_greynir"
                        )
                        save_corrections(corrections)
                    else:
                        print(f"Column {column_name} already exists in data. Skipping")
                case tool if tool in ["byt5-22-09", "byt5-23-12", "byt5-24-03"]:

                    column_name = f"ex_{i}_{tool}"
                    if column_name in corrections.columns:
                        print(
                            f"Column {column_name} already exists in data. Skipping..."
                        )
                        continue
                    byt_5_corrected = apply_correction_model(
                        tool, example_set, i, max_length
                    )
                    add_output_to_corrections(corrections, byt_5_corrected, column_name)
                    save_corrections(corrections)
                case "skrambi":
                    column_name = f"ex_{i}_skrambi"
                    if not column_name in corrections.columns:
                        print(f"Applying Skrambi corrections to ex_{i}")
                        annotations = get_skrambi_correction_bulk(example_set)
                        corrected = apply_skrambi_corrections(example_set, annotations)
                        corrections = add_output_to_corrections(
                            corrections, corrected, column_name
                        )
                        save_corrections(corrections)
                    else:
                        print(f"Column {column_name} already exists in data. Skipping")

                case "ice-gpt-sw3":
                    column_name = f"ex_{i}_ice-gpt-sw3"
                    if not column_name in corrections.columns:
                        gpt_corrected = apply_correction_model(
                            "ice-gpt-sw3", example_set, i, max_length
                        )
                        add_output_to_corrections(
                            corrections, gpt_corrected, column_name
                        )
                        save_corrections(corrections)
                    else:
                        print(
                            f"Column {column_name} already exists in data. Skipping..."
                        )
                case tool if tool in CONFIG["GLOBALS"]["manual_tools"]:
                    column_name = f"ex_{i}_{tool}"
                    manual_dir_path = os.path.join(
                        CONFIG["FILE_FOLDERS"]["base_dir"], "data", "output_manual"
                    )
                    manual_file_path = os.path.join(
                        manual_dir_path, f"{column_name}.txt"
                    )
                    with open(manual_file_path, "r") as f:
                        lines = f.readlines()
                        lines = [line.strip() for line in lines]
                        lines = [line for line in lines if line]

                        add_output_to_corrections(corrections, lines, column_name)
                        save_corrections(corrections)
                case _:
                    print(f"Tool {tool} not found. Skipping...")


def main():

    TOOLS = CONFIG["GLOBALS"]["tools"]
    model_dir = CONFIG["FILE_FOLDERS"]["model_dir"]
    base_dir = CONFIG["FILE_FOLDERS"]["base_dir"]

    corrections = initiate_corrections(overwrite=False)
    save_corrections(corrections)
    apply_all_corrections(corrections, TOOLS)


if __name__ == "__main__":
    main()
