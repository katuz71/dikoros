| # | Method | Path | Path params | Query params | Body | Response | Summary |
|---|--------|------|-------------|--------------|------|----------|---------|
| 1 | GET | `/about` | Ч | Ч | Ч | string | Get About Page |
| 2 | GET | `/admin` | Ч | Ч | Ч | string | Read Admin |
| 3 | GET | `/all-categories` | Ч | Ч | Ч | CategoryResponse[] | Get Categories |
| 4 | DELETE | `/api/admin/user/{phone}` | phone | Ч | Ч | object | Delete Admin User |
| 5 | GET | `/api/admin/users` | Ч | search,has_bonuses,sort_by,source | Ч | object | Get Admin Users |
| 6 | POST | `/api/admin/users/delete-batch` | Ч | Ч | BatchDeleteUsers | object | Delete Users Batch |
| 7 | GET | `/api/all-categories` | Ч | Ч | Ч | CategoryResponse[] | Get Categories |
| 8 | POST | `/api/auth` | Ч | Ч | UserAuth | object | Auth User |
| 9 | POST | `/api/auth/social-login` | Ч | Ч | SocialAuthRequest | object | Auth Social Login |
| 10 | GET | `/api/banners` | Ч | Ч | Ч | object | Get Banners |
| 11 | GET | `/api/categories` | Ч | Ч | Ч | object | Get Categories Api |
| 12 | POST | `/api/chat` | Ч | Ч | ChatRequest | object | Chat Endpoint Api |
| 13 | GET | `/api/clear_products` | Ч | Ч | Ч | object | Clear Products Db |
| 14 | DELETE | `/api/client/orders/clear/{phone}` | phone | Ч | Ч | object | Clear Client Orders |
| 15 | DELETE | `/api/client/orders/{order_id}` | order_id | Ч | Ч | object | Delete Client Order |
| 16 | GET | `/api/client/orders/{phone}` | phone | Ч | Ч | object | Get Client Orders |
| 17 | GET | `/api/delivery/cities` | Ч | q | Ч | object | Get Np Cities |
| 18 | GET | `/api/delivery/popular-cities` | Ч | Ч | Ч | object | Get Popular Cities |
| 19 | GET | `/api/delivery/warehouses` | Ч | city_ref | Ч | object | Get Np Warehouses |
| 20 | GET | `/api/image` | Ч | src,w,h,q,format | Ч | object | Get Resized Image |
| 21 | GET | `/api/orders` | Ч | Ч | Ч | object | Get Orders Api |
| 22 | POST | `/api/orders/delete-batch` | Ч | Ч | BatchDelete | object | Delete Orders Batch Api |
| 23 | DELETE | `/api/orders/{id}` | id | Ч | Ч | object | Delete Order Api |
| 24 | PUT | `/api/orders/{id}/status` | id | Ч | OrderStatusUpdate | object | Update Order Status Api |
| 25 | GET | `/api/orders/{order_id}` | order_id | Ч | Ч | object | Get Order By Id |
| 26 | POST | `/api/payment/callback` | Ч | Ч | Ч | object | Payment Callback Monobank |
| 27 | GET | `/api/post` | Ч | Ч | Ч | object | Get Posts |
| 28 | GET | `/api/post/{post_id}` | post_id | Ч | Ч | object | Get Post |
| 29 | GET | `/api/posts` | Ч | Ч | Ч | object | Get Posts |
| 30 | GET | `/api/posts/{post_id}` | post_id | Ч | Ч | object | Get Post |
| 31 | GET | `/api/product/{id}` | id | Ч | Ч | object | Get Product |
| 32 | GET | `/api/products` | Ч | page,limit,category,status,search | Ч | object | Get Products Paginated |
| 33 | GET | `/api/products/{id}` | id | Ч | Ч | object | Get Product |
| 34 | GET | `/api/promo-codes` | Ч | Ч | Ч | object | Get Promo Codes |
| 35 | POST | `/api/promo-codes` | Ч | Ч | PromoCodeCreate | object | Create Promo Code |
| 36 | POST | `/api/promo-codes/validate` | Ч | Ч | PromoCodeValidate | object | Validate Promo Code |
| 37 | DELETE | `/api/promo-codes/{id}` | id | Ч | Ч | object | Delete Promo Code |
| 38 | PUT | `/api/promo-codes/{id}/toggle` | id | Ч | Ч | object | Toggle Promo Code |
| 39 | POST | `/api/recalculate-cashback` | Ч | Ч | Ч | object | Recalculate All Cashback |
| 40 | POST | `/api/reviews` | Ч | Ч | ReviewCreate | object | Create Review |
| 41 | DELETE | `/api/reviews/{id}` | id | Ч | Ч | object | Delete Review |
| 42 | GET | `/api/reviews/{product_id}` | product_id | Ч | Ч | object | Get Product Reviews |
| 43 | POST | `/api/sync/catalog` | Ч | Ч | Ч | object | Sync Catalog Horoshop |
| 44 | POST | `/api/track` | Ч | Ч | AnalyticsEventReq | object | Track Event Endpoint |
| 45 | PUT | `/api/user/info/{phone}` | phone | Ч | UserInfoUpdate | object | Update User Info |
| 46 | GET | `/api/user/me` | Ч | Ч | Ч | UserResponse | Get Api User Me |
| 47 | POST | `/api/user/push-token` | Ч | Ч | PushTokenRequest | object | Save Push Token |
| 48 | GET | `/api/user/reviews/{phone}` | phone | Ч | Ч | object | Get User Reviews |
| 49 | GET | `/api/users` | Ч | search,has_bonuses,sort_by,source | Ч | object | Get Users |
| 50 | GET | `/api/users/export` | Ч | search,has_bonuses,sort_by,source | Ч | object | Export Users |
| 51 | PUT | `/api/users/{phone}` | phone | Ч | AdminUserUpdate | object | Update User |
| 52 | POST | `/api/v1/chat` | Ч | Ч | ChatRequest | object | Chat Endpoint Api V1 |
| 53 | GET | `/banners` | Ч | Ч | Ч | object | Get Banners |
| 54 | POST | `/banners` | Ч | Ч | BannerCreate | object | Create Banner |
| 55 | DELETE | `/banners/{id}` | id | Ч | Ч | object | Delete Banner |
| 56 | POST | `/categories` | Ч | Ч | Body_add_category_categories_post | object | Add Category |
| 57 | DELETE | `/categories/{category_id}` | category_id | Ч | Ч | object | Delete Category |
| 58 | POST | `/categories/{category_id}/banners` | category_id | Ч | Body_upload_category_banner_categories__category_id__banners_post | object | Upload Category Banner |
| 59 | DELETE | `/categories/{category_id}/banners` | category_id | image_url | Ч | object | Delete Category Banner |
| 60 | PUT | `/categories/{id}` | id | Ч | Body_update_category_categories__id__put | object | Update Category |
| 61 | POST | `/chat` | Ч | Ч | ChatRequest | ChatResponse | Chat Endpoint |
| 62 | POST | `/create_order` | Ч | Ч | OrderRequest | object | Create Order |
| 63 | GET | `/delete-account` | Ч | Ч | Ч | string | Get Delete Account |
| 64 | GET | `/delivery-payment` | Ч | Ч | Ч | string | Get Delivery Page |
| 65 | GET | `/health` | Ч | Ч | Ч | object | Health Check |
| 66 | POST | `/orders/delete-batch` | Ч | Ч | BatchDelete | object | Delete Orders Batch |
| 67 | GET | `/orders/export` | Ч | Ч | Ч | object | Export Orders |
| 68 | DELETE | `/orders/{id}` | id | Ч | Ч | object | Delete Order |
| 69 | PUT | `/orders/{id}/status` | id | Ч | OrderStatusUpdate | object | Update Order Status |
| 70 | GET | `/post` | Ч | Ч | Ч | object | Get Posts |
| 71 | GET | `/post/{post_id}` | post_id | Ч | Ч | object | Get Post |
| 72 | GET | `/posts` | Ч | Ч | Ч | object | Get Posts |
| 73 | POST | `/posts` | Ч | Ч | object | object | Create Post |
| 74 | GET | `/posts/{post_id}` | post_id | Ч | Ч | object | Get Post |
| 75 | DELETE | `/posts/{post_id}` | post_id | Ч | Ч | object | Delete Post |
| 76 | GET | `/privacy-policy` | Ч | Ч | Ч | string | Get Privacy Page |
| 77 | GET | `/product/{id}` | id | Ч | Ч | object | Get Product |
| 78 | GET | `/products` | Ч | page,limit,category,status,search | Ч | object | Get Products Paginated |
| 79 | POST | `/products` | Ч | Ч | Ч | object | Create Product |
| 80 | GET | `/products/by-external-id` | Ч | external_id | Ч | object | Get Product By External Id Query |
| 81 | GET | `/products/external` | Ч | external_id | Ч | object | Get Product By External Query |
| 82 | GET | `/products/external/{external_id}` | external_id | Ч | Ч | object | Get Product By External Id |
| 83 | GET | `/products/{id}` | id | Ч | Ч | object | Get Product |
| 84 | PUT | `/products/{id}` | id | Ч | Ч | object | Update Product |
| 85 | DELETE | `/products/{id}` | id | Ч | Ч | object | Delete Product |
| 86 | GET | `/returns` | Ч | Ч | Ч | string | Get Returns Page |
| 87 | POST | `/upload` | Ч | Ч | Body_upload_image_upload_post | object | Upload Image |
| 88 | POST | `/upload_csv` | Ч | Ч | Body_upload_csv_upload_csv_post | object | Upload Csv |
| 89 | GET | `/user/{identifier}` | identifier | Ч | Ч | object | Get User By Phone |
| 90 | GET | `/user/{phone}` | phone | Ч | Ч | UserResponse | Get User Profile |

