"""
Drag-and-Drop Ranking Layout
"""
import logging
from collections.abc import Mapping

logger = logging.getLogger(__name__)

def generate_drag_and_drop_layout(annotation_scheme):
    # Ensure that the required parameters are present in the annotation scheme
    for required in ["options"]:
        if required not in annotation_scheme:
            raise Exception(
                'Drag-and-Drop ranking for "%s" did not include %s' % (annotation_scheme["name"], required)
            )

    options = annotation_scheme["options"]

    # Setting up label validation for each label, if "required" is True,
    # the annotators will be asked to finish the current instance to proceed
    validation = ""
    label_requirement = annotation_scheme.get("label_requirement")
    if label_requirement and label_requirement.get("required"):
        validation = "required"
    
    # Building the HTML structure for drag-and-drop ranking
    schematic = (
        '<div><form class="annotation-form drag-and-drop" id="%s" action="/action_page.php">'
        '<fieldset> <legend>%s</legend><ul id="%s" class="rank-list">'
    ) % (annotation_scheme["name"], annotation_scheme["description"], annotation_scheme["name"])

    # schematic_div = ""
    # schematic_list = ""
    # for i, option in enumerate(options):
    #     schematic_div += (
    #         '<div class="rank-item" ondrop="drop(event)" ondragover="allowDrop(event)" id="%s-%s">%s</div>'
    #     ) % (annotation_scheme["name"], i, i + 1)
    #     schematic_list += (
    #         '<li class="draggable-item" draggable="true" ondragstart="drag(event)" name="%s" id="%s-%s" validation="%s" type="drag-drop">%s</li>'
    #     ) % (option, annotation_scheme["name"], option, validation, option)

    # schematic += schematic_div + schematic_list + '</ul></fieldset>\n</form></div>\n'

    for i, option in enumerate(options):
        schematic += (
            '<select type="select-one" name="%s" id="%s-%s" validation="%s" type="drag-drop">%s</selects>'
        ) % (option, annotation_scheme["name"], option, validation, option)

    schematic += '</ul></fieldset>\n</form></div>\n'

    # Add Script for drag-and-drop functionality
    # script = """
    # <style>
    #     .rank-list { 
    #         list-style-type: none; 
    #         padding: 0; 
    #     }
    #     .draggable-item {
    #         margin: 5px 0; 
    #         padding: 10px; 
    #         border: 2px solid #ccc; 
    #         cursor: pointer;
    #         background-color: #f9f9f9;
    #     }
    #     .rank-item {
    #         margin: 5px 0; 
    #         padding: 10px; 
    #         border: 2px solid #ccc; 
    #         cursor: pointer;
    #         background-color: #f9f9f9;
    #     }
    #     .draggable-item.dragover {
    #         border: 2px dashed #999;
    #     }
    # </style>
    # <script>
    #     const draggables = document.querySelectorAll('.draggable-item');
    #     const container = document.getElementById('%s');

    #     function allowDrop(ev) {
    #         ev.preventDefault();
    #     }

    #     function drag(ev) {
    #         ev.dataTransfer.setData("text", ev.target.id);
    #     }

    #     function drop(ev) {
    #         ev.preventDefault();
    #         var data = ev.dataTransfer.getData("text");
    #         ev.target.appendChild(document.getElementById(data));
    #     }

    #     draggables.forEach(draggable => {
    #         draggable.addEventListener('dragstart', () => {
    #             draggable.classList.add('dragging');
    #         });

    #         draggable.addEventListener('dragend', () => {
    #             draggable.classList.remove('dragging');
    #         });
    #     });
    # </script>
    # """ % annotation_scheme["name"]

    return schematic, []