import random
from dataclasses import dataclass, field
from typing import Optional
import uuid

WHO_QUESTIONS = [
    "کی بیشتر احتمال داره دوست‌دخترشو ننه صدا کنه؟",
    "کی بیشتر احتمال داره بعد از ۲ تا نوشیدنی گریه کنه؟",
    "کی بیشتر احتمال داره استوری ex خودشو هنوز چک کنه؟",
    "کی بیشتر احتمال داره بدون هیچ دلیلی یه نفر رو ghost کنه؟",
    "کی بیشتر احتمال داره با اولین کسی که بهش توجه کنه بره؟",
    "کی بیشتر احتمال داره مامانش جواب تلفنشو بده؟",
    "کی بیشتر احتمال داره بدون سوال بخوره بعد بپرسه چیه؟",
    "کی بیشتر احتمال داره تو بدترین وقت ممکن عاشق بشه؟",
    "کی بیشتر احتمال داره یه راز بزرگ داشته باشه که هیچ‌کس نمی‌دونه؟",
    "کی بیشتر احتمال داره سر یه قرار مهم دیر بیاد؟",
    "کی بیشتر احتمال داره اگه مشهور بشه همه رو فراموش کنه؟",
    "کی بیشتر احتمال داره تو رستوران از بشقاب بقیه بخوره؟",
    "کی بیشتر احتمال داره یه پیام خجالت‌آور اشتباهی بفرسته؟",
    "کی بیشتر احتمال داره تنها پیری کنه؟",
    "کی بیشتر احتمال داره گریه‌اش از یه فیلم بگیره؟",
    "کی بیشتر احتمال داره تو مهمونی به اتاق خواب پناه ببره؟",
    "کی بیشتر احتمال داره با غریبه‌ها راحت‌تر از آشناها باشه؟",
    "کی بیشتر احتمال داره تو امتحان تقلب کنه؟",
    "کی بیشتر احتمال داره بیشتر از همه بخوره؟",
    "کی بیشتر احتمال داره ادا آدم‌های مشهور رو دربیاره؟",
    "کی بیشتر احتمال داره برای رفیقش بیشتر از خودش غم بخوره؟",
    "کی بیشتر احتمال داره هرجایی بخوابه؟",
    "کی بیشتر احتمال داره از یه چیز ترسناک فیلم بگیره به‌جای فرار؟",
    "کی بیشتر احتمال داره همه رو ببخشه حتی وقتی نباید؟",
    "کی بیشتر احتمال داره بدون آرایش از خونه نره؟",
    "کی بیشتر احتمال داره اگه رئیس بشه آدم سختگیری بشه؟",
    "کی بیشتر احتمال داره تو بازی تقلب کنه؟",
    "کی بیشتر احتمال داره یه نفر رو فقط با یه جمله عاشق خودش کنه؟",
    "کی بیشتر احتمال داره تو خواب حرف بزنه؟",
    "کی بیشتر احتمال داره همه چیز رو به تأخیر بندازه؟",
    "کی بیشتر احتمال داره یه قرار کنسل کنه آخرین لحظه؟",
    "کی بیشتر احتمال داره خودشو عاقل‌ترین نفر فکر کنه؟",
    "کی بیشتر احتمال داره بیشتر از همه بدشانس باشه؟",
    "کی بیشتر احتمال داره بعد از یه شکست سریع بلند شه؟",
    "کی بیشتر احتمال داره اول بگه نه بعد بگه باشه؟",
    "کی بیشتر احتمال داره وقتی ناراحته بخنده؟",
    "کی بیشتر احتمال داره یه آدم سمی رو نگه داره چون تنهاست؟",
    "کی بیشتر احتمال داره تو دل همه باشه ولی رو زبون هیچ‌کس نباشه؟",
    "کی بیشتر احتمال داره یه بار دیگه به کسی که بهش آسیب زده اعتماد کنه؟",
    "کی بیشتر احتمال داره شب تولدش گریه کنه؟",
    # new batch
    "کی بیشتر احتمال داره یه پست پاک کنه چون لایک کمه؟",
    "کی بیشتر احتمال داره تو دستشویی موزیک گوش بده و آواز بخونه؟",
    "کی بیشتر احتمال داره سر یه موضوع پیش‌پاافتاده ۳ ساعت حرف بزنه؟",
    "کی بیشتر احتمال داره قبل از خواب یه ساعت بی‌هدف تو گوشی باشه؟",
    "کی بیشتر احتمال داره یه جمله رو ۱۰ بار ویرایش کنه قبل از فرستادن؟",
    "کی بیشتر احتمال داره موزیک غمگین گوش بده ولی حالش خوب باشه؟",
    "کی بیشتر احتمال داره از آدم‌های دیر پاسخ‌ده متنفر باشه ولی خودش دیر جواب بده؟",
    "کی بیشتر احتمال داره بگه «یه دقیقه» و یه ساعت بگذره؟",
    "کی بیشتر احتمال داره تو رستوران آخرین نفری باشه که غذاشو انتخاب کنه؟",
    "کی بیشتر احتمال داره وقتی عصبانیه بره آشپزخونه و چیزی بخوره؟",
    "کی بیشتر احتمال داره بدون اینکه کتابو تموم کنه ادعا کنه خوندتش؟",
    "کی بیشتر احتمال داره گیر یه موضوع فلسفی بیفته ساعت ۳ صبح؟",
    "کی بیشتر احتمال داره اول بگه «من نمیام» بعد اول از همه برسه؟",
    "کی بیشتر احتمال داره یه آدم رو دوست نداشته باشه ولی لایکشو بزنه؟",
    "کی بیشتر احتمال داره با یه اشتباه کوچیک یه هفته ناراحت بمونه؟",
    "کی بیشتر احتمال داره تو مهمونی با سگ یا گربه خونه بیشتر کنار باشه تا آدما؟",
    "کی بیشتر احتمال داره برای انجام ندادن یه کار صد تا بهانه داشته باشه؟",
    "کی بیشتر احتمال داره موقع دعوا بدترین چیزها رو بگه و بعد پشیمون بشه؟",
    "کی بیشتر احتمال داره بدون اطلاع قبلی ساعت ۳ شب بیاد در خونت؟",
    "کی بیشتر احتمال داره تو بدترین لحظه سلفی بگیره؟",
    "کی بیشتر احتمال داره یه رمز عبور رو ده بار اشتباه بزنه؟",
    "کی بیشتر احتمال داره شبا بخوابه ولی ساعت ۳ بیدار بشه و استوری بذاره؟",
    "کی بیشتر احتمال داره اگه ثروتمند بشه فراموش کنه از کجا اومده؟",
    "کی بیشتر احتمال داره تو جمع وانمود کنه حالش خوبه؟",
    "کی بیشتر احتمال داره از موقعیت ناخوشایند فرار کنه به جای رو به رو شدن؟",
    "کی بیشتر احتمال داره تو ماشین آواز بخونه وقتی تنهاست؟",
    "کی بیشتر احتمال داره دروغ مصلحتی بگه ولی خودش باورش بشه؟",
    "کی بیشتر احتمال داره با مامانش از دست تو شکایت کنه؟",
    "کی بیشتر احتمال داره حتی تو تعطیلات ایمیل کاری چک کنه؟",
    "کی بیشتر احتمال داره به اسم دیگه‌ای ذخیره‌ات کنه؟",
    "کی بیشتر احتمال داره یه ماه رژیم بگیره ولی روز اول بشکنه؟",
    "کی بیشتر احتمال داره هزار بار بگه «آخرین باره» ولی نباشه؟",
    "کی بیشتر احتمال داره تو صف ایستاده تلفنی دعوا کنه؟",
    "کی بیشتر احتمال داره یه نقشه بزرگ بکشه و هیچ‌وقت عملیش نکنه؟",
    "کی بیشتر احتمال داره عاشق کسی بشه که خیلی شبیه خودشه؟",
    "کی بیشتر احتمال داره هر شب یه پروفایل مختلف رو استالک کنه؟",
    "کی بیشتر احتمال داره وسط یه فیلم جدی بخنده؟",
    "کی بیشتر احتمال داره اگه پول زیاد داشته باشه همه رو خرج سفر کنه؟",
    "کی بیشتر احتمال داره تو مکالمه بقیه رو تصحیح کنه؟",
    "کی بیشتر احتمال داره به جای عذرخواهی هدیه بخره؟",
    "کی بیشتر احتمال داره از کسی که باهاش دعوا کرده چیزی بخواد ولی اول ببخشدش؟",
    # gen z / edgy batch
    "کی بیشتر احتمال داره با ChatGPT درد و دل کنه؟",
    "کی بیشتر احتمال داره یه پست بذاره، لایک کم باشه، پاکش کنه، دوباره بذاره؟",
    "کی بیشتر احتمال داره از یه ری‌اکشن اشتباه زیر پست سه روز اضطراب داشته باشه؟",
    "کی بیشتر احتمال داره تیک‌تاک بذاره ولی بعد از یه ساعت بترسه پاکش کنه؟",
    "کی بیشتر احتمال داره aesthetic فیدش مهم‌تر از واقعیتش باشه؟",
    "کی بیشتر احتمال داره وقتی جواب نمیده seen بذاره ولی بگه ندیدم؟",
    "کی بیشتر احتمال داره از یه meme بیشتر از یه خبر مهم گریه‌اش بگیره؟",
    "کی بیشتر احتمال داره یه آدم سمی رو فقط برای دیدن دعواش فالو کنه؟",
    "کی بیشتر احتمال داره از یه نفر unfollow کنه چون یه پست ناراحتش کرد؟",
    "کی بیشتر احتمال داره reply to story رو به‌عنوان استراتژی دیتینگ استفاده کنه؟",
    "کی بیشتر احتمال داره وقتی عاشق کسیه همه لینکداین و اینستا و اسپاتیفای‌شو چک کنه؟",
    "کی بیشتر احتمال داره اگه سلبریتی‌ای دنبلش کنه جیغ بزنه؟",
    "کی بیشتر احتمال داره از طرز نگاه کردن یه غریبه سراغ اینستاشو بگیره؟",
    "کی بیشتر احتمال داره اگه کسی باهاش گرم باشه فکر کنه عاشقشه؟",
    "کی بیشتر احتمال داره یه آهنگ بذاره بعد بگه «این دقیقاً منم»؟",
    "کی بیشتر احتمال داره لیست آهنگ‌هاش نشون‌دهنده‌ی واقعی‌ترین حسش باشه؟",
    "کی بیشتر احتمال داره یه آهنگ رو ۵۰ بار پشت سر هم گوش بده؟",
    "کی بیشتر احتمال داره تو پارتی بیشتر وقتش رو با گوشیش بگذرونه؟",
    "کی بیشتر احتمال داره تو خلوت آدم کاملاً متفاوتی باشه؟",
    "کی بیشتر احتمال داره وقتی ناراحته به هیچ‌کس نگه و بخنده؟",
    "کی بیشتر احتمال داره به‌جای خواب تا صبح ریلز ببینه؟",
    "کی بیشتر احتمال داره یه جواب passive-aggressive بده و بگه «چیزی نیست»؟",
    "کی بیشتر احتمال داره شبانه یه متن طولانی بفرسته و صبح پشیمون بشه؟",
    "کی بیشتر احتمال داره تو گروه pretend کنه داره گوش میده ولی گوش نمیده؟",
    "کی بیشتر احتمال داره از یه چیز کوچیک بزرگ‌ترین دراما رو بسازه؟",
    "کی بیشتر احتمال داره قبل از خواب هزار تا فکر کنه که نکنه یه چیز اشتباه گفته باشه؟",
    "کی بیشتر احتمال داره روز جمعه شب لیست هفته بنویسه و هیچ‌کدوم رو انجام نده؟",
    "کی بیشتر احتمال داره از یه compliment ساده ذوب بشه و نفهمه چی بگه؟",
    "کی بیشتر احتمال داره از یه نفر که بهش صادق بوده دلخور بشه؟",
    "کی بیشتر احتمال داره از یه رفیق به‌خاطر پیام ندادن ناراحت بشه ولی چیزی نگه؟",
    "کی بیشتر احتمال داره یه سری ذهن‌خوانی کنه و کل اشتباه باشه؟",
    "کی بیشتر احتمال داره وقتی کسی agree می‌کنه ذوق کنه انگار جایزه گرفته؟",
    "کی بیشتر احتمال داره از اینکه کسی پیاماشو آبی کرده ولی جواب نداده عصبانی بشه؟",
    "کی بیشتر احتمال داره تو هر جمعی devil's advocate باشه؟",
    "کی بیشتر احتمال داره وقتی یه چیز خوب بهش میگن گریه‌اش بگیره؟",
    "کی بیشتر احتمال داره به‌جای خوابیدن داستان‌های خودساخته تو ذهنش بسازه؟",
    "کی بیشتر احتمال داره یه چیز random بخره و بعد هرگز استفاده نکنه؟",
    "کی بیشتر احتمال داره تو شلوغ‌ترین لحظه حس کنه تنهاترینه؟",
    "کی بیشتر احتمال داره همه چیز رو با هوش مصنوعی تست کنه؟",
    "کی بیشتر احتمال داره هنوز به اولین عشقش فکر کنه؟",
    "کی بیشتر احتمال داره یه رابطه طولانی رو فقط با یه پیام تموم کنه؟",
    "کی بیشتر احتمال داره از یه غریبه تو مترو خوشش بیاد و هیچی نگه؟",
    "کی بیشتر احتمال داره یه چیز مهم رو از ترس قضاوت مخفی نگه داره؟",
    "کی بیشتر احتمال داره تو آیینه با خودش تمرین مکالمه کنه؟",
    "کی بیشتر احتمال داره از یه کسی که بهش گفته «یه بار دیگه» هنوز منتظر باشه؟",
    "کی بیشتر احتمال داره تو دعوا آروم‌ترین باشه ولی بعدش بیشترین آسیب رو ببینه؟",
    "کی بیشتر احتمال داره یه رفیقشو به غریبه‌ها بهتر از خودش توصیف کنه؟",
    "کی بیشتر احتمال داره اگه بهش بگن «از کی دوسم داری» یخ کنه؟",
    "کی بیشتر احتمال داره از یه ماجراجویی دوری کنه چون جوابش رو از قبل میدونه؟",
    "کی بیشتر احتمال داره همه‌چیزشو برای یه آدم خاص عوض کنه؟",
    "کی بیشتر احتمال داره از یه نفری که کمش کرده دفاع کنه؟",
    "کی بیشتر احتمال داره وقتی گریه می‌کنه صدا نکنه؟",
    "کی بیشتر احتمال داره اگه بهش بگی «ازت ناامید شدم» دو هفته اذیتش کنه؟",
    "کی بیشتر احتمال داره تو گروه خانوادگی چیزی اشتباهی فوروارد کنه؟",
    "کی بیشتر احتمال داره از یه چیز embarrassing ده سال پیش هنوز خجالت بکشه؟",
    "کی بیشتر احتمال داره اول همه بخنده بعد بفهمه چی گفتن؟",
    "کی بیشتر احتمال داره برای سرگرمی یه بار dating app نصب کنه؟",
    "کی بیشتر احتمال داره از یه فیلم هندی واقعاً گریه کنه؟",
    "کی بیشتر احتمال داره از اینکه کسی بهش «cute» بگه ناراحت بشه؟",
    "کی بیشتر احتمال داره برای یه نفر سه تا backup plan داشته باشه؟",
    "کی بیشتر احتمال داره یه رابطه سمی رو نگه داره چون از تنهایی می‌ترسه؟",
    "کی بیشتر احتمال داره از یه قرار فرار کنه به بهانه سردرد؟",
    "کی بیشتر احتمال داره وقتی دیده میشه خجالت بکشه ولی وقتی تنهاست کلاً رهاست؟",
    "کی بیشتر احتمال داره وقتی گرسنه‌ست بدترین تصمیم‌ها رو بگیره؟",
    "کی بیشتر احتمال داره روز قبل از امتحان کل کتاب رو از اول بخونه؟",
    "کی بیشتر احتمال داره از خرید آنلاین پشیمون بشه ولی یه ماه بعد دوباره همونو بخره؟",
    "کی بیشتر احتمال داره یه آهنگ غمگین بذاره فقط برای اینکه حالشو بدتر کنه؟",
    "کی بیشتر احتمال داره برای انجام ندادن یه کار صد تا توجیه منطقی داشته باشه؟",
    "کی بیشتر احتمال داره به‌جای عذرخواهی مستقیم یه پیام passive بفرسته؟",
    "کی بیشتر احتمال داره از یه آدم بدش بیاد ولی پستاشو هنوز چک کنه؟",
    "کی بیشتر احتمال داره وقتی می‌خنده دستشو جلو دهنش بگیره؟",
    "کی بیشتر احتمال داره یه تیپ شیک بپوشه ولی کفشش کثیف باشه؟",
    "کی بیشتر احتمال داره هر چیزی که می‌خوره ازش ریلز بگیره؟",
    "کی بیشتر احتمال داره در حین گریه سلفی بگیره؟",
    "کی بیشتر احتمال داره واقعاً باور کنه کاملاً منحصربه‌فرده؟",
    "کی بیشتر احتمال داره از یه کافه به‌خاطر وای‌فای سریعش عاشقش بشه؟",
    "کی بیشتر احتمال داره یه آدم رو استالک کنه که اصلاً نمیشناسدش؟",
    "کی بیشتر احتمال داره وقتی دوستش داره حرف می‌زنه تو ذهنش چیز دیگه‌ای فکر می‌کنه؟",
    "کی بیشتر احتمال داره اگه براش سورپرایز بزنن گریه کنه؟",
    "کی بیشتر احتمال داره از یه آدم خسته‌کننده نتونه فرار کنه و ساعت‌ها گوش بده؟",
    "کی بیشتر احتمال داره بعد از یه شب بد یه thread بلند بنویسه؟",
    "کی بیشتر احتمال داره خودشو نسل‌جدیدی‌ترین آدم جمع بدونه؟",
    "کی بیشتر احتمال داره وقتی می‌فهمه کسی ازش خوشش نمیاد کلاً خراب بشه؟",
    "کی بیشتر احتمال داره یه پلن کنسل کنه چون دیشب خیلی خوابیده و حالش نیست؟",
    "کی بیشتر احتمال داره به‌جای حل مشکل تو خودش بمونه؟",
    "کی بیشتر احتمال داره یه نقشه بزرگ برای زندگیش داشته باشه که به هیچ‌کس نگفته؟",
    "کی بیشتر احتمال داره وقتی تنهاست با خودش بلند حرف بزنه؟",
    "کی بیشتر احتمال داره از یه چیزی که گفته پشیمون بشه ولی continue بده؟",
    "کی بیشتر احتمال داره تو یه دروغ کوچیک گیر کنه و مجبور بشه یه دروغ بزرگ‌تر بگه؟",
    "کی بیشتر احتمال داره یه رشته توییت بخونه و گریه‌اش بگیره؟",
    "کی بیشتر احتمال داره از رقیب قدیمیش بهتر بشه فقط برای اینکه بهتره؟",
    "کی بیشتر احتمال داره همه چیز رو بیش از حد تحلیل کنه؟",
    "کی بیشتر احتمال داره یه لحظه‌ی awkward رو تا ابد تو ذهنش نگه داره؟",
    "کی بیشتر احتمال داره از شنیدن یه آهنگ خاص آدم متفاوتی بشه؟",
    "کی بیشتر احتمال داره تو بحث اصلی‌ترین آدم باشه حتی اگه دعوا نباشه؟",
    "کی بیشتر احتمال داره یه نفر رو secretly admire کنه و هرگز نگه؟",
    "کی بیشتر احتمال داره از یه غریبه‌ای که بهش مهربون بوده یه هفته فکر کنه؟",
    "کی بیشتر احتمال داره وقتی گریه می‌کنه اول مطمئن بشه قشنگ به نظر میرسه؟",
    "کی بیشتر احتمال داره یه چیز که باید عوض کنه رو normalize کنه؟",
    "کی بیشتر احتمال داره از یه «خوبی؟» واقعی جواب بده به جای «ممنون»؟",
    "کی بیشتر احتمال داره یه نفر رو دوست داشته باشه ولی به‌خاطر غرور چیزی نگه؟",
    "کی بیشتر احتمال داره یه قرار هیجان‌انگیز رو به یه نشست خونه و فیلم ترجیح بده؟",
    "کی بیشتر احتمال داره از یه چیزی که هیچ ربطی بهش نداره احساس گناه کنه؟",
    "کی بیشتر احتمال داره تو یه رابطه همیشه بیشتر دوست داشته باشه؟",
    "کی بیشتر احتمال داره از یه نفر که بهش آسیب زده معذرت‌خواهی قبول کنه؟",
    "کی بیشتر احتمال داره از یه بازی موبایل بیشتر از کار واقعیش وقت بذاره؟",
    "کی بیشتر احتمال داره از دیدن بچه‌های دیگه‌ها ذوب بشه ولی بگه بچه نمیخوام؟",
    "کی بیشتر احتمال داره تنها بره سینما و عالی بگذره؟",
    "کی بیشتر احتمال داره وسط یه جنگ اعصاب بگه «اصلاً مهم نیست»؟",
    "کی بیشتر احتمال داره یه کتاب شروع کنه، نصفه ولش کنه، بگه خوندمش؟",
    "کی بیشتر احتمال داره هر چیزی که بهش بگی رو به خودش نسبت بده؟",
]

