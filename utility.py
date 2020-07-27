class Utility:

    def calculate_age(birth_date, birth_month, birth_year):
        # if birth date is greater then current birth_month
        # then donot count this month and add 30 to the date so
        # as to subtract the date and get the remaining days

        import datetime
        # getting current date and time

        d = datetime.datetime.today()
        date_year = d.year
        date_month = d.month
        date_day = d.day
        month =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if birth_date > date_day:
            date_month = date_month - 1
            date_day = date_day + month[birth_month-1]

        # if birth month exceeds current month, then
        # donot count this year and add 12 to the
        # month so that we can subtract and find out 

        # the difference 
        if birth_month > date_month:
            date_year = date_year - 1
            date_month = date_month + 12

        # calculate date, month, year
        calculated_date = date_day - birth_date
        calculated_month = date_month - birth_month
        calculated_year = date_year - birth_year
        age = [calculated_year, calculated_month, calculated_date]
        return age

    def write_log(service_name, log):
        print('service_name : ',service_name)
        print('log : ',log)
        file = open("log/" + service_name + ".txt", "a")
        file.write("\n")
        file.write(log)
        file.close()