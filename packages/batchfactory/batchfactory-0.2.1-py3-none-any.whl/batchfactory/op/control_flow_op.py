from ..core.op_base import *
from ..core.entry import Entry
from ..lib.utils import FieldsRouter, hash_json


from typing import List, Tuple, Dict, Callable, TYPE_CHECKING
from copy import deepcopy
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..core.op_graph_segment import OpGraphSegment

class Replicate(SplitOp):
    "Replicate an entry to all out_ports, with optionally `replica_idx_field` field set to the out_port index."
    def __init__(self, n_out_ports:int = 2, replica_idx_field:str|None="replica_idx"):
        super().__init__(n_out_ports=n_out_ports)
        self.replica_idx_field = replica_idx_field
    def split(self, entry: Entry) -> Dict[int, Entry]:
        output_entries = {}
        for i in range(self.n_out_ports):
            new_entry = deepcopy(entry)
            if self.replica_idx_field:
                new_entry.data[self.replica_idx_field] = i
            output_entries[i] = new_entry
        return output_entries
    
class Collect(MergeOp):
    "Collect data from in_port 1"
    def __init__(self, *fields):
        """
        - collects data from in_port 1
        - `Collect('field1', 'field2')` 
        """
        super().__init__(n_in_ports=2, wait_all=True)
        self.field_mappings = FieldsRouter(*fields, style="tuple")
    def merge(self, entries: Dict[int, Entry]) -> Entry:
        for field in self.field_mappings.froms:
            if field in entries[1].data:
                entries[0].data[field] = entries[1].data[field]
        return entries[0]


class BeginIfOp(SplitOp,ABC):
    "Switch to port 1 if criteria is met"
    def __init__(self):
        super().__init__(n_out_ports=2)
    def split(self, entry: Entry) -> Dict[int, Entry]:
        if self.criteria(entry):
            return {1: entry}
        else:
            return {0: entry}
    @abstractmethod
    def criteria(self, entry: Entry) -> bool:
        "if true, switch to port 1"
        pass

class BeginIf(BeginIfOp):
    """
    - `BeginIf(lambda data: data['condition'])`
    - `BeginIf(lambda x, y: x > y, 'x', 'y')`
    """
    def __init__(self,criteria:Callable,*fields):
        super().__init__()
        self._criteria = criteria
        self.router = FieldsRouter(*fields, style="tuple") if fields else None
    def criteria(self, entry: Entry) -> bool:
        if self.router:
            return self._criteria(*self.router.read_tuple(entry.data))
        else:
            return self._criteria(entry.data)
    
class EndIf(MergeOp):
    "Take entry from either branch of if"
    def __init__(self):
        super().__init__(n_in_ports=2, wait_all=False)
    def merge(self, entries: Dict[int, Entry]) -> Entry:
        if len(entries)>1:
            raise ValueError("Entries with same idx comes from both branch of If")
        entry = next(iter(entries.values()))
        # should not increase rev here
        return entry
    
def If(criteria:Callable, true_chain:'OpGraphSegment|BaseOp|None', false_chain=None) -> 'OpGraphSegment':
    """
    - `If(lambda data: data['condition'], true_chain, false_chain)`
    """
    begin = BeginIf(criteria)
    end = EndIf()
    if false_chain is not None: 
        main_chain = begin | false_chain | end
    else:
        main_chain = begin | end
    if true_chain is not None:
        true_chain = true_chain.to_segment()
        main_chain.wire(begin, true_chain, 1, 0)
        main_chain.wire(true_chain, end, 0, 1)
    else:
        main_chain.wire(begin, end, 1, 1)
    return main_chain

class LoopOp(RouterOp,ABC):
    """
    - please connect loop body from out_port 1 to in_port 1
    - choose the entry with higher rev. if rev is equal, choose from in_port 1
    - then increase rev by 1, and call corresponding methods (see code for detail of execution order)
    - then route the entry to out_port 0 (exit loop) or out_port 1 (continue loop) based on `criteria`
    """
    def __init__(self):
        super().__init__(n_in_ports=2, n_out_ports=2, wait_all=False)

    def route(self, bundle: Dict[int, Entry]) -> Dict[int, Entry]:
        in_port, entry = self._pick(bundle)

        if in_port == 0: self.initialize(entry)
        if in_port == 1: self.post_increment(entry)
        if in_port == 1: entry.rev += 1
        out_port = 1 if self.criteria(entry) else 0
        if out_port == 0: self.finalize(entry)
        elif out_port == 1: self.pre_increment(entry)

        return {out_port: entry}

    def _pick(self, bundle)-> Tuple[int, Entry]:
        entry0, entry1 = bundle.get(0), bundle.get(1)
        if entry1 is not None:
            if entry0 is None or entry1.rev >= entry0.rev: # we haven't increase entry1.rev yet. so entry1 have priority
                return 1, entry1
        if entry0 is not None:
            return 0, entry0
        raise ValueError("Should not pass an empty bundle to an RouterOp")

    @abstractmethod
    def criteria(self, entry: Entry) -> bool:
        "if true, route to loop branch (out_port 1)\nDo not touch rev here"
        pass
    def initialize(self, entry: Entry) -> None:
        "initialize the entry when it enters the loop entrance (coming from in_port 0)\nDo not touch rev here"
        pass
    def pre_increment(self, entry: Entry) -> None:
        "updates the entry each time it enters the loop body (exiting towards out_port 1)\nDo not touch rev here"
        pass
    def post_increment(self, entry: Entry) -> None:
        "updates the entry each time it leaves the loop body (coming from in_port 1)\nDo not touch rev here"
        pass
    def finalize(self, entry: Entry) -> None:
        "updates the entry when it exits the loop (exiting towards out_port 0)\nDo not touch rev here"
        pass

