import datetime
import os
import fitz  # PyMuPDF
from PIL import Image

def split_pdf_into_images(pdf_path, images_output_dir, num_parts=2, split_orientation='horizontal'):
    """
    Splits each page of the given PDF into 'num_parts' number of parts, either 'horizontal' or 'vertical'.

    :param pdf_path: str, path to the PDF file
    :param images_output_dir: str, base directory to save images
    :param num_parts: int, number of parts to split each page into
    :param split_orientation: str, either 'horizontal' or 'vertical' for the split orientation
    """
    
    # Ensure num_parts is a positive integer
    assert num_parts > 0, "num_parts must be a positive integer."
    assert split_orientation in ['horizontal', 'vertical'], "split_orientation must be either 'horizontal' or 'vertical'."

    # Create output directory if it does not exist
    base_image_path = os.path.join(images_output_dir, os.path.splitext(os.path.basename(pdf_path))[0])
    os.makedirs(base_image_path, exist_ok=True)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    page_count = pdf_document.page_count

    # Process each page
    for page_number in range(page_count):
        page = pdf_document[page_number]
        zoom_level = 2.0  # Increase the resolution
        transform_matrix = fitz.Matrix(zoom_level, zoom_level).prerotate(0)
        pixmap = page.get_pixmap(matrix=transform_matrix, alpha=False)

        # Convert to PIL Image
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Determine the dimensions of each split part
        part_width = pixmap.width if split_orientation == 'vertical' else pixmap.width // num_parts
        part_height = pixmap.height // num_parts if split_orientation == 'vertical' else pixmap.height

        # Split and save each part
        for part_index in range(num_parts):
            left = part_width * part_index if split_orientation == 'horizontal' else 0
            upper = part_height * part_index if split_orientation == 'vertical' else 0
            right = left + part_width if split_orientation == 'horizontal' else pixmap.width
            lower = upper + part_height if split_orientation == 'vertical' else pixmap.height

            part_image = image.crop((left, upper, right, lower))

            # Save each part
            part_image_filename = f'page_{page_number + 1}_part_{part_index + 1}.png'
            part_image.save(os.path.join(base_image_path, part_image_filename))
            print(f'Saving page {page_number + 1}, part {part_index + 1} of {num_parts}, as {part_image_filename}')

    # Print timing info
    end_time = datetime.datetime.now()
    print(f'{pdf_path} - Conversion to images took {(end_time - start_time).seconds} seconds')

if __name__ == "__main__":
    pdf_file_path = '0.pdf'
    output_directory = "pdf_images"
    number_of_parts = 2  # Specify number of parts here
    orientation = 'horizontal'  # Specify split orientation: 'horizontal' or 'vertical'
    
    # Start the timer
    start_time = datetime.datetime.now()

    # Execute the function
    split_pdf_into_images(pdf_file_path, output_directory, number_of_parts, orientation)
