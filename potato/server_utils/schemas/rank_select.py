"""
Select Layout
"""

import os
from pathlib import Path


def generate_rank_select_layout(annotation_scheme):

    # setting up label validation for each label, if "required" is True, the annotators will be asked to finish the current instance to proceed
    validation = ""
    label_requirement = (
        annotation_scheme["label_requirement"] if "label_requirement" in annotation_scheme else None
    )
    if label_requirement and ("required" in label_requirement) and label_requirement["required"]:
        validation = "required"

    schematic = (
          ('<form id="%s" class="annotation-form select" action="/action_page.php">' % annotation_scheme["name"] )
        + "  <fieldset>"
        + ("  <legend>%s</legend>" % annotation_scheme["description"])
    )

    cur_program_dir = Path(os.path.abspath(__file__)).parent.parent.parent.absolute()  # get the current program dir (for the case of pypi, it will be the path where potato is installed)
    predefined_labels_dict = {
        "country": os.path.join(cur_program_dir, "static/survey_assets/country_dropdown_list.html"),
        "ethnicity": os.path.join(cur_program_dir, "static/survey_assets/ethnicity_dropdown_list.html"),
        "religion": os.path.join(cur_program_dir, "static/survey_assets/religion_dropdown_list.html"),
    }

    options = ""
    # directly use the predefined labels if annotation_scheme["use_predefined_labels"] is defined
    if (
        "use_predefined_labels" in annotation_scheme
        and annotation_scheme["use_predefined_labels"] in predefined_labels_dict
    ):
        with open(predefined_labels_dict[annotation_scheme["use_predefined_labels"]]) as r:
            options += r.read()

    else:
        # if annotation_scheme['labels'] is defined as a path
        if type(annotation_scheme["labels"]) == str and os.path.exists(annotation_scheme["labels"]):
            with open(annotation_scheme["labels"], "r") as r:
                labels = [it.strip() for it in r.readlines()]
        else:
            labels = annotation_scheme["labels"]

        options += '<option disabled selected value> -- select an option -- </option>'
        for i, label_data in enumerate(labels, 1):

            label = label_data if isinstance(label_data, str) else label_data["name"]

            name = annotation_scheme["name"] + ":::" + label
            class_name = annotation_scheme["name"]
            key_value = name
            label_content = label
            options += ('<option class="%s" id="%s" name="%s" value="%s">%s</option>') % (
                class_name,
                name,
                name,
                label_content,
                label_content,
            )

    for i, label_data in enumerate(annotation_scheme["labels"]):
        if i == 0:
            additional_label = " (Best follow-up question)"
        elif i == len(annotation_scheme["labels"]) - 1:
            additional_label = " (Worst follow-up question)"
        else: 
            additional_label = ""
        schematic += (
            '<label value="%s" style="display: inline-block; width:220px">%s</label> ' % (i + 1, "%s%s" % ((i + 1), additional_label)) + 
            '<select type="select-one" class="%s" id="%s-%s" name="%s" validation="%s">'
            % (
                annotation_scheme["description"],
                annotation_scheme["name"], i + 1,
                annotation_scheme["name"] + "-%s" % (i+1) + ":::select-one",
                validation,
            )
        ) + options + "</select><br>"

    schematic += "\n</fieldset>\n</form>\n"
    return schematic, []
