import argparse
import os

class Query(object):
    """docstring for Query"""
    def __init__(self, data):
        super(Query, self).__init__()
        self._query_prefix = 'q'
        self._query = self._parse(data)

    def get_data(self):
        constructed_page = self._query_prefix + " " + ' '.join(self._query)
        return constructed_page

    def _parse(self, data):
        data = data.lower()
        query_split = [i.strip() for i in data.split(' ')]
        if len(query_split) < 2:
            raise Exception('query data format error')

        if query_split[0].lower() != self._query_prefix:
            raise Exception('Invalid data')

        return query_split[1:]

    def get_keywords(self):
        return self._query

class Page(object):
    """docstring for Page"""
    def __init__(self, data):
        super(Page, self).__init__()
        self._page_prefix = 'p'
        self._page = self._parse(data)

    def get_raw_data(self):
        constructed_page = self._page_prefix + " " + ' '.join(self._page)
        return constructed_page

    def _parse(self, data):
        data = data.lower()
        page_split = [i.strip() for i in data.split(' ')]
        if len(page_split) < 2:
            raise Exception('page data format error')

        if page_split[0].lower() != self._page_prefix:
            raise Exception('Invalid data')

        return page_split[1:]

    def get_content(self):
        return self._page
    
        
class SearchEngine(object):
    def __init__(self):
        super(SearchEngine, self).__init__()
        self._n = 8
        self._pages = []
        self._index = {}
        
    def add_page(self, page):
        self._add_to_pages_with_rank(page)
        self._create_index(page)

    def _add_to_pages_with_rank(self, page):
        # Add keyword ranks into pages
        content = page.get_content()
        content_dict = {}
        content_length = len(content)
        for i in range(len(content)):
            key = content[i].strip()
            content_dict[key] = self._n - i
        self._pages.append(content_dict)

    def _create_index(self, page):
        # Create index of keywords
        for keyword in page.get_content():
            if keyword not in self._index.keys():
                self._index[keyword] = []
            self._index[keyword].append(len(self._pages)-1)

    def search(self, query):
        pages = self._get_pages_containing_query_keywords(query)
        ranked_pages = []
        for p in pages:
            page = self._get_page(p)
            ranked_pages.append({'rank': self._get_ranking(query, page), 'page': p})
        sorted_ranked_pages = [i['page'] for i in self._get_sorted_ranked_pages(ranked_pages)]
        return self._get_result_formatted_string(sorted_ranked_pages)

    def _get_result_formatted_string(self, sorted_ranked_pages):
        result_string = ''
        for i in sorted_ranked_pages:
            result_string += "P%s " % (i+1)
        return result_string.strip()
        
    def _get_sorted_ranked_pages(self, ranked_pages):
        return sorted(ranked_pages, key=lambda x: x['rank'], reverse=True)

    def _get_pages_containing_query_keywords(self, query):
        keywords = query.get_keywords()
        pages = []
        for keyword in keywords:
            pages += self._index.get(keyword, [])
        return list(set(pages))

    def _get_page(self, index):
        if index >= len(self._pages):
            return None
        return self._pages[index]
        
    def _get_ranking(self, query, page):
        keywords = query.get_keywords()
        page_rank = 0
        for i in range(len(keywords)):
            if keywords[i] in page:
                page_rank += (self._n - i) * page[keywords[i]]
        return page_rank

def main(args):
    se = SearchEngine()
    question_count = 0
    with open(args['file']) as f:
        for line in f:
            if line.lower()[:1] == 'p':
                page = Page(line)
                se.add_page(page)

            elif line.lower()[:1] == 'q':
                query = Query(line)
                result = se.search(query)
                print('Q' + str(question_count+1) + ": " + result)
                question_count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help="File path to read quotes from.",
        default=os.path.join(os.path.abspath(os.path.dirname(".")), "data.txt")
    )
    args = vars(parser.parse_args())
    main(args)