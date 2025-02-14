import pandas as pd
import jsonlines

# Read in the data
data = pd.read_csv('./test_qs_post_all_good_4o.csv')
pilot_data = pd.read_json('./test_qs_post_all_good_4o_pilot.jsonl', lines=True)
pilot_thread_ids = set(pilot_data['id'].unique())

context_str = """<big><strong>Context</strong></big><br><strong>Patient Info</strong><br>{patient_info}<br><strong>Clinical Conversation</strong><br>{clinical_convo}"""
# q_options_str = """<br><big><strong>Question and Answer to Evaluate</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}<strong>Answer</strong> {correct_answer}<br>"""
# q_options_str = """<br><big><strong>Question and Answer to Evaluate</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}"""
q_options_str = """<br><big><strong>Question and Options</strong></big><br><strong>Question</strong> {question}<br><strong>Options</strong><br>{options}"""
options_str = """A. {option_a}<br>B. {option_b}<br>C. {option_c}<br>D. {option_d}<br>"""
data_arr = []

print(data.columns)
print(data.head(1))

for i, row in data.iterrows():
    if row['thread_id'] in pilot_thread_ids:
        print("Removing thread included in pilot: ", row['thread_id'])
        continue
    sample = {c: row[c] for c in data.columns if c != 'text'}
    cur_options_str = options_str.format(option_a=row['optionA'], option_b=row['optionB'], option_c=row['optionC'], option_d=row['optionD'])
    # display_text_str = [context_str.format(patient_info=row['patient_info'], clinical_convo=row['clinical_convo']).replace('\n\n', '<br>').replace('\n', '<br>'), q_options_str.format(question=row['question'], options=cur_options_str, correct_answer=row['correct_answer'])]
    display_text_str = [context_str.format(patient_info=row['patient_info'], clinical_convo=row['clinical_convo']).replace('\n\n', '<br>').replace('\n', '<br>'), q_options_str.format(question=row['question'], options=cur_options_str)]
    sample['text'] = display_text_str
    sample['id'] = row['thread_id']
    data_arr.append(sample)

jsonlines.open('./test_qs_post_all_good_4o.jsonl', 'w').write_all(data_arr)