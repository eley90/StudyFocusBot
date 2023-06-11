""" Here is room No. 2"""
import discord
import os
from keep_alive import keep_alive
import asyncio
from random import randint
from datetime import datetime as datetime, date
import time
from user import User, session, StudySession, Achievement

client = discord.Client(intents=discord.Intents.all())

users = dict()  # has this structure {'user_id': user obj}
end_flag = True
start_flag = False
study_session = None

channel = client.get_channel('channel_id')


async def timer(channel):
    while True:
        await asyncio.sleep(3600)
        await channel.send(
            'Dear Students :raised_hands:\nThe study session is over.Please type end in the text-channel and enter how many task you have completed.\nI hope you had a great learning experience and hope to see you soon :thumbsup::skin-tone-1:')


@client.event
async def help_fnct():

    channel = client.get_channel('channel_id')
    content = ':warning:Available commands:\n:arrow_right: **start** - to start a study session\n:arrow_right: **task** followed by the task itself - to enter the task for the session\nEx: task: read chapter 1 or task do exercise 1\n:arrow_right: **show** - to have an overview of your current tasks\n:arrow_right: **del** followed by the task - to delete a task\nEx: del read chapter 1\n:arrow_right: **p** - to send an angry notification if your study partner is distracted\n__also available in the chat from the voice-channel__\n:arrow_right: **end** - to end the study session\n:exclamation: You will receive a reminder towards the end of the study session that it is ending.'

    allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)  # Allow no mentions
    await channel.send(content, allowed_mentions=allowed_mentions)


@client.event
async def check_achievements(user):

    channel = client.get_channel('channel_id')
    last_session = session.query(StudySession).order_by(StudySession.end_time.desc()).first()
    if last_session:
        last_achievement = session.query(Achievement).join(StudySession).filter(Achievement.user == user).filter(
            Achievement.study_session == last_session).order_by(StudySession.end_time.desc()).first()
        if last_achievement:
            previous_achievements = session.query(Achievement).join(StudySession).filter(
                Achievement.user == user).filter(Achievement.study_session != last_session).order_by(
                StudySession.end_time.desc()).all()
            if previous_achievements:
                previous_avg = sum([ach.value for ach in previous_achievements]) / len(previous_achievements)
                if last_achievement.value > previous_avg:
                    await channel.send(
                        f"{user.user_name} Congratulations! Your achievement in the last study session is better than your average achievements in previous sessions.")
                elif last_achievement.value < previous_avg:
                    await channel.send(
                        f"{user.user_name} Your achievement in the last study session is lower than your average achievements in previous sessions. Keep up the good work and improve!")
                else:
                    await channel.send(
                        f" {user.user_name}Your achievement in the last study session is the same as your average achievements in previous sessions. Keep up the good work!")
            else:
                await channel.send(
                    f" {user.user_name} This is your first study session. Keep up the good work and improve!")
        else:
            await channel.send(f"{user.user_name} You have not completed any tasks in the last study session.")
    else:
        await channel.send(f"{user.user_name} There are no study sessions recorded yet.")


@client.event
async def task():

    channel = client.get_channel('channel_id')
    await asyncio.sleep(2)
    content = ":exclamation:Enter your **tasks** by typing: task: example of a task"
    allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)
    await channel.send(content, allowed_mentions=allowed_mentions)


@client.event
async def start_session():

    channel = client.get_channel('channel_id')
    await channel.send("Welcome Study Buddies :smiley:\n")
    await asyncio.sleep(2)
    content = "\nPlease enter either **1** or **2** to __START__.\n:question:To have an overview of the available commands type **!help**."
    allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)  #
    await channel.send(content, allowed_mentions=allowed_mentions)
    await task()
    client.loop.create_task(timer(channel))


