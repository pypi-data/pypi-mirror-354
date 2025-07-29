# -*- coding: utf-8 -*-

from . import Currency


class Account(object):

    def __init__(self, wallet, endpoint=None):
        logger.info(
            "Load wallet with address 0x%s on server %r",
            wallet["address"],
            wallet["server"]["name"],
        )
        self._wallet = wallet
        self._account = None
        self._endpoint = endpoint

    @staticmethod
    def from_file(cls, filename, endpoint=None):
        logger.info("Opening file %r", filename)
        return cls(json.load(filename), endpoint)

    @staticmethod
    def from_json(cls, json_string, endpoint=None):
        logger.info("Parsing JSON (size: %s)", len(json_string))
        return cls(json.loads(json_string), endpoint)

    @property
    def currency(self):
        if self._currency is None:
            self._currency = Currency(
                self.data["server"]["name"],
                endpoint=self._endpoint
            )
        return self._currency

    def unlock(self, password):
        self._account = Account.privateKeyToAccount(
            Account.decrypt(self._wallet_content, password)
        )

    def use_endpoint(self, endpoint):
        self._endpoint = endpoint

    def __getattr__(self, label):
        ## YYYvlab: don't commit that !
        import ipdb; ipdb.set_trace()  # fmt: skip
        pass



