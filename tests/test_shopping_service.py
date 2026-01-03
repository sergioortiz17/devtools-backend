"""Unit tests for shopping service."""
import pytest
from decimal import Decimal

from app.shopping.service import ShoppingCalculatorService
from app.shopping.models import ShoppingTotalRequest, ShoppingTotalResponse


class TestShoppingCalculatorService:
    """Test cases for shopping calculator service."""
    
    @pytest.fixture
    def service(self):
        """Create shopping calculator service instance."""
        return ShoppingCalculatorService()
    
    def test_calculate_total_basic(self, service):
        """Test basic total calculation."""
        request = ShoppingTotalRequest(
            costs={"apple": 1.50, "banana": 0.75},
            items=["apple", "banana"],
            tax=0.1
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 2.25
        assert result.tax_amount == 0.23  # Rounded from 0.225
        assert result.total == 2.48  # 2.25 + 0.23
        assert "apple" in result.items_found
        assert "banana" in result.items_found
        assert len(result.items_not_found) == 0
    
    def test_calculate_total_with_missing_items(self, service):
        """Test calculation with items not in costs dictionary."""
        request = ShoppingTotalRequest(
            costs={"apple": 1.50, "banana": 0.75},
            items=["apple", "nonexistent", "banana"],
            tax=0.1
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 2.25
        assert "nonexistent" in result.items_not_found
        assert len(result.items_found) == 2
        assert len(result.items_not_found) == 1
    
    def test_calculate_total_zero_tax(self, service):
        """Test calculation with zero tax."""
        request = ShoppingTotalRequest(
            costs={"item": 10.00},
            items=["item"],
            tax=0.0
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 10.00
        assert result.tax_amount == 0.00
        assert result.total == 10.00
    
    def test_calculate_total_high_tax(self, service):
        """Test calculation with high tax rate."""
        request = ShoppingTotalRequest(
            costs={"item": 100.00},
            items=["item"],
            tax=0.25  # 25% tax
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 100.00
        assert result.tax_amount == 25.00
        assert result.total == 125.00
    
    def test_calculate_total_rounding(self, service):
        """Test that values are properly rounded."""
        request = ShoppingTotalRequest(
            costs={"item1": 1.111, "item2": 2.222},
            items=["item1", "item2"],
            tax=0.1
        )
        
        result = service.calculate_total(request)
        
        # All values should be rounded to 2 decimal places
        assert result.subtotal == 3.33
        assert result.tax_amount == 0.33
        assert result.total == 3.66
    
    def test_calculate_total_empty_items(self, service):
        """Test calculation with empty items list."""
        request = ShoppingTotalRequest(
            costs={"item": 10.00},
            items=[],
            tax=0.1
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 0.0
        assert result.tax_amount == 0.0
        assert result.total == 0.0
        assert len(result.items_found) == 0
        assert len(result.items_not_found) == 0
    
    def test_calculate_total_all_items_missing(self, service):
        """Test calculation when all items are missing."""
        request = ShoppingTotalRequest(
            costs={"apple": 1.50},
            items=["missing1", "missing2"],
            tax=0.1
        )
        
        result = service.calculate_total(request)
        
        assert result.subtotal == 0.0
        assert result.tax_amount == 0.0
        assert result.total == 0.0
        assert len(result.items_found) == 0
        assert len(result.items_not_found) == 2
    
    def test_round_to_decimal_places(self, service):
        """Test rounding method."""
        assert service._round_to_decimal_places(1.234) == 1.23
        assert service._round_to_decimal_places(1.235) == 1.24  # Round half up
        assert service._round_to_decimal_places(1.236) == 1.24
        assert service._round_to_decimal_places(0.001) == 0.0
        assert service._round_to_decimal_places(0.005) == 0.01
    
    def test_calculate_subtotal(self, service):
        """Test subtotal calculation method."""
        items = ["apple", "banana", "missing"]
        costs = {"apple": 1.50, "banana": 0.75}
        
        subtotal, items_found, items_not_found = service._calculate_subtotal(items, costs)
        
        assert subtotal == 2.25
        assert "apple" in items_found
        assert "banana" in items_found
        assert "missing" in items_not_found
        assert len(items_found) == 2
        assert len(items_not_found) == 1
    
    def test_calculate_tax_and_total(self, service):
        """Test tax and total calculation method."""
        tax_amount, total = service._calculate_tax_and_total(100.0, 0.1)
        
        assert tax_amount == 10.0
        assert total == 110.0
    
    def test_calculate_tax_and_total_zero_subtotal(self, service):
        """Test tax calculation with zero subtotal."""
        tax_amount, total = service._calculate_tax_and_total(0.0, 0.1)
        
        assert tax_amount == 0.0
        assert total == 0.0

