TEXTS = {
    "welcome": "Hello, {name}! 👋\n\nI'm a bot for ordering creative services. Choose the section you need in the menu below!",
    "menu_catalog": "📋 Services Catalog",
    "menu_my_orders": "🛒 My Orders",
    "menu_about": "ℹ️ About Us",
    "menu_contacts": "📞 Contacts",
    "menu_language": "🌐 Language",
    
    "catalog_title": "📋 **Services Catalog**\n\nChoose the service you're interested in:",
    "back_to_main": "🔙 Back",
    "back_to_services": "🔙 Back to services",
    
    "service_template": """
{name}

{description}

💵 **Price:** {price}

📝 **What's included:**
• Professional work execution
• Project details discussion
• Revisions according to your requirements
• Timely project delivery

Would you like to place an order for this service?
    """,
    
    "order_prompt": "Great! You selected: {service_name}\n\nPlease describe your order details:\n• What needs to be done\n• Deadlines\n• Special requirements\n\nJust send a message with the task description.",
    
    "contact_prompt": "📞 Now provide your contact details:\n(Telegram username, phone number or email)",
    
    "order_confirmed": """
✅ **Your order has been accepted!**

**Service:** {service_name}
**Order number:** #{order_id}

We will contact you shortly to clarify the details.

Thank you for choosing us! 💫
    """,
    
    "contacts_info": "📞 Our contacts:\n\nEmail: example@mail.com\nTelegram: @username\nWorking hours: 10:00 - 20:00",
    
    "about_info": "We are a team of professionals in:\n• Video editing\n• Graphic design\n• 3D modeling\n• Content creation\n\nWe work efficiently and fast! 🚀",
    
    "no_orders": "You don't have any orders yet",
    "user_orders_title": "📦 **Your Orders:**\n\n",
    
    "order_notification": """
🚨 **NEW ORDER** #{order_id}

👤 **Client:**
• Name: {user_name}
• Username: @{username}
• ID: {user_id}

📋 **Service:** {service_name}

📝 **Order Description:**
{description}

📞 **Contact Details:**
{contact_info}

🕒 **Order Time:** {created_at}
    """,
    
    "select_language": "🌐 Choose language:",
    "language_changed": "Language changed to English ✅",
    
    "services": {
        "video_editing": {
            "name": "🎬 Video Editing",
            "description": "Professional video editing of any complexity",
            "price": "from $15"
        },
        "preview": {
            "name": "🖼️ Thumbnail Creation",
            "description": "Bright and attractive video thumbnails",
            "price": "from $8"
        },
        "modeling_3d": {
            "name": "🎨 3D Modeling",
            "description": "3D models creation and visualization",
            "price": "from $30"
        },
        "photoshop": {
            "name": "📷 Photoshop Work",
            "description": "Photo editing, collages, retouching",
            "price": "from $12"
        },
        "product_cards": {
            "name": "🛍️ Product Cards",
            "description": "Creating product cards for marketplaces",
            "price": "from $5"
        }
    }
}