---

## ╤їхь√ фрээ√ї (components/schemas)

┬ёхую ёїхь: 27

### AdminUserUpdate
    phone: string | null
    name: string | null
    city: string | null
    warehouse: string | null
    user_ukrposhta: string | null
    email: string | null
    contact_preference: string | null
    bonus_balance: integer | null
    total_spent: number | null

### AnalyticsEventReq
  * event_name: string
    properties: object
    user_data: object

### BannerCreate
  * image_url: string

### BatchDelete
  * ids: array

### BatchDeleteUsers
  * phones: array

### Body_add_category_categories_post
  * name: string
    banner: string

### Body_update_category_categories__id__put
  * name: string
    banner: string

### Body_upload_category_banner_categories__category_id__banners_post
  * file: string

### Body_upload_csv_upload_csv_post
  * file: string

### Body_upload_image_upload_post
  * file: string

### CategoryResponse
  * id: integer
  * name: string
    banner_url: string | null
    banners: array

### ChatMessage
  * role: string
  * content: string

### ChatRequest
  * messages: array

### ChatResponse
  * message: string
  * products: array

### HTTPValidationError
    detail: array

### OrderItem
  * id: integer
    product_id: integer | null
  * name: string
  * price: number
  * quantity: integer
    packSize: string | null
    unit: string | null
    variant_info: string | null

