#!/usr/bin/python

if __name__ == "__main__":
    import smtplib
    import json
    import urllib2
    import time
    from email.mime.multipart import MIMEMultipart
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText

    fromaddr = 'ryan.taylor@hulu.com'
    toaddrs  = 'ryan.taylor@hulu.com'
    date     = time.strftime('%Y-%m-%d')
    subject  = 'Channel list ' + date

    req = urllib2.Request('https://stormwatch.prod.hulu.com/api/channels/month_url')
    opener = urllib2.build_opener()
    f = opener.open(req)
    json = json.loads(f.read())
    
    csv = "Id,S3-Akamai:live_dash,S3-Akamai:live_hls,S3-Akamai:hls_unencrypted,S3-CloudFront:live_dash,S3-CloudFront:live_hls,S3-CloudFront:hls_unencrypted\n"
    for line in (json):
        csv += line['id'] + "," + \
            line["S3-Akamai"]["live_dash"] + "," + \
            line["S3-Akamai"]["live_hls"] + "," + \
            line["S3-Akamai"]["hls_unencrypted"] + "," + \
            line["S3-CloudFront"]["live_dash"] + "," + \
            line["S3-CloudFront"]["live_hls"] + "," + \
            line["S3-CloudFront"]["hls_unencrypted"] + "\n"


    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg.preamble = "Multipart message.\n"
    msg.attach(MIMEText('Attached is the channel list for ' + date + ' CSV', 'plain'))
    
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(csv)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='channels-' + date + '.csv')
    msg.attach(attachment)
                              
    server = smtplib.SMTP('smtp.prod.hulu.com')
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()