from io import FileIO, BytesIO

from pypdf import PdfReader, PdfWriter
import pathlib
import argparse

from pypdf.generic import IndirectObject, Destination


def extract_sections(file: PdfReader) -> list[int]:
    """
    Attempt to automatically extract main sections from a PDF file.
    By section I mean the sections created by \section in LaTeX.

    :param file:
    :return: List of page numbers where the sections start.
    """
    # Note: I have assumed that everything that is a Destination
    # is a section. This seems to work for one of the files I've tested.
    main_sections = filter(lambda x: isinstance(x, Destination), file.outline)

    # noinspection PyTypeChecker
    # note that we add one, because apparently the page number
    # is 0-indexed
    page_numbers = map(
        lambda x: file.get_page_number(file.get_object(x.page)) + 1, main_sections
    )
    return list(page_numbers)


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
        pages_to_add = file.pages[start - 1 : end - 1]
        for page in pages_to_add:
            file_writer.add_page(page)
        file_writer.write(output_obj)
        output_files.append(output_obj)
    return output_files


parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to the PDF file to split")
parser.add_argument(
    "--indices",
    help="Indices to split the PDF file at. "
    "Delimit with commas. "
    "Will attempt to extract sections if not provided.",
)
parser.add_argument(
    "--start-question-number", help="The question number to start at.", default=1
)
parser.add_argument(
    "--output-dir",
    help="Directory to output the split files to.",
    default="split_output",
)


if __name__ == "__main__":
    args = parser.parse_args()
    input_path = pathlib.Path(args.path).resolve()
    output_dir = pathlib.Path(args.output_dir).resolve()
    output_dir.mkdir(exist_ok=True)

    file = PdfReader(input_path)
    if args.indices is None:
        indices = extract_sections(file)
        print(indices)
    else:
        indices = [int(i) for i in args.indices.split(",")]
    if max(indices) - 1 > len(file.pages):
        raise ValueError("One of the indices is out of bounds.")
    # add split for last page
    indices.append(len(file.pages) + 1)
    output_files = split_pdf_file(file, indices)
    for i, output_file in enumerate(output_files):
        output_path = output_dir / f"Q{args.start_question_number + i}.pdf"
        with FileIO(output_path, "wb") as f:
            f.write(output_file.getvalue())
