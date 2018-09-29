import unittest
import se

class TestPageObject(unittest.TestCase):
    
    def test_get_raw_data(self):
        page_data = "P Ford Car Review"
        page = se.Page(page_data)
        self.assertEqual(page.get_raw_data(), page_data.lower(), 'output data not equal to input data')

    def test_invalid_data_exception(self):
        page_data = "asdad asdad asd asd"
        with self.assertRaises(Exception) as e:
            se.Page(page_data)
        self.assertTrue('Invalid data' in str(e.exception))

    def test_data_format_exception(self):
        page_data = "P"
        with self.assertRaises(Exception) as e:
            se.Page(page_data)
        self.assertTrue('format error' in str(e.exception))


class TestQueryObject(unittest.TestCase):
    
    def test_get_data(self):
        query_data = "Q Ford Review"
        query = se.Query(query_data)
        self.assertEqual(query.get_data(), query_data.lower(), 'output data not equal to input data')
    
    def test_invalid_data_exception(self):
        query_data = "asdad asdad asd asd"
        with self.assertRaises(Exception) as e:
            se.Query(query_data)
        self.assertTrue('Invalid data' in str(e.exception))

    def test_data_format_exception(self):
        query_data = "Q"
        with self.assertRaises(Exception) as e:
            se.Query(query_data)
        self.assertTrue('format error' in str(e.exception))
        

class TestSearchEngineObject(unittest.TestCase):
    
    def test_instantiate_object(self):
        engine = se.SearchEngine()
        self.assertIsInstance(engine, se.SearchEngine)

    def test_add_page(self):
        page_data = "P Ford Car Review"
        page = se.Page(page_data)
        engine = se.SearchEngine()
        self.assertIsNone(engine.add_page(page))

    def test_search(self):
        engine = se.SearchEngine()
        engine.add_page(se.Page("P Ford Car Review"))
        engine.add_page(se.Page("P Review Car"))
        engine.add_page(se.Page("P Review Ford"))
        engine.add_page(se.Page("P Toyota Car"))
        engine.add_page(se.Page("P Honda Car"))
        engine.add_page(se.Page("P Car"))
        result = engine.search(se.Query("Q Ford"))
        self.assertEqual(result, "P1 P3")



        


if __name__ == '__main__':
    unittest.main()
