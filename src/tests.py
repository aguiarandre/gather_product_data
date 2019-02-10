from Kabum import KabumProduct
import pandas
import logging


logging.basicConfig(filename='logger.tests',
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s : %(levelname)s - %(module)s - %(funcName)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")

# suite of tests:
class SuiteOfTests():
    
    
    def run_tests(self):
        '''
        This should be changed to :
        
        # TODO: Study 
            import unittest
            unittest.TestSuite()
        soon.
        
        For now, it's ok to hard code it.
        '''
        
        errors = 0
        
        # run all tests: 
        try:
            self.test_no_product_id()
            logging.info(f"test_no_product_id ok")
        except:
            errors += 1
            
        try:
            self.test_list_of_products()
            logging.info(f"test_list_of_products ok")
        except:
            errors += 1
            
        logging.info(f"Number of errors: {errors}")
        
        return True

    # LIST OF TESTS.
    
    
    # Test no product Id:
    
    def test_no_product_id(self):
        test = KabumProduct(url = 'https://www.kabum.com.br/produto/99711/smartphone-motorola-moto-g7-power-32gb-12mp-tela-6-2-azul-navy-xt1955-1')
        test.update_info()
        test.to_dataframe()

        return True

    # test list of product ids:
    def test_list_of_products(self):
        produtos = ['LOGITECH G513','CORSAIR K70 LUX RED','SSD Kingston 2.5´ 120GB'] # just for the sake of information.
        product_ids = ['96290','82068','85196']

        df = pandas.DataFrame()

        for product_id in product_ids:
            product = KabumProduct(product_id)
            product.update_info()

            df_foo = product.to_dataframe()
            df = pandas.concat([df, df_foo], ignore_index=True)
        df

        return True
    
SuiteOfTests().run_tests()
