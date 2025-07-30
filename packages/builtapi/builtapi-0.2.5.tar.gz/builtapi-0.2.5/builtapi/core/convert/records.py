from typing import Dict, Union

from builtapi.core.schemas.records import RecordCreateResult, RecordCreateResultList, RecordsList, Record


def convert_record_into_dataclass(data: Dict) -> Record:
    current_index = data.get('_id')
    data.pop('_id')
    return Record(id=current_index, data=data.get('data'), meta=data.get('meta'))


def create_record_callback(method):

    def inner(*args, **kwargs) -> RecordCreateResult:
        callback = method(*args, **kwargs)
        return RecordCreateResult(id=callback.get('_id'), result=callback.get('result'))

    return inner


def create_record_callback_list(method):

    def inner(*args, **kwargs) -> RecordCreateResultList:
        callback = method(*args, **kwargs)
        items = [RecordCreateResult(id=i.get('_id'), result=i.get('result')) for i in callback]
        return RecordCreateResultList(items=items)

    return inner


def records_list(method):

    def inner(*args, **kwargs) -> RecordsList:
        record_list = method(*args, **kwargs)
        if record_list.get('items') is None:
            items = []
        else:
            items = [convert_record_into_dataclass(i) for i in record_list.get('items')]
        return RecordsList(take=record_list.get('take'), count=record_list.get('count'),
                           total=record_list.get('total'), items=items)

    return inner


def record(method):

    def inner(*args, **kwargs) -> Union[None, Record]:
        obtained_record = method(*args, **kwargs)
        if obtained_record is None:
            return None
        else:
            return convert_record_into_dataclass(obtained_record)

    return inner