### OrderRequest
  * name: string
  * phone: string
    email: string | null
    contact_preference: string | null
  * city: string
    cityRef: string | null
  * warehouse: string
    warehouseRef: string | null
  * items: array
  * totalPrice: number
    payment_method: string
    bonus_used: integer
    use_bonuses: boolean
    user_phone: string | null
    delivery_method: string | null
    bonus_balance: integer | null
    total_spent: number | null
    push_token: string | null
    return_url: string | null

### OrderStatusUpdate
  * new_status: string

### PromoCodeCreate
  * code: string
    discount_percent: integer
    discount_amount: number
    max_uses: integer
    expires_at: string | null

### PromoCodeValidate
  * code: string

### PushTokenRequest
  * auth_id: string
  * token: string
    send_welcome: boolean

### ReviewCreate
  * product_id: integer
  * user_name: string
    user_phone: string | null
  * rating: integer
    comment: string | null

### SocialAuthRequest
  * token: string
  * provider: string
    phone: string | null

### UserAuth
  * phone: string

### UserInfoUpdate
    name: string | null
    phone: string | null
    city: string | null
    warehouse: string | null
    user_ukrposhta: string | null
    email: string | null
    contact_preference: string | null

### UserResponse
    phone: string | null
    bonus_balance: integer
    total_spent: number
    cashback_percent: integer
    name: string | null
    city: string | null
    warehouse: string | null
    ukrposhta: string | null
    email: string | null
    contact_preference: string | null
    referrer: string | null
    created_at: string | null

### ValidationError
  * loc: array
  * msg: string
  * type: string

