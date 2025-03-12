import pandas as pd
import jsonlines
import json
import random

# Read in the data
with open('./sample_for_human_eval.json', 'r') as f:
    data = json.load(f)

options = ['A', 'B', 'C', 'D', 'E', 'F']
sample_variants = ["human_output", "output_base", "output_dpo_policy", "output_ppo_reward", "output_ppo_policy", "output_dpo_coarse", ""]
context_str = """<big><strong>Context</strong></big><br><strong>Patient</strong><br>{patient_info}<br>"""
# q_options_str = """<br><big><strong>Question and Answer to Evaluate</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}<strong>Answer</strong> {correct_answer}<br>"""
# q_options_str = """<br><big><strong>Question and Answer to Evaluate</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}"""
q_options_str = """<br><big><strong>Options for a follow-up question</strong></big>"""
options_str = """A. {A}<br>B. {B}<br>C. {C}<br>D. {D}<br>E. {E}<br> F. {F}<br>"""
data_arr = []

for i, row in enumerate(data):
    sample = {c: row[c] for c in row.keys() if c != 'text'}
    shuffled_variants = random.sample(sample_variants, len(sample_variants))
    sample['option_assignments'] = {options[i]: k for i, k in enumerate(shuffled_variants)}
    cur_options_str = options_str.format(**{k: row[v] for k, v in sample['option_assignments'].items()})
    # display_text_str = [context_str.format(patient_info=row['patient_info'], clinical_convo=row['clinical_convo']).replace('\n\n', '<br>').replace('\n', '<br>'), q_options_str.format(question=row['question'], options=cur_options_str, correct_answer=row['correct_answer'])]
    display_text_str = [context_str.format(patient_info=row['context'].replace('Patient: ', '').replace(' Doctor:', '')), q_options_str, cur_options_str]
    sample['text'] = display_text_str
    # sample['id'] = row['id']
    data_arr.append(sample)

jsonlines.open('./sample_for_human_eval_formatted.jsonl', 'w').write_all(data_arr)