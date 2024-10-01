from tokenizer import tokenize
from collections import namedtuple
from typing import List
from difflib import SequenceMatcher

_EvaluationResults = namedtuple('EvaluationResults', ['true_positive', 'false_positive', 'true_negative', 'false_negative'])

def align_tokens(a_tokens, b_tokens):
    """
    Align tokens from a_tokens to b_tokens using SequenceMatcher.

    Returns a list of tuples:
    - (a_token, b_token): Tokens are aligned.
    - (a_token, None): Token in a_tokens is deleted in b_tokens.
    - (None, b_token): Token in b_tokens is inserted in a_tokens.
    """
    matcher = SequenceMatcher(None, a_tokens, b_tokens)
    alignment = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Tokens match; align them directly.
            for i, j in zip(range(i1, i2), range(j1, j2)):
                alignment.append((a_tokens[i], b_tokens[j]))
        elif tag == 'replace':
            # Tokens differ; align all tokens, even if lengths differ.
            a_range = range(i1, i2)
            b_range = range(j1, j2)
            max_len = max(len(a_range), len(b_range))
            for k in range(max_len):
                a_token = a_tokens[i1 + k] if k < len(a_range) else None
                b_token = b_tokens[j1 + k] if k < len(b_range) else None
                alignment.append((a_token, b_token))
        elif tag == 'delete':
            # Tokens deleted from a_tokens.
            for i in range(i1, i2):
                alignment.append((a_tokens[i], None))
        elif tag == 'insert':
            # Tokens inserted in b_tokens.
            for j in range(j1, j2):
                alignment.append((None, b_tokens[j]))
    return alignment

def get_actions(alignment):
    """
    Given an alignment list, returns a list of actions corresponding to each token in the reference.

    Each action is a tuple (action, token), where action is one of:
    - 'equal': Token is the same in both sequences.
    - 'replace': Token is different between the sequences.
    - 'delete': Token is missing in the other sequence.
    - 'insert': Token is inserted in the other sequence.
    """
    actions = []
    for a_token, b_token in alignment:
        if a_token == b_token:
            actions.append(('equal', b_token))
        elif a_token is None:
            actions.append(('insert', b_token))
        elif b_token is None:
            actions.append(('delete', a_token))
        else:
            actions.append(('replace', b_token))
    return actions


def compare_actions(expected_actions, observed_actions):
    tp = fp = fn = tn = 0
    # print(expected_actions)
    # print(observed_actions)
    for expected_action, observed_action in zip(expected_actions, observed_actions):
        expected_tag, expected_token = expected_action
        observed_tag, observed_token = observed_action

        if expected_tag == observed_tag:
            if expected_tag != 'equal':
                if expected_token == observed_token:
                    tp += 1  # Correctly changed
                else:
                    # NOTE: hér þarf að hafa augun opin.
                    fp += 1  # Incorrect change
                    
            else:
                tn += 1  # Correctly unchanged
        else:
            if expected_tag != 'equal' and observed_tag == 'equal':
                fn += 1  # Should have been changed but wasn't
            elif expected_tag == 'equal' and observed_tag != 'equal':
                fp += 1  # Should not have been changed but was
            else:
                # Both expected and observed actions are changes but differ
                fn += 1  # Expected change did not happen
                fp += 1  # Unexpected change happened
    return tp, fp, tn, fn



def get_expected_token_differences(input: List[str], reference: List[str]):
    """
    Compare two lists of items (input and reference) and return the differences between them.
    It considers modifications, additions, and deletions, and re-aligns indexes after added or deleted tokens.
    
    Args:
        input (List[str]): List of tokens from the input text.
        reference (List[str]): List of tokens from the reference text.

    Returns:
        A tuple containing:
              - input_diffs: Tokens from `input` that differ from `reference`.
              - reference_diffs: Corresponding tokens from `reference` that differ from `input`.
              - modified_indexes: Indexes of tokens that differ in both `input` and `reference`.
              - added_indexes: Indexes of tokens that are in `input` but not in `reference`.
              - deleted_indexes: Indexes of tokens that are in `reference` but not in `input`.
    """
    input_diffs = []
    reference_diffs = []
    modified_indexes = []
    added_indexes = []
    deleted_indexes = []

    i, j = 0, 0  # Pointers for `input` and `reference` lists

    while i < len(input) and j < len(reference):
        if input[i] == reference[j]:
            # Tokens match, continue comparing next tokens
            i += 1
            j += 1
        else:
            # Tokens differ, figure out if it's a modification, addition, or deletion
            if i + 1 < len(input) and input[i + 1] == reference[j]:
                # It's an added token in `input`
                added_indexes.append(i)
                input_diffs.append(input[i])
                i += 1
            elif j + 1 < len(reference) and input[i] == reference[j + 1]:
                # It's a deleted token in `reference`
                deleted_indexes.append(j)
                reference_diffs.append(reference[j])
                j += 1
            else:
                # It's a modification (token differs in both)
                modified_indexes.append(i)
                input_diffs.append(input[i])
                reference_diffs.append(reference[j])
                i += 1
                j += 1

    # If there are any remaining tokens in `input`, they are additions
    while i < len(input):
        added_indexes.append(i)
        input_diffs.append(input[i])
        i += 1

    # If there are any remaining tokens in `reference`, they are deletions
    while j < len(reference):
        deleted_indexes.append(j)
        reference_diffs.append(reference[j])
        j += 1

    return input_diffs, reference_diffs, modified_indexes, added_indexes, deleted_indexes, len(input), len(reference)
    
def true_positive(observed_actions, expected_actions):
    score = sum(1 for exp_act, obs_act in zip(expected_actions, observed_actions)
                if exp_act[0] == obs_act[0] and exp_act[0] != 'equal')
    return score

def false_positive(observed_actions, expected_actions):
    score = sum(1 for exp_act, obs_act in zip(expected_actions, observed_actions)
                if exp_act[0] == 'equal' and obs_act[0] != 'equal')
    return score

def false_negative(observed_actions, expected_actions):
    score = sum(1 for exp_act, obs_act in zip(expected_actions, observed_actions)
                if exp_act[0] != 'equal' and obs_act[0] == 'equal')
    return score

def true_negative(observed_actions, expected_actions):
    score = sum(1 for exp_act, obs_act in zip(expected_actions, observed_actions)
                if exp_act[0] == obs_act[0] == 'equal')
    return score


def token_level_eval(input_text: str, output_text: str, reference_text: str):
    input_tokens = [token.txt for token in tokenize(input_text) if token.txt != '']
    output_tokens = [token.txt for token in tokenize(output_text) if token.txt != '']
    reference_tokens = [token.txt for token in tokenize(reference_text) if token.txt != '']

    # Align tokens
    expected_alignment = align_tokens(input_tokens, reference_tokens)
    observed_alignment = align_tokens(input_tokens, output_tokens)
    

    # Get actions
    expected_actions = get_actions(expected_alignment)
    observed_actions = get_actions(observed_alignment)

    # Ensure both action lists are the same length
    max_len = max(len(expected_actions), len(observed_actions))
    expected_actions.extend([('equal', '')] * (max_len - len(expected_actions)))
    observed_actions.extend([('equal', '')] * (max_len - len(observed_actions)))

    # Compare actions
    tp, fp, tn, fn = compare_actions(expected_actions, observed_actions)

    return _EvaluationResults(tp, fp, tn, fn)