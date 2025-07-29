from epure import epure
from .taalc_transaction import TaalcTransaction
from .taalc_nft import TaalcNft
from .taalc_nft_token import TaalcNftToken
# from .currency_transaction import CurrencyTransaction
# from epure import Elist


class NftTransaction(TaalcTransaction):    
    taalc_nft_token: TaalcNftToken
    amount: int    

    def __init__(self, sent_from, sent_to, transaction_batch=None):
        super().__init__()