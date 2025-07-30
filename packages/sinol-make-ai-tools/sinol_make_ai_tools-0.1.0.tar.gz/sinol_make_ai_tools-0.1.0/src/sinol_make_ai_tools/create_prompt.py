import sys

def main(args):
    with open('prompt.txt', 'w', encoding='utf-8') as prompt_file:
        prompt_file.write(
            r"""You are tasked with creating competitive programing problem packages. These are directories full of files. I am aware that you are incapable of generating directories, so I created a serialized format of a directory to aid you in the process. Here is an example. Let's say we have the following directory structure:
```
.
├── file1.txt
└── dir/
    ├── file2.txt
    └── file3.txt
```
Then the serialized directory looks like this:

```
file1.txt
Content of file1
----------
dir/file2.txt
Content of file2
----------
dir/file3.txt
Content of file3
----------
```

Here are two example problem packages:

```
config.yml
title: Sumżyce
sinol_task_id: sum
sinol_contest_type: oi
memory_limit: 131072
time_limits:
  0: 1000
  1: 1000
  2: 1000
scores:
  1: 30
  2: 70
sinol_expected_scores:
  sum.cpp:
    expected:
      0: {points: 0, status: OK}
      1: {points: 30, status: OK}
      2: {points: 70, status: OK}
    points: 100
  sum2.cpp:
    expected:
      0: {points: 0, status: OK}
      1: {points: 30, status: OK}
      2: {points: 70, status: OK}
    points: 100
  sumb1.cpp:
    expected:
      0: {points: 0, status: OK}
      1: {points: 30, status: OK}
      2: {points: 0, status: WA}
    points: 30
  sums1.cpp:
    expected:
      0: {points: 0, status: WA}
      1: {points: 30, status: OK}
      2: {points: 0, status: TL}
    points: 30

----------
doc/spiral.cls
% Autor: Bartosz Kostka
% Licencja: CC BY-NC-SA 4.0
%
% Modyfikacje:


\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{spiral}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

\usepackage[a4paper, includeheadfoot, margin=40pt, footskip=\dimexpr\headsep+\ht\strutbox\relax, bmargin = \dimexpr60pt+2\ht\strutbox\relax,]{geometry}

\usepackage[utf8]{inputenc}
\usepackage{cmbright}
%\usepackage{newtxmath}
\usepackage{amsfonts, amsmath, amssymb}
\usepackage[T1]{fontenc}
\usepackage[polish]{babel}

\usepackage{multirow}
\usepackage{graphicx}
\usepackage{tabularx}
\usepackage{verbatim}
\usepackage{fancyvrb}
\usepackage{lastpage}
\usepackage{bbding}
\usepackage{tikz}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{ifmtarg}


% removes section numbers
\renewcommand{\@seccntformat}[1]{}

% footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}


\fancyfoot[C]{
      \hrule
      \vspace{4pt}
      \begin{footnotesize}
          \begin{tabularx}{1.015\textwidth}{lXr}
          \hspace{-13pt}
          \begin{tabular}{l}\title \\ \textcopyright \ \the\year{} XIV LO im. Stanisława Staszica \\ \href{https://sio2.staszic.waw.pl}{sio2.staszic.waw.pl}\end{tabular} &
          \begin{tabular}{c}\\ Szablon treści zadania został zaadaptowany z szablonu \\ stworzonego przez Bartosza Kostkę, dostępnego pod \\ warunkami licencji CC BY-NC-SA 4.0. \end{tabular} &
          \begin{tabular}{r}\vspace{3pt} \thepage/\pageref*{LastPage} \\ \raisebox{-8pt}{\href{https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pl}{\includegraphics[height=18px]{licencja}}} \end{tabular}
          \end{tabularx}
      \end{footnotesize}
}

% \lfoot{\footnotesize \title \\ XIV Olimpiada Informatyczna Juniorów \\ \href{https://oij.edu.pl}{oij.edu.pl} }
% \rfoot{\footnotesize \vspace{13pt} \thepage/\pageref*{LastPage}}
\renewcommand{\headrulewidth}{0px}
\setlength{\headheight}{0px}

\def\ifdef#1{\ifcsname#1\endcsname}

\ifdef{authorskey} \else \def\authorskey{Autor zadania} \fi

% header
\def\makeheader{%
  \raisebox{15px}{
  \hspace{-20px}
  \begin{minipage}[b][50px]{0.85\textwidth}
  \hspace{2px}
  {\LARGE \bf \title \ifdef{mode} \hspace{-8pt} \normalsize{(\mode)} \fi} \\
  \begin{small}
  \begin{tabularx}{\textwidth}{Xrl} \\
    \bf \contest &
    \ifdef{id} Kod zadania: \fi
    &
    \ifdef{id} \bf \detokenize\expandafter{\id} \fi \\
    \desc &
    \ifdef{ML} Limit pamięci: \fi
    \ifdef{setters} Opracowanie: \fi
    &
    \ifdef{ML} \bf \ML \fi
    \ifdef{setters} \bf \setters \fi \\
  \end{tabularx}
  \end{small}
  \end{minipage}
  \begin{minipage}[b][50px]{0.15\textwidth}
  \hspace{15px}\raisebox{3px}{\includegraphics[width=60px]{logo}}
  \end{minipage}
  }
  \vspace{-25px}
  \hrule
  \vspace{12px}
}

\usepackage{accsupp}
\newcommand{\noncopynumber}[1]{%
    \BeginAccSupp{method=escape,ActualText={}}%
    #1%
    \EndAccSupp{}%
}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstset{
  keywordstyle=\bfseries\color{magenta},
  numberstyle=\tiny\color{codegray},
  stringstyle=\color{codepurple},
  frame=none,
  breaklines=true,
  inputencoding=utf8,
  extendedchars=true,
  numberstyle=\footnotesize,
  texcl=true,
  backgroundcolor=\color{backcolour},
  columns=fullflexible,
  commentstyle=\color{codegreen},
  xleftmargin=4.5em,
  framexleftmargin=3em,
  showstringspaces=true,
  numbers=left,
  keepspaces=true,
  basicstyle=\small\fontfamily{fvm}\selectfont,
}

\newcommand\includecode[2]{
  \vspace{-0.7em}
  \lstinputlisting[#1]{#2}
}

\newcommand\includefile[1]{
  \vspace{-0.7em}
  \VerbatimInput[frame=single]{#1}
}

\newcommand\example[1]{
  \begin{center}%
  \begin{minipage}[t]{0.45\textwidth}%
  \vspace{0pt}%
      \noindent Wejście dla testu {\tt \detokenize\expandafter{\id}#1}:%
      \includefile{../in/\id#1.in}%
  \end{minipage}\hfill%
  \begin{minipage}[t]{0.1\textwidth}%
  \end{minipage}%
  \begin{minipage}[t]{0.45\textwidth}%
  \vspace{0pt}%
      \noindent Wyjście dla testu {\tt \detokenize\expandafter{\id}#1}:%
      \includefile{../out/\id#1.out}
  \end{minipage}%
  \end{center}%
}

\newcommand\fullexample[1]{
  \noindent Wejście dla testu {\tt \detokenize\expandafter{\id}#1}:%
  \includefile{../in/\id#1.in}%

  \noindent Wyjście dla testu {\tt \detokenize\expandafter{\id}#1}:%
  \includefile{../out/\id#1.out}
}

\newcommand\note[1]{
  \noindent {\bf Wyjaśnienie do przykładu:} #1
}

\newenvironment{ocen}{%
  \subsection{Pozostałe testy przykładowe}
  \begin{itemize}
}{
  \end{itemize}
}%

\newcommand\testocen[2]{
   \item[-] test {\tt \id#1}: #2
}

\newenvironment{subtasks}{
\tabularx{\textwidth}{|c|X|c|c|}
\hline
\textbf{Podzadanie} & \textbf{Ograniczenia} & \textbf{Limit czasu} & \textbf{Liczba punktów}\\
\hline
}{
\endtabularx
}

\newcommand\subtask[4]{
  #1 & #2 & #3 & #4\\ \hline
}

\newcommand\twocol[2]{%
\begin{center}%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#1}%
\end{minipage}\hfill%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#2}%
\end{minipage}%
\end{center}}

----------
doc/sumzad.tex
\documentclass{spiral}
\def\title{Sumżyce}
\def\id{sum}
\def\contest{} % np: WWI 2024 -- grupa 0
\def\desc{} % np: Dzień 4 -- 20 sierpnia 2024
\def\ML{128 MiB}

\begin{document}
  \makeheader

  Wyobraź sobie, że dwie samotne liczby, które przez długi czas wędrowały po
  matematycznym świecie, nie wiedząc, że ich przeznaczeniem jest spotkać się,
  w końcu trafiają na siebie. Każda z nich miała swoje miejsce, ale nie były
  pełne, dopóki nie zdecydowały się połączyć. A potem, po chwilowej
  nieśmiałości, postanawiają dodać do siebie swoje wartości. Ich spotkanie nie
  jest przypadkowe -- to moment pełen emocji, jak spotkanie starych przyjaciół,
  którzy odkrywają, że razem są silniejsi i bardziej znaczący.

  Teraz, gdy te liczby połączyły swoje siły, wypisz ich sumę, aby na zawsze
  pamiętać, jak wielką moc mają w sobie, kiedy współpracują!

  \section{Wejście}
  % Poprawna forma w sekcji Wejście to np. "jest"/"znajduje się".
  % Nie należy używać trybów przypuszczających ani wspominać o wczytywaniu.
  W pierwszym wierszu wejścia standardowego znajdują się dwie liczby całkowite
  $a$ oraz $b$ ($|a|, |b| \leq 10^{18}$), oznaczające liczby które spotkały się.

  \section{Wyjście}
  % Poprawna forma w sekcji Wyjście to np. "powinno być".
  % Nie należy używać "jest" ani wspominać o wypisywaniu.
  W jedynym wierszu wyjścia standardowego powinna znaleźć się jedna liczba
  całkowita -- suma liczb $a$ i $b$.

  \section{Przykłady}
  \example{0a}
  \note{Odpowiedzią jest $58$, ponieważ jest to suma liczb $21$ i $37$}

  \example{0b}

  \section{Ocenianie}
  \begin{subtasks}
    \subtask{1}{$0 \leq a, b \leq 10^6$}{$1$ s}{$30$}
    \subtask{2}{brak dodatkowych ograniczeń}{$1$ s}{$70$}
  \end{subtasks}

  % \newpage
  % \begin{center}
  %   \includegraphics[scale=0.4]{obrazek.png}
  % \end{center}

\end{document}

----------
prog/oi.h
/*
   oi.h - pakiet funkcji do pisania weryfikatorow wejsc (inwer) i wyjsc (chk)
   Oryginalny autor: Piotr Niedzwiedz
*/

#ifndef OI_LIB_OI_H_
#define OI_LIB_OI_H_

#include <algorithm>
#include <assert.h>
#include <concepts>
#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <climits>
#include <cmath>
#include <optional>
#include <random>
#include <sstream>
#include <vector>

using std::vector;
using std::max;
using std::swap;

// We want prevent usage of standard random function.
int rand(){
  fprintf(stderr, "DONT USE rand or random_shuffle!\nUse oi::Random class.\n");
  exit(1);
  return 0;
}

namespace oi {

enum Lang {
  EN = 0,
  PL = 1
};

class Reader;

class Scanner {
 protected:
  static const int realNumbersLimit = 20;

  Lang lang;
  Reader* reader;
  void(*end)(const char* msg, int line, int position);

  void readULL(unsigned long long int limit, unsigned long long int &val, bool &sign);
  void readLDB(long double limit, long double &val, bool &sign);

 public:
  Scanner(const char* file, Lang _lang = Lang(EN));
  Scanner(const char* file, void(*endf)(const char* msg, int line, int position), Lang _lang = Lang(EN));
  Scanner(FILE* input, Lang _lang = Lang(EN));
  Scanner(FILE* input, void(*endf)(const char* msg, int line, int position), Lang _lang = Lang(EN));
  ~Scanner();

  template <typename... Ts>
  void                error(const Ts&... args);

  // Skips all whitespaces until any occurrence of EOF or other non-white character.
  int                 skipWhitespaces();
  // Skips all whitespaces until any occurrence of EOF, EOLN or other non-white character.
  int                 skipWhitespacesUntilEOLN();

  int                 readInt(int min_value = INT_MIN, int max_value = INT_MAX);
  unsigned int        readUInt(unsigned int min_value = 0, unsigned int max_value = UINT_MAX);
  long long           readLL(long long int min_value = LLONG_MIN, long long int max_value = LLONG_MAX);
  unsigned long long  readULL(unsigned long long int min_value = 0, unsigned long long int max_value = ULLONG_MAX);

  float               readFloat(float min_value, float max_value);
  double              readDouble(double min_value, double max_value);
  long double         readLDouble(long double min_value, long double max_value);

  char                readChar();

  // Newline character is read, but isn't added to s
  int                 readLine(char* s, int size);

  // Reads a string until occurrence of EOF, EOLN or whitespace.
  // Returns the number of characters read (possibly 0).
  int                 readString(char* s, int size);

  void                readEof();
  void                readEofOrEoln();
  void                readEoln();
  void                readSpace();
  void                readTab();

  bool                isEOF();
 private:
  Scanner(Scanner &) {}
};

template <typename RandGen = std::mt19937_64> // use a fully portable random number generator such as a mersenne twister
class Random {
 public:
  explicit Random(std::optional<typename RandGen::result_type> seed = {}) {
    if (seed) {
      setSeed(*seed);
    }
   }

  void setSeed(RandGen::result_type seed) {
    rg_.seed(seed);
  }

  template <std::integral T = RandGen::result_type>
    requires (sizeof(T) <= sizeof(typename RandGen::result_type))
  T rand() {
    return static_cast<T>(rg_());
  }

  // returns a random integer in inclusive range [min, max]
  // example usage:
  //   oi::Random gen(2137);
  //   int a = gen.rand_range();
  //   long long b = gen.rand_range<long long>();
  template <std::integral T = int>
  T rand_range(T min, T max)
  {
    assert(min <= max);
    // do not use std::uniform_int_distribution because of portability concerns
    return static_cast<T>(rand() % (max - min + 1) + min);
  }

  // returns true with probability p, false with probability 1 - p
  bool rand_bool(double p) {
    assert(0 <= p && p <= 1);
    // do not use std::uniform_real_distribution because of portability concerns
    return rand<uint64_t>() / static_cast<long double>(std::numeric_limits<uint64_t>::max()) < p;
  }

  template<typename RandomIt>
  void shuffle(RandomIt first, RandomIt last) {
    // do not use std::shuffle because of portability concerns
    auto n = last - first;
    for (int i = 1; i < n; ++i) {
      int to = rand_range(0, i);
      swap(first[to], first[i]);
    }
  }

 private:
  RandGen rg_;
};

class Reader {
 private:
  static const int bufferSize = 1000;
  char Buffer[bufferSize];
  int head, tail;
  int line, position;
  void fillBuffer();
  FILE* input;
 public:
  explicit Reader(const char* file);
  explicit Reader(FILE* _input);
  ~Reader();
  bool isEOF();
  int getLine() {return line;}
  int getPosition() {return position;}
  char read(bool move = false);
 private:
  Reader(Reader &) {};
};


const char* msgLeadingZeros[]= {
  "Leading zeros",
  "Zera wiodace"};
const char* msgMinusZero[]= {
  "Minus zero -0",
  "Minus zero -0"};
const char* msgNoNumber[]= {
  "No number",
  "Brak liczby"};
const char* msgNoChar[]= {
  "No char - EOF",
  "Brak znaku - EOF"};
const char* msgNotEof[]= {
  "Not EOF",
  "Brak konca pliku"};
const char* msgNotEoln[]= {
  "Not EOLN",
  "Brak konca linii"};
const char* msgNotEofOrEoln[]= {
  "Not EOF or EOLN",
  "Brak konca linii i brak konca pliku"};
const char* msgNotSpace[]= {
  "Not space",
  "Brak spacji"};
const char* msgNotTab[]= {
  "Not tab",
  "Brak znaku tabulacji"};
const char* msgOutOfRangeInt[]= {
  "Integer out of range",
  "Liczba calkowita spoza zakresu"};
const char* msgOutOfRangeReal[]= {
  "Real number out of range",
  "Liczba rzeczywista spoza zakresu"};
const char* msgRealNumberLimit[]= {
  "Too many digits after dot",
  "Za duzo cyfr po kropce dziesietnej"};
const char* msgBadRealNumberFormat[]= {
  "Bad real number format",
  "Niepoprawny format liczby rzeczywistej"};

// ------------------------------- Implementation -----------------------------

typedef unsigned long long ull;
typedef unsigned int uint;
typedef long long ll;
typedef long double ldb;


inline bool isDot(char x) {
  return x == '.';
}

inline bool isEOLN(char x) {
  return x == '\n';
}

inline bool isMinus(char x) {
  return x == '-';
}

inline bool isSpace(char x) {
  return x == ' ';
}

inline bool isTab(char x) {
  return x == '\t';
}

inline bool isWhitespace(char x) {
  return x == ' ' || x == '\t' || x == '\n';
}

void endDefault(const char* msg, int line, int position) {
  printf("ERROR (line: %d, position: %d): %s\n", line, position, msg);
  exit(1);
}
// --------------------------- Reader's methods -------------------------------

Reader::Reader(const char* file) {
  assert((input = fopen(file, "r")) != NULL);
  head = tail= 0;
  line = position = 1;
}

Reader::Reader(FILE* _input) {
  input = _input;
  head = tail = 0;
  line = position = 1;
}

Reader::~Reader() {
  assert(fclose(input) == 0);
}

void Reader::fillBuffer() {
  while ((tail + 1) % bufferSize != head) {
    int v = getc(input);
    if (v == EOF) break;
    Buffer[tail] = static_cast<char>(v);
    tail = (tail + 1) % bufferSize;
  }
}

bool Reader::isEOF() {
  fillBuffer();
  return head == tail;
}

char Reader::read(bool move) {
  fillBuffer();
  assert((head != tail) || (!move));
  if (head == tail) return 0;
  char v = Buffer[head];
  if (move) {
    if (isEOLN(v)) {
      line++;
      position = 1;
    } else {
      position++;
    }
    head = (head + 1) % bufferSize;
  }
  return v;
}

// ---------------------------- Scanner's methods -----------------------------

Scanner::Scanner(const char* file, Lang _lang): lang(_lang) {
  reader = new Reader(file);
  end = endDefault;
}

Scanner::Scanner(const char* file, void(*endf)(const char* msg, int line, int position), Lang _lang): lang(_lang) {
  reader = new Reader(file);
  end = endf;
}

Scanner::Scanner(FILE* input, Lang _lang): lang(_lang) {
  reader = new Reader(input);
  end = endDefault;
}

Scanner::Scanner(FILE* input, void(*endf)(const char* msg, int line, int position), Lang _lang): lang(_lang) {
  reader = new Reader(input);
  end = endf;
}

Scanner::~Scanner() {
  delete reader;
}

template <typename... Ts>
void Scanner::error(const Ts&... args) {
  std::ostringstream oss;
  (oss << ... << args);
  int l = reader->getLine();
  int p = reader->getPosition();
  delete reader;
  end(oss.str().c_str(), l, p);
}

int Scanner::skipWhitespaces() {
  int result = 0;
  while (isWhitespace(reader->read())) {
    reader->read(1);
    result++;
  }
  return result;
}


int Scanner::skipWhitespacesUntilEOLN() {
  int result = 0;
  while (isWhitespace(reader->read()) && !isEOLN(reader->read())) {
    reader->read(1);
    result++;
  }
  return result;
}


// INTEGERS

int Scanner::readInt(int min_value, int max_value) {
  return (int)readLL(min_value, max_value);
}

uint Scanner::readUInt(uint min_value, uint max_value) {
  return (uint)readULL(min_value, max_value);
}

inline bool lower_equal(ull a, bool sign_a, ull b, bool sign_b) {
  if (sign_a != sign_b) return sign_a;
  if (sign_a) return a >= b;
  return a <= b;
}
inline ull spec_abs(ll x) {
  if (x < 0) return (-(x + 1)) + 1;
  return x;
}

ll Scanner::readLL(ll min_value, ll max_value) {
  assert(min_value <= max_value);
  bool sign;
  ull val;
  readULL(max(spec_abs(min_value), spec_abs(max_value)), val, sign);
  ll v = val;
  if (!(lower_equal(spec_abs(min_value), min_value < 0, v, sign) &&
        lower_equal(v, sign, spec_abs(max_value), max_value < 0)))
    error(msgOutOfRangeInt[lang]);
  if (sign) v *= -1;
  return v;
}

ull Scanner::readULL(ull min_value, ull max_value) {
  assert(min_value <= max_value);
  bool sign;
  ull val;
  readULL(max_value, val, sign);
  if (sign) error(msgOutOfRangeInt[lang]);
  if (!(min_value <= val))
    error(msgOutOfRangeInt[lang]);
  return val;
}

// REAL NUMBERS

float Scanner::readFloat(float min_value, float max_value) {
  return (float)readLDouble(min_value, max_value);
}

double Scanner::readDouble(double min_value, double max_value) {
  return (double)readLDouble(min_value, max_value);
}

long double Scanner::readLDouble(long double min_value, long double max_value) {
  assert(min_value <= max_value);
  bool sign;
  ldb val;
  readLDB(max(fabsl(min_value), fabsl(max_value)), val, sign);
  if (sign) val *= -1;
  if (!(min_value <= val && val <= max_value))
    error(msgOutOfRangeReal[lang]);
  return val;
}

// STRINGS

int Scanner::readString(char* s, int size) {
  int x = 0;
  while ( x < size - 1 && !isEOF() && !isWhitespace(reader->read()))
    s[x++] = reader->read(1);
  s[x]=0;
  return x;
}

int Scanner::readLine(char* s, int size) {
  int x = 0;
  while ( x < size - 1 && !isEOLN(reader->read()) && !isEOF())
    s[x++] = reader->read(1);
  s[x] = 0;
  if (isEOLN(reader->read())) reader->read(1);
  return x;
}

char Scanner::readChar() {
  if (reader->isEOF()) error(msgNoChar[lang]);
  return reader->read(1);
}

// WHITESPACES

void Scanner::readEof() {
  if (!reader->isEOF()) error(msgNotEof[lang]);
}

void Scanner::readEoln() {
  if (!isEOLN(reader->read())) error(msgNotEoln[lang]);
  reader->read(1);
}

void Scanner::readEofOrEoln() {
  if (isEOLN(reader->read())) {
    reader->read(1);
  } else if (!reader->isEOF()) {
    error(msgNotEofOrEoln[lang]);
  }
}


void Scanner::readSpace() {
  if (!isSpace(reader->read())) error(msgNotSpace[lang]);
  reader->read(1);
}

void Scanner::readTab() {
  if (!isTab(reader->read())) error(msgNotTab[lang]);
  reader->read(1);
}

bool Scanner::isEOF() {
  return reader->isEOF();
}


// PROTECTED

void Scanner::readULL(ull limit, ull &val, bool &sign) {
  sign = 0;
  val = 0;
  sign = isMinus(reader->read());
  if (sign) reader->read(1);
  int zeros = 0;
  int valDigits = 0;
  while ('0' == reader->read()) {
    zeros++;
    valDigits++;
    reader->read(1);
    if (zeros > 1) error(msgLeadingZeros[lang]);
  }
  int limDigits = 0;
  ull tmp = limit;
  while (tmp) {
    limDigits++;
    tmp /= 10;
  }
  if (!limDigits) limDigits = 1;
  while (isdigit(reader->read())) {
    valDigits++;
    if (valDigits > limDigits) error(msgOutOfRangeInt[lang]);
    char x = reader->read(1);
    if (valDigits == limDigits) {
      if (limit / 10 < val) error(msgOutOfRangeInt[lang]);
      if (limit / 10 == val && limit % 10 < (ull)(x - '0')) error(msgOutOfRangeInt[lang]);
    }
    val = val * 10 + x - '0';
  }
  if (val > 0 && zeros) error(msgLeadingZeros[lang]);
  if (sign && zeros) error(msgMinusZero[lang]);
  if (!valDigits) error(msgNoNumber[lang]);
}

void Scanner::readLDB(ldb, ldb &val, bool &sign) {
  sign = 0;
  val = 0;
  sign = isMinus(reader->read());
  if (sign) reader->read(1);
  int zeros = 0;
  int valDigits = 0;
  while ('0' == reader->read()) {
    zeros++;
    valDigits++;
    reader->read(1);
    if (zeros > 1) error(msgLeadingZeros[lang]);
  }
  if (zeros && isdigit(reader->read())) error(msgLeadingZeros[lang]);
  while (isdigit(reader->read())) {
    valDigits++;
    char x = reader->read(1);
    val = val * 10.0 + x - '0';
  }
  if (!valDigits) error(msgNoNumber[lang]);
  if (isDot(reader->read())) {
    reader->read(1);
    ldb dec = 1;
    int dotDigits = 0;
    while (isdigit(reader->read())) {
      dotDigits++;
      if (dotDigits > realNumbersLimit) error(msgRealNumberLimit[lang]);
      char x = reader->read(1);
      dec /= 10.0;
      val += dec * (x - '0');
    }
    if (!dotDigits) error(msgBadRealNumberFormat[lang]);
  }
}

}  // namespace oi

#endif  // OI_LIB_OI_H_

----------
prog/sum.cpp
#include <iostream>
using namespace std;

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int64_t a, b;
    cin >> a >> b;
    cout << a + b << "\n";

    return 0;
}

----------
prog/sumingen.cpp
#include "oi.h"
#include <bits/stdc++.h>
using namespace std;

const string task_id = "sum";

struct RandTest
{
    int64_t range;
};

struct PositiveTest
{
    int64_t range;
};

struct ConstTest
{
    int64_t a, b;
};

struct TestCase
{
    inline static int next_seed = 0xC0FFEE;
    int seed = next_seed++;

    int64_t a, b;

    TestCase(const RandTest& args)
    {
        oi::Random rng(seed);
        a = rng.rand_range(-args.range, args.range);
        b = rng.rand_range(-args.range, args.range);
    }

    TestCase(const PositiveTest& args)
        : TestCase(RandTest{.range = args.range})
    {
        a = abs(a);
        b = abs(b);
    }

    TestCase(const ConstTest& args)
        : a(args.a), b(args.b)
    {}

    friend ostream& operator<<(ostream& os, const TestCase& test)
    {
        os << test.a << " " << test.b << "\n";
        return os;
    }
};

int main() 
{
    vector<vector<TestCase>> test_groups = {
        {
            ConstTest{.a = 21, .b = 37},
            ConstTest{.a = -21, .b = 37},
        },
        {
            PositiveTest{.range = (int)1e3},
            PositiveTest{.range = (int)1e3},
            PositiveTest{.range = (int)1e3},
            PositiveTest{.range = (int)1e6},
            PositiveTest{.range = (int)1e6},
            PositiveTest{.range = (int)1e6},
        },
        {
            PositiveTest{.range = (int64_t)1e18},
            PositiveTest{.range = (int64_t)1e18},
            PositiveTest{.range = (int64_t)1e18},
            RandTest{.range = (int64_t)1e18},
            RandTest{.range = (int64_t)1e18},
            RandTest{.range = (int64_t)1e18},
        },
    };

    for (int i = 0; i < ssize(test_groups); ++i)
    {
        const vector<TestCase>& group = test_groups[i];
        const string group_name = to_string(i);

        for (int j = 0; j < ssize(group); ++j)
        {
            const TestCase& test = group[j];
            const string test_name = {(char)('a' + j)};

            const string file_name = task_id + group_name + test_name + ".in";
            fprintf(stderr, "writing %s (seed=%d)\n", file_name.c_str(), test.seed);
            ofstream{file_name} << test;
        }
    }

    return 0;
}

----------
prog/suminwer.cpp
#include "oi.h"

using ll = long long;

const ll max_range_1 = 1e6;
const ll max_range_2 = 1e18;

int main()
{
    oi::Scanner input_file(stdin, oi::PL);

    const ll a = input_file.readLL(-max_range_2, max_range_2);
    input_file.readSpace();
    const ll b = input_file.readLL(-max_range_2, max_range_2);
    input_file.readEoln();

    input_file.readEof();

    const bool subtask_1 = (0 <= a && a <= max_range_1 && 0 <= b && b <= max_range_1);
    const bool subtask_2 = (llabs(a) <= max_range_2 && llabs(b) <= max_range_2);

    const int print_w = (int) log10((double) max_range_2) + 1;
    printf("OK | a = %*lld b = %*lld subtasks = [%c%c]\n",
        print_w, a,
        print_w, b,
        (subtask_1 ? '1' : ' '),
        (subtask_2 ? '2' : ' ')

    );

    return 0;
}

----------
prog/sums1.cpp
#include <iostream>
using namespace std;

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int64_t a, b;
    cin >> a >> b;

    int64_t sum = 0;
    volatile int64_t a_ = llabs(a), b_ = llabs(b);
    for (int64_t i = 0; i < a_; ++i)
        sum += (a > 0) ? 1 : -1;
    for (int64_t i = 0; i < b_; ++i)
        sum += (b > 0) ? 1 : -1;
    cout << sum;

    return 0;
}

----------
```

```
config.yml
title: Kompleks mniejszości
sinol_task_id: inw
sinol_contest_type: oi
memory_limit: 524288
time_limits:
  0: 1000
  1: 1000
  2: 5000
  3: 5000
  4: 5000
scores:
  1: 30
  2: 40
  3: 20
  4: 10
sinol_expected_scores:
  inw.cpp:
    expected:
      0: {points: 0, status: OK}
      1: {points: 30, status: OK}
      2: {points: 40, status: OK}
      3: {points: 20, status: OK}
      4: {points: 10, status: OK}
    points: 100
  inws1.cpp:
    expected:
      0: {points: 0, status: OK}
      1: {points: 30, status: OK}
      2: {points: 0, status: TL}
      3: {points: 0, status: TL}
      4: {points: 0, status: TL}
    points: 30

----------
doc/inwsol.tex
\documentclass{spiral}
\def\title{Kompleks mniejszości}
\def\id{inw}
\def\contest{smolPREOI 2024} % np: WWI 2024 -- grupa 0
\def\desc{Dzień 2 -- 14 grudnia 2024} % np: Dzień 4 -- 20 sierpnia 2024
\def\ML{512 MiB}

\begin{document}
  \makeheader
  \noindent
Przypomnę treść:\\
  Pracownicy Bajtcorpu tworzą drzewo, w którym każdy poza CEO ma dokładnie
  jednego szefa. Każdy pracownik ma swoje ID od $1$ do $n$, będące nie
  tylko identyfikatorem, ale również wyznaczający jego zarobki ($i$-ty
  pracownik zarabia $i$ bajtalarów miesięcznie). CEO ma id równe 1.
  Pracownikowi robi się smutno, gdy widzą że inny pracownik będący 
  bezpośrednio lub pośrednio pod jego nadzorem zarabia więcej niż on.\\
  Bajtek postanowił zrobić apkę dla na rzecz zdrowia psychicznego pracowników
  Bajtcorpu. Apka mówi każdemu pracownikowi ile jest pracowników pod jego
  nadzorem którzy zarabiają mniej niż on. Pomóż Bajtkowi to zaimplementować!\\[10pt]
  \noindent
  Można oczywiście przekazywać dzieciom w dfs-ie vector z listą przodków przez referencję oraz kazać każdemu wierzchołkowi dodać $+1$ do odpowiedzi dla każdego wierzchołka o większym indeksie w otrzymanym vectorze. To jest rozwiązanie $O(n^2)$ dające punkty z pierwszego podzadania.\\
  \noindent
  Podzadanie ze ścieżką to znany wszystkim problem zliczania inwersji w ciągu. Można to zrobić chociażby drzewem przedziałowym w następujący sposób: przechodzimy się po ciągu i dla każdego elemntu najpierw robimy $+1$ na pozycji równej jego wartości, następnie liczymy sumę na przedziale $(0, w)$, gdzie $w$ to ten element i w ten sposób uzyskujemy odpowiedź dla elementu $w$.\\
  \noindent
  Żeby zrobić zadanie na $O(nlog^2n)$ można przerobić solva dla ścieżki na drzewo za pomocą sztuczki mniejszy do większego; dziecko z największym poddrzewem przekazuje rozicowi drzewo przedziałowe, a rozdzic dodaje do otrzymanego drzewa przedziałowego indeksy wierzchołków z poddrzew pozostałych dzieci.\\
  Wzorcówka jest na $O(nlogn)$. Trzeba rozłożyć drzewo na euler tour (czyli ciąg indeksów wierzchołków posortowany po preorderach). Wtedy zadanie sprowadza się do pytania "ile jest elementów ciągu na przedziale $[l, r)$ mniejszych od $x$" ($x$ to indeks wierzchołka dla którego chcemy uzyskać odpowiedź, a $[l, r)$ to jego zakres jego poddrzewa w euler tourze). Dla każdego $x$ możemy pozdzielić pytanie na dwa pytania: ile jest elementów mniejszych od $x$ na przedziale $[0, l)$ i ile jest elementów mniejszych od $x$ na przedziale $[0, r)$, a szukana wartość to różnica tych odpowiedzi. Można więc dla każdego $x$ stworzyć dwa zapytania, a następnie posortować te zapytania po długości przedziału o które pytają. Wtedy można się przejść po euler tourze i każdy element najpierw dodać, a następnie odpowiedzieć na wszystkie pytania pytające o przedział kończący się na tym elemencie.\\
  To tyle. Mój kod ma poniżej 100 lin. Jak widać, nie jest to zbyt skomplikowane zadanie.\\

\end{document}

----------
doc/inwzad.tex
\documentclass{spiral}
\def\title{Kompleks mniejszości}
\def\id{inw}
\def\contest{smolPREOI 2024} % np: WWI 2024 -- grupa 0
\def\desc{Dzień 2 -- 14 grudnia 2024} % np: Dzień 4 -- 20 sierpnia 2024
\def\ML{512 MiB}

\begin{document}
  \makeheader

  Pracownicy Bajtcorpu tworzą drzewo, w którym każdy poza CEO ma dokładnie
  jednego szefa. Każdy pracownik ma swoje ID od $1$ do $n$, będące nie
  tylko identyfikatorem, ale również wyznaczający jego zarobki ($i$-ty
  pracownik zarabia $i$ bajtalarów miesięcznie). CEO ma id równe 1.
  Pracownikowi robi się smutno, gdy widzą że inny pracownik będący 
  bezpośrednio lub pośrednio pod jego nadzorem zarabia więcej niż on.\\
  Bajtek postanowił zrobić apkę dla na rzecz zdrowia psychicznego pracowników
  Bajtcorpu. Apka mówi każdemu pracownikowi ile jest pracowników pod jego
  nadzorem którzy zarabiają mniej niż on. Pomóż Bajtkowi to zaimplementować!

  \section{Wejście}
  % Poprawna forma w sekcji Wejście to np. "jest"/"znajduje się".
  % Nie należy używać trybów przypuszczających ani wspominać o wczytywaniu.
  W pierwszym wierszu wejścia znajduje się jedna liczba całkowita $n$
  ($1 \leqslant n \leqslant 10^6$). W każdym z następnych $n - 1$ wierszy
  wejścia znajdują się po dwie liczby całkowite $a$ i $b$ 
  ($1 \leqslant a, b \leqslant n$) oznaczające, że pracownik $a$ jest szefem
  pracownika $b$. Pracownik $1$ jest jedynym bez szefa.

  \section{Wyjście}
  % Poprawna forma w sekcji Wyjście to np. "powinno być".
  % Nie należy używać "jest" ani wspominać o wypisywaniu.
  W $i$-tym wierszu wyjścia powinna się znaleźć jedna liczba całkowita będąca
  równa liczbie wierzchołków w poddrzewie wierzchołka $i$ o indeksie mniejszym
  od $i$.

  \section{Przykłady}
  \example{0a}

  \example{0b}

  \section{Ocenianie}
  \begin{subtasks}
    \subtask{1}{$n \leqslant 1000$}{$1$ s}{$30$}
    \subtask{2}{$n \leqslant 10^5$}{$1$ s}{$40$}
    \subtask{3}{drzewo jest ścieżką w której 1 jest końcem}{$5$ s}{$20$}
    \subtask{4}{brak dodatkowych ograniczeń}{$5$ s}{$10$}
  \end{subtasks}

  % \newpage
  % \begin{center}
  %   \includegraphics[scale=0.4]{obrazek.png}
  % \end{center}

\end{document}

----------
doc/spiral.cls
% Autor: Bartosz Kostka
% Licencja: CC BY-NC-SA 4.0
%
% Modyfikacje:


\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{spiral}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

\usepackage[a4paper, includeheadfoot, margin=40pt, footskip=\dimexpr\headsep+\ht\strutbox\relax, bmargin = \dimexpr60pt+2\ht\strutbox\relax,]{geometry}

\usepackage[utf8]{inputenc}
\usepackage{cmbright}
%\usepackage{newtxmath}
\usepackage{amsfonts, amsmath, amssymb}
\usepackage[T1]{fontenc}
\usepackage[polish]{babel}

\usepackage{multirow}
\usepackage{graphicx}
\usepackage{tabularx}
\usepackage{verbatim}
\usepackage{fancyvrb}
\usepackage{lastpage}
\usepackage{bbding}
\usepackage{tikz}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{ifmtarg}


% removes section numbers
\renewcommand{\@seccntformat}[1]{}

% footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}


\fancyfoot[C]{
      \hrule
      \vspace{4pt}
      \begin{footnotesize}
          \begin{tabularx}{1.015\textwidth}{lXr}
          \hspace{-13pt}
          \begin{tabular}{l}\title \\ \textcopyright \ \the\year{} XIV LO im. Stanisława Staszica \\ \href{https://sio2.staszic.waw.pl}{sio2.staszic.waw.pl}\end{tabular} &
          \begin{tabular}{c}\\ Szablon treści zadania został zaadaptowany z szablonu \\ stworzonego przez Bartosza Kostkę, dostępnego pod \\ warunkami licencji CC BY-NC-SA 4.0. \end{tabular} &
          \begin{tabular}{r}\vspace{3pt} \thepage/\pageref*{LastPage} \\ \raisebox{-8pt}{\href{https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pl}{\includegraphics[height=18px]{licencja}}} \end{tabular}
          \end{tabularx}
      \end{footnotesize}
}

% \lfoot{\footnotesize \title \\ XIV Olimpiada Informatyczna Juniorów \\ \href{https://oij.edu.pl}{oij.edu.pl} }
% \rfoot{\footnotesize \vspace{13pt} \thepage/\pageref*{LastPage}}
\renewcommand{\headrulewidth}{0px}
\setlength{\headheight}{0px}

\def\ifdef#1{\ifcsname#1\endcsname}

\ifdef{authorskey} \else \def\authorskey{Autor zadania} \fi

% header
\def\makeheader{%
  \raisebox{15px}{
  \hspace{-20px}
  \begin{minipage}[b][50px]{0.85\textwidth}
  \hspace{2px}
  {\LARGE \bf \title \ifdef{mode} \hspace{-8pt} \normalsize{(\mode)} \fi} \\
  \begin{small}
  \begin{tabularx}{\textwidth}{Xrl} \\
    \bf \contest &
    \ifdef{id} Kod zadania: \fi
    &
    \ifdef{id} \bf \detokenize\expandafter{\id} \fi \\
    \desc &
    \ifdef{ML} Limit pamięci: \fi
    \ifdef{setters} Opracowanie: \fi
    &
    \ifdef{ML} \bf \ML \fi
    \ifdef{setters} \bf \setters \fi \\
  \end{tabularx}
  \end{small}
  \end{minipage}
  \begin{minipage}[b][50px]{0.15\textwidth}
  \hspace{15px}\raisebox{3px}{\includegraphics[width=60px]{logo}}
  \end{minipage}
  }
  \vspace{-25px}
  \hrule
  \vspace{12px}
}

\usepackage{accsupp}
\newcommand{\noncopynumber}[1]{%
    \BeginAccSupp{method=escape,ActualText={}}%
    #1%
    \EndAccSupp{}%
}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstset{
  keywordstyle=\bfseries\color{magenta},
  numberstyle=\tiny\color{codegray},
  stringstyle=\color{codepurple},
  frame=none,
  breaklines=true,
  inputencoding=utf8,
  extendedchars=true,
  numberstyle=\footnotesize,
  texcl=true,
  backgroundcolor=\color{backcolour},
  columns=fullflexible,
  commentstyle=\color{codegreen},
  xleftmargin=4.5em,
  framexleftmargin=3em,
  showstringspaces=true,
  numbers=left,
  keepspaces=true,
  basicstyle=\small\fontfamily{fvm}\selectfont,
}

\newcommand\includecode[2]{
  \vspace{-0.7em}
  \lstinputlisting[#1]{#2}
}

\newcommand\includefile[1]{
  \vspace{-0.7em}
  \VerbatimInput[frame=single]{#1}
}

\newcommand\example[1]{
  \begin{center}%
  \begin{minipage}[t]{0.45\textwidth}%
  \vspace{0pt}%
      \noindent Wejście dla testu {\tt \detokenize\expandafter{\id}#1}:%
      \includefile{../in/\id#1.in}%
  \end{minipage}\hfill%
  \begin{minipage}[t]{0.1\textwidth}%
  \end{minipage}%
  \begin{minipage}[t]{0.45\textwidth}%
  \vspace{0pt}%
      \noindent Wyjście dla testu {\tt \detokenize\expandafter{\id}#1}:%
      \includefile{../out/\id#1.out}
  \end{minipage}%
  \end{center}%
}

\newcommand\fullexample[1]{
  \noindent Wejście dla testu {\tt \detokenize\expandafter{\id}#1}:%
  \includefile{../in/\id#1.in}%

  \noindent Wyjście dla testu {\tt \detokenize\expandafter{\id}#1}:%
  \includefile{../out/\id#1.out}
}

\newcommand\note[1]{
  \noindent {\bf Wyjaśnienie do przykładu:} #1
}

\newenvironment{ocen}{%
  \subsection{Pozostałe testy przykładowe}
  \begin{itemize}
}{
  \end{itemize}
}%

\newcommand\testocen[2]{
   \item[-] test {\tt \id#1}: #2
}

\newenvironment{subtasks}{
\tabularx{\textwidth}{|c|X|c|c|}
\hline
\textbf{Podzadanie} & \textbf{Ograniczenia} & \textbf{Limit czasu} & \textbf{Liczba punktów}\\
\hline
}{
\endtabularx
}

\newcommand\subtask[4]{
  #1 & #2 & #3 & #4\\ \hline
}

\newcommand\twocol[2]{%
\begin{center}%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#1}%
\end{minipage}\hfill%
\begin{minipage}[t]{0.5\textwidth}%
\vspace{0pt}%
{#2}%
\end{minipage}%
\end{center}}

----------
prog/inw.cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define all(x) x.begin(), x.end()
#define len(x) ((ll) x.size())

struct Quest
{
    ll pos;
    ll author;
    ll multplier;
};

const ll max_n = 1000'001;
array<ll, max_n> answers;
array<vector<ll>, max_n> neigh;
vector<ll> euler_tour;
vector<Quest> quests;
array<ll, max_n * 2> tree;
ll n;

void add(ll p)
{
    for (tree[p += n+1] = 1; p > 1; p >>= 1) tree[p >> 1] = tree[p] + tree[p^1];
}

ll sum(ll l, ll r)
{
    ll answer = 0;

    for (l += n+1, r += n+1; l < r; l >>= 1, r >>= 1)
    {
        if (l&1) answer += tree[l++];
        if (r&1) answer += tree[--r];
    }

    return answer;
}

void dfs(ll node, ll father)
{
    euler_tour.push_back(node);
    quests.push_back({len(euler_tour) - 1, node, -1});

    for (ll v : neigh[node])
    {
        if (v == father) continue;
        dfs(v, node);
    }

    quests.push_back({len(euler_tour) - 1, node, 1});
}

bool comp_quests(const Quest& a, const Quest& b)
{
    return a.pos < b.pos;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;

    for (ll i = 0; i < n - 1; i++)
    {
        ll a, b;
        cin >> a >> b;
        neigh[a].push_back(b);
        neigh[b].push_back(a);
    }

    dfs(1, 0);
    sort(all(quests), comp_quests);

    for (ll i = 0, quest_index = 0; i < n; i++)
    {
        add(euler_tour[i]);

        while (quest_index < len(quests) && quests[quest_index].pos == i)
        {
            Quest q = quests[quest_index++];
            answers[q.author] += q.multplier * sum(0, q.author);
        }
    }

    for (ll i = 1; i <= n; i++)
    {
        cout << answers[i] << "\n";
    }

    return 0;
}

----------
prog/inwingen.cpp
#include "oi.h"
#include <bits/stdc++.h>
using namespace std;

const string task_id = "inw";
#define len(x) ((int64_t) x.size())

struct ConstNTest
{
    int64_t n;
    vector<int64_t> child_count_prob_dist;
};

struct StarTest
{
    int64_t n;
    vector<int64_t> dist() const
    {
        vector<int64_t> answer;
        for (int64_t i = 0; i < n - 2; i++) answer.push_back(0);
        answer.push_back(1);
        return answer;
    }
};

struct LineTest
{
    int64_t n;
    vector<int64_t> dist() const
    {
        return {1};
    }
};

struct ConstTest
{
    int64_t n;
    vector<array<int64_t, 2>> edges;
};

struct TestCase
{
    inline static int next_seed = 0xC0FFEE;
    int seed = next_seed++;

    int64_t n;
    vector<array<int64_t, 2>> edges;

    TestCase(const ConstNTest& test) : n(test.n)
    {
        oi::Random rng(seed);
        int64_t probability_sum = 0;

        for (int64_t p : test.child_count_prob_dist)
        {
            probability_sum += p;
        }

        vector<int64_t> vertecies;

        for (int64_t i = 1; i <= n; i++)
        {
            vertecies.push_back(i);
        }

        rng.shuffle(vertecies.begin() + 1, vertecies.end());

        int64_t child_index = 1;
        for (int64_t node : vertecies)
        {
            int64_t dist_value = rng.rand_range((int64_t) 0, probability_sum - 1);
            int64_t child_count = 0;

            for (int64_t sum = 0; sum <= dist_value; )
            {
                sum += test.child_count_prob_dist[child_count];
                child_count++;
            }

            for (; child_count && child_index < len(vertecies); child_index++)
            {
                edges.push_back({{node, vertecies[child_index]}});
                child_count--;
            }
        }
    }

    TestCase(const StarTest& test)
        : TestCase(ConstNTest{.n = test.n, .child_count_prob_dist = test.dist()})
    {}

    TestCase(const LineTest& test)
        : TestCase(ConstNTest{.n = test.n, .child_count_prob_dist = test.dist()})
    {}

    TestCase(const ConstTest& test)
        : n(test.n), edges(test.edges)
    {}

    friend ostream& operator<<(ostream& os, const TestCase& test)
    {
        os << test.n << "\n";

        for (int64_t i = 0; i < test.n - 1; i++)
        {
            os << test.edges[i][0] << " " << test.edges[i][1] << "\n";
        }

        return os;
    }
};

int main() 
{
    const int64_t max_n_1 = 1000;
    const int64_t max_n_2 = 100'000;
    const int64_t max_n_3 = 1000'000;
    vector<vector<TestCase>> test_groups = {
        {
            ConstTest{.n = 4, .edges = {{{{1, 2}}, {{1, 4}}, {{4, 3}}}}},
            ConstTest
            {
                .n = 7, 
                .edges = 
                {{
                    {{1, 4}}, 
                    {{1, 5}},
                    {{4, 2}},
                    {{4, 3}},
                    {{4, 6}},
                    {{1, 7}}
                }},
            },
        },
        {
            ConstNTest{.n =       1, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =     100, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =      10, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {2, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {100, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {100, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1, 100}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {100, 1, 1}},
            ConstNTest{.n = max_n_1, .child_count_prob_dist = {1, 2, 3}},
        },
        {
            ConstNTest{.n =       1, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =     100, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =      10, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {2, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {100000, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {100000, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1, 100000}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {100000, 1, 1}},
            ConstNTest{.n = max_n_2, .child_count_prob_dist = {1, 2, 3}},
        },
        {
            LineTest{.n = 1},
            LineTest{.n = 10},
            LineTest{.n = 100},
            LineTest{.n = 1000},
            LineTest{.n = 10000},
            LineTest{.n = 10000},
            LineTest{.n = max_n_3},
            LineTest{.n = max_n_3},
            LineTest{.n = max_n_3},
            LineTest{.n = max_n_3},
            LineTest{.n = max_n_3},
        },
        {
            ConstNTest{.n =       1, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =     100, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n =      10, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {4, 3, 2, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {2, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {100000, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {100000, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1, 100000}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {100000, 1, 1}},
            ConstNTest{.n = max_n_3, .child_count_prob_dist = {1, 2, 3}},
        },
    };

    for (int i = 0; i < ssize(test_groups); ++i)
    {
        const vector<TestCase>& group = test_groups[i];
        const string group_name = to_string(i);

        for (int j = 0; j < ssize(group); ++j)
        {
            const TestCase& test = group[j];
            const string test_name = {(char)('a' + j)};

            const string file_name = task_id + group_name + test_name + ".in";
            fprintf(stderr, "writing %s (seed=%d)\n", file_name.c_str(), test.seed);
            ofstream{file_name} << test;
        }
    }

    return 0;
}

----------
prog/inwinwer.cpp
#include "oi.h"
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define len(x) ((ll) x.size())

const ll max_n_1 = 1000;
const ll max_n_2 = 100'000;
const ll max_n_3 = 1000'000;
ll n;
vector<array<ll, 2>> edges;
array<vector<ll>, max_n_3 + 1> neigh;
array<bool, max_n_3 + 1> visited;

void dfs(ll node)
{
    visited[node] = true;

    for (ll v : neigh[node])
    {
        if (visited[v]) continue;
        dfs(v);
    }
}

void build_neigh()
{
    for (ll i = 0; i < n - 1; i++)
    {
        neigh[edges[i][0]].push_back(edges[i][1]);
        neigh[edges[i][1]].push_back(edges[i][0]);
    }
}

bool is_tree()
{
    dfs(1);

    for (ll i = 1; i <= n; i++)
    {
        if (!visited[i]) return false;
    }

    return true;
}

bool is_line()
{
    if (n == 1) return true;
    if (len(neigh[1]) != 1) return false;

    for (ll i = 1; i <= n; i++)
    {
        if (len(neigh[i]) != 1 && len(neigh[i]) != 2) return false;
    }

    return true;
}

int main()
{
    oi::Scanner input_file(stdin, oi::PL);

    n = input_file.readLL(1, max_n_3);
    input_file.readEoln();

    for (int i = 0; i < n - 1; i++)
    {
        ll a = input_file.readLL(1, n);
        input_file.readSpace();
        ll b = input_file.readLL(1, n);
        input_file.readEoln();
        edges.push_back({{a, b}});
    }

    input_file.readEof();
    build_neigh();

    const bool subtask_1 = (is_tree() && n <= max_n_1);
    const bool subtask_2 = (is_tree() && n <= max_n_2);
    const bool subtask_3 = (is_tree() && is_line());
    const bool subtask_4 = (is_tree());

    const int print_w = (int) log10((double) max_n_3) + 1;
    printf("OK | n = %*lld subtasks = [%c%c%c%c]\n",
        print_w, n,
        (subtask_1 ? '1' : ' '),
        (subtask_2 ? '2' : ' '),
        (subtask_3 ? '3' : ' '),
        (subtask_4 ? '4' : ' ')
    );

    return 0;
}

----------
prog/inws1.cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define len(x) ((ll) x.size())
#define all(x) x.begin(), x.end()

ll n;
const ll max_n = 1000'001;
array<ll, max_n> answers;
array<vector<ll>, max_n> neigh;

void dfs(ll node, ll father, vector<ll>& ancestors)
{
    for (ll v : ancestors)
    {
        if (v > node) answers[v]++;
    }

    ancestors.push_back(node);

    for (ll v : neigh[node])
    {
        if (v == father) continue;
        dfs(v, node, ancestors);
    }

    ancestors.pop_back();
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;

    for (ll i = 0; i < n - 1; i++)
    {
        ll a, b;
        cin >> a >> b;
        neigh[a].push_back(b);
        neigh[b].push_back(a);
    }

    vector<ll> ancestors = {};
    dfs(1, 0, ancestors);

    for (int i = 1; i <= n; i++)
    {
        cout << answers[i] << "\n";
    }
}

----------
prog/oi.h
/*
   oi.h - pakiet funkcji do pisania weryfikatorow wejsc (inwer) i wyjsc (chk)
   Oryginalny autor: Piotr Niedzwiedz
*/

#ifndef OI_LIB_OI_H_
#define OI_LIB_OI_H_

#include <algorithm>
#include <assert.h>
#include <concepts>
#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <climits>
#include <cmath>
#include <optional>
#include <random>
#include <sstream>
#include <vector>

using std::vector;
using std::max;
using std::swap;

// We want prevent usage of standard random function.
int rand(){
  fprintf(stderr, "DONT USE rand or random_shuffle!\nUse oi::Random class.\n");
  exit(1);
  return 0;
}

namespace oi {

enum Lang {
  EN = 0,
  PL = 1
};

class Reader;

class Scanner {
 protected:
  static const int realNumbersLimit = 20;

  Lang lang;
  Reader* reader;
  void(*end)(const char* msg, int line, int position);

  void readULL(unsigned long long int limit, unsigned long long int &val, bool &sign);
  void readLDB(long double limit, long double &val, bool &sign);

 public:
  Scanner(const char* file, Lang _lang = Lang(EN));
  Scanner(const char* file, void(*endf)(const char* msg, int line, int position), Lang _lang = Lang(EN));
  Scanner(FILE* input, Lang _lang = Lang(EN));
  Scanner(FILE* input, void(*endf)(const char* msg, int line, int position), Lang _lang = Lang(EN));
  ~Scanner();

  template <typename... Ts>
  void                error(const Ts&... args);

  // Skips all whitespaces until any occurrence of EOF or other non-white character.
  int                 skipWhitespaces();
  // Skips all whitespaces until any occurrence of EOF, EOLN or other non-white character.
  int                 skipWhitespacesUntilEOLN();

  int                 readInt(int min_value = INT_MIN, int max_value = INT_MAX);
  unsigned int        readUInt(unsigned int min_value = 0, unsigned int max_value = UINT_MAX);
  long long           readLL(long long int min_value = LLONG_MIN, long long int max_value = LLONG_MAX);
  unsigned long long  readULL(unsigned long long int min_value = 0, unsigned long long int max_value = ULLONG_MAX);

  float               readFloat(float min_value, float max_value);
  double              readDouble(double min_value, double max_value);
  long double         readLDouble(long double min_value, long double max_value);

  char                readChar();

  // Newline character is read, but isn't added to s
  int                 readLine(char* s, int size);

  // Reads a string until occurrence of EOF, EOLN or whitespace.
  // Returns the number of characters read (possibly 0).
  int                 readString(char* s, int size);

  void                readEof();
  void                readEofOrEoln();
  void                readEoln();
  void                readSpace();
  void                readTab();

  bool                isEOF();
 private:
  Scanner(Scanner &) {}
};

template <typename RandGen = std::mt19937_64> // use a fully portable random number generator such as a mersenne twister
class Random {
 public:
  explicit Random(std::optional<typename RandGen::result_type> seed = {}) {
    if (seed) {
      setSeed(*seed);
    }
   }

  void setSeed(RandGen::result_type seed) {
    rg_.seed(seed);
  }

  template <std::integral T = RandGen::result_type>
    requires (sizeof(T) <= sizeof(typename RandGen::result_type))
  T rand() {
    return static_cast<T>(rg_());
  }

  // returns a random integer in inclusive range [min, max]
  // example usage:
  //   oi::Random gen(2137);
  //   int a = gen.rand_range();
  //   long long b = gen.rand_range<long long>();
  template <std::integral T = int>
  T rand_range(T min, T max)
  {
    assert(min <= max);
    // do not use std::uniform_int_distribution because of portability concerns
    return static_cast<T>(rand() % (max - min + 1) + min);
  }

  // returns true with probability p, false with probability 1 - p
  bool rand_bool(double p) {
    assert(0 <= p && p <= 1);
    // do not use std::uniform_real_distribution because of portability concerns
    return rand<uint64_t>() / static_cast<long double>(std::numeric_limits<uint64_t>::max()) < p;
  }

  template<typename RandomIt>
  void shuffle(RandomIt first, RandomIt last) {
    // do not use std::shuffle because of portability concerns
    auto n = last - first;
    for (int i = 1; i < n; ++i) {
      int to = rand_range(0, i);
      swap(first[to], first[i]);
    }
  }

 private:
  RandGen rg_;
};

class Reader {
 private:
  static const int bufferSize = 1000;
  char Buffer[bufferSize];
  int head, tail;
  int line, position;
  void fillBuffer();
  FILE* input;
 public:
  explicit Reader(const char* file);
  explicit Reader(FILE* _input);
  ~Reader();
  bool isEOF();
  int getLine() {return line;}
  int getPosition() {return position;}
  char read(bool move = false);
 private:
  Reader(Reader &) {};
};


const char* msgLeadingZeros[]= {
  "Leading zeros",
  "Zera wiodace"};
const char* msgMinusZero[]= {
  "Minus zero -0",
  "Minus zero -0"};
const char* msgNoNumber[]= {
  "No number",
  "Brak liczby"};
const char* msgNoChar[]= {
  "No char - EOF",
  "Brak znaku - EOF"};
const char* msgNotEof[]= {
  "Not EOF",
  "Brak konca pliku"};
const char* msgNotEoln[]= {
  "Not EOLN",
  "Brak konca linii"};
const char* msgNotEofOrEoln[]= {
  "Not EOF or EOLN",
  "Brak konca linii i brak konca pliku"};
const char* msgNotSpace[]= {
  "Not space",
  "Brak spacji"};
const char* msgNotTab[]= {
  "Not tab",
  "Brak znaku tabulacji"};
const char* msgOutOfRangeInt[]= {
  "Integer out of range",
  "Liczba calkowita spoza zakresu"};
const char* msgOutOfRangeReal[]= {
  "Real number out of range",
  "Liczba rzeczywista spoza zakresu"};
const char* msgRealNumberLimit[]= {
  "Too many digits after dot",
  "Za duzo cyfr po kropce dziesietnej"};
const char* msgBadRealNumberFormat[]= {
  "Bad real number format",
  "Niepoprawny format liczby rzeczywistej"};

// ------------------------------- Implementation -----------------------------

typedef unsigned long long ull;
typedef unsigned int uint;
typedef long long ll;
typedef long double ldb;


inline bool isDot(char x) {
  return x == '.';
}

inline bool isEOLN(char x) {
  return x == '\n';
}

inline bool isMinus(char x) {
  return x == '-';
}

inline bool isSpace(char x) {
  return x == ' ';
}

inline bool isTab(char x) {
  return x == '\t';
}

inline bool isWhitespace(char x) {
  return x == ' ' || x == '\t' || x == '\n';
}

void endDefault(const char* msg, int line, int position) {
  printf("ERROR (line: %d, position: %d): %s\n", line, position, msg);
  exit(1);
}
// --------------------------- Reader's methods -------------------------------

Reader::Reader(const char* file) {
  assert((input = fopen(file, "r")) != NULL);
  head = tail= 0;
  line = position = 1;
}

Reader::Reader(FILE* _input) {
  input = _input;
  head = tail = 0;
  line = position = 1;
}

Reader::~Reader() {
  assert(fclose(input) == 0);
}

void Reader::fillBuffer() {
  while ((tail + 1) % bufferSize != head) {
    int v = getc(input);
    if (v == EOF) break;
    Buffer[tail] = static_cast<char>(v);
    tail = (tail + 1) % bufferSize;
  }
}

bool Reader::isEOF() {
  fillBuffer();
  return head == tail;
}

char Reader::read(bool move) {
  fillBuffer();
  assert((head != tail) || (!move));
  if (head == tail) return 0;
  char v = Buffer[head];
  if (move) {
    if (isEOLN(v)) {
      line++;
      position = 1;
    } else {
      position++;
    }
    head = (head + 1) % bufferSize;
  }
  return v;
}

// ---------------------------- Scanner's methods -----------------------------

Scanner::Scanner(const char* file, Lang _lang): lang(_lang) {
  reader = new Reader(file);
  end = endDefault;
}

Scanner::Scanner(const char* file, void(*endf)(const char* msg, int line, int position), Lang _lang): lang(_lang) {
  reader = new Reader(file);
  end = endf;
}

Scanner::Scanner(FILE* input, Lang _lang): lang(_lang) {
  reader = new Reader(input);
  end = endDefault;
}

Scanner::Scanner(FILE* input, void(*endf)(const char* msg, int line, int position), Lang _lang): lang(_lang) {
  reader = new Reader(input);
  end = endf;
}

Scanner::~Scanner() {
  delete reader;
}

template <typename... Ts>
void Scanner::error(const Ts&... args) {
  std::ostringstream oss;
  (oss << ... << args);
  int l = reader->getLine();
  int p = reader->getPosition();
  delete reader;
  end(oss.str().c_str(), l, p);
}

int Scanner::skipWhitespaces() {
  int result = 0;
  while (isWhitespace(reader->read())) {
    reader->read(1);
    result++;
  }
  return result;
}


int Scanner::skipWhitespacesUntilEOLN() {
  int result = 0;
  while (isWhitespace(reader->read()) && !isEOLN(reader->read())) {
    reader->read(1);
    result++;
  }
  return result;
}


// INTEGERS

int Scanner::readInt(int min_value, int max_value) {
  return (int)readLL(min_value, max_value);
}

uint Scanner::readUInt(uint min_value, uint max_value) {
  return (uint)readULL(min_value, max_value);
}

inline bool lower_equal(ull a, bool sign_a, ull b, bool sign_b) {
  if (sign_a != sign_b) return sign_a;
  if (sign_a) return a >= b;
  return a <= b;
}
inline ull spec_abs(ll x) {
  if (x < 0) return (-(x + 1)) + 1;
  return x;
}

ll Scanner::readLL(ll min_value, ll max_value) {
  assert(min_value <= max_value);
  bool sign;
  ull val;
  readULL(max(spec_abs(min_value), spec_abs(max_value)), val, sign);
  ll v = val;
  if (!(lower_equal(spec_abs(min_value), min_value < 0, v, sign) &&
        lower_equal(v, sign, spec_abs(max_value), max_value < 0)))
    error(msgOutOfRangeInt[lang]);
  if (sign) v *= -1;
  return v;
}

ull Scanner::readULL(ull min_value, ull max_value) {
  assert(min_value <= max_value);
  bool sign;
  ull val;
  readULL(max_value, val, sign);
  if (sign) error(msgOutOfRangeInt[lang]);
  if (!(min_value <= val))
    error(msgOutOfRangeInt[lang]);
  return val;
}

// REAL NUMBERS

float Scanner::readFloat(float min_value, float max_value) {
  return (float)readLDouble(min_value, max_value);
}

double Scanner::readDouble(double min_value, double max_value) {
  return (double)readLDouble(min_value, max_value);
}

long double Scanner::readLDouble(long double min_value, long double max_value) {
  assert(min_value <= max_value);
  bool sign;
  ldb val;
  readLDB(max(fabsl(min_value), fabsl(max_value)), val, sign);
  if (sign) val *= -1;
  if (!(min_value <= val && val <= max_value))
    error(msgOutOfRangeReal[lang]);
  return val;
}

// STRINGS

int Scanner::readString(char* s, int size) {
  int x = 0;
  while ( x < size - 1 && !isEOF() && !isWhitespace(reader->read()))
    s[x++] = reader->read(1);
  s[x]=0;
  return x;
}

int Scanner::readLine(char* s, int size) {
  int x = 0;
  while ( x < size - 1 && !isEOLN(reader->read()) && !isEOF())
    s[x++] = reader->read(1);
  s[x] = 0;
  if (isEOLN(reader->read())) reader->read(1);
  return x;
}

char Scanner::readChar() {
  if (reader->isEOF()) error(msgNoChar[lang]);
  return reader->read(1);
}

// WHITESPACES

void Scanner::readEof() {
  if (!reader->isEOF()) error(msgNotEof[lang]);
}

void Scanner::readEoln() {
  if (!isEOLN(reader->read())) error(msgNotEoln[lang]);
  reader->read(1);
}

void Scanner::readEofOrEoln() {
  if (isEOLN(reader->read())) {
    reader->read(1);
  } else if (!reader->isEOF()) {
    error(msgNotEofOrEoln[lang]);
  }
}


void Scanner::readSpace() {
  if (!isSpace(reader->read())) error(msgNotSpace[lang]);
  reader->read(1);
}

void Scanner::readTab() {
  if (!isTab(reader->read())) error(msgNotTab[lang]);
  reader->read(1);
}

bool Scanner::isEOF() {
  return reader->isEOF();
}


// PROTECTED

void Scanner::readULL(ull limit, ull &val, bool &sign) {
  sign = 0;
  val = 0;
  sign = isMinus(reader->read());
  if (sign) reader->read(1);
  int zeros = 0;
  int valDigits = 0;
  while ('0' == reader->read()) {
    zeros++;
    valDigits++;
    reader->read(1);
    if (zeros > 1) error(msgLeadingZeros[lang]);
  }
  int limDigits = 0;
  ull tmp = limit;
  while (tmp) {
    limDigits++;
    tmp /= 10;
  }
  if (!limDigits) limDigits = 1;
  while (isdigit(reader->read())) {
    valDigits++;
    if (valDigits > limDigits) error(msgOutOfRangeInt[lang]);
    char x = reader->read(1);
    if (valDigits == limDigits) {
      if (limit / 10 < val) error(msgOutOfRangeInt[lang]);
      if (limit / 10 == val && limit % 10 < (ull)(x - '0')) error(msgOutOfRangeInt[lang]);
    }
    val = val * 10 + x - '0';
  }
  if (val > 0 && zeros) error(msgLeadingZeros[lang]);
  if (sign && zeros) error(msgMinusZero[lang]);
  if (!valDigits) error(msgNoNumber[lang]);
}

void Scanner::readLDB(ldb, ldb &val, bool &sign) {
  sign = 0;
  val = 0;
  sign = isMinus(reader->read());
  if (sign) reader->read(1);
  int zeros = 0;
  int valDigits = 0;
  while ('0' == reader->read()) {
    zeros++;
    valDigits++;
    reader->read(1);
    if (zeros > 1) error(msgLeadingZeros[lang]);
  }
  if (zeros && isdigit(reader->read())) error(msgLeadingZeros[lang]);
  while (isdigit(reader->read())) {
    valDigits++;
    char x = reader->read(1);
    val = val * 10.0 + x - '0';
  }
  if (!valDigits) error(msgNoNumber[lang]);
  if (isDot(reader->read())) {
    reader->read(1);
    ldb dec = 1;
    int dotDigits = 0;
    while (isdigit(reader->read())) {
      dotDigits++;
      if (dotDigits > realNumbersLimit) error(msgRealNumberLimit[lang]);
      char x = reader->read(1);
      dec /= 10.0;
      val += dec * (x - '0');
    }
    if (!dotDigits) error(msgBadRealNumberFormat[lang]);
  }
}

}  // namespace oi

#endif  // OI_LIB_OI_H_

----------
```

The first package, which describes the problem "Sumżyce", is a template package, with example components. The second package, which describes the problem titled "Kompleks mniejszości", is a real problem package from a real competitive programing contest. I'll highlight a few important points about the packages:
- Packages have an id, which is usually three letter long, which is contained in the names of some program files, and which is described in the config.yml file.
- The config.yml file contains metadata about the package. You are to fill this with default values of your chosing. You may be instructed to change them later.
- The prog directory contains a few programs. It also contains oi.h, a header file with ulitity functions. You are to use the ulility functions in other generated programs.
- Among the programs in prog is a ingen program, which generates input files for the problem's tests. When creating your ingen, generate many diverse tests. Create a few test classes and about 10 tests from each class. Make sure that these classes accept parameters and make sure that the parameters with which you instantiate the classes satisfy the criteria given in the problem statement.
- prog also contains inwer, which should verify the tests generated by ingen.
- The main solution is in the file <id>.cpp. Try your best to write a solution with a good time complexity.
- There are also brute force solutions. There should be one for every subtask. Their files are named <id>s<subtask index>.cpp. Try your best to write solutions with time complexities that match the subtasks.
- The doc directory contains a spiral.cls file with helper macros.
- doc contains a problem statement named <id>zad.tex. Make sure that the values in the subtask section match those of the config file.
- doc also contains a solution file named <id>sol.tex. Fill it with solutions of all the subtasks, but don't include any code.
- Some files are not included in the serialized packages, because they are not text files. These include doc/licencja.pdf and doc/logo.pdf. You may assume that they exist in the packages and in your package after it will have been unserialized.
- Do not include oi.h and spiral.cls when you output in the serialized format, even when prompted to generate all package files.

Also, here are a few tips based on failures of previous attempts to generate packages:
- When writing c++ code, make sure not to trigger -Wsign-compare or -Wconversion. In general, don't trigger any compiler warnings, because I compile with -Werror.

When asked to generate files, generate these files and only these files in the serialized format. Make sure to embed your output in a fenced code block so that it can be easily copied into a text file and converted to a directory with files. Do not describe what you generated unless asked to do so.
Here is the description of the problem:

"""
        )

        with open('description.txt', 'r', encoding='utf-8') as description_file:
            prompt_file.write(description_file.read())
        
        prompt_file.write(
            "\n\nHow would you solve this problem? Don't generate any code yet, just describe your solution."
        )

        print(f"Prompt created in {prompt_file.name}")

if __name__ == "__main__":
    main("")