MOODS = [
    # originals
    {"name": "کنایی",           "emoji": "🙄", "color": "#6366f1"},
    {"name": "فلرت",            "emoji": "😏", "color": "#ec4899"},
    {"name": "عصبانی",          "emoji": "😡", "color": "#ef4444"},
    {"name": "غمگین",           "emoji": "😢", "color": "#3b82f6"},
    {"name": "هیجان‌زده",       "emoji": "🤩", "color": "#f59e0b"},
    {"name": "رسمی",            "emoji": "🧐", "color": "#475569"},
    {"name": "بچگانه",          "emoji": "🍼", "color": "#22c55e"},
    {"name": "شرور",            "emoji": "😈", "color": "#7c3aed"},
    # new
    {"name": "دیوا",            "emoji": "💅", "color": "#e879f9"},
    {"name": "مست",             "emoji": "🥴", "color": "#84cc16"},
    {"name": "ترسیده",          "emoji": "😱", "color": "#1e293b"},
    {"name": "دراماتیک",     "emoji": "🎭", "color": "#db2777"},
    {"name": "لهجه هندی",       "emoji": "🪷", "color": "#f97316"},
    {"name": "لهجه روسی",       "emoji": "🥶", "color": "#334155"},
    {"name": "لهجه عربی",       "emoji": "🫡", "color": "#15803d"},
    {"name": "لهجه اصفهانی",    "emoji": "🎶", "color": "#0891b2"},
    {"name": "لهجه شمالی",      "emoji": "🌊", "color": "#0d9488"},
    {"name": "لهجه سبزواری",    "emoji": "🌾", "color": "#b45309"},
    # new moods
    {"name": "رپ‌خوان",         "emoji": "🎤", "color": "#1e1b4b"},
    {"name": "روبات",           "emoji": "🤖", "color": "#0d3b4f"},
    {"name": "مغرور",           "emoji": "👑", "color": "#78350f"},
    {"name": "جن‌زده",          "emoji": "👻", "color": "#2e1065"},
    {"name": "خوشتیپ",          "emoji": "😎", "color": "#0f172a"},
    {"name": "گریون",           "emoji": "😭", "color": "#172554"},
    {"name": "لهجه آذری",       "emoji": "🎺", "color": "#7c2d12"},
    {"name": "پشیمون",          "emoji": "🫠", "color": "#881337"},
    {"name": "خواب‌آلود",       "emoji": "🥱", "color": "#292524"},
    {"name": "پارتی‌باز",       "emoji": "🪩", "color": "#4a044e"},
]

