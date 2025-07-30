from ..core import ApplyOp, BrokerJobStatus, OutputOp, SourceOp
from ..core.entry import Entry
from ..lib.utils import _to_list_2, hash_text, hash_texts, hash_json, FieldsRouter
from ..lib.markdown_utils import iter_markdown_lines, iter_markdown_entries, write_markdown

from typing import Union, List, Dict, Any, Literal, Iterator, Tuple
import re
import jsonlines,json
from glob import glob
import itertools as itt
from abc import abstractmethod, ABC
from copy import deepcopy
import os
from dataclasses import asdict
from copy import deepcopy


class ReaderOp(SourceOp, ABC):
    def __init__(self,
                    fields: List[str],
                    offset: int = 0,
                    max_count: int = None,
                    fire_once: bool = True
                    ):
        super().__init__(fire_once=fire_once)
        self.fields = fields
        self.offset = offset
        self.max_count = max_count
    @abstractmethod
    def _iter_records(self) -> Iterator[Tuple[str,Dict]]:
        """Abstract method to iterate over records in the data source."""
        pass
    def generate_batch(self)-> Dict[str,Entry]:
        stop = self.offset + self.max_count if self.max_count is not None else None
        entries = {}
        for idx,json_obj in itt.islice(self._iter_records(), self.offset, stop):
            entry = Entry(idx=idx)
            for field in self.fields:
                entry.data[field] = json_obj.get(field, None)
            entries[idx] = entry
        return entries

class ReadJson(ReaderOp):
    def __init__(self, 
                 glob_str: str, 
                 fields: List[str],
                 idx_field: str = None,
                 hash_fields: Union[str, List[str]] = None,
                 offset: int = 0,
                 max_count: int = None,
                 fire_once: bool = True
                 ):
        super().__init__(fields=fields, offset=offset, max_count=max_count, fire_once=fire_once)
        if not idx_field and not hash_fields:
            raise ValueError("At least one of idx_field or hash_fields must be provided.")
        self.glob_str = glob_str
        self.idx_field = idx_field
        self.hash_fields = FieldsRouter(hash_fields,style="tuple") if hash_fields is not None else None
    def _iter_records(self) -> Iterator[Tuple[str,Dict]]:
        for path in sorted(glob(self.glob_str)):
            if path.endswith('.jsonl'):
                with jsonlines.open(path) as reader:
                    for record in reader:
                        idx = self._generate_idx(record)#, self.idx_field, self.hash_fields)
                        yield idx, record
            elif path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    if isinstance(records, dict):
                        records = [records]  # Ensure data is a list of dicts
                    for record in records:
                        idx = self._generate_idx(record)#, self.idx_field, self.hash_fields)
                        yield idx, record
    def generate_idx_from_json(self, json_obj) -> str:
        """Generate an index for the entry based on idx_field and/or hash_fields."""
        idx = ""
        if self.index_field is not None:
            idx = json_obj.get(self.index_field, "")
        if self.hash_fields is not None:
            if idx:
                idx += "_"
            idx += hash_json({k:json_obj.get(k,"") for k in self.hash_fields.froms})
        return idx

def generate_directory_str(directory: List[str]) -> str:
    directory = [d.strip().replace(" ", "_").replace("/", "_") for d in directory]
    return "/".join(directory)

def generate_idx_from_directory_keyword(directory: List[str], keyword: str)-> str:
    directory = [d.strip().replace(" ", "_").replace("/", "_") for d in directory]
    keyword = keyword.strip().replace(" ", "_").replace("/", "_")
    return hash_text("/".join(directory) + "/" + keyword)

def remove_markdown_headings(text: str) -> str:
    text= re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    return text

