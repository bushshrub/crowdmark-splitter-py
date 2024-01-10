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

Subsections are handled properly. I recommend
putting a `\newpage` after each section, since
this ensures each file corresponds exactly
to one question.


Of course, you can also specify the split points manually with the
`--indices` flag. For example, if you want to split the pdf
at pages 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, and 21, you would run
`python splitter.py [path to pdf] --indices 1,3,5,7,9,11,13,15,17,19,21`
See the actual code for behaviour.

If the first question isn't question 1, but rather question n,
specify it with the flag `--start-question-number [n]`. This will
reindex the output filenames.

## Support
Lol
