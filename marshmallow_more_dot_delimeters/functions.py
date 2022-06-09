
# Given the results of marshmallow-sqlalchemy schema query, ensure that only the requested data is returned.
def _respect_more_delimiters(initial_result, fields):
    if initial_result is None:
        return None

    if fields is None:
        return initial_result

    result_transformed = {}
    finished_fields = []

    for field in fields:
        if field in finished_fields:
            continue

        parts = field.split(".")
        d = result_transformed
        r = initial_result

        for count, part in enumerate(parts[:-1]):

            if part not in d and part in r:
                if r[part] is None:
                    d[part] = None
                else:
                    d[part] = [] if isinstance(r[part], list) else {}

            if part in r and not d[part] is None:
                d, r = d[part], r[part]

            else:
                raise Exception(f'The model has no nested object named {part}')

            if isinstance(r, list):
                relevant_fields = [".".join(field.split(".")) for field in fields if field.split(".")[count] == part]
                finished_fields.extend(relevant_fields)
                new_fields = [".".join(field.split(".")[count+1:]) for field in relevant_fields if field.split(".")[count] == part]

                for subpart in r:
                    q = _respect_more_delimiters(subpart, new_fields)
                    d.append(q)
                break

        if parts[-1] in r:
            d[parts[-1]] = r[parts[-1]]

    return result_transformed


def get_results(Schema, model, fields):
    if fields is None or (len(fields) == 1 and fields[0] == ''):
        fields = None

    fieldsCut = None
    if not fields is None:
        # marshmallow_sqlalchemy accepts at most two delimeters
        fieldsCut = [".".join(field.split(".")[:2]) for field in fields]

    try:
        if fieldsCut is None:
            schema = Schema()
        else:
            schema = Schema(only=fieldsCut)

    except:
        return {
            "results": None,
            "errors": [{
                "code": 2,
                "message": "Fields are incorrect"
            }]}

    try:
        res = _respect_more_delimiters(schema.dump(model), fields)
    except:
        return {
            "results": None,
            "errors": [{
                "code": 2,
                "message": "Fields are incorrect"
            }]}

    return {"results": res}


def get_results_from_custom_schema(schema, model, fields):
    return {"results": _respect_more_delimiters(schema.dump(model), fields)}
