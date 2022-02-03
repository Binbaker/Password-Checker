import sys 
import requests
import hashlib

def request_api_data(chars):
    url = 'https://api.pwnedpasswords.com/range/' + chars
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}')
    return res
         
def get_password_count(hashes, h_toCheck):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, times in hashes:
        if h == h_toCheck:
            return times
    return 0 

def pwned_api_check(password):
    # check password if it exist in API response 
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[0:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_count(response, tail)


def main(args):
    for pwd in args:
        count = pwned_api_check(pwd)
        if count:
            print(f'{pwd} was found {count} times ... I think you should change it')
        else:
            print(f'{pwd} was NOT found. Good job by making your password hard to crack')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))