# Split pdf files for crowdmark

Python version

## Setup
Make sure you have poetry installed.
Then run `poetry install` to install it.

## Example usage

`python splitter.py [path to pdf]`
Without specifying the split points, the program
will attempt to automatically detect where to split. This is useful
if you use a section per question in your PDF like

```tex
\section{Question 1}

\subsection{Part a}

\subsection{Part b}

\newpage

\section{Question 2}

\newpage
```

it is the most optimal. It handles subsections fine.

If the first question isn't question 1, but rather question n,
specify it with the flag `--start-question-number [n]`