SENTENCES = [
    # everyday
    "همه چیز خوبه",
    "اینترنت قطعه",
    "شام آماده‌ست",
    "ببخشید دیر کردم",
    "صبح بخیر همه",
    "فردا می‌بینمت",
    "خیلی خسته‌ام",
    "پیتزا تموم شد",
    "مامانم زنگ زد",
    "کسی میدونه پسورد وای‌فای چیه؟",
    "این لباس بهم میاد؟",
    "من رژیمم ولی فقط یه تیکه کوچیک",
    "پنجشنبه‌ست!",
    "یه چیزی توی آشپزخونه بو گرفت",
    "چرا همه انقدر بهم نگاه می‌کنن؟",
    "ماشینم خراب شد",
    "جیبم خالیه",
    # dramatic
    "یه چیزی دارم بهت بگم",
    "باید باهات حرف بزنم",
    "باورم نمیشه این کارو کردی",
    "این آخرین باره که اینو میگم",
    "باید یه راز بهت بگم",
    "چرا هیچکس منو درک نمیکنه؟",
    "دیگه نمیتونم ادامه بدم",
    "نمیفهمم چی شد",
    "داری بهم خیانت میکنی؟",
    "باور کن من آدم بدی نیستم",
    "می‌خوام باهات قهر کنم",
    "خواهش می‌کنم نرو",
    "این همون چیزیه که همیشه می‌خواستم",
    "نمیدونم چرا ولی داری گریم میاد",
    # work / achievement
    "امروز اخراجم کردن",
    "جلسه ۵ دقیقه دیگه شروع میشه",
    "تازه برنده لاتاری شدم",
    "میخوام استعفا بدم",
    "امتحانمو قبول شدم!",
    "اوه، یه جلسه دیگه",
    "این بهترین ایده‌ایه که تا حالا شنیدم",
    "باید زودتر میومدی",
    # feelings
    "خیلی دلم برات تنگ شده بود",
    "عاشقتم",
    "ازت متنفرم",
    "امروز خیلی خوشگلی",
    "فکر کنم گم شدم",
    "عصبانی نیستم، فقط ناامیدم",
    "یه لطف ازت می‌خوام",
    "فقط میخوام بخوابم",
    "می‌خوای بریم بیرون؟",
    "تولدمه!",
    "امروز بهترین روز زندگیمه",
    # random fun
    "فکر کنم فر رو روشن گذاشتم",
    "عاشق دوشنبه‌ام",
    "این غذا خوشمزه‌ترین چیزیه که تا حالا خوردم",
    "میشه یه کم ساکت باشی؟",
    "می‌تونی کمکم کنی؟",
    # gen z / edgy batch
    "داری منو گس‌لایت می‌کنی؟",
    "این یه red flag بزرگه",
    "ما یه situationship داریم",
    "اون آدم خیلی toxic-ه",
    "من فقط یه bit introvert-ام",
    "امروز lowkey حالم خوبه",
    "این خیلی cringe بود",
    "این خیلی vibe داره",
    "داری toxic بودن رو normalize می‌کنی",
    "می‌خوام باهاتون کافه بریم، حساسیت‌هامو process کنم",
    "من یه شخص خیلی complex‌ام",
    "از دستت خسته شدم ولی نمیتونم برم",
    "چرا همه بهم می‌گن overthink می‌کنی؟",
    "امشب main character خودمم",
    "الان باید ریلز بگیرم",
    "یکی به من بگه چیکار کنم",
    "دیگه هیچ‌کس منو نمیفهمه",
    "تو بدترین timing عاشق شدم",
    "چرا wifi قطعه همیشه وقتی لازمش دارم؟",
    "یه نفر یه چیز بگه من بخندم",
    "امشب خونه‌نشینی می‌کنم و پشیمون نیستم",
    "می‌خوام برم یه جایی که هیچکس نشناسدم",
    "همه‌ی نقشه‌هام بهم ریخت",
    "من فقط میخوام یه سگ بگیرم و تنها زندگی کنم",
    "الان بگو ببینم راستشو",
    "چطوری این رو explainکنم بدون اینکه خل به نظر برسم؟",
    "من officially دیگه umad نیستم",
    "پاهاتو چرا نمیزاری بخورم",
    "باز قهوه‌ام سرد شد",
    "فردا مهم‌ترین روز زندگیمه",
]


