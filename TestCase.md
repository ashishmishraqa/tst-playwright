# 1. User Account & Registration

1. User Registration: Automate successful registration with valid data and verify error messages for existing emails or mismatched passwords.
2. Login/Logout: Test valid credentials, invalid passwords, and the "Forgotten Password" workflow.
3. Account Management: Automate updating personal information (Name, Email, Telephone) and managing the Address Book.
4. Newsletter Subscription: Verify that a user can subscribe/unsubscribe from the newsletter through their account dashboard.

# 2. Product Search & Navigation
1. Search Functionality: Automate searches for existing products (e.g., "MacBook"), non-existent products, and partial matches.
2. Category Navigation: Verify that clicking on categories (Laptops, Components, Tablets) loads the correct product listings.
3. Product Comparison: Test the "Product Compare" feature by adding two or more items and verifying the comparison table.
4. Sorting & Pagination: Automate changing the sort order (Price, Name, Rating) and navigating through multiple pages of results.

# 3. Shopping Cart & Wishlist
1. Add to Cart: Verify adding products from the homepage, search results, and product detail pages. 
2. Cart Management: Test updating product quantities, removing items, and verifying that the "Total" price updates dynamically.
3. Wishlist: Automate adding items to the wishlist (requires login) and moving them from the wishlist to the cart.
4. Coupon & Voucher Codes: Test the application of valid and invalid discount codes in the shopping cart.



# 4. End-to-End Checkout Flow!
[img.png](ecart/tests/img.png)


# 5. Advanced & Edge Case Scenarios
1. Once the basics are covered, these scenarios improve the robustness of your framework.
Product Options: Automate selecting specific attributes like Color, Size, or Date (e.g., for products like the Apple Cinema 30").
Currency Switcher: Verify that changing the currency (Euro, Pound, Dollar) updates the prices across the entire site instantly.
Responsive Testing: Run your scripts across different screen resolutions to ensure elements like the "Cart" button remain clickable.
Broken Links: Use a script to crawl the homepage and verify all footer links (About Us, Delivery Information, etc.) return a 200 OK status.