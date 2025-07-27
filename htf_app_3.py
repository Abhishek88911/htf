import os
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp, sp
from kivy.lang import Builder
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.effects.scroll import ScrollEffect

# Set window size for mobile phone
Window.size = (360, 640)

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')
    
# Create products directory
if not os.path.exists('images/products'):
    os.makedirs('images/products')
    
# Create profile directory
if not os.path.exists('images/profiles'):
    os.makedirs('images/profiles')

# Sample product images mapping
product_images = {
    "Organic Tomatoes": "tomato.png",
    "Fresh Carrots": "carrot.png",
    "Wheat Grains": "wheat.png",
    "Basmati Rice": "rice.png",
    "Apples": "apple.png",
    "Mangoes": "mango.png",
    "Potatoes": "potato.png",
    "Onions": "onion.png",
    "Garlic": "garlic.png",
    "Cabbage": "cabbage.png",
    "Cauliflower": "cauliflower.png",
    "Spinach": "spinach.png",
    "Bananas": "banana.png",
    "Oranges": "orange.png",
    "Grapes": "grapes.png"
}

# Sample profile images
profile_images = {
    "Rajesh Kumar": "farmer1.png",
    "Priya Sharma": "buyer1.png",
    "Vikram Singh": "farmer2.png",
    "Anjali Patel": "buyer2.png",
    "Buyer User": "buyer_profile.png"
}

