class Config:
    CMD_CHARACTER     = '!'

    CLIENT_SERVERIP   = '0.0.0.0'
    CLIENT_SERVERPORT = 10000
    
    WEB_SERVERIP      = '0.0.0.0'
    WEB_SERVERPORT    = 11111

    CROSSDOMAIN       = '<cross-domain-policy><allow-access-from domain="*" to-ports="*" /></cross-domain-policy>'

    XAT_IP            = 'fwdelb01-1365137239.us-east-1.elb.amazonaws.com'
    XAT_PORT          = 80