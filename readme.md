
##setup peewee
git clone https://github.com/coleifer/peewee.git
cd peewee
python setup.py install


##interesting docs
http://docs.peewee-orm.com/en/latest/peewee/querying.html

d = Domain.find_or_create_by_name('test.com')
print d.to_string()

http://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address
ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