# Main app structure
Builder.load_string('''
<CustomButton@Button>:
    background_normal: ''
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0.2, 0.7, 0.3, 1) if self.state == 'normal' else (0.15, 0.6, 0.25, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]
    canvas.after:
        Color:
            rgba: (0.1, 0.5, 0.2, 1) if self.state == 'normal' else (0.1, 0.4, 0.15, 1)
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(12)]
            width: 1.5
            dash_offset: 5
            dash_length: 3

<AnimatedLabel@Label>:
    canvas.before:
        Color:
            rgba: (0.95, 0.98, 0.95, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]

<RoleSelectionScreen>:
    FloatLayout:
        canvas:
            Color:
                rgba: (0.9, 0.95, 0.9, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        
        AnimatedLabel:
            text: '🌾'
            font_size: sp(80)
            size_hint: None, None
            size: dp(120), dp(120)
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            canvas.before:
                PushMatrix
            canvas.after:
                PopMatrix
            on_touch_down: self.animate_logo()
        
        AnimatedLabel:
            text: 'Help The Farmers'
            font_size: sp(28)
            bold: True
            color: (0.2, 0.4, 0.2, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        
        AnimatedLabel:
            text: 'Empowering Farmers, Connecting Buyers'
            font_size: sp(16)
            color: (0.3, 0.3, 0.3, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.48}
        
        CustomButton:
            id: farmer_btn
            text: 'I am a Farmer'
            size_hint: 0.8, None
            height: dp(50)
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            on_press: 
                root.animate_button(self)
                root.select_role('farmer')
        
        CustomButton:
            id: buyer_btn
            text: 'I am a Buyer'
            size_hint: 0.8, None
            height: dp(50)
            pos_hint: {'center_x': 0.5, 'center_y': 0.25}
            on_press: 
                root.animate_button(self)
                root.select_role('buyer')

<FarmerHomeScreen>:
    TabbedPanel:
        do_default_tab: False
        background_color: (0.9, 0.95, 0.9, 1)
        tab_pos: 'top_mid'
        
        TabbedPanelItem:
            text: 'My Products'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                
                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(10)
                    
                    TextInput:
                        id: search_input
                        hint_text: 'Search your products...'
                        size_hint_x: 0.7
                        background_normal: ''
                        background_active: ''
                        background_color: (1, 1, 1, 1)
                        foreground_color: (0, 0, 0, 1)
                        padding: [dp(10), dp(15), dp(10), dp(5)]
                        multiline: False
                        on_text: root.search_products(self.text)
                    
                    CustomButton:
                        text: 'Add'
                        size_hint_x: 0.3
                        on_press: 
                            root.animate_button(self)
                            root.show_add_product_popup()
                
                ScrollView:
                    effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                    GridLayout:
                        id: products_grid
                        cols: 1
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height
                        padding: [dp(5), dp(5), dp(5), dp(5)]
        
        TabbedPanelItem:
            text: 'Orders'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                
                Label:
                    text: 'Recent Orders'
                    font_size: sp(20)
                    bold: True
                    size_hint_y: None
                    height: dp(40)
                    color: (0.2, 0.4, 0.2, 1)
                
                ScrollView:
                    effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                    GridLayout:
                        id: orders_grid
                        cols: 1
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height
                        padding: [dp(5), dp(5), dp(5), dp(5)]
        
        TabbedPanelItem:
            text: 'Profile'
            ScrollView:
                effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                    size_hint_y: None
                    height: dp(700)
                    
                    BoxLayout:
                        size_hint_y: None
                        height: dp(120)
                        spacing: dp(20)
                        
                        Image:
                            id: profile_img
                            source: root.profile_image
                            size_hint: None, None
                            size: dp(100), dp(100)
                            canvas.before:
                                PushMatrix
                                Rotate:
                                    angle: root.profile_rotation
                                    origin: self.center
                            canvas.after:
                                PopMatrix
                        
                        CustomButton:
                            text: 'Change Photo'
                            size_hint_x: 0.6
                            background_normal: ''
                            background_color: (0.8, 0.8, 0.8, 0.5)
                            on_press: 
                                root.animate_button(self)
                                root.rotate_profile()
                    
                    Label:
                        text: 'Account Settings'
                        font_size: sp(20)
                        bold: True
                        size_hint_y: None
                        height: dp(40)
                        color: (0.2, 0.4, 0.2, 1)
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(200)
                        
                        TextInput:
                            id: username_input
                            hint_text: 'Username'
                            text: root.username
                            background_normal: ''
                            background_color: (1, 1, 1, 1)
                            padding: [dp(10), dp(15), dp(10), dp(5)]
                            multiline: False
                        
                        TextInput:
                            id: location_input
                            hint_text: 'Location'
                            text: root.location
                            background_normal: ''
                            background_color: (1, 1, 1, 1)
                            padding: [dp(10), dp(15), dp(10), dp(5)]
                            multiline: False
                        
                        CustomButton:
                            text: 'Save Changes'
                            size_hint_y: None
                            height: dp(50)
                            on_press: 
                                root.animate_button(self)
                                root.save_profile_changes()
                    
                    Label:
                        text: 'App Settings'
                        font_size: sp(20)
                        bold: True
                        size_hint_y: None
                        height: dp(40)
                        color: (0.2, 0.4, 0.2, 1)
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(120)
                        
                        BoxLayout:
                            size_hint_y: None
                            height: dp(50)
                            spacing: dp(10)
                            
                            Label:
                                text: 'Dark Mode'
                                font_size: sp(18)
                                color: (0.2, 0.2, 0.2, 1)
                                size_hint_x: 0.7
                                halign: 'left'
                                text_size: self.width, None
                            
                            Switch:
                                id: dark_mode_switch
                                active: root.dark_mode
                                on_active: 
                                    root.animate_switch(self)
                                    root.toggle_dark_mode(self.active)
                        
                        CustomButton:
                            text: 'Logout'
                            size_hint_y: None
                            height: dp(50)
                            background_color: (0.8, 0.2, 0.2, 1)
                            on_press: 
                                root.animate_button(self)
                                root.logout()

<BuyerHomeScreen>:
    TabbedPanel:
        do_default_tab: False
        background_color: (0.9, 0.95, 0.9, 1)
        tab_pos: 'top_mid'
        
        TabbedPanelItem:
            text: 'Products'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                
                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    
                    TextInput:
                        id: search_input
                        hint_text: 'Search for fresh produce...'
                        background_normal: ''
                        background_active: ''
                        background_color: (1, 1, 1, 1)
                        foreground_color: (0, 0, 0, 1)
                        padding: [dp(10), dp(15), dp(10), dp(5)]
                        multiline: False
                        on_text: root.search_products(self.text)
                
                ScrollView:
                    effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                    GridLayout:
                        id: products_grid
                        cols: 2
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height
                        padding: [dp(5), dp(5), dp(5), dp(5)]
        
        TabbedPanelItem:
            text: 'My Orders'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                
                Label:
                    text: 'Your Orders'
                    font_size: sp(20)
                    bold: True
                    size_hint_y: None
                    height: dp(40)
                    color: (0.2, 0.4, 0.2, 1)
                
                ScrollView:
                    effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                    GridLayout:
                        id: orders_grid
                        cols: 1
                        spacing: dp(10)
                        size_hint_y: None
                        height: self.minimum_height
                        padding: [dp(5), dp(5), dp(5), dp(5)]
        
        TabbedPanelItem:
            text: 'Profile'
            ScrollView:
                effect_cls: 'ScrollEffect' if root.scroll_effect == 'normal' else 'DampedScrollEffect'
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(20)
                    spacing: dp(20)
                    size_hint_y: None
                    height: dp(700)
                    
                    BoxLayout:
                        size_hint_y: None
                        height: dp(120)
                        spacing: dp(20)
                        
                        Image:
                            source: root.profile_image
                            size_hint: None, None
                            size: dp(100), dp(100)
                            canvas.before:
                                PushMatrix
                                Rotate:
                                    angle: root.profile_rotation
                                    origin: self.center
                            canvas.after:
                                PopMatrix
                        
                        CustomButton:
                            text: 'Change Photo'
                            size_hint_x: 0.6
                            background_normal: ''
                            background_color: (0.8, 0.8, 0.8, 0.5)
                            on_press: 
                                root.animate_button(self)
                                root.rotate_profile()
                    
                    Label:
                        text: 'Account Settings'
                        font_size: sp(20)
                        bold: True
                        size_hint_y: None
                        height: dp(40)
                        color: (0.2, 0.4, 0.2, 1)
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(200)
                        
                        TextInput:
                            id: username_input
                            hint_text: 'Username'
                            text: root.username
                            background_normal: ''
                            background_color: (1, 1, 1, 1)
                            padding: [dp(10), dp(15), dp(10), dp(5)]
                            multiline: False
                        
                        TextInput:
                            id: location_input
                            hint_text: 'Location'
                            text: root.location
                            background_normal: ''
                            background_color: (1, 1, 1, 1)
                            padding: [dp(10), dp(15), dp(10), dp(5)]
                            multiline: False
                        
                        CustomButton:
                            text: 'Save Changes'
                            size_hint_y: None
                            height: dp(50)
                            on_press: 
                                root.animate_button(self)
                                root.save_profile_changes()
                    
                    Label:
                        text: 'App Settings'
                        font_size: sp(20)
                        bold: True
                        size_hint_y: None
                        height: dp(40)
                        color: (0.2, 0.4, 0.2, 1)
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(120)
                        
                        BoxLayout:
                            size_hint_y: None
                            height: dp(50)
                            spacing: dp(10)
                            
                            Label:
                                text: 'Dark Mode'
                                font_size: sp(18)
                                color: (0.2, 0.2, 0.2, 1)
                                size_hint_x: 0.7
                                halign: 'left'
                                text_size: self.width, None
                            
                            Switch:
                                id: dark_mode_switch
                                active: root.dark_mode
                                on_active: 
                                    root.animate_switch(self)
                                    root.toggle_dark_mode(self.active)
                        
                        CustomButton:
                            text: 'Logout'
                            size_hint_y: None
                            height: dp(50)
                            background_color: (0.8, 0.2, 0.2, 1)
                            on_press: 
                                root.animate_button(self)
                                root.logout()

<ProductItem@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(150)
    padding: dp(5)
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: (0.95, 0.98, 0.95, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]
    Image:
        id: product_img
        source: root.product_image
        size_hint_y: None
        height: dp(100)
        allow_stretch: True
    Label:
        text: root.product_name
        font_size: sp(14)
        bold: True
        size_hint_y: None
        height: dp(20)
        text_size: self.width, None
        halign: 'center'
        color: (0.2, 0.2, 0.2, 1)
    Label:
        text: root.product_price
        font_size: sp(12)
        size_hint_y: None
        height: dp(20)
        text_size: self.width, None
        halign: 'center'
        color: (0.3, 0.5, 0.3, 1)

<BuyerProductItem@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(200)
    padding: dp(5)
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: (0.95, 0.98, 0.95, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]
    Image:
        id: product_img
        source: root.product_image
        size_hint_y: None
        height: dp(100)
        allow_stretch: True
    Label:
        text: root.product_name
        font_size: sp(14)
        bold: True
        size_hint_y: None
        height: dp(20)
        text_size: self.width, None
        halign: 'center'
        color: (0.2, 0.2, 0.2, 1)
    Label:
        text: root.product_price
        font_size: sp(12)
        size_hint_y: None
        height: dp(20)
        text_size: self.width, None
        halign: 'center'
        color: (0.3, 0.5, 0.3, 1)
    CustomButton:
        text: 'Buy Now'
        size_hint_y: None
        height: dp(30)
        on_press: 
            root.buy_product()
            root.animate_button(self)

<OrderItem@BoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(100)
    padding: dp(10)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: (0.95, 0.98, 0.95, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]
    Image:
        source: root.order_image
        size_hint_x: None
        width: dp(80)
        allow_stretch: True
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(5)
        Label:
            text: root.order_product
            font_size: sp(16)
            bold: True
            text_size: self.width, None
            halign: 'left'
            color: (0.2, 0.2, 0.2, 1)
        Label:
            text: root.order_buyer
            font_size: sp(14)
            text_size: self.width, None
            halign: 'left'
            color: (0.4, 0.4, 0.4, 1)
        Label:
            text: root.order_status
            font_size: sp(14)
            text_size: self.width, None
            halign: 'left'
            color: (0.3, 0.5, 0.3, 1)

<AddProductPopup>:
    title: 'Add New Product'
    size_hint: 0.9, 0.8
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        TextInput:
            id: product_name
            hint_text: 'Product Name'
            size_hint_y: None
            height: dp(50)
            background_normal: ''
            background_color: (1, 1, 1, 1)
            padding: [dp(10), dp(15), dp(10), dp(5)]
        TextInput:
            id: product_category
            hint_text: 'Category (e.g., Vegetables, Fruits)'
            size_hint_y: None
            height: dp(50)
            background_normal: ''
            background_color: (1, 1, 1, 1)
            padding: [dp(10), dp(15), dp(10), dp(5)]
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            TextInput:
                id: product_quantity
                hint_text: 'Quantity'
                size_hint_x: 0.5
                background_normal: ''
                background_color: (1, 1, 1, 1)
                padding: [dp(10), dp(15), dp(10), dp(5)]
                input_filter: 'int'
            TextInput:
                id: product_price
                hint_text: 'Price (₹)'
                size_hint_x: 0.5
                background_normal: ''
                background_color: (1, 1, 1, 1)
                padding: [dp(10), dp(15), dp(10), dp(5)]
                input_filter: 'float'
        TextInput:
            id: product_description
            hint_text: 'Description'
            size_hint_y: None
            height: dp(100)
            background_normal: ''
            background_color: (1, 1, 1, 1)
            padding: [dp(10), dp(15), dp(10), dp(5)]
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Button:
                text: 'Add Image'
                size_hint_x: 0.5
                background_normal: ''
                background_color: (0.8, 0.8, 0.8, 0.5)
                on_press: 
                    root.animate_button(self)
                    root.show_toast('Feature coming soon!')
            Image:
                id: product_image_preview
                size_hint_x: 0.5
                source: 'images/default_product.png'
                allow_stretch: True
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            CustomButton:
                text: 'Cancel'
                on_press: 
                    root.animate_button(self)
                    root.dismiss()
            CustomButton:
                text: 'Add Product'
                on_press: 
                    root.animate_button(self)
                    root.add_product()

<BuyPopup@Popup>:
    title: 'Confirm Purchase'
    size_hint: 0.8, 0.4
    product_name: ''
    product_price: ''
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        Label:
            text: f'Buy {root.product_name} for {root.product_price}'
            font_size: sp(18)
            halign: 'center'
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Label:
                text: 'Quantity:'
                size_hint_x: 0.4
            TextInput:
                id: quantity
                text: '1'
                input_filter: 'int'
                size_hint_x: 0.6
        Label:
            text: 'Total: ' + root.calculate_total()
            font_size: sp(16)
            bold: True
            color: (0.2, 0.5, 0.2, 1)
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            CustomButton:
                text: 'Cancel'
                on_press: 
                    root.animate_button(self)
                    root.dismiss()
            CustomButton:
                text: 'Confirm'
                on_press: 
                    root.animate_button(self)
                    root.confirm_purchase()
''')

