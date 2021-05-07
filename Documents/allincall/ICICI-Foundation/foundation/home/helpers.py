
import datetime 



def calculates_dates(days):
    todays_date = datetime.datetime.now()
    old_date = datetime.timedelta(days = days)
    final_date = todays_date - old_date
    batch_start_to_date = str(todays_date)[0:10]
    batch_start_from_date = str(final_date)[0:10]

    print('FINAL -' +batch_start_from_date)

    return batch_start_from_date,batch_start_to_date