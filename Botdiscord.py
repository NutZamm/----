import discord
from discord import File

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    channel = client.get_channel(123456789) # ใส่ ID ของ Channel ที่ต้องการให้ Bot แจ้งเตือน
    await member.create_dm() # สร้างห้อง DM ของผู้ใช้งานที่เข้าร่วม
    await member.dm_channel.send(f'สวัสดี {member.name}, ยินดีต้อนรับสู่เซิร์ฟเวอร์ของเรา!') # ส่งข้อความต้อนรับไปยังห้อง DM ของผู้ใช้งาน
    if member.avatar:
        file = await member.avatar_url_as(size=128).read() # ดึงภาพโปรไฟล์ของผู้ใช้งาน
        await channel.send(f'{member.mention} ได้เข้าร่วมเซิร์ฟเวอร์เรา', file=File(file, filename='profile.png')) # แนบภาพโปรไฟล์และส่งข้อความแจ้งเตือนไปยัง Channel ที่เราต้องการให้แจ้งเตือน
    else:
        await channel.send(f'{member.mention} ได้เข้าร่วมเซิร์ฟเวอร์เรา') # ส่งข้อความแจ้งเตือนไปยัง Channel ที่เราต้องการให้แจ้งเตือน

@client.event
async def on_member_remove(member):
    channel = client.get_channel(123456789) # ใส่ ID ของ Channel ที่ต้องการให้ Bot แจ้งเตือน
    if member.avatar:
        file = await member.avatar_url_as(size=128).read() # ดึงภาพโปรไฟล์ของผู้ใช้งาน
        await channel.send(f'{member.mention} ได้ออกจากเซิร์ฟเวอร์เรา', file=File(file, filename='profile.png')) # แนบภาพโปรไฟล์และส่งข้อความแจ้งเตือนไปยัง Channel ที่เราต้องการให้แจ้งเตือน
    else:
        await channel.send(f'{member.mention} ได้ออกจากเซิร์ฟเวอร์เรา') # ส่งข้อความแจ้งเตือนไปยัง Channel ที่เราต้องการให้แจ้งเตือน
        
        
client.run('your-bot-token-goes-here')