class RoleSelectionScreen(Screen):
    def select_role(self, role):
        # Add transition animation
        self.manager.transition = FadeTransition(duration=0.3)
        if role == 'farmer':
            self.manager.current = 'farmer_home'
        else:
            self.manager.current = 'buyer_home'
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)

class FarmerHomeScreen(Screen):
    profile_image = StringProperty('images/profiles/farmer1.png')
    username = StringProperty('Rajesh Kumar')
    location = StringProperty('Punjab, India')
    dark_mode = NumericProperty(0)
    scroll_effect = StringProperty('damped')
    profile_rotation = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(FarmerHomeScreen, self).__init__(**kwargs)
        self.sample_products = [
            {
                'name': 'Organic Tomatoes', 
                'image': 'images/products/tomato.png',
                'price': '₹50/kg',
                'quantity': '100 kg',
                'category': 'Vegetables'
            },
            {
                'name': 'Fresh Carrots', 
                'image': 'images/products/carrot.png',
                'price': '₹40/kg',
                'quantity': '80 kg',
                'category': 'Vegetables'
            },
            {
                'name': 'Wheat Grains', 
                'image': 'images/products/wheat.png',
                'price': '₹30/kg',
                'quantity': '500 kg',
                'category': 'Grains'
            },
            {
                'name': 'Basmati Rice', 
                'image': 'images/products/rice.png',
                'price': '₹80/kg',
                'quantity': '300 kg',
                'category': 'Grains'
            },
            {
                'name': 'Apples', 
                'image': 'images/products/apple.png',
                'price': '₹120/kg',
                'quantity': '50 kg',
                'category': 'Fruits'
            },
            {
                'name': 'Mangoes', 
                'image': 'images/products/mango.png',
                'price': '₹80/kg',
                'quantity': '70 kg',
                'category': 'Fruits'
            },
            {
                'name': 'Potatoes', 
                'image': 'images/products/potato.png',
                'price': '₹35/kg',
                'quantity': '200 kg',
                'category': 'Vegetables'
            },
            {
                'name': 'Onions', 
                'image': 'images/products/onion.png',
                'price': '₹45/kg',
                'quantity': '150 kg',
                'category': 'Vegetables'
            }
        ]
        
        self.orders = [
            {
                'product': 'Organic Tomatoes',
                'image': 'images/products/tomato.png',
                'buyer': 'Priya Sharma',
                'quantity': '20 kg',
                'price': '₹1000',
                'status': 'Delivered'
            },
            {
                'product': 'Fresh Carrots',
                'image': 'images/products/carrot.png',
                'buyer': 'Vikram Singh',
                'quantity': '15 kg',
                'price': '₹600',
                'status': 'In Transit'
            },
            {
                'product': 'Basmati Rice',
                'image': 'images/products/rice.png',
                'buyer': 'Anjali Patel',
                'quantity': '50 kg',
                'price': '₹4000',
                'status': 'Pending'
            }
        ]
    
    def on_enter(self, *args):
        Clock.schedule_once(self.load_products, 0.1)
        Clock.schedule_once(self.load_orders, 0.1)
    
    def load_products(self, *args):
        products_grid = self.ids.products_grid
        products_grid.clear_widgets()
        
        for product in self.sample_products:
            item = ProductItem(
                product_name=product['name'],
                product_image=product['image'],
                product_price=product['price']
            )
            # Add animation
            item.opacity = 0
            anim = Animation(opacity=1, duration=0.5, t='out_quad')
            anim.start(item)
            products_grid.add_widget(item)
    
    def load_orders(self, *args):
        orders_grid = self.ids.orders_grid
        orders_grid.clear_widgets()
        
        for order in self.orders:
            item = OrderItem(
                order_product=order['product'],
                order_image=order['image'],
                order_buyer=f"Buyer: {order['buyer']}",
                order_status=f"Status: {order['status']}",
                order_quantity=f"Qty: {order['quantity']}",
                order_price=f"Total: {order['price']}"
            )
            # Add animation
            item.opacity = 0
            anim = Animation(opacity=1, duration=0.5, t='out_quad')
            anim.start(item)
            orders_grid.add_widget(item)
    
    def search_products(self, query):
        products_grid = self.ids.products_grid
        products_grid.clear_widgets()
        
        if not query:
            self.load_products()
            return
            
        filtered_products = [p for p in self.sample_products if query.lower() in p['name'].lower()]
        
        for product in filtered_products:
            item = ProductItem(
                product_name=product['name'],
                product_image=product['image'],
                product_price=product['price']
            )
            # Add animation
            item.opacity = 0
            anim = Animation(opacity=1, duration=0.5, t='out_quad')
            anim.start(item)
            products_grid.add_widget(item)
    
    def show_add_product_popup(self):
        popup = AddProductPopup()
        popup.bind(on_dismiss=self.load_products)
        popup.open()
    
    def save_profile_changes(self):
        self.username = self.ids.username_input.text
        self.location = self.ids.location_input.text
        self.show_toast("Profile updated successfully!")
    
    def toggle_dark_mode(self, active):
        self.dark_mode = active
        theme = "Dark" if active else "Light"
        self.show_toast(f"{theme} mode enabled")
    
    def rotate_profile(self):
        anim = Animation(profile_rotation=self.profile_rotation + 360, duration=1, t='out_back')
        anim.start(self)
    
    def logout(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'role_selection'
    
    def show_toast(self, message):
        toast = Label(text=message, size_hint_y=None, height=dp(40), 
                      color=(1, 1, 1, 1), bold=True)
        toast_layout = FloatLayout()
        toast_layout.add_widget(toast)
        
        popup = Popup(title='', content=toast_layout, size_hint=(0.8, None), height=dp(50),
                      background_color=(0.2, 0.7, 0.3, 0.9), separator_height=0)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)
    
    def animate_switch(self, switch):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.9, 0.95, 0.9, 1), duration=0.1)
        anim.start(switch)

