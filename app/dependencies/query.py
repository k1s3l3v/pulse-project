from fastapi import Query


def get_trimmed_query(name: str, *args, type_: type = str, **kwargs):
    kwargs['alias'] = kwargs.get('alias', name)

    def query(q: type_ = Query(*args, **kwargs)) -> type_:
        return type_(q.strip()) if q is not None else None

    return query