@client.event
async def end_session():

    channel = client.get_channel('channel_id')
    duration = study_session.end_time - study_session.start_time
    seconds = duration.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    with open('done.gif', 'rb') as gif_file:
        await channel.send(file=discord.File(gif_file, 'file.gif'))
    embed = discord.Embed(
        description=f"Congratulations, you have completed your study session!\nYour session lasted {hours} hours and {minutes} minutes",
        color=discord.Color.green())
    await channel.send(embed=embed)
    for user in users:
        await channel.send("How many tasks have you done completely {}? ".format(
            users[user].user_name.split('#')[0]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    author = message.author

    global end_flag, start_flag, study_session, start_time

    if msg.isnumeric():
        if end_flag and not start_flag:
            user_temp = users[str(author.id)]
            user_temp.comp_tasks = float(msg)
            points = user_temp.calculate_points(study_session=study_session)

            dana = await client.fetch_user('757894678027698197')
            elmira = await client.fetch_user('439071369163046913')

            await message.channel.send('{} your points:\t{}'.format(
                user_temp.user_name, points))

            await check_achievements(user_temp)
            channel = client.get_channel(1090673713374044273)
            await channel.send(embed=discord.Embed(
                description=f"** {user_temp.user_name} Please provide a brief summary to your study partner about the tasks and materials you learned in the session**",
                color=discord.Color.red()))
            if float(points):
                await dana.send('{} user: {} has accumulated {} points'.format(
                    date.today(), user_temp, points))
                await elmira.send('{} user: {} has accumulated {} points'.format(
                    date.today(), user_temp, points))

        if msg.__eq__('1') and (str(author.id) not in users) and not end_flag:
            user = User(str(author), author.id)
            existed_user = session.query(User).filter_by(user_id=user.user_id).first()
            if not existed_user:
                session.add(user)
                session.commit()
            users.update({'{}'.format(author.id): user})
            await message.delete()
        elif msg.__eq__('2') and (str(author.id) not in users) and not end_flag:
            user = User(str(author), author.id)
            existed_user = session.query(User).filter_by(user_id=user.user_id).first()
            if not existed_user:
                session.add(user)
                session.commit()
            users.update({'{}'.format(author.id): User(str(author), author.id)})
            await message.delete()

        elif str(author.id) in users and not end_flag:
            await asyncio.gather(
                message.channel.send("{} you are already a member!!".format(str(author).split('#')[0])),
                message.delete())

    elif not msg.isnumeric():
        if msg.__eq__('start study session') or msg.__eq__('start') and (
                not start_flag) and end_flag:
            users.clear()
            end_flag = False
            start_flag = True
            start_time = time.time()
            study_session = StudySession(start_time=datetime.utcnow())
            session.add(study_session)
            session.commit()
            await start_session()
            while not end_flag and start_flag:
                await asyncio.sleep(randint(600, 1200))
                users_ids = list(users.keys())
                user_one = users_ids[0]
                user_two = users_ids[1]
                user_1 = await client.fetch_user(int(user_one))
                user_2 = await client.fetch_user(int(user_two))
                await user_1.send("This is a reminder to check on your study partner!")
                await asyncio.sleep(randint(480, 720))
                await user_2.send("This is a reminder to check on your study partner!")

        elif msg.__eq__('p') and not end_flag and start_flag:
            voice_channel = client.get_channel(1090673713374044275)
            if len(users) == 2:
                for user_id in users:
                    if user_id != str(author.id):
                        users[str(user_id)].update_credit_points()

                        await asyncio.gather(message.channel.send("{} PAY ATTENTION!!!".format(
                            users[user_id].user_name)), message.channel.send(":rage:\n{} PAY ATTENTION!!!".format(
                            users[user_id].user_name)), message.delete())
                        with open('angry2.gif', 'rb') as gif_file:
                            await message.channel.send(file=discord.File(gif_file, 'file.gif'))
                            await voice_channel.send(file=discord.File(gif_file, 'file.gif'))
            else:
                embed = discord.Embed(description="NO OTHER USER", color=discord.Color.red())
                await asyncio.gather(message.channel.send(embed=embed), message.delete())


        elif (msg.startswith('task')) and (str(
                author.id) in users) and (not end_flag) and start_flag:

            users[str(author.id)].update_tasks(msg[5:], study_session)
            await message.delete()

        elif (msg.startswith('show')) and (str(
                author.id) in users) and (not end_flag) and start_flag:
            if len(users[str(author.id)].tasks) > 0 and (str(author.id) in users):
                i = 1
                for task in users[str(author.id)].tasks:
                    if task.study_session == study_session:
                        if i == 1:
                            await message.channel.send("Here your tasks {}:".format(str(author).split('#')[0]))

                        embed = discord.Embed(description=f"{str(i)}" + "." + f"{task.name}",
                                              color=discord.Color.blurple())
                        await message.channel.send(embed=embed)

                        i += 1

            else:
                await message.channel.send(
                    f"{str(author).split('#')[0]} you have not set any tasks for this session yet.")

        elif (msg.startswith('del')) and (str(author.id) in users) and not end_flag and start_flag:
            task = msg[4:]
            delete_msg = users[str(author.id)].delete_task(task, study_session)
            await asyncio.gather(message.channel.send(delete_msg), message.delete())

        elif (msg.startswith('end')) and (str(
                author.id) in users) and (not end_flag) and start_flag:
            end_flag = True
            start_flag = False
            study_session.end_time = datetime.utcnow()
            session.commit()
            await end_session()
            jobs = [job for job in asyncio.all_tasks() if job._coro.__name__ == 'timer']
            for job in jobs:
                job.cancel()

        elif (msg.startswith('!help')):
            await help_fnct()
        elif end_flag and not start_flag:
            await message.channel.send(
                "The session has stopped\nYou should start a new session!")


client.run(os.getenv('TOKEN'))
keep_alive()