class BuyerHomeScreen(Screen):
    profile_image = StringProperty('images/profiles/buyer_profile.png')
    username = StringProperty('Buyer User')
    location = StringProperty('Mumbai, India')
    dark_mode = NumericProperty(0)
    scroll_effect = StringProperty('damped')
    profile_rotation = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(BuyerHomeScreen, self).__init__(**kwargs)
        self.all_products = [
            {
                'name': 'Organic Tomatoes', 
                'image': 'images/products/tomato.png',
                'price': '₹50/kg',
                'farmer': 'Rajesh Kumar'
            },
            {
                'name': 'Fresh Carrots', 
                'image': 'images/products/carrot.png',
                'price': '₹40/kg',
                'farmer': 'Rajesh Kumar'
            },
            {
                'name': 'Wheat Grains', 
                'image': 'images/products/wheat.png',
                'price': '₹30/kg',
                'farmer': 'Vikram Singh'
            },
            {
                'name': 'Basmati Rice', 
                'image': 'images/products/rice.png',
                'price': '₹80/kg',
                'farmer': 'Anjali Patel'
            },
            {
                'name': 'Apples', 
                'image': 'images/products/apple.png',
                'price': '₹120/kg',
                'farmer': 'Priya Sharma'
            },
            {
                'name': 'Mangoes', 
                'image': 'images/products/mango.png',
                'price': '₹80/kg',
                'farmer': 'Priya Sharma'
            },
            {
                'name': 'Potatoes', 
                'image': 'images/products/potato.png',
                'price': '₹35/kg',
                'farmer': 'Vikram Singh'
            },
            {
                'name': 'Onions', 
                'image': 'images/products/onion.png',
                'price': '₹45/kg',
                'farmer': 'Anjali Patel'
            }
        ]
        
        self.orders = [
            {
                'product': 'Organic Tomatoes',
                'image': 'images/products/tomato.png',
                'farmer': 'Rajesh Kumar',
                'quantity': '5 kg',
                'price': '₹250',
                'status': 'Delivered'
            },
            {
                'product': 'Basmati Rice',
                'image': 'images/products/rice.png',
                'farmer': 'Anjali Patel',
                'quantity': '10 kg',
                'price': '₹800',
                'status': 'In Transit'
            }
        ]
    
    def on_enter(self, *args):
        Clock.schedule_once(self.load_products, 0.1)
        Clock.schedule_once(self.load_orders, 0.1)
    
    def load_products(self, *args):
        products_grid = self.ids.products_grid
        products_grid.clear_widgets()
        
        for product in self.all_products:
            item = BuyerProductItem(
                product_name=product['name'],
                product_image=product['image'],
                product_price=product['price']
            )
            # Add animation
            item.scale = 0
            anim = Animation(scale=1, duration=0.5, t='out_back')
            anim.start(item)
            products_grid.add_widget(item)
    
    def load_orders(self, *args):
        orders_grid = self.ids.orders_grid
        orders_grid.clear_widgets()
        
        for order in self.orders:
            item = OrderItem(
                order_product=order['product'],
                order_image=order['image'],
                order_buyer=f"Farmer: {order['farmer']}",
                order_status=f"Status: {order['status']}",
                order_quantity=f"Qty: {order['quantity']}",
                order_price=f"Total: {order['price']}"
            )
            # Add animation
            item.opacity = 0
            anim = Animation(opacity=1, duration=0.5, t='out_quad')
            anim.start(item)
            orders_grid.add_widget(item)
    
    def search_products(self, query):
        products_grid = self.ids.products_grid
        products_grid.clear_widgets()
        
        if not query:
            self.load_products()
            return
            
        filtered_products = [p for p in self.all_products if query.lower() in p['name'].lower()]
        
        for product in filtered_products:
            item = BuyerProductItem(
                product_name=product['name'],
                product_image=product['image'],
                product_price=product['price']
            )
            # Add animation
            item.scale = 0
            anim = Animation(scale=1, duration=0.5, t='out_back')
            anim.start(item)
            products_grid.add_widget(item)
    
    def buy_product(self, product_name, product_price):
        popup = BuyPopup(product_name=product_name, product_price=product_price)
        popup.open()
    
    def toggle_dark_mode(self, active):
        self.dark_mode = active
        theme = "Dark" if active else "Light"
        self.show_toast(f"{theme} mode enabled")
    
    def rotate_profile(self):
        anim = Animation(profile_rotation=self.profile_rotation + 360, duration=1, t='out_back')
        anim.start(self)
    
    def save_profile_changes(self):
        self.username = self.ids.username_input.text
        self.location = self.ids.location_input.text
        self.show_toast("Profile updated successfully!")
    
    def logout(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'role_selection'
    
    def show_toast(self, message):
        toast = Label(text=message, size_hint_y=None, height=dp(40), 
                      color=(1, 1, 1, 1), bold=True)
        toast_layout = FloatLayout()
        toast_layout.add_widget(toast)
        
        popup = Popup(title='', content=toast_layout, size_hint=(0.8, None), height=dp(50),
                      background_color=(0.2, 0.7, 0.3, 0.9), separator_height=0)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)
    
    def animate_switch(self, switch):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.9, 0.95, 0.9, 1), duration=0.1)
        anim.start(switch)