class WhileNode(LoopOp):
    "Please see `While` function for usage."
    def __init__(self, criteria, *criteria_fields):
        super().__init__()
        self._criteria = criteria
        self.criteria_router = FieldsRouter(*criteria_fields, style="tuple") if criteria_fields else None
    def criteria(self, entry: Entry) -> bool:
        if self.criteria_router:
            return self._criteria(*self.criteria_router.read_tuple(entry.data))
        else:
            return self._criteria(entry.data)
        
def While(criteria:Callable, body_chain:'OpGraphSegment|BaseOp') -> 'OpGraphSegment':
    """
    - `While(lambda data: data['condition'], loop_body)`
    """
    loop_nome = WhileNode(criteria)
    main_chain = loop_nome.to_segment()
    body_chain = body_chain.to_segment()
    main_chain.wire(loop_nome, body_chain, 1, 0)
    main_chain.wire(body_chain, loop_nome, 0, 1)
    return main_chain

class RepeatNode(LoopOp):
    "See `Repeat` function for usage."
    def __init__(self, max_rounds=None, rounds_field="rounds", max_rounds_field=None, initial_value:int|None=0):
        super().__init__()
        self.rounds_field = rounds_field
        self.initial_value:int|None = initial_value
        self.max_rounds = max_rounds
        self.max_rounds_field = max_rounds_field
        if max_rounds is None and max_rounds_field is None:
            raise ValueError("Either max_rounds or max_rounds_field must be provided.")
    def initialize(self, entry: Entry) -> None:
        if self.initial_value is not None:
            entry.data[self.rounds_field] = self.initial_value
        else:
            if self.rounds_field not in entry.data:
                raise ValueError(f"Entry does not have field '{self.rounds_field}' to initialize the loop count.")
    def criteria(self, entry: Entry) -> bool:
        max_rounds = _get_field_or_value(entry.data, self.max_rounds_field, self.max_rounds)
        finished_rounds = entry.data[self.rounds_field]
        return finished_rounds < max_rounds
    def pre_increment(self, entry: Entry) -> None:
        # note we use pre_increment instead of post_increment here
        entry.data[self.rounds_field] += 1


def Repeat(body_chain:'OpGraphSegment|BaseOp', 
           max_rounds=None, rounds_field="rounds", max_rounds_field=None, initial_value:int|None=0):
    """
    - `Repeat(loop_body,5,"rounds")`
    - `Repeat(loop_body,max_rounds_field='max_rounds')`
    - Note the subtle difference compared to `for` clause in c language:
        - **rounds represents how many times it enters the loop body**
        - for example, `Repeat(loop_body,5)` results in `rounds` being 1,2,3,4,5 in loop body, and 5 after exiting the loop
    - If `initial_value` is set to None, it will fetch the initial value from `rounds_field`
    """
    node = RepeatNode(max_rounds=max_rounds, rounds_field=rounds_field, 
                      max_rounds_field=max_rounds_field, initial_value=initial_value)
    main_chain = node.to_segment()
    body_chain = body_chain.to_segment()
    main_chain.wire(node, body_chain, 1, 0)
    main_chain.wire(body_chain, node, 0, 1)
    return main_chain


def _broadcast_lists(lists):
    lists = list(lists)
    max_len = max(len(lst) for lst in lists if isinstance(lst, (list, tuple)))
    for i in range(len(lists)):
        if not isinstance(lists[i], (list, tuple)):
            lists[i] = [lists[i]] * max_len
    return lists


def _explode_entry_by_lists(entry: Entry, router: FieldsRouter,
                     master_idx_field: str | None = None,
                     list_idx_field: str | None = None) -> Dict[str, Entry]:
    """Explode an entry to multiple entries based on the router."""
    output_entries = {}
    for list_idx, items in enumerate(zip(*_broadcast_lists(router.read_tuple(entry.data)))):
        new_data = {t: i for t, i in zip(router.tos, items)}
        if master_idx_field is not None:
            new_data[master_idx_field] = entry.idx
        if list_idx_field is not None:
            new_data[list_idx_field] = list_idx
        spawn_idx = hash_json(new_data)
        spawn_entry = Entry(idx=spawn_idx, data=new_data)
        output_entries[spawn_idx] = spawn_entry
    return output_entries


