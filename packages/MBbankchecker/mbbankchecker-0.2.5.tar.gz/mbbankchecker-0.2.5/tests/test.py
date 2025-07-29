from mbbank import MBBank
import datetime

mb = MBBank(username="0943525578", password="Krisktan5436*****")
end_query_day = datetime.datetime.now()
start_query_day = end_query_day - datetime.timedelta(days=30)
# print(mb.userinfo())
print(mb.inquiryAccountName(creditAccount="9961384366", creditAccountType="ACCOUNT", bankCode="970436"))