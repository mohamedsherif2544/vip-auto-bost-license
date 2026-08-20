import requests
import json
import time
import telebot

# ===== توكن البوت بتاعك =====
BOT_TOKEN = '8787621277:AAHs1EWT6AIgzmTjkhvm8ntSHK-KT-udNjw'

bot = telebot.TeleBot(BOT_TOKEN)

# ===== عنوان السيرفر =====
SERVER_URL = 'https://mohamedsherif3032.pythonanywhere.com'

# ===== أمر بدء التشغيل =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🤖 **مرحباً بك في بوت إدارة الترخيص!**\n\n"
        "📋 **الأوامر المتاحة:**\n"
        "🔹 /add_device AA:BB:CC:DD:EE:FF - إضافة جهاز\n"
        "🔹 /remove_device AA:BB:CC:DD:EE:FF - حذف جهاز\n"
        "🔹 /list_devices - عرض الأجهزة المسموحة"
    )

# ===== أمر إضافة جهاز =====
@bot.message_handler(commands=['add_device'])
def add_device(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ استخدم: /add_device AA:BB:CC:DD:EE:FF")
            return
        
        device_mac = parts[1].strip().upper()
        
        response = requests.post(
            f"{SERVER_URL}/add_device",
            json={'device': device_mac, 'name': message.from_user.first_name}
        )
        
        if response.status_code == 200:
            bot.reply_to(message, f"✅ تم إضافة الجهاز: {device_mac}")
        else:
            bot.reply_to(message, "❌ حدث خطأ في الإضافة")
            
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

# ===== أمر حذف جهاز =====
@bot.message_handler(commands=['remove_device'])
def remove_device(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "❌ استخدم: /remove_device AA:BB:CC:DD:EE:FF")
            return
        
        device_mac = parts[1].strip().upper()
        
        response = requests.post(
            f"{SERVER_URL}/remove_device",
            json={'device': device_mac}
        )
        
        if response.status_code == 200:
            bot.reply_to(message, f"✅ تم حذف الجهاز: {device_mac}")
        else:
            bot.reply_to(message, "❌ حدث خطأ في الحذف")
            
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {str(e)}")

# ===== أمر عرض الأجهزة =====
@bot.message_handler(commands=['list_devices'])
def list_devices(message):
    try:
        response = requests.get(f"{SERVER_URL}/list_devices")
        devices = response.json()
        
        if not devices:
            bot.reply_to(message, "📭 لا يوجد أجهزة مسموحة حالياً")
            return
        
        msg = "📱 **الأجهزة المسموحة:**\n━━━━━━━━━━━━━━━━━━━\n"
        for mac, info in devices.items():
            name = info.get('name', 'مستخدم')
            msg += f"🔹 `{mac}`\n   👤 {name}\n\n"
        
        bot.reply_to(message, msg, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ في جلب البيانات: {str(e)}")

# ===== أمر مساعدة =====
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
        "🆘 **قائمة الأوامر:**\n\n"
        "/start - عرض الترحيب\n"
        "/help - عرض المساعدة\n"
        "/add_device AA:BB:CC:DD:EE:FF - إضافة جهاز\n"
        "/remove_device AA:BB:CC:DD:EE:FF - حذف جهاز\n"
        "/list_devices - عرض الأجهزة المسموحة"
    )

# ===== تشغيل البوت =====
if __name__ == '__main__':
    # === حذف الويب هوك أولاً ===
    try:
        bot.remove_webhook()
        print("✅ تم حذف الويب هوك بنجاح")
    except Exception as e:
        print(f"⚠️ خطأ في حذف الويب هوك: {e}")
    
    print("🚀 البوت شغال على جهازك المحلي!")
    bot.polling(none_stop=True)