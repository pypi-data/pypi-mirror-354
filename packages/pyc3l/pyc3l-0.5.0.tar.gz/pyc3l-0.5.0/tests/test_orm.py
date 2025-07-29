# -*- coding: utf-8 -*-

import unittest
from pyc3l import Pyc3l


class test_pyc3l_instanciation(unittest.TestCase):
    def test_no_args(self):

        pyc3l = Pyc3l()

        for encoded, to_encode in ORACLE.items():
            self.assertEqual(encodeNumber(to_encode), encoded)
            self.assertEqual(to_encode, decode_data('int256', encoded))

    def test_encodeAddressForTransaction(self):

        # When
        address_1 = "0xE00000000000000000000000000000000000000E"
        address_2 = "E00000000000000000000000000000000000000E"
        address_3 = "E000000000000000000000000000000000000000E"
        address_4 = "E0000000000000000000000000000000000000E"

        # then
        self.assertEqual(
            encodeAddressForTransaction(address_1),
            "000000000000000000000000E00000000000000000000000000000000000000E",
        )
        self.assertEqual(
            encodeAddressForTransaction(address_2),
            "000000000000000000000000E00000000000000000000000000000000000000E",
        )

        with self.assertRaises(Exception):
            encodeAddressForTransaction(address_3)
        with self.assertRaises(Exception):
            encodeAddressForTransaction(address_4)



if __name__ == "__main__":
    unittest.main()
