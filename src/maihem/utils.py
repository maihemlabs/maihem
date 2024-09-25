import os
import pymupdf
import docx2txt

from typing import List, Iterable, Optional
import re


def extract_text(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return extract_pdf_text(file_path)
    elif file_extension == ".docx":
        return extract_docx_text(file_path)
    elif file_extension in [".txt", ".md"]:
        return extract_text_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def extract_pdf_text(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_docx_text(file_path):
    text = docx2txt.process(file_path)
    return text


def extract_text_file(file_path):
    doc = pymupdf.open(file_path, filetype="txt")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


class TextSplitter:
    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        separators: List[str] = ["\n\n", "\n", " ", ""],
    ):
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._separators = separators
        self._is_separator_regex = False
        self._keep_separator = False
        self._length_function = len

    def split_text(self, text: str) -> List[str]:
        return self._split_text(text, self._separators)

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to use
        separator = separators[-1]
        new_separators = []
        for i, _s in enumerate(separators):
            _separator = _s if self._is_separator_regex else re.escape(_s)
            if _s == "":
                separator = _s
                break
            if re.search(_separator, text):
                separator = _s
                new_separators = separators[i + 1 :]
                break

        _separator = separator if self._is_separator_regex else re.escape(separator)
        splits = self._split_text_with_regex(text, _separator, self._keep_separator)

        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        _separator = "" if self._keep_separator else separator
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, _separator)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_info = self._split_text(s, new_separators)
                    final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, _separator)
            final_chunks.extend(merged_text)
        return final_chunks

    @staticmethod
    def _split_text_with_regex(
        text: str, separator: str, keep_separator: bool
    ) -> List[str]:
        if separator:
            if keep_separator:
                splits = re.split(f"({separator})", text)
                return [
                    splits[i] + splits[i + 1] for i in range(0, len(splits) - 1, 2)
                ] + ([splits[-1]] if len(splits) % 2 == 1 else [])
            else:
                return re.split(separator, text)
        else:
            return list(text)

    def _merge_splits(self, splits: Iterable[str], separator: str) -> List[str]:

        separator_len = self._length_function(separator)

        docs = []
        current_doc: List[str] = []
        total = 0
        for d in splits:
            _len = self._length_function(d)
            if (
                total + _len + (separator_len if len(current_doc) > 0 else 0)
                > self._chunk_size
            ):
                if total > self._chunk_size:
                    logger.warning(
                        f"Created a chunk of size {total}, "
                        f"which is longer than the specified {self._chunk_size}"
                    )
                if len(current_doc) > 0:
                    doc = self._join_docs(current_doc, separator)
                    if doc is not None:
                        docs.append(doc)

                    while total > self._chunk_overlap or (
                        total + _len + (separator_len if len(current_doc) > 0 else 0)
                        > self._chunk_size
                        and total > 0
                    ):
                        total -= self._length_function(current_doc[0]) + (
                            separator_len if len(current_doc) > 1 else 0
                        )
                        current_doc = current_doc[1:]
            current_doc.append(d)
            total += _len + (separator_len if len(current_doc) > 1 else 0)
        doc = self._join_docs(current_doc, separator)
        if doc is not None:
            docs.append(doc)
        return docs

    def _join_docs(self, docs: List[str], separator: str) -> Optional[str]:
        text = separator.join(docs)
        text = text.strip()
        if text == "":
            return None
        return text