WL_SCENARIOS = [
    ("وقتی یه دختر تو کافه قهوه‌شو پرت می‌کنه رو صورتت",
     "تو مراسم عزا وقتی ناخواسته به بیوه خیره شدی"),
    ("وقتی می‌فهمی اسمت تو گوشی رفیقت با فحش ذخیره‌ست",
     "وقتی آسانسور گیر می‌کنه و کنارت رئیس سختگیرته"),
    ("وقتی مامانت وسط لایو اینستاگرامت ظاهر میشه",
     "وقتی پیام خیلی صمیمی رو اشتباهی به گروه خانوادگی فرستادی"),
    ("وقتی تو رستوران می‌بینی ex‌ات با نفر جدیدش سر میز کناریته",
     "وقتی می‌فهمی ده دقیقه با میکروفن روشن تو جلسه آنلاین بودی"),
    ("وقتی وسط یه مکالمه جدی کاملاً تصادفی خندیدی",
     "وقتی طرفی که سه هفته پیش ghostش کردی جلوی مغازه‌ات ظاهر میشه"),
    ("وقتی داری سخنرانی می‌کنی و می‌فهمی لباست برعکسه",
     "وقتی دکتر میگه نتیجه آزمایشت غیرعادیه"),
    ("وقتی رفیقت تو ماشین می‌فهمه عاشقشی",
     "وقتی تو جمع می‌خندن و تو نفهمیدی چرا"),
    ("وقتی استاد می‌پرسه کی جواب رو بلده و فقط تو دستتو بالا بردی",
     "وقتی می‌خوای قهر کنی ولی گرسنه‌ای"),
    ("وقتی رأس ساعت ۳ صبح یه پیام از شماره ناشناس میاد",
     "وقتی می‌فهمی جمله‌ای که فکر می‌کردی خیلی باحاله totally cringe بوده"),
    ("وقتی پدرت اولین باره وارد اتاقت میشه بعد از یه هفته",
     "وقتی می‌بینی کسی داره استوری گریه‌ات رو screenshot می‌کنه"),
    ("وقتی داری بهش می‌گی دوستش داری و اینترنتت قطع میشه",
     "وقتی پیش روان‌پزشک می‌فهمی مشکلت اسم داره"),
    ("وقتی رفیقت میگه «می‌خوام یه چیزی بگم» ولی ساکت میشه",
     "وقتی جلوی همه می‌لرزی ولی نباید معلوم بشه"),
    ("وقتی از یه قرار فرار کردی ولی طرف دقیقاً جلوی مغازه‌ای که رفتی ایستاده",
     "وقتی می‌فهمی همه تو اتاق فکر می‌کنن تو اشتباه می‌کنی"),
    ("وقتی نصفه‌شب با صدای بلند می‌خندی و مامانت میاد ببینه چیه",
     "وقتی طرفی که دوستش داشتی بهت میگه «تو مثل داداشمی»"),
    ("وقتی همه فکر می‌کنن داری گریه می‌کنی ولی فقط دودت رفته چشمت",
     "وقتی یه نفر تو مترو از پشت صداتو می‌زنه ولی نمی‌شناسیش"),
    ("وقتی داری غذا می‌خوری و می‌بینی تاریخ مصرفش گذشته",
     "وقتی می‌فهمی رفیقت همه رازاتو به یه نفر دیگه گفته"),
    ("وقتی می‌فهمی ده تا لایک پستت از فامیله",
     "وقتی ساعت ۴ صبح یه ایده به ذهنت می‌رسه که فکر می‌کنی دنیا رو عوض می‌کنه"),
    ("وقتی تو ماشین داری آواز می‌خونی و می‌بینی کسی فیلمت گرفته",
     "وقتی می‌فهمی پست حذف‌شده‌ات screenshot داره"),
    ("وقتی می‌فهمی همه یه سفر رفتن و بهت نگفتن",
     "وقتی ادعا کردی کتاب خوندی ولی ازش سوال پرسیدن"),
    ("وقتی تو صف بانک یه دعوا می‌بینی و باید طرف بگیری",
     "وقتی از تمام کلاس فقط تو امتحان افتادی"),
    ("وقتی داری برای کسی دروغ می‌گی و اون دقیقاً پشت سرته",
     "وقتی می‌فهمی از اول اشتباه دکمه‌های پیراهنتو زدی"),
    ("وقتی مطمئنی جواب درسته ولی وقتی نوشتی همه خندیدن",
     "وقتی می‌بینی طرفی که ۳ سال دوستش داشتی ازدواج کرده"),
    ("وقتی میهمانی به آخرش رسیده ولی کسی بلند نمیشه بره",
     "وقتی بهترین دوستت میگه «باید بریم» و بعد ۴۵ دقیقه می‌مونه"),
    ("وقتی تو خواب حرف زدی و جلوی همه رو شدی",
     "وقتی یه چیزی که از بچگی ازش می‌ترسیدی بالاخره سر راهته"),
    ("وقتی می‌بینی ex‌ات الان خیلی بهتره از وقتی باهات بود",
     "وقتی برای اولین بار تو دعوا داری می‌بازی"),
    ("وقتی اشتباهی به جای بهترین دوستت به ex‌ات پیام دادی",
     "وقتی داری ریلز می‌گیری و یه غریبه وارد فریم می‌شه و خیره نگاهت می‌کنه"),
    ("وقتی یه نفر بهت میگه «چرا انقدر ساکتی؟» تو یه مهمونی",
     "وقتی می‌بینی قیمت همه چیز دو برابر شده ولی حقوقت نه"),
    ("وقتی از روان‌پزشک بیرون میای و باید حالتو به بقیه توضیح بدی",
     "وقتی رفیقت میگه «با یه نفر آشنا می‌کنمت» و نمی‌پرسی کیه"),
    ("وقتی تو جمع می‌بینی کسی که دوستش داری با یکی دیگه‌ست",
     "وقتی ساعت ۱۲ شب می‌فهمی فردا امتحان داری"),
    ("وقتی بهترین جواب موقعی به ذهنت می‌رسه که بحث تموم شده",
     "وقتی می‌فهمی از اول اشتباه می‌خوندی اسم طرف رو"),
    ("وقتی تو حمام ایده‌ای داری که فکر می‌کنی بیزنس میلیاردی می‌شه",
     "وقتی می‌فهمی کل مکالمه رو غلط فهمیدی"),
    ("وقتی یه عکس خجالت‌آور قدیمیت دست یه نفر افتاده",
     "وقتی به طور تصادفی خودتو تو آیینه می‌بینی و لحظه‌ای نمی‌شناسیش"),
    ("وقتی استاد میگه «این سوال برای تنبیه‌هاست» و چشمش به توئه",
     "وقتی کسی که باهاش قهری تولدتو تبریک میگه"),
    ("وقتی می‌خوای یه جوک بگی ولی punch line رو فراموش کردی",
     "وقتی تمام روز منتظر یه پیام بودی و اومد ولی فقط یه کلمه بود"),
    ("وقتی وسط یه بازی آنلاین مامانت پشت سرت ظاهر میشه",
     "وقتی می‌فهمی مدت‌هاست اشتباه اسم یه غذا رو تلفظ می‌کردی"),
    ("وقتی دوستت بدون اطلاع تو ازت screenshot گرفته",
     "وقتی یه نفر که ازش بدت میاد به موقع بهت کمک می‌کنه"),
    ("وقتی می‌خوای خداحافظی کنی ولی هر دوتون همون مسیر رو دارین",
     "وقتی به اشتباه to everyone در یه جلسه زوم چیزی تایپ می‌کنی"),
    ("وقتی یه نفر می‌گه «به نظرم یکی دوستت داره» و اشاره به توئه",
     "وقتی بعد از یه مهمونی می‌فهمی کل شب اسفناج لای دندونت بوده"),
    ("وقتی رفیقت تو بدترین لحظه ممکن بهت زنگ می‌زنه",
     "وقتی تو صف کافه می‌بینی هرکی قبل از تو سفارش داد زودتر غذاشو گرفت"),
    ("وقتی می‌فهمی حرفایی که فکر می‌کردی تو ذهنته رو بلند گفتی",
     "وقتی تو یه مهمونی شلوغ هیچ‌کسی نمی‌دونه اسمته"),
]


