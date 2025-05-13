# Resume Parser

A simple yet powerful **Resume Parser** built with **Streamlit** that extracts useful information from resumes uploaded in PDF or DOCX format. The parser identifies key details such as **Name**, **Contact Information**, **Email**, **Skills**, **Education**, and **Social Media Links** (LinkedIn, GitHub, etc.).

This project is still in development and is continuously being improved with new features and optimizations.

## Features

- **Upload PDF/DOCX Files**: Supports uploading of resumes in PDF and DOCX formats.
- **Extracted Information**:
  - Name
  - Contact Number
  - Email Address
  - Education Details
  - Skills (from a predefined list of tech and soft skills)
  - Social Media Links (GitHub, LinkedIn, Instagram, etc.)
- **User Interface**: Simple and user-friendly interface with Streamlit for easy interaction.
- **In Development**: Ongoing improvements to enhance the parser and UI.

## Tech Stack

- **Streamlit**: For building the interactive user interface.
- **Python Libraries**:
  - `PyPDF2`: For extracting text from PDF files.
  - `python-docx`: For extracting text from DOCX files.
  - `re` (Regex): For parsing and extracting structured data like emails, phone numbers, etc.

## Libraries Needed

To run the project, you will need to install the following libraries:

```bash
pip install streamlit python-docx PyPDF2
```
streamlit: For creating the web application and UI.

python-docx: For handling DOCX files and extracting text.

PyPDF2: For reading and extracting text from PDF files.

## Project Status
This project is currently in development. While the core features are functional, there are still improvements and bug fixes planned for the future. Feel free to contribute or report issues!

## Contribution Guidelines
We welcome contributions to this project! If you’d like to contribute, please fork the repository, make your changes, and open a pull request.

## To Report an Issue
Check if the issue already exists by searching in the Issues section.

If not, open a new issue with a clear description of the bug or feature request.

## Code of Conduct
Please follow the Contributor Covenant Code of Conduct when contributing.

## License
This project is open-source and available under the MIT License.

## Acknowledgments
Thanks to Streamlit for providing an easy-to-use framework for building web apps.

The python-docx and PyPDF2 libraries were used for handling DOCX and PDF files respectively.
