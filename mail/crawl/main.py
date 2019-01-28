import imaplib
import email
import sys


class Mail(object):
    user = ''
    password = ''
    imap = 'imap.exmail.qq.com'

    def __init__(self, u, p):
        self.user = u
        self.password = p
        self.conn = None
        self.unseen = []
        self.all = []
        try:
            self.conn = imaplib.IMAP4_SSL(self.imap)
            self.conn.login(self.user, self.password)
        except imaplib.IMAP4.error as e:
            print("登录失败: %s" % e)
            sys.exit(1)
        print("登录成功")
        self.conn.select()

    def unseen_mail(self):
        """ 未读邮件 """
        result, data = self.conn.search(None, 'UNSEEN')
        if result == 'OK':
            self.unseen = data[0].split()
            print('未读邮件数量:%s' % len(self.unseen))
            # print(' '.join([str(i) for i in self.unseen]))

    def all_mail(self):
        """ 所有邮件 """
        result, data = self.conn.search(None, 'ALL')
        if result == 'OK':
            self.all = data[0].split()
            print('所有邮件数量:%s' % len(self.all))

    def parse_header(self, msg):
        data, charset = email.header.decode_header(msg['subject'])[0]
        subject = str(data, charset)

        print("Subject: ", subject)
        print("From: ", email.utils.parseaddr(msg['From'])[1])
        print("To: ", email.utils.parseaddr(msg['To'])[1])
        print("Date: ", msg['Date'])

    def parse_part_to_str(self, part):
        charset = part.get_charset() or 'utf-8'
        payload = part.get_payload(decode=True)
        if not payload:
            return
        return str(part.get_payload(decode=True), charset)

    def parse_body(self, msg):
        for part in msg.walk():
            if not part.is_multipart():
                charset = part.get_charset()
                contenttype = part.get_content_type()
                name = part.get_param("name")
                if name:
                    fh = email.header.Header(name)
                    fdh = email.header.decode_header(fh)
                    fname = fdh[0][0]
                    print('附件名:', fname)
                else:
                    print(self.parse_part_to_str(part))


    def parse(self):
        nums = self.all[10:12]
        for num in nums:
            try:
                result, data = self.conn.fetch(num, '(RFC822)')
                if result == 'OK':
                    msg = email.message_from_string(data[0][1].decode())
                    print('Message %s' % num.decode())
                    self.parse_header(msg)
                    print('-'* 20)
                    self.parse_body(msg)
            except Exception as e:
                print('Message %s 解析错误:%s' % (num, e))


    def over(self):
        self.conn.close()
        self.conn.logout()

    def run(self):
        self.unseen_mail()
        self.all_mail()
        self.parse()
        self.over()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: %s <user> <pass>" % sys.argv[0])
        sys.exit(1)
    mail = Mail(sys.argv[1], sys.argv[2])
    mail.run()
