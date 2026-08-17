import pytest
from ecart.configs.settings import TestData
from playwright.sync_api import expect


class TestMp3Players:

    @pytest.mark.parametrize(
        "dropdown_option",
        ["Name (A - Z)", "Price (Low > High)"],
        ids=["name_sort", "price_sort"],
    )
    def test_sorting_mp3_players(self, home_page, dropdown_option):
        """Test sorting options for MP3 Players page."""
        mp3_player_page = home_page.navigate_to_mp3_players()
        expect(mp3_player_page.page).to_have_title(TestData.MP3_PLAYERS_PAGE_TITLE)
        mp3_player_page.select_sorting_options(dropdown_option)
        # fetch all product names after sorting
        if dropdown_option == "Name (A - Z)":
            product_names = mp3_player_page.get_product_names()
            assert product_names == sorted(
                product_names
            ), "Product names are not sorted in ascending order."
        if dropdown_option == "Price (Low > High)":
            product_prices = mp3_player_page.get_product_prices()
            assert product_prices == sorted(
                product_prices, reverse=True
            ), "Product prices are not sorted in descending order."
