from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import subprocess
import urllib.parse
from os.path import exists as file_exists

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Enter Website URL : ')

async def downloading(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Downloading please wait...')
    web_url = update.message.text
    parsed_url = urllib.parse.urlparse(web_url)
    web_host = parsed_url.netloc

    if file_exists(f'./{web_host}'):
        pass
    else:
        runcmd(f'wget --mirror --convert-links --adjust-extension --page-requisites --no-parent {web_url}', verbose = True)

    if file_exists(f'./{web_host}.zip'):
        pass
    else:
        runcmd(f'zip -r {web_host}.zip {web_host}', verbose = True)

    await update.message.reply_document(f'{web_host}.zip')

app = ApplicationBuilder().token("5841321451:AAFXw0yt4wZRq1GokonT9AoUpl7m6xWv804").build()


app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("download", download))
app.add_handler(MessageHandler(filters.TEXT, downloading))

app.run_polling()
