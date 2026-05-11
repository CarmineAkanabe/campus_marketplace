# Campus Marketplace Project Plan

## Progress
- Phase 1 completed: core app model scaffolding, URL routing, authentication flow, product listing, purchase request model, review and notification models are implemented.
- Phase 3 completed: seller request management, buyer request detail, review submission flow, and seller rating display are implemented.
- Phase 4 completed: notifications list and mark-as-read, buyer/seller dashboard views, and notification creation for requests and reviews are implemented.
- Phase 5 completed: recommendation engine, analytics tracking, and scraper support are implemented.
- Phase 6 completed: templates polished, unit tests added, database migrations created for advanced features, and documentation updated.

## Purpose
This file outlines the implementation plan for the Campus Marketplace project. The plan is organized by phase and focuses on clear, understandable code that is easy to explain and modify.

## Phase 1 — Project audit and design
1. Review app structure and confirm responsibilities for each Django app.
   - `users` handles authentication, roles, profiles.
   - `products` handles product listings, categories, images.
   - `requestsystem` handles buyer purchase requests and seller responses.
   - `reviews` handles buyer ratings and seller reviews.
   - `notifications` handles user alerts and updates.
   - `dashboard` handles buyer/seller summary pages.
   - `analytics`, `recommendations`, `scraper` are optional feature apps.
2. Define database models and relationships.
   - User roles: buyer, seller.
   - Product fields: name, description, category, price, condition, image, availability.
   - Request fields: buyer, product, message, status.
   - Review fields: buyer, seller, rating, comment.
   - Notification fields: user, title, message, read status.
   - Favorite products and scraped price data.
3. Design URL endpoints and templates for each major flow.

## Phase 2 — Core user functionality
4. Implement authentication and role-based access in `users`.
   - Register, login, logout.
   - Role selection for buyer or seller.
   - Use Django auth and clean form validation.
5. Build `products` CRUD functionality.
   - Product creation, update, delete.
   - Product listing and detail pages.
   - File upload support for product images.
6. Add search and filtering.
   - Keyword search, category filter, price range, condition, availability.
   - Keep query logic simple and readable.

## Phase 3 — Buyer / seller interactions
7. Implement purchase requests in `requestsystem`.
   - Buyers send requests.
   - Sellers view and respond to requests.
   - Request status tracking: pending, accepted, rejected, completed.
8. Add reviews and ratings in `reviews`.
   - Buyers rate sellers.
   - Shows average seller rating.
9. Add favorites/wishlist support.
   - Buyers save/remove favorite products.
   - Favorite list page for easy access.

## Phase 4 — Notifications and dashboard
10. Build notification system in `notifications`.
    - Notify users about new requests, updates, reviews.
    - Simple read/unread state.
11. Create buyer and seller dashboards.
    - Buyer dashboard: favorites, requests, notifications, recommendations.
    - Seller dashboard: product statistics, request stats, sales overview.

## Phase 5 — Optional advanced features
12. Implement recommendations in `recommendations`.
    - Related product suggestions.
    - Popular or category-based recommendations.
13. Implement analytics in `analytics`.
    - Track popular products, search trends, request metrics.
14. Add scraping support in `scraper` if desired.
    - External price comparisons for product pricing.

## Phase 6 — Polish and delivery
15. Add templates and front-end pages.
16. Add unit tests for models and views.
17. Ensure security and explainability.
    - Clear variable names, comments, and modular code.
    - Use role checks and form validation.
18. Document the project structure and setup steps.

## Notes for explanation
- Keep each app small and focused.
- Use descriptive model and view names.
- Add short comments where the logic is not obvious.
- Prefer step-by-step flow in views so the teacher can follow the live changes.
