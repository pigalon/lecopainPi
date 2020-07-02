from flask import abort

class Pagination:
    
    @staticmethod
    def get_paginated_db(results, url, page, per_page, prev_page, next_page):
        page = int(page)
        per_page = int(per_page)
        count = len(results)
        
        obj = {}
        obj['page'] = page
        obj['per_page'] = per_page
        obj['count'] = count
                
        
        if page < 1 or per_page < 0:
            obj['results'] = []
            return obj
        # make response
        
        # make URLs
        # make previous url
        if prev_page is None:
            obj['previous'] = ''
        else:
            #start_copy = max(1, start - limit)
            obj['previous'] = url + '?page=%d&per_page=%d' % (prev_page, per_page)
        # make next url
        if next_page is None:
            obj['next'] = ''
        else:
            obj['next'] = url + '?page=%d&per_page=%d' % (next_page, per_page)
        # finally extract result according to bounds
        obj['results'] = results[0:per_page]
        return obj

    @staticmethod
    def get_paginated_list(results, url, start, limit):
        start = int(start)
        limit = int(limit)
        count = len(results)
        
        obj = {}
        obj['start'] = start
        obj['limit'] = limit
        obj['count'] = count
                
        
        if count < start or limit < 0:
            obj['results'] = []
            return obj
        # make response
        
        # make URLs
        # make previous url
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # make next url
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        # finally extract result according to bounds
        obj['results'] = results[(start - 1):(start - 1 + limit)]
        return obj