class ProductItem(BoxLayout):
    product_name = StringProperty('')
    product_image = StringProperty('')
    product_price = StringProperty('')

class BuyerProductItem(BoxLayout):
    product_name = StringProperty('')
    product_image = StringProperty('')
    product_price = StringProperty('')
    
    def buy_product(self):
        # Get the app instance
        app = App.get_running_app()
        # Get the buyer screen
        buyer_screen = app.root.get_screen('buyer_home')
        # Show buy popup
        buyer_screen.buy_product(self.product_name, self.product_price)
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)

class OrderItem(BoxLayout):
    order_product = StringProperty('')
    order_image = StringProperty('')
    order_buyer = StringProperty('')
    order_status = StringProperty('')
    order_quantity = StringProperty('')
    order_price = StringProperty('')

class AddProductPopup(Popup):
    default_image = StringProperty('images/default_product.png')
    
    def add_product(self):
        # In a real app, you would save the product to a database
        self.dismiss()
        # Show confirmation
        self.show_toast("Product added successfully!")
    
    def show_toast(self, message):
        toast = Label(text=message, size_hint_y=None, height=dp(40), 
                      color=(1, 1, 1, 1), bold=True)
        toast_layout = FloatLayout()
        toast_layout.add_widget(toast)
        
        popup = Popup(title='', content=toast_layout, size_hint=(0.8, None), height=dp(50),
                      background_color=(0.2, 0.7, 0.3, 0.9), separator_height=0)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)

