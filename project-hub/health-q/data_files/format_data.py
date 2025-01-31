import pandas as pd
import jsonlines

# Read in the data
data = pd.read_csv('./test_qs_post_all_good_4o_pilot.csv')

context_str = """<big><strong>Context</strong></big><br><strong>Patient Info</strong><br>{patient_info}<br><strong>Clinical Conversation</strong><br>{clinical_convo}"""
q_options_str = """<br><big><strong>Question and Answer to Evaluate</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}<strong>Answer</strong> {correct_answer}<br>"""
options_str = """A. {option_a}<br>B. {option_b}<br>C. {option_c}<br>D. {option_d}<br>"""
data_arr = []

for i, row in data.iterrows():
    sample = {c: row[c] for c in data.columns if c != 'text'}
    cur_options_str = options_str.format(option_a=row['optionA'], option_b=row['optionB'], option_c=row['optionC'], option_d=row['optionD'])
    display_text_str = [context_str.format(patient_info=row['patient_info'], clinical_convo=row['clinical_convo']).replace('\n\n', '<br>').replace('\n', '<br>'), q_options_str.format(question=row['question'], options=cur_options_str, correct_answer=row['correct_answer'])]
    sample['text'] = display_text_str
    data_arr.append(sample)

jsonlines.open('./test_qs_post_all_good_4o_pilot.jsonl', 'w').write_all(data_arr)