class ReadMarkdown(ReaderOp):
    def __init__(self, 
                    glob_str: str,
                    keyword_field = "keyword",
                    context_field = "context",
                    directory_field = "directory",
                    offset: int = 0,
                    max_count: int = None,
                    fire_once: bool = True,
                    directory_mode: Literal['list', 'str'] = 'list',
                    format: Literal['lines', 'entries'] = 'entries',
                    ):
        if format == 'lines': context_field = None
        fields = [keyword_field, context_field, directory_field]
        fields = [f for f in fields if f]
        super().__init__(fields=fields, offset=offset, max_count=max_count, fire_once=fire_once)
        self.glob_str = glob_str
        self.keyword_field = keyword_field
        self.context_field = context_field
        self.directory_field = directory_field
        self.directory_mode = directory_mode
        self.format = format
    def _iter_records(self) -> Iterator[Dict[str, Any]]:
        factory = {"lines": iter_markdown_lines, "entries": iter_markdown_entries}[self.format]
        for path in sorted(glob(self.glob_str)):
            for directory, keyword, context in factory(path):
                idx = generate_idx_from_directory_keyword(directory, keyword)
                record = {self.keyword_field: keyword}
                if self.context_field and self.format == "entries":
                    record[self.context_field] = context
                if self.directory_field:
                    if self.directory_mode == 'list':
                        record[self.directory_field] = directory
                    elif self.directory_mode == 'str':
                        record[self.directory_field] = generate_directory_str(directory)
                yield idx, record

class ReadTxtFolder(ReaderOp):
    def __init__(self, 
                glob_str: str,
                text_field: str = "text",
                filename_field = "filename",
                    offset: int = 0,
                    max_count: int = None,
                    fire_once: bool = True,
    ):
        fields = [filename_field, "text"]
        super().__init__(fields=[f for f in fields if f], offset=offset, max_count=max_count, fire_once=fire_once)
        self.filename_field = filename_field
        self.glob_str = glob_str
        self.text_field = text_field
    def _iter_records(self) -> Iterator[Tuple[str, Dict]]:
        for path in sorted(glob(self.glob_str)):
            if not path.endswith('.txt'):
                continue
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            idx = hash_text(path)
            record = {self.text_field: text}
            if self.filename_field:
                record[self.filename_field] = os.path.basename(path)
            yield idx, record




class ReadMarkdownLines(ReadMarkdown):
    def __init__(self,*args, **kwargs):
        kwargs['format'] = 'lines'
        super().__init__(*args, **kwargs)
class ReadMarkdownEntries(ReadMarkdown):
    def __init__(self,*args, **kwargs):
        kwargs['format'] = 'entries'
        super().__init__(*args, **kwargs)

class WriteMarkdownEntries(OutputOp):
    def __init__(self, path: str, 
                 context_field: str = "text",
                 keyword_field: str = "keyword",
                 directory_field: str = "directory"):
        super().__init__()
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.directory_field = directory_field
        self.keyword_field = keyword_field
        self.context_field = context_field
    def output_batch(self, entries: Dict[str, Entry]) -> None:
        tuples = []
        # if os.path.exists(self.path):
        #     tuples.extend(iter_markdown_entries(self.path))
        for entry in entries.values():
            directory = entry.data.get("directory", [])
            if isinstance(directory, str):
                directory = directory.split("/")
            keyword = entry.data.get(self.keyword_field, "")
            context = entry.data.get(self.context_field, "")
            context = remove_markdown_headings(context)
            tuples.append((directory, keyword, context))
        write_markdown(tuples, self.path)
        print(f"Output {len(entries)} entries to {os.path.abspath(self.path)}")