class BuyPopup(Popup):
    product_name = StringProperty('')
    product_price = StringProperty('')
    
    def __init__(self, product_name, product_price, **kwargs):
        super(BuyPopup, self).__init__(**kwargs)
        self.product_name = product_name
        self.product_price = product_price
    
    def calculate_total(self):
        try:
            quantity = int(self.ids.quantity.text)
            price = float(self.product_price.split('₹')[1].split('/')[0])
            total = quantity * price
            return f'₹{total:.2f}'
        except:
            return '₹0.00'
    
    def confirm_purchase(self):
        try:
            quantity = int(self.ids.quantity.text)
            price = float(self.product_price.split('₹')[1].split('/')[0])
            total = quantity * price
            
            # Get the app instance
            app = App.get_running_app()
            # Get the buyer screen
            buyer_screen = app.root.get_screen('buyer_home')
            
            # Add to orders
            new_order = {
                'product': self.product_name,
                'image': f'images/products/{self.product_name.replace(" ", "_").lower()}.png',
                'farmer': 'New Farmer',
                'quantity': f'{quantity} kg',
                'price': f'₹{total:.2f}',
                'status': 'Processing'
            }
            buyer_screen.orders.insert(0, new_order)
            buyer_screen.load_orders()
            
            # Show success message
            buyer_screen.show_toast(f"Order placed for {quantity} kg of {self.product_name}!")
            self.dismiss()
        except Exception as e:
            print(f"Error: {e}")
            self.show_toast("Invalid quantity")
    
    def show_toast(self, message):
        toast = Label(text=message, size_hint_y=None, height=dp(40), 
                      color=(1, 1, 1, 1), bold=True)
        toast_layout = FloatLayout()
        toast_layout.add_widget(toast)
        
        popup = Popup(title='', content=toast_layout, size_hint=(0.8, None), height=dp(50),
                      background_color=(0.8, 0.2, 0.2, 0.9), separator_height=0)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    
    def animate_button(self, button):
        anim = Animation(background_color=(0.1, 0.8, 0.3, 1), duration=0.1) + \
               Animation(background_color=(0.2, 0.7, 0.3, 1), duration=0.1)
        anim.start(button)

class HTFApp(App):
    def build(self):
        self.title = "Help The Farmers"
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(RoleSelectionScreen(name='role_selection'))
        sm.add_widget(FarmerHomeScreen(name='farmer_home'))
        sm.add_widget(BuyerHomeScreen(name='buyer_home'))
        return sm

if __name__ == '__main__':
    HTFApp().run()