class ExplodeList(BatchOp):
    "Explode a list to multiple entries, each with a single item from the list."
    def __init__(self, in_list_fields="list", out_item_fields="item",
                 master_idx_field="master_idx", list_idx_field="list_idx"):
        super().__init__(consume_all_batch=True)
        self.router = FieldsRouter(in_list_fields, out_item_fields, style="map")
        self.master_idx_field = master_idx_field
        self.list_idx_field = list_idx_field
    def update_batch(self, batch: Dict[str, Entry]) -> Dict[str, Entry]:
        output_entries = {}
        for entry in batch.values():
            output_entries.update(_explode_entry_by_lists(entry, self.router,
                                                 master_idx_field=self.master_idx_field,
                                                 list_idx_field=self.list_idx_field))
        return output_entries


class SpawnFromList(SpawnOp):
    "Explode a list to multiple entries to port 1, each with a single item from the list."
    def __init__(self,
                 in_list_fields="list",
                 out_item_fields="item",
                 master_idx_field="master_idx",
                 list_idx_field="list_idx",
                 spawn_idx_list_field="spawn_idx_list",
    ):
        super().__init__()
        self.router = FieldsRouter(in_list_fields, out_item_fields, style="map")
        self.master_idx_field = master_idx_field
        self.list_idx_field = list_idx_field
        self.spawn_idx_list_field = spawn_idx_list_field
    def spawn_entries(self, entry: Entry) -> Dict[str, Entry]:
        """Entry->{new_idx:new_Entry}"""
        output_entries = _explode_entry_by_lists(entry, self.router,
                                         master_idx_field=self.master_idx_field,
                                         list_idx_field=self.list_idx_field)
        if self.spawn_idx_list_field is not None:
            entry.data[self.spawn_idx_list_field] = list(output_entries.keys())
        return output_entries
            
class CollectAllToList(CollectAllOp):
    "Concentrate items from multiple entries into a list."
    def __init__(self, 
                in_item_fields="item",
                out_list_fields="list",
                master_idx_field="master_idx",
                list_idx_field="list_idx",
                spawn_idx_list_field="spawn_idx_list",
    ):
        super().__init__()
        self.router = FieldsRouter(in_item_fields, out_list_fields, style="map")
        self.master_idx_field = master_idx_field
        self.list_idx_field = list_idx_field
        self.spawn_idx_list_field = spawn_idx_list_field
    def get_master_idx(self, spawn: Entry)->str|None:
        return spawn.data[self.master_idx_field]
    def is_ready(self,master_entry: Entry, spawn_bundle:Dict[str,Entry]) -> bool:
        for spawn_idx in master_entry.data[self.spawn_idx_list_field]:
            if spawn_idx not in spawn_bundle:
                return False
        return True
    def update_master(self, master_entry: Entry, spawn_bundle: Dict[str, Entry])->None:
        zipped_output_lists = []
        for spawn_idx in master_entry.data[self.spawn_idx_list_field]:
            zipped_output_lists.append(self.router.read_tuple(spawn_bundle[spawn_idx].data))
        for t,lst in zip(self.router.tos, zip(*zipped_output_lists)):
            master_entry.data[t] = list(lst)

        
def ListParallel(spawn_body:'OpGraphSegment|BaseOp',
        in_list_fields="list",
        out_item_fields="item",
        in_item_fields=None,
        out_list_fields=None,
        master_idx_field="master_idx",
        list_idx_field="list_idx",
        spawn_idx_list_field="spawn_idx_list",
        master_body:'OpGraphSegment|BaseOp|None'=None,
    ):
    Begin = SpawnFromList(
        in_list_fields=in_list_fields,
        out_item_fields=out_item_fields,
        master_idx_field=master_idx_field,
        list_idx_field=list_idx_field,
        spawn_idx_list_field=spawn_idx_list_field
    )
    End = CollectAllToList(
        in_item_fields=in_item_fields or out_item_fields,
        out_list_fields=out_list_fields or in_list_fields,
        master_idx_field=master_idx_field,
        list_idx_field=list_idx_field,
        spawn_idx_list_field=spawn_idx_list_field
    )
    if master_body is not None:
        main_chain = Begin | master_body | End
    else:
        main_chain = Begin | End
    spawn_body = spawn_body.to_segment()
    main_chain.wire(Begin, spawn_body, 1, 0)
    main_chain.wire(spawn_body, End, 0, 1)
    return main_chain

          





def _get_field_or_value(data,field,value):
    return value if field is None else data[field]

__all__ = [
    "Replicate",
    "Collect",
    "BeginIf",
    "EndIf",
    "If",
    "LoopOp",
    "WhileNode",
    "While",
    "RepeatNode",
    "Repeat",
    "ExplodeList",
    "SpawnFromList",
    "CollectAllToList",
    "ListParallel",
]
