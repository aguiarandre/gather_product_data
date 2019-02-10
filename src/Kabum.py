import requests
from bs4 import BeautifulSoup
from typing import Union, Optional, List
import pandas
import logging
import datetime
import re

#logging.basicConfig(level=logging.INFO)

class Product(object):
    '''
    Docstring for Product - TODO.
    
    The idea is just to create a simple template for classes to inheritance from and, thus, 
    create more specific and meaningful applications for each type of product of interest.
    '''
        
    def __init__(self, *args, **kwargs):
        '''
        Initialize empty product.
        All products have: name, price and category
        '''
        self.price = None
        self.name = None
        self.category = None
        

class OnlineProduct(Product):
    '''
    Docstring for OnlineProduct - TODO.
    
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize an Online Product.
        A specific feature of an online product is its url
        '''
        super().__init__(self, *args, **kwargs)
        self.is_promo = False
        # soup is the beautifulsoup object of the url
        self.soup = None 
        self.url = None        

class KabumProduct(OnlineProduct):
    '''
    Docstring TODO.
    '''

    
    def __init__(self, product_id: Optional[Union[str, int, List[str]]] = None, *args, **kwargs):
        '''
        Initialize the specific online product from Kabum store (kabum.com.br/)
        
        Their product have specific product_ids, which can be used to search for it in their webpage.
        Ideally, to instantiate a Kabum Product, one should give only the product id of interest, as in:
            product = KabumProduct(product_id = 96290) or
            product = KabumProduct(product_id = '96290') or even
            product = KabumProduct(product_id = ['96290']) 
        
        Alternatively, one can provide the URL itself along with no product_id, p.e.:
            product = KabumProduct(url = 'https://www.kabum.com.br/produto/99711/smartphone-motorola-moto-g7-power-32gb-12mp-tela-6-2-azul-navy-xt1955-1')
            
        
        '''
        
        super().__init__(self, *args, **kwargs)
        self.id = product_id
        self.date = None
        
        ## initialize product
        
        # if product id is provided, then:
        if self.id:
            if isinstance(self.id, list):
                if len(self.id) == 1:
                    self.id = ", ".join(self.id)
                else:
                    logging.error('Too many ids. Only able to handle one at a time.')
            
            if isinstance(self.id, str) or isinstance(self.id, int):
                self.url = f'''https://www.kabum.com.br/produto/{self.id}/'''
            else:
                logging.error('''Could not create url. Probably there are some problems with the product_id type you are providing.''')
        else:
            try:
                # try to get url as a keyword argument
                self.url = kwargs.pop('url')
            except:
                logging.info(f'No URL nor product_id provided. Creating an empty product')
                self.url = None
    
    def __str__(self):
        json_like_str = f'''
        ID do Produto: {self.id}, 
        Nome do Produto: {self.name}, 
        Preço: {self.price},
        Categoria: {self.category},
        Produto em promoção: {self.is_promo}
        '''
        return json_like_str
    
        
    def __repr__(self):
        return f'KabumProduct #{self.id}, Inherited from OnlineProduct, Inherited from Product.'
       
    def to_dataframe(self) -> pandas.DataFrame:
        d = {'pk_product_id': [self.id], 
             'product_name': [self.name], 
             'is_promo': [self.is_promo],
             'dbl_price': [self.price],
             'cat_prod': self.category,
             'dt_ref': self.date}

        return pandas.DataFrame(data=d)    
    
    @staticmethod
    def _format_time_now() -> str:
        today = datetime.date.today()
        day = f'{today.day:02.0f}'
        month = f'{today.month:02.0f}'
        year = f'{today.year:04.0f}'

        return year+month+day
    
    def _extract_info(self) -> bool:
    
        # get variable google_tag_params from website.
        regex_var = re.compile('var google_tag_params = \{([^}]+)\}')
        google_tag_params = "".join(re.findall(regex_var, self.soup.text))
        #print(google_tag_params)
        
        # get name of the product
        for val in google_tag_params.split('\n'):
            if ('pname' in val):
                index = google_tag_params.split('\n').index(val)
                
        regex_pname = re.compile('(?<=pname: ).*$')
        self.name = str(re.findall(regex_pname, google_tag_params.split('\n')[index])).split("\"")[1]
        
        # get category of the product
        for val in google_tag_params.split('\n'):
            if ('pcat' in val):
                index = google_tag_params.split('\n').index(val)

        regex_pcat = re.compile('(?<=pcat: ).*$')
        product_category = str(re.findall(regex_pcat, google_tag_params.split('\n')[index])).split("\"")[1]
        # transform this variable a bit
        regex_pcat = re.compile('[\W_]+')
        self.category = regex_pcat.sub('', product_category)
        
        # get price of the product
        regex_decimal = re.compile('\d+\.\d+')
        self.price = float(re.findall(regex_decimal, google_tag_params.split('\n')[-2])[0])   
        
        # get id if it comes from a url only call
        if not self.id:
            for val in google_tag_params.split('\n'):
                if ('prodid' in val):
                    index = google_tag_params.split('\n').index(val)

            regex_pid = re.compile('(?<=prodid: ).*$')
        
            self.id = int(re.findall(re.compile('\d+'), 
                                 str(re.findall(regex_pid, google_tag_params.split('\n')[index])).split("\"")[1])[0])
            
            logging.warning(f"As you're using the URL to access the product, i'm inputting the Product Id")
            
        
        # update time of queries
        self.date = self._format_time_now()
                
        # TODO: pegar quantos % de desconto no boleto
        return True
    
    
        
    def update_info(self): 
        '''
        Docstring to be done
        '''
        
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

        # this specific div-class happens when the product is under promotion
        
        if self.soup.findAll("div", {"class": "box_preco-cm"}): #hack way to check if product is under promotion - this may change over time
            self.is_promo = True

        if(self._extract_info()):
            logging.info(f'Product information updated at {self.date}.')
        
    
    def store_results():
        pass
    # TODO: Submit results to mySQL database (or maybe Hadoop CDH)
    

# Test example:
'''
produtos = ['LOGITECH G513','CORSAIR K70 LUX RED','SSD Kingston 2.5´ 120GB'] # just for the sake of information.
product_ids = ['96290','82068','85196']

df = pandas.DataFrame()

for product_id in product_ids:
    product = KabumProduct(product_id)
    product.update_info()

    df_foo = product.to_dataframe()
    df = pandas.concat([df, df_foo], ignore_index=True)

df    
'''
