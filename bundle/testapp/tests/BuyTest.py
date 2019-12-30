import unittest

from engine.modules.building import service
from engine.modules.building.service import BuyException
from game.entities import Country, Area


class BuyTest(unittest.TestCase):

    def test_money_fail(self):
        country = Country(iso='UK', gold=19, pop=1)
        area = Area(iso='UK', tile='city')

        with self.assertRaises(BuyException) as context:
            service.buy_item(area, country, 'inf')
        self.assertEqual(context.exception.reason, 'not_enough_gold')
        self.assertIsNone(area.unit)

    def test_pop_limit_fail(self):
        country = Country(iso='UK', gold=20, pop=0)
        area = Area(iso='UK', tile='city')

        with self.assertRaises(BuyException) as context:
            service.buy_item(area, country, 'inf')
        self.assertEqual(context.exception.reason, 'not_enough_pop')
        self.assertIsNone(area.unit)


    def test_occupied_fail(self):
        country = Country(iso='UK', gold=20, pop=1)
        area = Area(iso='UK', tile='city', unit='inf')

        with self.assertRaises(BuyException) as context:
            service.buy_item(area, country, 'inf')
        self.assertEqual(context.exception.reason, 'item_exists')

        # try:
        #     service.buy_item(area, country, 'cav')
        # except BuyException as e:
        #     self.fail("test_occupied_fail raised BuyException({}) unexpectedly!".format(e.reason))

    def test_not_mine_fail(self):
        country = Country(iso='AT', gold=20, pop=1)
        area = Area(iso='UK', tile='city')

        with self.assertRaises(BuyException) as context:
            service.buy_item(area, country, 'inf')
        self.assertEqual(context.exception.reason, 'not_mine')
        self.assertIsNone(area.unit)

    def test_not_city_fail(self):
        country = Country(iso='UK', gold=20, pop=1)
        area = Area(iso='UK')

        with self.assertRaises(BuyException) as context:
            service.buy_item(area, country, 'inf')
        self.assertEqual(context.exception.reason, 'missing_city')
        self.assertIsNone(area.unit)

    def test_buy_pass(self):
        country = Country(iso='UK', gold=20+70+120, pop=3)

        try:
            area = Area(iso='UK', tile='city')

            service.buy_item(area, country, 'inf')
            self.assertEqual(area.unit, 'inf')
            self.assertEqual(country.gold, 70+120)
            self.assertEqual(country.pop, 2)
        except BuyException as e:
            self.fail("test_occupied_fail raised BuyException({}) unexpectedly!".format(e.reason))

        try:
            area = Area(iso='UK', tile='city')

            service.buy_item(area, country, 'cav')
            self.assertEqual(area.unit, 'cav')
            self.assertEqual(country.gold, 120)
            self.assertEqual(country.pop, 1)
        except BuyException as e:
            self.fail("test_occupied_fail raised BuyException({}) unexpectedly!".format(e.reason))

        try:
            area = Area(iso='UK', tile='city')

            service.buy_item(area, country, 'art')
            self.assertEqual(area.unit, 'art')
            self.assertEqual(country.gold, 0)
            self.assertEqual(country.pop, 0)
        except BuyException as e:
            self.fail("test_occupied_fail raised BuyException({}) unexpectedly!".format(e.reason))




if __name__ == '__main__':
    unittest.main()
