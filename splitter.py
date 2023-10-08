from io import FileIO, BytesIO

from pypdf import PdfReader, PdfWriter
import pathlib
import argparse


def split_pdf_file(file: PdfReader, indices: list[int]) -> list[BytesIO]:
    """
    Split a PDF file into multiple files.
    For example, if a file has 10 pages, and you pass in indices
    1, 5, 7, 10 then you will get 3 files:
    File 1 containing pages 1-4,
    File 2 containing pages 5-6,
    File 3 containing pages 7-9.


    Assumptions:
        indices is sorted, nonempty, and contains valid indices.

    :param file:
    :param indices:
    :return:
    """
    output_files = []
    for i in range(len(indices) - 1):
        start = indices[i]
        end = indices[i + 1]
        # print(f"#{i+2} Pages included: {list(range(start, end))}")
        output_obj = BytesIO()
        file_writer = PdfWriter()
        pages_to_add = file.pages[start-1:end-1]
        for page in pages_to_add:
            file_writer.add_page(page)
        file_writer.write(output_obj)
        output_files.append(output_obj)
    return output_files


parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to the PDF file to split")
parser.add_argument(
    "indices",
    help="Indices to split the PDF file at. Delimit with commas."
)
parser.add_argument("--start-question-number", help="The question number to start at.",
                    default=2)
parser.add_argument("--output-dir", help="Directory to output the split files to.",
                    default="split_output")


if __name__ == "__main__":
    args = parser.parse_args()
    input_path = pathlib.Path(args.path).resolve()
    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(exist_ok=True)
    indices = [int(i) for i in args.indices.split(",")]
    file = PdfReader(input_path)
    if max(indices) - 1 > len(file.pages):
        raise ValueError("One of the indices is out of bounds.")
    output_files = split_pdf_file(file, indices)
    for i, output_file in enumerate(output_files):
        output_path = output_dir / f"Q{args.start_question_number + i}.pdf"
        with FileIO(output_path, "wb") as f:
            f.write(output_file.getvalue())