class FromList(SourceOp):
    def __init__(self,
                 input_list: List[Dict],
                 fire_once: bool = True,
                 output_field: str = None,
                 ):
        super().__init__(fire_once=fire_once)
        self.input_list = input_list
        self.output_field = output_field
    def generate_batch(self) -> Dict[str, Entry]:
        entries = {}
        for obj in self.input_list:
            entry = self._make_entry(obj)
            entries[entry.idx] = entry
        return entries
    def _make_entry(self,obj):
        if isinstance(obj, Entry):
            return obj
        elif isinstance(obj, dict):
            if all(k in obj for k in ["idx", "data"]):
                return Entry(idx=obj["idx"], data=obj["data"])
            else:
                if "idx" in obj:
                    return Entry(idx=obj["idx"], data=deepcopy(obj))
                else:
                    return Entry(idx=hash_json(obj), data=deepcopy(obj))
        elif isinstance(obj, (int, float, str, bool)) and self.output_field is not None:
            return Entry(idx=hash_text(str(obj)), data={self.output_field: obj})
        else:
            raise ValueError(f"Unsupported object type for entry creation: {type(obj)}")


class ToList(OutputOp):
    def __init__(self):
        super().__init__()
        self._output_entries = {}
    def output_batch(self, entries: Dict[str, Entry]) -> None:
        for idx, entry in entries.items():
            if idx in self._output_entries:
                if entry.rev < self._output_entries[idx].rev:
                    continue
            self._output_entries[idx] = entry
    def get_output(self) -> List[Entry]:
        return list(self._output_entries.values())

class PrintEntry(OutputOp):
    def __init__(self,first_n=None):
        super().__init__()
        self.first_n = first_n
    def output_batch(self, entries: Dict[str, Entry]) -> None:
        if not entries: return
        for entry in list(entries.values())[:self.first_n]:
            print("idx:", entry.idx, "rev:", entry.rev)
            print(entry.data)
            print()
        print()

class PrintField(OutputOp):
    def __init__(self, field="text", first_n=5):
        super().__init__()
        self.field = field
        self.first_n = first_n
    def output_batch(self,entries:Dict[str,Entry])->None:
        if not entries: return
        for entry in list(entries.values())[:self.first_n]:
            print(f"Index: {entry.idx}, Revision: {entry.rev}")
            print(entry.data.get(self.field, None))
            print()
        print()

class WriteJsonl(OutputOp):
    def __init__(self, path: str, 
                 output_fields: str|List[str]=None,
                 only_current:bool=False):
        """if only_current, will ignore old entries in the output file that are not appearing in the current batch,
        otherwise will update on old entries based on idx and rev if output file already exists.
        will only output entry.data, but flattened idx and rev into entry.data
        """
        super().__init__()
        self.path = path
        self.only_current = only_current
        self.output_fields = _to_list_2(output_fields) if output_fields else None
        self._output_entries = {}
    def output_batch(self,entries:Dict[str,Entry])->None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._output_entries.clear()
        if (not self.only_current) and os.path.exists(self.path):
            with jsonlines.open(self.path, 'r') as reader:
                for record in reader:
                    entry = Entry(
                        idx=record['idx'],
                        rev=record.get('rev', 0),
                        data=record
                    )
                    self._update(entry)
        for entry in entries.values():
            self._update(entry)
        with jsonlines.open(self.path, 'w') as writer:
            for entry in self._output_entries.values():
                record = self._prepare_output(entry)
                writer.write(record)
        print(f"Output {len(self._output_entries)} entries to {os.path.abspath(self.path)}")
        self._output_entries.clear()
    def _prepare_output(self,entry:Entry):
        if not self.output_fields:
            record = deepcopy(entry.data)
        else:
            record = {k: entry.data[k] for k in self.output_fields}
        record['idx'] = entry.idx
        record['rev'] = entry.rev
        return record
    def _update(self,new_entry):
        if new_entry.idx in self._output_entries and new_entry.rev < self._output_entries[new_entry.idx].rev:
                print("failed")
                return
        self._output_entries[new_entry.idx] = new_entry

__all__ = [
    "ToList",
    "PrintEntry",
    "PrintField",
    "WriteJsonl",
    "ReaderOp",
    "ReadJson",
    "ReadTxtFolder",
    "ReadMarkdownLines",
    "ReadMarkdownEntries",
    "WriteMarkdownEntries",
    "FromList",
]