def format_parties_response(data, total, limit, offset):
    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset
    }