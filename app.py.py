import fitz # PyMuPDF
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


def extract_text_from_pdf(pdf_file):
  """Extracts text from a PDF file"""
  doc = fitz.open(pdf_file)
  text = ""
  for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text += page.get_text()
  return text


def determine_highest_marks_subject(pdf_text):
  """Parses marks from the text and determines the subject with the highest marks

  Args:
      pdf_text: The extracted text from the PDF file

  Returns:
      The subject with the highest marks and its marks, or None if no marks are found.
  """
  subjects_marks = {}
  lines = pdf_text.split('\n')
  for line in lines:
    if "marks" in line.lower() and ":" in line:  # Find lines containing "marks" and ":"
      subject, marks_str = line.split(":")  # Split the line by ":"
      subject = subject.strip().split()[-1]  # Extract the subject name
      marks_str = marks_str.strip()
      if marks_str.isdigit():
        marks = int(marks_str)
        subjects_marks[subject] = marks

  if subjects_marks:
    highest_marks_subject = max(subjects_marks, key=subjects_marks.get)
    highest_marks = subjects_marks[highest_marks_subject]
    return highest_marks_subject, highest_marks
  else:
    return None


@app.route("/")
def index():
  """Renders the index.html template"""
  return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
  """Handles file upload and processes the PDF"""
  if request.method == "POST":
    if "pdfFile" not in request.files:
      return redirect(request.url)

    file = request.files["pdfFile"]

    if file.filename != "Marksheet_proj.pdf":
      return redirect(request.url)

    pdf_path = f"22BCE5179/{file.filename}"
    file.save(pdf_path)

    pdf_text = extract_text_from_pdf(pdf_path)
    highest_marks_subject, highest_marks = determine_highest_marks_subject(pdf_text)

    if highest_marks_subject is not None:
      return render_template("result.html", highest_marks_subject=highest_marks_subject, highest_marks=highest_marks)
    else:
      return "No marks found in the marksheets."


if __name__ == "__main__":
  app.run(debug=True)