@dataclass
class Player:
    id: str
    name: str
    score: int = 0


@dataclass
class Room:
    id: str
    players: list = field(default_factory=list)
    state: str = "lobby"
    game_mode: str = "faztoumim"       # "faztoumim" | "who"

    # ── فازتومیم fields ───────────────────────────────
    actor_index: int = 0
    sentence: str = ""
    mood: dict = field(default_factory=dict)
    guesses: dict = field(default_factory=dict)

    # ── shared ────────────────────────────────────────
    rounds_played: int = 0
    max_rounds: int = 0
    _sentence_queue: list = field(default_factory=list)

    # ── کدوم‌تون fields ───────────────────────────────
    who_question: str = ""
    who_votes: dict = field(default_factory=dict)   # voter_id → target_id
    who_shame: dict = field(default_factory=dict)   # player_id → shame count
    who_tied: list = field(default_factory=list)    # ids of tied players
    _who_q_queue: list = field(default_factory=list)

    # ── خط کیه؟ fields ───────────────────────────────
    wl_scenario_a: str = ""
    wl_scenario_b: str = ""
    wl_answers: dict = field(default_factory=dict)       # player_id → text
    wl_votes: dict = field(default_factory=dict)          # voter_id → target_player_id (round vote)
    wl_scores: dict = field(default_factory=dict)         # player_id → cumulative pts
    wl_answer_order: list = field(default_factory=list)   # shuffled player_ids for voting
    wl_tied: list = field(default_factory=list)           # player_ids tied after round vote
    wl_tb_votes: dict = field(default_factory=dict)       # voter_id → target_id (tiebreak vote)
    _wl_q_queue: list = field(default_factory=list)

    def host_id(self) -> Optional[str]:
        return self.players[0].id if self.players else None

    def current_actor(self) -> Optional[Player]:
        if self.players:
            return self.players[self.actor_index % len(self.players)]
        return None

    def _next_sentence(self) -> str:
        if not self._sentence_queue:
            self._sentence_queue = random.sample(SENTENCES, len(SENTENCES))
        return self._sentence_queue.pop()

    def start_round(self):
        self.sentence = self._next_sentence()
        self.mood = random.choice(MOODS)
        self.guesses = {}
        self.state = "acting"

    def begin_game(self, rounds_per_player: int = 1):
        rpp = max(1, min(rounds_per_player, 10))
        self.max_rounds = rpp * len(self.players)
        self._sentence_queue = random.sample(SENTENCES, len(SENTENCES))
        self.start_round()

    def actor_done(self):
        self.state = "guessing"

    def submit_guess(self, player_id: str, mood_name: str) -> bool:
        actor = self.current_actor()
        if not actor or player_id == actor.id:
            return False
        self.guesses[player_id] = mood_name
        non_actors = [p for p in self.players if p.id != actor.id]
        return len(self.guesses) >= len(non_actors)

    def do_reveal(self):
        self.state = "reveal"
        actor = self.current_actor()
        correct_mood = self.mood["name"]
        correct_count = sum(1 for g in self.guesses.values() if g == correct_mood)
        if actor:
            actor.score += correct_count  # actor earns 1 pt per correct guesser
        for player in self.players:
            if player.id in self.guesses and self.guesses[player.id] == correct_mood:
                player.score += 1        # correct guesser also earns 1 pt

    def next_round(self):
        self.rounds_played += 1
        self.actor_index = (self.actor_index + 1) % len(self.players)
        if self.rounds_played >= self.max_rounds:
            self.state = "ended"
        else:
            self.start_round()

    def play_again(self, rounds_per_player: int = 1):
        for p in self.players:
            p.score = 0
        self.rounds_played = 0
        self.actor_index = 0
        self.begin_game(rounds_per_player)

    # ── کدوم‌تون بیشتر methods ───────────────────────────

    def _who_next_q(self) -> str:
        if not self._who_q_queue:
            self._who_q_queue = random.sample(WHO_QUESTIONS, len(WHO_QUESTIONS))
        return self._who_q_queue.pop()

    def start_who(self, rounds: int = 10):
        self.max_rounds = max(1, min(rounds, 30))
        self.rounds_played = 0
        self.who_shame = {p.id: 0 for p in self.players}
        self._who_q_queue = random.sample(WHO_QUESTIONS, len(WHO_QUESTIONS))
        self.who_question = self._who_next_q()
        self.who_votes = {}
        self.who_tied = []
        self.state = "who_preparing"

    def who_launch(self, custom_q: str = "") -> None:
        if custom_q.strip():
            self.who_question = custom_q.strip()
        self.who_votes = {}
        self.who_tied = []
        self.state = "who_voting"

    def _vote_counts(self) -> dict:
        counts = {p.id: 0 for p in self.players}
        for target in self.who_votes.values():
            counts[target] = counts.get(target, 0) + 1
        return counts

    def who_vote(self, voter_id: str, target_id: str) -> bool:
        if voter_id in self.who_votes:
            return False
        valid = [p.id for p in self.players]
        if target_id not in valid:
            return False
        self.who_votes[voter_id] = target_id
        return len(self.who_votes) >= len(self.players)

    def who_reveal(self) -> None:
        counts = self._vote_counts()
        if not counts:
            self.state = "who_reveal"
            return
        max_v = max(counts.values())
        leaders = [pid for pid, c in counts.items() if c == max_v]
        if len(leaders) > 1:
            self.who_tied = leaders
            self.who_votes = {}
            self.state = "who_tiebreak"
        else:
            self.who_shame[leaders[0]] = self.who_shame.get(leaders[0], 0) + 1
            self.state = "who_reveal"

    def who_tiebreak_vote(self, voter_id: str, target_id: str) -> bool:
        if voter_id in self.who_votes:
            return False
        if target_id not in self.who_tied:
            return False
        self.who_votes[voter_id] = target_id
        return len(self.who_votes) >= len(self.players)

    def who_tiebreak_reveal(self) -> None:
        counts = {pid: 0 for pid in self.who_tied}
        for target in self.who_votes.values():
            if target in counts:
                counts[target] += 1
        if counts:
            winner = max(counts, key=counts.get)
            self.who_shame[winner] = self.who_shame.get(winner, 0) + 1
        self.state = "who_reveal"

    def who_next(self) -> None:
        self.rounds_played += 1
        if self.rounds_played >= self.max_rounds:
            self.state = "who_ended"
        else:
            self.who_question = self._who_next_q()
            self.who_votes = {}
            self.who_tied = []
            self.state = "who_preparing"

    def who_play_again(self, rounds: int = 10) -> None:
        self.start_who(rounds)

    # ── خط کیه؟ methods ──────────────────────────────────

    def _wl_next_scenario(self) -> tuple:
        if not self._wl_q_queue:
            self._wl_q_queue = random.sample(WL_SCENARIOS, len(WL_SCENARIOS))
        return self._wl_q_queue.pop()

    def start_wl(self, rounds: int = 8) -> None:
        self.max_rounds = max(1, min(rounds, 20))
        self.rounds_played = 0
        self.wl_scores = {p.id: 0 for p in self.players}
        self._wl_q_queue = random.sample(WL_SCENARIOS, len(WL_SCENARIOS))
        s = self._wl_next_scenario()
        self.wl_scenario_a, self.wl_scenario_b = s
        self.wl_answers = {}
        self.wl_votes = {}
        self.wl_answer_order = []
        self.wl_tied = []
        self.wl_tb_votes = {}
        self.state = "wl_writing"

    def wl_submit(self, player_id: str, text: str) -> bool:
        text = text.strip()
        if not text or player_id in self.wl_answers:
            return False
        self.wl_answers[player_id] = text
        return len(self.wl_answers) >= len(self.players)

    def wl_move_to_vote(self) -> None:
        order = list(self.wl_answers.keys())
        random.shuffle(order)
        self.wl_answer_order = order
        self.wl_votes = {}
        self.state = "wl_voting"

    def wl_vote(self, voter_id: str, target_id: str) -> bool:
        if voter_id in self.wl_votes or target_id == voter_id:
            return False
        if target_id not in self.wl_answers:
            return False
        self.wl_votes[voter_id] = target_id
        eligible = [
            p.id for p in self.players
            if any(pid != p.id for pid in self.wl_answers)
        ]
        return len(self.wl_votes) >= len(eligible)

    def wl_do_reveal(self) -> None:
        vc: dict = {}
        for tid in self.wl_votes.values():
            vc[tid] = vc.get(tid, 0) + 1
        if not vc:
            self.state = "wl_reveal"
            return
        max_v = max(vc.values())
        leaders = [pid for pid, c in vc.items() if c == max_v]
        if len(leaders) > 1:
            # Tie — run tiebreak before awarding any points
            self.wl_tied = leaders
            self.wl_tb_votes = {}
            self.state = "wl_tiebreak"
        else:
            for tid in self.wl_votes.values():
                self.wl_scores[tid] = self.wl_scores.get(tid, 0) + 1
            self.state = "wl_reveal"

    def wl_tiebreak_vote(self, voter_id: str, target_id: str) -> bool:
        if voter_id in self.wl_tb_votes or target_id == voter_id:
            return False
        if target_id not in self.wl_tied:
            return False
        self.wl_tb_votes[voter_id] = target_id
        eligible = [
            p.id for p in self.players
            if any(pid != p.id for pid in self.wl_tied)
        ]
        return len(self.wl_tb_votes) >= len(eligible)

    def wl_tiebreak_reveal(self) -> None:
        # Award original round votes
        for tid in self.wl_votes.values():
            self.wl_scores[tid] = self.wl_scores.get(tid, 0) + 1
        # Award tiebreak votes on top (break the deadlock with bonus points)
        for tid in self.wl_tb_votes.values():
            if tid in self.wl_tied:
                self.wl_scores[tid] = self.wl_scores.get(tid, 0) + 1
        self.state = "wl_reveal"

    def wl_next(self) -> None:
        self.rounds_played += 1
        if self.rounds_played >= self.max_rounds:
            self.state = "wl_ended"
        else:
            s = self._wl_next_scenario()
            self.wl_scenario_a, self.wl_scenario_b = s
            self.wl_answers = {}
            self.wl_votes = {}
            self.wl_answer_order = []
            self.wl_tied = []
            self.wl_tb_votes = {}
            self.state = "wl_writing"

    def wl_play_again(self, rounds: int = 8) -> None:
        self.start_wl(rounds)

    # ── to_dict ──────────────────────────────────────────

    def to_dict(self, for_player_id: str = None) -> dict:
        actor = self.current_actor()
        non_actors = [p for p in self.players if actor and p.id != actor.id]
        data = {
            "state":           self.state,
            "game_mode":       self.game_mode,
            "room_id":         self.id,
            "host_id":         self.host_id(),
            "players":         [{"id": p.id, "name": p.name, "score": p.score} for p in self.players],
            "rounds_played":   self.rounds_played,
            "max_rounds":      self.max_rounds,
        }

        # ── faztoumim-specific ────────────────────────
        if self.game_mode == "faztoumim":
            data.update({
                "actor_id":        actor.id if actor else None,
                "actor_name":      actor.name if actor else None,
                "sentence":        self.sentence,
                "mood_options":    MOODS,
                "guesses_count":   len(self.guesses),
                "non_actor_count": len(non_actors),
            })
            if for_player_id and actor and for_player_id == actor.id and self.state == "acting":
                data["secret_mood"] = self.mood
            if self.state == "guessing":
                data["guessed_ids"] = list(self.guesses.keys())
            if self.state in ("reveal", "ended"):
                data["revealed_mood"] = self.mood
                data["correct_count"] = sum(1 for g in self.guesses.values() if g == self.mood["name"])

        # ── who-game-specific ─────────────────────────
        if self.game_mode == "who":
            data["who_shame"] = self.who_shame
            data["who_votes_count"] = len(self.who_votes)

            # question: only host sees it during preparing
            if self.state == "who_preparing":
                if for_player_id == self.host_id():
                    data["who_question"] = self.who_question
            elif self.state in ("who_voting", "who_tiebreak", "who_reveal", "who_ended"):
                data["who_question"] = self.who_question

            if self.state == "who_voting":
                data["who_voted_ids"] = list(self.who_votes.keys())
                if for_player_id:
                    data["my_vote"] = self.who_votes.get(for_player_id)

            if self.state == "who_tiebreak":
                data["who_tied"] = self.who_tied
                data["who_voted_ids"] = list(self.who_votes.keys())
                if for_player_id:
                    data["my_vote"] = self.who_votes.get(for_player_id)

            if self.state in ("who_reveal", "who_ended"):
                counts = self._vote_counts()
                max_v = max(counts.values()) if counts else 0
                winners = [pid for pid, c in counts.items() if c == max_v] if counts else []
                breakdown = []
                for voter_id, target_id in self.who_votes.items():
                    voter  = next((p for p in self.players if p.id == voter_id),  None)
                    target = next((p for p in self.players if p.id == target_id), None)
                    if voter and target:
                        breakdown.append({"voter": voter.name, "target": target.name,
                                          "voter_id": voter_id, "target_id": target_id})
                data["who_round_counts"] = counts
                data["who_winner_ids"]   = winners
                data["who_winner_votes"] = max_v
                data["who_breakdown"]    = breakdown

        # ── خط کیه؟ specific ─────────────────────────
        if self.game_mode == "wl":
            data.update({
                "wl_scenario_a":    self.wl_scenario_a,
                "wl_scenario_b":    self.wl_scenario_b,
                "wl_scores":        self.wl_scores,
                "wl_submitted_count": len(self.wl_answers),
                "wl_submitted_ids": list(self.wl_answers.keys()),
            })
            if self.state == "wl_writing":
                if for_player_id and for_player_id in self.wl_answers:
                    data["wl_my_answer"] = self.wl_answers[for_player_id]
            elif self.state == "wl_voting":
                data["wl_answer_list"] = [
                    {"id": pid, "text": self.wl_answers[pid]}
                    for pid in self.wl_answer_order
                ]
                data["wl_voted_ids"] = list(self.wl_votes.keys())
                if for_player_id:
                    data["wl_my_vote"]      = self.wl_votes.get(for_player_id)
                    data["wl_my_answer_id"] = for_player_id if for_player_id in self.wl_answers else None
            elif self.state == "wl_tiebreak":
                tb_order = [pid for pid in self.wl_answer_order if pid in self.wl_tied]
                data["wl_answer_list"] = [
                    {"id": pid, "text": self.wl_answers.get(pid, "")}
                    for pid in tb_order
                ]
                data["wl_tied"]      = self.wl_tied
                data["wl_voted_ids"] = list(self.wl_tb_votes.keys())
                if for_player_id:
                    data["wl_my_vote"]      = self.wl_tb_votes.get(for_player_id)
                    data["wl_my_answer_id"] = for_player_id if for_player_id in self.wl_tied else None
            elif self.state in ("wl_reveal", "wl_ended"):
                # Combine original + tiebreak votes for final display
                vc: dict = {}
                for tid in self.wl_votes.values():
                    vc[tid] = vc.get(tid, 0) + 1
                for tid in self.wl_tb_votes.values():
                    if tid in self.wl_tied:
                        vc[tid] = vc.get(tid, 0) + 1
                data["wl_answer_list"] = [
                    {"id": pid,
                     "text":   self.wl_answers.get(pid, ""),
                     "author": next((p.name for p in self.players if p.id == pid), "؟"),
                     "votes":  vc.get(pid, 0)}
                    for pid in self.wl_answer_order
                ]
                max_v = max(vc.values()) if vc else 0
                data["wl_round_winner_ids"] = [pid for pid, c in vc.items() if c == max_v] if vc else []
                data["wl_round_max_votes"]  = max_v
                data["wl_had_tiebreak"]     = bool(self.wl_tied)

        return data


rooms: dict[str, Room] = {}


def make_room_code() -> str:
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        code = "".join(random.choices(chars, k=4))
        if code not in rooms:
            return code


def create_room(host_name: str) -> tuple[Room, Player]:
    code = make_room_code()
    room = Room(id=code)
    player = Player(id=str(uuid.uuid4())[:8], name=host_name)
    room.players.append(player)
    rooms[code] = room
    return room, player


def join_room(room_id: str, name: str) -> tuple[Optional[Room], Optional[Player], Optional[str]]:
    room = rooms.get(room_id.upper())
    if not room:
        return None, None, "اتاق پیدا نشد"
    name = name.strip()
    # Allow rejoining by matching name — works even mid-game
    for player in room.players:
        if player.name.strip() == name:
            return room, player, None
    # New player — only allowed in lobby
    if room.state != "lobby":
        return None, None, "بازی شروع شده — با اسم قبلیت دوباره وارد شو"
    if len(room.players) >= 12:
        return None, None, "اتاق پر شده"
    player = Player(id=str(uuid.uuid4())[:8], name=name)
    room.players.append(player)
    return room, player, None
