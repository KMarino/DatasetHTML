# Make html code!
import json
import os

# Define some useful function
def start_html(title):
    return ['<head>', '<title>' + title + '</title>']
def end_html():
    return ['</head>']
def start_table(padding):
    return ['<table cellpadding="' + str(padding) + 'px">']
def end_table():
    return ['</table>']
def start_row():
    return ['<tr>']
def end_row():
    return ['</tr>']
def make_text_cell(text):
    return ['<td>' + text + '</td>']
def make_img_cell(url, height, width):
    return ['<td><div class="image"><strong><img alt="image_url" src="' + url + '" width="' + str(width) + '", height="' + str(height) + '"/></strong></div></td>']
def make_coco_img_cell(image_name, height, width):
    if 'train' in image_name:
        subtype = 'train2014'
    elif 'val' in image_name:
        subtype = 'val2014'
    full_url = 'https://s3-us-west-2.amazonaws.com/ai2-vision/aishwarya/mscoco_images/' + subtype + '/' + image_name
    return make_img_cell(full_url, height, width)
def make_empty_cell():
    return ['<td></td>']

def make_html_file(questions, num_cols, num_rows):
    # Start html
    html_lines = []
    html_lines += start_html('Title')
    html_lines += start_table(5)

    # Get image cells
    image_cells = [make_coco_img_cell(q['image_name'], 200, 200) for q in questions]
    
    # Get question cells
    question_cells = [make_text_cell('Q: ' + q['question']) for q in questions]
    
    # Get answers celis
    answer_cells = [make_text_cell('A: ' + " ".join(q['answers'])) for q in questions]

    # Build the table
    while len(image_cells) + len(question_cells) + len(answer_cells) > 0:
        html_lines += start_row()

        # Image row
        if len(image_cells) == len(question_cells) and len(image_cells) == len(answer_cells):
            for i in range(min(num_cols, len(image_cells))):
                html_lines += image_cells[0]
                del image_cells[0]  
        elif len(image_cells) < len(question_cells) and len(question_cells) == len(answer_cells):
            for i in range(min(num_cols, len(question_cells))):
                html_lines += question_cells[0]
                del question_cells[0]  
        else:
            for i in range(min(num_cols, len(answer_cells))):
                html_lines += answer_cells[0]
                del answer_cells[0]  
        html_lines += end_row()

    # End html
    html_lines += end_table()
    html_lines += end_html()

    return html_lines    

def main():
    # Load in the train and test annotations
    train_json = '/home/kennethm/searchVQA/data/ckvqa/raw/ckvqa_train_dataset.json'
    with open(train_json, 'r') as f:
        train_json = json.load(f)
    val_json = '/home/kennethm/searchVQA/data/ckvqa/raw/ckvqa_val_dataset.json'
    with open(val_json, 'r') as f:
        val_json = json.load(f)

    # Choose parameters
    num_cols = 3
    num_rows = 20
    per_page = num_cols * num_rows

    # Make the webpages
    os.system('mkdir -p CKVQA')
    count = 0
    for i in range(0, len(train_json['questions']), per_page):
        q_subset = train_json['questions'][i:i+per_page]
        subset_html = make_html_file(q_subset, num_cols, num_rows)
        # Write to file
        with open('CKVQA/train_%d.html' % count, 'w') as f:
            f.write("".join(subset_html))
        count += 1

    count = 0
    for i in range(0, len(val_json['questions']), per_page):
        q_subset = val_json['questions'][i:i+per_page]
        subset_html = make_html_file(q_subset, num_cols, num_rows)
        
        # Write to file
        with open('CKVQA/val_%d.html' % count, 'w') as f:
            f.write("".join(subset_html))
        count += 1    

def debug():
    # First make the heading stuff
    html_lines = []
    html_lines += start_html('Title TODO')
    html_lines += start_table(5)

    # Start new row
    html_lines += start_row()

    # Add text in row
    html_lines += make_text_cell('row 1')

    # Add image in row
    html_lines += make_img_cell("https://s3-us-west-2.amazonaws.com/ai2-vision/aishwarya/mscoco_images/train2014/COCO_train2014_000000225709.jpg", 200, 200)
    html_lines += end_row()

    # Add text in row
    html_lines += start_row()
    html_lines += make_text_cell('row 2')

    # Add image in row
    html_lines += make_coco_img_cell("COCO_train2014_000000225709.jpg", 200, 200)
    html_lines += end_row()

    html_lines += end_table()
    html_lines += end_html()

    # Write to file
    with open('demo.html', 'w') as f:
        f.write("".join(html_lines))

if __name__ == '__main__':
    main()
